from torchdistill.common.main_util import load_ckpt
from torchdistill.models.official import get_object_detection_model
from torchdistill.models.registry import get_model
from torchdistill.models.registry import register_model_class, register_model_func

from sc2bench.models.detection.base import check_if_updatable_detection_model

DETECTION_MODEL_CLASS_DICT = dict()
DETECTION_MODEL_FUNC_DICT = dict()


def register_detection_model_class(cls):
    DETECTION_MODEL_CLASS_DICT[cls.__name__] = cls
    register_model_class(cls)
    return cls


def register_detection_model_func(func):
    DETECTION_MODEL_FUNC_DICT[func.__name__] = func
    register_model_func(func)
    return func


def get_detection_model(cls_or_func_name, **kwargs):
    if cls_or_func_name in DETECTION_MODEL_CLASS_DICT:
        print("testy boy 1a")
        return DETECTION_MODEL_CLASS_DICT[cls_or_func_name](**kwargs)
    elif cls_or_func_name in DETECTION_MODEL_FUNC_DICT:
        print("testy boy 1b")
        return DETECTION_MODEL_FUNC_DICT[cls_or_func_name](**kwargs)
    return None


def load_detection_model(model_config, device, strict=True):
    model = get_object_detection_model(model_config)
    model_name = model_config['name']
    if model is None:
        model = get_detection_model(model_name, **model_config['params'])

    if model is None:
        repo_or_dir = model_config.get('repo_or_dir', None)
        model = get_model(model_name, repo_or_dir, **model_config['params'])

    if model_config.get('update_before_ckpt', False) and check_if_updatable_detection_model(model):
        model.update()

    ckpt_file_path = model_config['ckpt']
    load_ckpt(ckpt_file_path, model=model, strict=strict)
    return model.to(device)
