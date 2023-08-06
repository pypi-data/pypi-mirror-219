import pathlib
import os
import tempfile
PYDLMETA_PATH = pathlib.Path(__file__).parent.parent
PYDLMETA_TMP_ROOT = pathlib.Path(
    os.environ.get('PYDLMETA_TMP_ROOT',
                   f"{tempfile._get_default_tempdir()}/pydlmeta"))