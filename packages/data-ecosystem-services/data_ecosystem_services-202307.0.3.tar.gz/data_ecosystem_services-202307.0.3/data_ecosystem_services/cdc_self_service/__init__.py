"""Initialize the cdc_self_service subpackage of data_ecosystem_services package"""
# allow absolute import from the root folder
# whatever its name is.
from . import pipeline_metadata
from . import logging_metadata
from . import job_metadata
from . import environment_metadata
from . import dataset_metadata
import sys  # don't remove required for error handling
import os

# Import from sibling directory ..\developer_service
OS_NAME = os.name

sys.path.append("..")
if OS_NAME.lower() == "nt":
    print("cdc_self_service: windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(
        os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("cdc_self_service: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))


__all__ = ['dataset_metadata', 'environment_metadata',
           'job_metadata', 'logging_metadata', 'pipeline_metadata']
