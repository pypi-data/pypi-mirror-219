from ._version import __version__
from .utils import *
from .select import *

def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": "jupyterlab_nodeeditor"
    }]
