from abaqus import mdb, openMdb
from abml.abml_models import Abml_Model
from abml.abml_session import Abml_Session
from abml.abml_analysis import Abml_Analysis
from abml.abml_helpers import cprint, sort_dict_by_suffix
import logging
from os import getcwd, chdir

logger = logging.getLogger("test_model")


class Abml_Cae:
    def __init__(self, analysis, session, models, **kwargs):
        self.kwargs = kwargs

        cae_path = self.kwargs.get("cae", None)
        cwd = self.kwargs.get("cwd", getcwd())
        chdir(cwd)

        if cae_path is not None:
            self.open_cae(cae_path)

        for model in models:
            Abml_Model(**{model:models[model]})
        
        if session is not None:
            Abml_Session(**session)
        
        if analysis is not None:
            Abml_Analysis(**analysis)
        
        if ("Model-1" not in models.keys()) and ("Model-1" in mdb.models.keys()):
            try:
                del mdb.models["Model-1"]
            except KeyError:
                pass


    def open_cae(self, path):
        openMdb(pathName=path)

    def save_cae(self, filename):
        mdb.saveAs(pathName=filename)
