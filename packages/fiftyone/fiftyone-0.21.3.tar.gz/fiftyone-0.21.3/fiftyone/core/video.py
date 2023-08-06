"""
Video frame views.

| Copyright 2017-2023, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
from collections import defaultdict
from copy import deepcopy
import logging
import os

from bson import ObjectId
from pymongo import UpdateOne

import eta.core.utils as etau

import fiftyone as fo
import fiftyone.core.dataset as fod
import fiftyone.core.fields as fof
import fiftyone.core.media as fom
import fiftyone.core.sample as fos
import fiftyone.core.odm as foo
import fiftyone.core.odm.sample as foos
import fiftyone.core.utils as fou
import fiftyone.core.validation as fova
import fiftyone.core.view as fov

fouv = fou.lazy_import("fiftyone.utils.video")


logger = logging.getLogger(__name__)


class FrameView(fos.SampleView):
    """A frame in a :class:`FramesView`.

    :class:`FrameView` instances should not be created manually; they are
    generated by iterating over :class:`FramesView` instances.

    Args:
        doc: a :class:`fiftyone.core.odm.DatasetSampleDocument`
        view: the :class:`FramesView` that the frame belongs to
        selected_fields (None): a set of field names that this view is
            restricted to
        excluded_fields (None): a set of field names that are excluded from
            this view
        filtered_fields (None): a set of field names of list fields that are
            filtered in this view
    """

    @property
    def _sample_id(self):
        return ObjectId(self._doc.sample_id)

    def _save(self, deferred=False):
        if deferred:
            raise NotImplementedError(
                "Frames views do not support save contexts"
            )

        super()._save(deferred=deferred)
        self._view._sync_source_sample(self)


class FramesView(fov.DatasetView):
    """A :class:`fiftyone.core.view.DatasetView` of frames from a video
    :class:`fiftyone.core.dataset.Dataset`.

    Frames views contain an ordered collection of frames, each of which
    corresponds to a single frame of a video from the source collection.

    Frames retrieved from frames views are returned as :class:`FrameView`
    objects.

    Args:
        source_collection: the
            :class:`fiftyone.core.collections.SampleCollection` from which this
            view was created
        frames_stage: the :class:`fiftyone.core.stages.ToFrames` stage that
            defines how the frames were created
        frames_dataset: the :class:`fiftyone.core.dataset.Dataset` that serves
            the frames in this view
    """

    def __init__(
        self,
        source_collection,
        frames_stage,
        frames_dataset,
        _stages=None,
        _name=None,
    ):
        if _stages is None:
            _stages = []

        self._source_collection = source_collection
        self._frames_stage = frames_stage
        self._frames_dataset = frames_dataset
        self.__stages = _stages
        self.__name = _name

    def __copy__(self):
        return self.__class__(
            self._source_collection,
            deepcopy(self._frames_stage),
            self._frames_dataset,
            _stages=deepcopy(self.__stages),
            _name=self.__name,
        )

    @property
    def _base_view(self):
        return self.__class__(
            self._source_collection,
            self._frames_stage,
            self._frames_dataset,
        )

    @property
    def _dataset(self):
        return self._frames_dataset

    @property
    def _root_dataset(self):
        return self._source_collection._root_dataset

    @property
    def _sample_cls(self):
        return FrameView

    @property
    def _stages(self):
        return self.__stages

    @property
    def _all_stages(self):
        return (
            self._source_collection.view()._all_stages
            + [self._frames_stage]
            + self.__stages
        )

    @property
    def media_type(self):
        return fom.IMAGE

    def _get_sample_only_fields(
        self, include_private=False, use_db_fields=False
    ):
        sample_only_fields = set(
            self._get_default_sample_fields(
                include_private=include_private, use_db_fields=use_db_fields
            )
        )

        # If sample_frames != dynamic, `filepath` can be synced
        config = self._frames_stage.config or {}
        if config.get("sample_frames", None) != "dynamic":
            sample_only_fields.discard("filepath")

        return sample_only_fields

    def _tag_labels(self, tags, label_field, ids=None, label_ids=None):
        ids, label_ids = super()._tag_labels(
            tags, label_field, ids=ids, label_ids=label_ids
        )

        frame_field = self._source_collection._FRAMES_PREFIX + label_field
        self._source_collection._tag_labels(
            tags, frame_field, ids=ids, label_ids=label_ids
        )

    def _untag_labels(self, tags, label_field, ids=None, label_ids=None):
        ids, label_ids = super()._untag_labels(
            tags, label_field, ids=ids, label_ids=label_ids
        )

        frame_field = self._source_collection._FRAMES_PREFIX + label_field
        self._source_collection._untag_labels(
            tags, frame_field, ids=ids, label_ids=label_ids
        )

    def set_values(self, field_name, *args, **kwargs):
        # The `set_values()` operation could change the contents of this view,
        # so we first record the sample IDs that need to be synced
        if self._stages:
            ids = self.values("id")
        else:
            ids = None

        super().set_values(field_name, *args, **kwargs)

        field = field_name.split(".", 1)[0]
        self._sync_source(fields=[field], ids=ids)
        self._sync_source_field_schema(field_name)

    def set_label_values(self, field_name, *args, **kwargs):
        super().set_label_values(field_name, *args, **kwargs)

        frame_field = self._source_collection._FRAMES_PREFIX + field_name
        self._source_collection.set_label_values(frame_field, *args, **kwargs)

    def save(self, fields=None):
        """Saves the frames in this view to the underlying dataset.

        .. note::

            This method is not a :class:`fiftyone.core.stages.ViewStage`;
            it immediately writes the requested changes to the underlying
            dataset.

        .. warning::

            This will permanently delete any omitted or filtered contents from
            the frames of the source dataset.

        Args:
            fields (None): an optional field or list of fields to save. If
                specified, only these fields are overwritten
        """
        if etau.is_str(fields):
            fields = [fields]

        super().save(fields=fields)

        self._sync_source(fields=fields)

    def keep(self):
        """Deletes all frames that are **not** in this view from the underlying
        dataset.

        .. note::

            This method is not a :class:`fiftyone.core.stages.ViewStage`;
            it immediately writes the requested changes to the underlying
            dataset.
        """

        # The `keep()` operation below will delete frames, so we must sync
        # deletions to the source dataset first
        self._sync_source(update=False, delete=True)

        super().keep()

    def keep_fields(self):
        """Deletes any sample fields that have been excluded in this view from
        the frames of the underlying dataset.

        .. note::

            This method is not a :class:`fiftyone.core.stages.ViewStage`;
            it immediately writes the requested changes to the underlying
            dataset.
        """
        self._sync_source_keep_fields()

        super().keep_fields()

    def reload(self):
        """Reloads the view.

        Note that :class:`FrameView` instances are not singletons, so any
        in-memory frames extracted from this view will not be updated by
        calling this method.
        """
        self._source_collection.reload()

        #
        # Regenerate the frames dataset
        #
        # This assumes that calling `load_view()` when the current patches
        # dataset has been deleted will cause a new one to be generated
        #
        self._frames_dataset.delete()
        _view = self._frames_stage.load_view(self._source_collection)
        self._frames_dataset = _view._frames_dataset

        super().reload()

    def _set_labels(self, field_name, sample_ids, label_docs):
        super()._set_labels(field_name, sample_ids, label_docs)

        self._sync_source(fields=[field_name], ids=sample_ids)

    def _delete_labels(self, ids, fields=None):
        super()._delete_labels(ids, fields=fields)

        if fields is not None:
            if etau.is_str(fields):
                fields = [fields]

            frame_fields = [
                self._source_collection._FRAMES_PREFIX + f for f in fields
            ]
        else:
            frame_fields = None

        self._source_collection._delete_labels(ids, fields=frame_fields)

    def _sync_source_sample(self, sample):
        self._sync_source_schema()

        dst_dataset = self._source_collection._root_dataset
        sample_only_fields = self._get_sample_only_fields(
            include_private=True, use_db_fields=True
        )

        updates = {
            k: v
            for k, v in sample.to_mongo_dict().items()
            if k not in sample_only_fields
        }

        if not updates:
            return

        match = {
            "_sample_id": sample._sample_id,
            "frame_number": sample.frame_number,
        }

        dst_dataset._frame_collection.update_one(match, {"$set": updates})

    def _sync_source(self, fields=None, ids=None, update=True, delete=False):
        dst_dataset = self._source_collection._root_dataset
        sample_only_fields = self._get_sample_only_fields(
            include_private=True, use_db_fields=True
        )

        if fields is not None:
            fields = [f for f in fields if f not in sample_only_fields]
            if not fields:
                return

        if update:
            self._sync_source_schema(fields=fields)

            pipeline = []

            if ids is not None:
                pipeline.append(
                    {
                        "$match": {
                            "_id": {"$in": [ObjectId(_id) for _id in ids]}
                        }
                    }
                )

            if fields is None:
                sample_only_fields.discard("_sample_id")
                sample_only_fields.discard("frame_number")

                pipeline.append(
                    {"$project": {f: False for f in sample_only_fields}}
                )
            else:
                project = {f: True for f in fields}
                project["_id"] = True
                project["_sample_id"] = True
                project["frame_number"] = True
                pipeline.append({"$project": project})

            pipeline.append(
                {
                    "$merge": {
                        "into": dst_dataset._frame_collection_name,
                        "on": ["_sample_id", "frame_number"],
                        "whenMatched": "merge",
                        "whenNotMatched": "discard",
                    }
                }
            )

            self._frames_dataset._aggregate(pipeline=pipeline)

        if delete:
            frame_ids = self._frames_dataset.exclude(self).values("id")
            dst_dataset._clear_frames(frame_ids=frame_ids)

    def _sync_source_field_schema(self, path):
        field = self.get_field(path)
        if field is None:
            return

        dst_dataset = self._source_collection._dataset
        dst_dataset._merge_frame_field_schema({path: field})

        if self._source_collection._is_generated:
            self._source_collection._sync_source_field_schema(path)

    def _sync_source_schema(self, fields=None, delete=False):
        if delete:
            schema = self.get_field_schema()
        else:
            schema = self._frames_dataset.get_field_schema()

        src_schema = self._source_collection.get_frame_field_schema()
        dst_dataset = self._source_collection._root_dataset

        add_fields = []
        del_fields = []

        if fields is not None:
            # We're syncing specific fields; if they are not present in source
            # collection, add them

            for field_name in fields:
                if field_name not in src_schema:
                    add_fields.append(field_name)
        else:
            # We're syncing all fields; add any missing fields to source
            # collection and, if requested, delete any source fields that
            # aren't in this view

            default_fields = set(
                self._get_default_sample_fields(include_private=True)
            )

            for field_name in schema.keys():
                if (
                    field_name not in src_schema
                    and field_name not in default_fields
                ):
                    add_fields.append(field_name)

            if delete:
                for field_name in src_schema.keys():
                    if field_name not in schema:
                        del_fields.append(field_name)

        for field_name in add_fields:
            field_kwargs = foo.get_field_kwargs(schema[field_name])
            dst_dataset.add_frame_field(field_name, **field_kwargs)

        if delete:
            for field_name in del_fields:
                dst_dataset.delete_frame_field(field_name)

    def _sync_source_keep_fields(self):
        schema = self.get_field_schema()
        src_schema = self._source_collection.get_frame_field_schema()

        del_fields = set(src_schema.keys()) - set(schema.keys())
        if del_fields:
            prefix = self._source_collection._FRAMES_PREFIX
            _del_fields = [prefix + f for f in del_fields]
            self._source_collection.exclude_fields(_del_fields).keep_fields()


def make_frames_dataset(
    sample_collection,
    sample_frames=False,
    fps=None,
    max_fps=None,
    size=None,
    min_size=None,
    max_size=None,
    sparse=False,
    output_dir=None,
    rel_dir=None,
    frames_patt=None,
    force_sample=False,
    skip_failures=True,
    verbose=False,
    name=None,
):
    """Creates a dataset that contains one sample per frame in the video
    collection.

    The returned dataset will contain all frame-level fields and the ``tags``
    of each video as sample-level fields, as well as a ``sample_id`` field that
    records the IDs of the parent sample for each frame.

    By default, ``sample_frames`` is False and this method assumes that the
    frames of the input collection have ``filepath`` fields populated pointing
    to each frame image. Any frames without a ``filepath`` populated will be
    omitted from the frames dataset.

    When ``sample_frames`` is True, this method samples each video in the
    collection into a directory of per-frame images and stores the filepaths in
    the ``filepath`` frame field of the source dataset. By default, each folder
    of images is written using the same basename as the input video. For
    example, if ``frames_patt = "%%06d.jpg"``, then videos with the following
    paths::

        /path/to/video1.mp4
        /path/to/video2.mp4
        ...

    would be sampled as follows::

        /path/to/video1/
            000001.jpg
            000002.jpg
            ...
        /path/to/video2/
            000001.jpg
            000002.jpg
            ...

    However, you can use the optional ``output_dir`` and ``rel_dir`` parameters
    to customize the location and shape of the sampled frame folders. For
    example, if ``output_dir = "/tmp"`` and ``rel_dir = "/path/to"``, then
    videos with the following paths::

        /path/to/folderA/video1.mp4
        /path/to/folderA/video2.mp4
        /path/to/folderB/video3.mp4
        ...

    would be sampled as follows::

        /tmp/folderA/
            video1/
                000001.jpg
                000002.jpg
                ...
            video2/
                000001.jpg
                000002.jpg
                ...
        /tmp/folderB/
            video3/
                000001.jpg
                000002.jpg
                ...

    By default, samples will be generated for every video frame at full
    resolution, but this method provides a variety of parameters that can be
    used to customize the sampling behavior.

    .. note::

        If this method is run multiple times with ``sample_frames`` set to
        True, existing frames will not be resampled unless you set
        ``force_sample`` to True.

    .. note::

        The returned dataset is independent from the source collection;
        modifying it will not affect the source collection.

    Args:
        sample_collection: a
            :class:`fiftyone.core.collections.SampleCollection`
        sample_frames (False): whether to assume that the frame images have
            already been sampled at locations stored in the ``filepath`` field
            of each frame (False), or whether to sample the video frames now
            according to the specified parameters (True)
        fps (None): an optional frame rate at which to sample each video's
            frames
        max_fps (None): an optional maximum frame rate at which to sample.
            Videos with frame rate exceeding this value are downsampled
        size (None): an optional ``(width, height)`` at which to sample frames.
            A dimension can be -1, in which case the aspect ratio is preserved.
            Only applicable when ``sample_frames=True``
        min_size (None): an optional minimum ``(width, height)`` for each
            frame. A dimension can be -1 if no constraint should be applied.
            The frames are resized (aspect-preserving) if necessary to meet
            this constraint. Only applicable when ``sample_frames=True``
        max_size (None): an optional maximum ``(width, height)`` for each
            frame. A dimension can be -1 if no constraint should be applied.
            The frames are resized (aspect-preserving) if necessary to meet
            this constraint. Only applicable when ``sample_frames=True``
        sparse (False): whether to only sample frame images for frame numbers
            for which :class:`fiftyone.core.frame.Frame` instances exist in the
            input collection. This parameter has no effect when
            ``sample_frames==False`` since frames must always exist in order to
            have ``filepath`` information used
        output_dir (None): an optional output directory in which to write the
            sampled frames. By default, the frames are written in folders with
            the same basename of each video
        rel_dir (None): a relative directory to remove from the filepath of
            each video, if possible. The path is converted to an absolute path
            (if necessary) via :func:`fiftyone.core.utils.normalize_path`. This
            argument can be used in conjunction with ``output_dir`` to cause
            the sampled frames to be written in a nested directory structure
            within ``output_dir`` matching the shape of the input video's
            folder structure
        frames_patt (None): a pattern specifying the filename/format to use to
            write or check or existing sampled frames, e.g., ``"%%06d.jpg"``.
            The default value is
            ``fiftyone.config.default_sequence_idx + fiftyone.config.default_image_ext``
        force_sample (False): whether to resample videos whose sampled frames
            already exist. Only applicable when ``sample_frames=True``
        skip_failures (True): whether to gracefully continue without raising
            an error if a video cannot be sampled
        verbose (False): whether to log information about the frames that will
            be sampled, if any
        name (None): a name for the dataset

    Returns:
        a :class:`fiftyone.core.dataset.Dataset`
    """
    fova.validate_video_collection(sample_collection)

    if sample_frames != True:
        l = locals()
        for var in ("size", "min_size", "max_size"):
            if l[var]:
                logger.warning(
                    "Ignoring '%s' when sample_frames=%s", var, sample_frames
                )

    if frames_patt is None:
        frames_patt = (
            fo.config.default_sequence_idx + fo.config.default_image_ext
        )

    #
    # Create dataset with proper schema
    #

    dataset = fod.Dataset(name=name, _frames=True)
    dataset.media_type = fom.IMAGE
    dataset.add_sample_field("sample_id", fof.ObjectIdField)

    frame_schema = sample_collection.get_frame_field_schema()
    dataset._sample_doc_cls.merge_field_schema(frame_schema)

    dataset.create_index("sample_id")

    # This index will be used when populating the collection now as well as
    # later when syncing the source collection
    dataset.create_index([("sample_id", 1), ("frame_number", 1)], unique=True)

    _make_pretty_summary(dataset)

    # Initialize frames dataset
    sample_view, frames_to_sample = _init_frames(
        dataset,
        sample_collection,
        sample_frames,
        output_dir,
        rel_dir,
        frames_patt,
        fps,
        max_fps,
        sparse,
        force_sample,
        verbose,
    )

    # Sample frames, if necessary
    if sample_view is not None:
        logger.info("Sampling video frames...")
        fouv.sample_videos(
            sample_view,
            output_dir=output_dir,
            rel_dir=rel_dir,
            frames_patt=frames_patt,
            frames=frames_to_sample,
            size=size,
            min_size=min_size,
            max_size=max_size,
            original_frame_numbers=True,
            force_sample=True,
            save_filepaths=True,
            skip_failures=skip_failures,
        )

    #
    # Merge frame data
    #

    pipeline = []

    if sample_frames == "dynamic":
        pipeline.append({"$project": {"filepath": False}})

    pipeline.extend(
        [
            {"$addFields": {"_dataset_id": dataset._doc.id}},
            {
                "$merge": {
                    "into": dataset._sample_collection_name,
                    "on": ["_sample_id", "frame_number"],
                    "whenMatched": "merge",
                    "whenNotMatched": "discard",
                }
            },
        ]
    )

    sample_collection._aggregate(frames_only=True, post_pipeline=pipeline)

    if sample_frames == False and not dataset:
        logger.warning(
            "Your frames view is empty. Note that you must either "
            "pre-populate the `filepath` field on the frames of your video "
            "collection or pass `sample_frames=True` to this method to "
            "perform the sampling. See "
            "https://docs.voxel51.com/user_guide/using_views.html#frame-views "
            "for more information."
        )

    return dataset


def _make_pretty_summary(dataset):
    set_fields = ["id", "sample_id", "filepath", "frame_number"]
    all_fields = dataset._sample_doc_cls._fields_ordered
    pretty_fields = set_fields + [f for f in all_fields if f not in set_fields]
    dataset._sample_doc_cls._fields_ordered = tuple(pretty_fields)


def _init_frames(
    dataset,
    src_collection,
    sample_frames,
    output_dir,
    rel_dir,
    frames_patt,
    fps,
    max_fps,
    sparse,
    force_sample,
    verbose,
):
    if (
        (sample_frames != False and not sparse)
        or fps is not None
        or max_fps is not None
    ):
        # We'll need frame counts to determine what frames to include/sample
        src_collection.compute_metadata()

    if sample_frames == True and verbose:
        logger.info("Determining frames to sample...")

    #
    # Initialize frames dataset with proper frames
    #

    docs = []
    src_docs = []
    src_inds = []
    missing_filepaths = []

    id_map = {}
    sample_map = defaultdict(set)
    frame_map = defaultdict(set)

    src_dataset = src_collection._root_dataset
    is_clips = src_collection._dataset._is_clips
    if src_collection.has_frame_field("filepath"):
        view = src_collection.select_fields("frames.filepath")
    else:
        view = src_collection.select_fields()

    # If we're sampling frames on a view that may have filtered frames, we must
    # consult the full dataset to see which frames already have docs/filepaths
    has_docs_map = None
    has_filepaths_map = None
    if (
        sample_frames == True
        and not sparse
        and isinstance(src_collection, fov.DatasetView)
        and src_collection._needs_frames()
    ):
        id_field = "sample_id" if is_clips else "id"
        _view = src_dataset.select(src_collection.values(id_field))
        ids, fns = _view.values(["_id", "frames.frame_number"])

        has_docs_map = {_id: set(_fns) for _id, _fns in zip(ids, fns)}

        if src_dataset.has_frame_field("filepath"):
            ids, fns = _view.match_frames(
                fo.ViewField("filepath") != None,
                omit_empty=False,
            ).values(["_id", "frames.frame_number"])
            has_filepaths_map = {_id: set(_fns) for _id, _fns in zip(ids, fns)}

    for sample in view._aggregate(attach_frames=True):
        video_path = sample["filepath"]
        tags = sample.get("tags", [])
        metadata = sample.get("metadata", None) or {}
        frame_rate = metadata.get("frame_rate", None)
        total_frame_count = metadata.get("total_frame_count", -1)
        frames = sample.get("frames", [])

        frame_ids_map = {}
        frames_with_docs = set()
        frames_with_filepaths = set()
        for frame in frames:
            _frame_id = frame["_id"]
            fn = frame["frame_number"]
            filepath = frame.get("filepath", None)

            if sample_frames != False or filepath is not None:
                frame_ids_map[fn] = _frame_id

            if sample_frames == True:
                frames_with_docs.add(fn)
                if filepath is not None:
                    frames_with_filepaths.add(fn)

        if is_clips:
            _sample_id = sample["_sample_id"]
            support = sample["support"]
        else:
            _sample_id = sample["_id"]
            support = None

        _outpath = fouv._get_outpath(
            video_path, output_dir=output_dir, rel_dir=rel_dir
        )
        images_patt = os.path.join(os.path.splitext(_outpath)[0], frames_patt)

        # Determine which frame numbers to include in the frames dataset and
        # whether any frame images need to be sampled
        doc_frame_numbers, sample_frame_numbers = _parse_video_frames(
            video_path,
            sample_frames,
            images_patt,
            support,
            total_frame_count,
            frame_rate,
            frame_ids_map,
            force_sample,
            sparse,
            fps,
            max_fps,
            verbose,
        )

        # Record things that need to be sampled
        # Note: [] means no frames, None means all frames
        if sample_frame_numbers != []:
            id_map[video_path] = str(_sample_id)

            if sample_frame_numbers is None:
                sample_map[video_path] = None
            elif sample_map[video_path] is not None:
                sample_map[video_path].update(sample_frame_numbers)

        # Determine if any docs/filepaths are missing from the source dataset
        if sample_frames == True:
            if has_docs_map is not None:
                frames_with_docs = has_docs_map[_sample_id]

            if has_filepaths_map is not None:
                frames_with_filepaths = has_filepaths_map[_sample_id]

            target_frames = set(doc_frame_numbers)
            missing_docs = target_frames - frames_with_docs
            missing_fps = target_frames - frames_with_filepaths
        else:
            missing_docs = None
            missing_fps = None

        # Create necessary frame documents
        for fn in doc_frame_numbers:
            if is_clips:
                fns = frame_map[video_path]
                if fn in fns:
                    continue  # frame has already been sampled

                fns.add(fn)

            _id = frame_ids_map.get(fn, None)
            _filepath = images_patt % fn
            _rand = foos._generate_rand(_filepath)
            _dataset_id = dataset._doc.id

            if missing_fps is not None and fn in missing_fps:
                missing_filepaths.append((_sample_id, fn, _filepath))

            if sample_frames == "dynamic":
                filepath = video_path
            else:
                # This will be overwritten in the final merge if the actual
                # filepath is different
                filepath = _filepath

            doc = {
                "filepath": filepath,
                "tags": tags,
                "metadata": None,
                "frame_number": fn,
                "_media_type": "image",
                "_rand": _rand,
                "_sample_id": _sample_id,
                "_dataset_id": _dataset_id,
            }

            if _id is not None:
                doc["_id"] = _id
            elif missing_docs is not None and fn in missing_docs:
                # Found a frame that we want to include in the frames dataset
                # whose image is already sampled but for which there is no
                # frame doc in the source collection. We need to create a frame
                # doc so that the frames dataset can use the same frame ID
                src_docs.append({"_sample_id": _sample_id, "frame_number": fn})
                src_inds.append(len(docs))

            docs.append(doc)

            # Commit batch of docs to frames dataset
            if len(docs) >= 10000:
                _insert_docs(docs, src_docs, src_inds, dataset, src_dataset)

    # Add remaining docs to frames dataset
    _insert_docs(docs, src_docs, src_inds, dataset, src_dataset)

    # Add missing frame filepaths to source collection
    if missing_filepaths:
        logger.info(
            "Setting %d frame filepaths on the input collection that exist "
            "on disk but are not recorded on the dataset",
            len(missing_filepaths),
        )
        src_dataset.add_frame_field("filepath", fof.StringField)
        ops = [
            UpdateOne(
                {"_sample_id": _sample_id, "frame_number": fn},
                {"$set": {"filepath": filepath}},
            )
            for _sample_id, fn, filepath in missing_filepaths
        ]
        src_dataset._bulk_write(ops, frames=True)

    #
    # Finalize which frame images need to be sampled, if any
    #
    # We first populate `sample_map` and then convert to `ids_to_sample` and
    # `frames_to_sample` here to avoid resampling frames when working with clip
    # views with multiple overlapping clips into the same video
    #

    ids_to_sample = []
    frames_to_sample = []
    for video_path, sample_frame_numbers in sample_map.items():
        ids_to_sample.append(id_map[video_path])
        if sample_frame_numbers is not None:
            sample_frame_numbers = sorted(sample_frame_numbers)

        frames_to_sample.append(sample_frame_numbers)

    if ids_to_sample:
        if src_dataset.media_type == fom.GROUP:
            sample_view = src_dataset.select_group_slices(media_type=fom.VIDEO)
        else:
            sample_view = src_dataset

        sample_view = sample_view.select(ids_to_sample, ordered=True)
    else:
        sample_view = None

    return sample_view, frames_to_sample


def _insert_docs(docs, src_docs, src_inds, dataset, src_dataset):
    if src_docs:
        foo.insert_documents(src_docs, src_dataset._frame_collection)

        for idx, src_doc in enumerate(src_docs):
            docs[src_inds[idx]]["_id"] = src_doc["_id"]

        src_docs.clear()
        src_inds.clear()

    if docs:
        foo.insert_documents(docs, dataset._sample_collection)
        docs.clear()


def _parse_video_frames(
    video_path,
    sample_frames,
    images_patt,
    support,
    total_frame_count,
    frame_rate,
    frame_ids_map,
    force_sample,
    sparse,
    fps,
    max_fps,
    verbose,
):
    #
    # Determine target frames, taking subsampling into account
    #

    if fps is not None or max_fps is not None:
        target_frame_numbers = fouv.sample_frames_uniform(
            frame_rate,
            total_frame_count=total_frame_count,
            support=support,
            fps=fps,
            max_fps=max_fps,
        )
    elif support is not None:
        first, last = support
        target_frame_numbers = list(range(first, last + 1))
    else:
        target_frame_numbers = None  # all frames

    #
    # Determine frames for which to generate documents
    #

    if target_frame_numbers is None:
        if total_frame_count < 0:
            doc_frame_numbers = sorted(frame_ids_map.keys())
        else:
            doc_frame_numbers = list(range(1, total_frame_count + 1))
    else:
        doc_frame_numbers = target_frame_numbers

    if sparse or sample_frames == False:
        doc_frame_numbers = [
            fn for fn in doc_frame_numbers if fn in frame_ids_map
        ]

    if sample_frames != True:
        return doc_frame_numbers, []

    #
    # Determine frames that need to be sampled
    #

    if force_sample:
        sample_frame_numbers = doc_frame_numbers
    else:
        sample_frame_numbers = _get_non_existent_frame_numbers(
            images_patt, doc_frame_numbers
        )

    if (
        target_frame_numbers is None
        and len(sample_frame_numbers) == len(doc_frame_numbers)
        and len(doc_frame_numbers) >= total_frame_count
    ):
        sample_frame_numbers = None  # all frames

    if verbose:
        count = total_frame_count if total_frame_count >= 0 else "???"
        if sample_frame_numbers is None:
            logger.info(
                "Must sample all %s frames of '%s'",
                count,
                video_path,
            )
        elif sample_frame_numbers != []:
            logger.info(
                "Must sample %d/%s frames of '%s'",
                len(sample_frame_numbers),
                count,
                video_path,
            )
        else:
            logger.info("Required frames already present for '%s'", video_path)

    return doc_frame_numbers, sample_frame_numbers


def _get_non_existent_frame_numbers(images_patt, frame_numbers):
    return [fn for fn in frame_numbers if not os.path.isfile(images_patt % fn)]
