"""
FiftyOne Zoo models provided by :mod:`torchvision:torchvision.models`.

| Copyright 2017-2023, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import inspect
from packaging import version

import eta.core.utils as etau

import fiftyone as fo
import fiftyone.core.utils as fou
import fiftyone.utils.torch as fout
import fiftyone.zoo.models as fozm

fou.ensure_torch()
import torchvision


class TorchvisionImageModelConfig(
    fout.TorchImageModelConfig, fozm.HasZooModel
):
    """Configuration for running a :class:`TorchvisionImageModel`.

    Args:
        entrypoint_fcn: a fully-qualified function string like
            ``"torchvision.models.inception_v3"`` specifying the entrypoint
            function that loads the model
        entrypoint_args (None): a dictionary of arguments for
            ``entrypoint_fcn``
        output_processor_cls: a string like
            ``"fifytone.utils.torch.ClassifierOutputProcessor"`` specifying the
            :class:`fifytone.utils.torch.OutputProcessor` to use
        output_processor_args (None): a dictionary of arguments for
            ``output_processor_cls(classes=classes, **kwargs)``
        confidence_thresh (None): an optional confidence threshold apply to any
            applicable predictions generated by the model
        labels_string (None): a comma-separated list of the class names for the
            model, if applicable
        labels_path (None): the path to the labels map for the model, if
            applicable
        mask_targets (None): a mask targets dict for the model, if applicable
        mask_targets_path (None): the path to a mask targets map for the model,
            if applicable
        skeleton (None): a keypoint skeleton dict for the model, if applicable
        image_min_size (None): resize the input images during preprocessing, if
            necessary, so that the image dimensions are at least this
            ``(width, height)``
        image_min_dim (None): resize input images during preprocessing, if
            necessary, so that the smaller image dimension is at least this
            value
        image_max_size (None): resize the input images during preprocessing, if
            necessary, so that the image dimensions are at most this
            ``(width, height)``
        image_max_dim (None): resize input images during preprocessing, if
            necessary, so that the largest image dimension is at most this
            value.
        image_size (None): a ``(width, height)`` to which to resize the input
            images during preprocessing
        image_dim (None): resize the smaller input dimension to this value
            during preprocessing
        image_mean (None): a 3-array of mean values in ``[0, 1]`` for
            preprocessing the input images
        image_std (None): a 3-array of std values in ``[0, 1]`` for
            preprocessing the input images
            inputs that are lists of Tensors
        embeddings_layer (None): the name of a layer whose output to expose as
            embeddings. Prepend ``"<"`` to save the input tensor instead
        use_half_precision (None): whether to use half precision (only
            supported when using GPU)
        cudnn_benchmark (None): a value to use for
            :attr:`torch:torch.backends.cudnn.benchmark` while the model is
            running
    """

    def __init__(self, d):
        d = self.init(d)
        super().__init__(d)


class TorchvisionImageModel(fout.TorchImageModel):
    """Wrapper for evaluating a :mod:`torchvision:torchvision.models` model on
    images.

    Args:
        config: an :class:`TorchvisionImageModelConfig`
    """

    def _download_model(self, config):
        config.download_model_if_necessary()

    def _load_network(self, config):
        entrypoint = etau.get_function(config.entrypoint_fcn)
        kwargs = config.entrypoint_args or {}
        model_dir = fo.config.model_zoo_dir

        monkey_patcher = _make_load_state_dict_from_url_monkey_patcher(
            entrypoint, model_dir
        )
        with monkey_patcher:
            # Builds net and loads state dict from `model_dir`
            model = entrypoint(**kwargs)

        return model


def _make_load_state_dict_from_url_monkey_patcher(entrypoint, model_dir):
    """Monkey patches all instances of ``load_state_dict_from_url()`` that are
    reachable from the given ``entrypoint`` function in the
    :mod:`torchvision:torchvision.models` namespace so that models will be
    loaded from ``model_dir`` and not from the Torch Hub cache directory.
    """
    entrypoint_module = inspect.getmodule(entrypoint)
    if version.parse(torchvision.__version__) >= version.parse("0.12.0"):
        entrypoint_module = torchvision._internally_replaced_utils

    load_state_dict_from_url = entrypoint_module.load_state_dict_from_url

    def custom_load_state_dict_from_url(url, **kwargs):
        return load_state_dict_from_url(url, model_dir=model_dir, **kwargs)

    return fou.MonkeyPatchFunction(
        entrypoint_module,
        custom_load_state_dict_from_url,
        fcn_name=load_state_dict_from_url.__name__,
        namespace=torchvision.models,
    )
