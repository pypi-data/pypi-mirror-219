import os
import tempfile
from pydlmeta.config import PYDLMETA_TMP_ROOT

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def get_temp_path():
    if not os.path.isdir(PYDLMETA_TMP_ROOT):
        os.makedirs(PYDLMETA_TMP_ROOT)

    return os.path.abspath(
        os.path.join(PYDLMETA_TMP_ROOT, next(tempfile._get_candidate_names())))
