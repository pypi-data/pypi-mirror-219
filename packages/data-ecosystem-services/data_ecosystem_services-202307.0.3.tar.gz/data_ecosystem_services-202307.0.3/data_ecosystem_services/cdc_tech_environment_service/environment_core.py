""" Module for spark and os environment for cdc_tech_environment_service with minimal dependencies. """

import os
from typing import Tuple
from pathlib import Path

# library management
from importlib import util  # library management

# error handling
from subprocess import check_output, Popen, PIPE, CalledProcessError
import subprocess

#  data
os.environ['PYARROW_IGNORE_TIMEZONE'] = '1'
pyspark_pandas_loader = util.find_spec("pyspark.pandas")
pyspark_pandas_found = pyspark_pandas_loader is not None


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class EnvironmentCore:
    """ EnvironmentCore class with minimal dependencies for the developer service.
    - This class is used to configure the python environment.
    - This class also provides a broad set of generic utility functions.
    """

    @staticmethod
    def get_environment_name() -> Tuple[str, str, str]:
        """Returns the environment, project id and virtual environment name

        The function assumes that the virtual environment name is in the format `project_environment`,
        where `project` represents the project id and `environment` represents the environment (like 'dev', 'prod', etc.)

        Returns:
            Tuple[str, str, str]: A tuple where the first element is the environment, 
            the second element is the project id and the third element is the virtual environment name. 
            Returns None for all if no virtual environment is active.
        """
        env_path = os.getenv('VIRTUAL_ENV')

        if not env_path:
            return None, None, None

        virtual_env = os.path.basename(env_path)

        if '_' not in virtual_env:
            path = Path(env_path)
            if len(path.parts) > 2:
                project_id = os.path.basename(os.path.normpath(path))
                virtual_env = project_id + "_dev"
            else:
                virtual_env = 'ocio_pade_dev'
                project_id = "ocio_pade"
            environment = "dev"
        else:
            virtual_env = virtual_env.lower()
            parts = virtual_env.rsplit('_', 2)
            if len(parts) > 2:
                project_id = parts[0] + "_" + parts[1]
                environment = parts[2]
                virtual_env = project_id + "_" + environment
            else:
                virtual_env = 'ocio_pade_dev'
                project_id = "ocio_pade"

        return environment, project_id, virtual_env

    @classmethod
    def print_version(cls) -> str:
        """ Prints version of library

        Returns:
            str: version of library
        """

        print_version_command = ["poetry", "version"]
        print_version_command_string = ' '.join(print_version_command)
        print(print_version_command_string)
        current_working_dir = os. getcwd()
        print_version_result = f"current_working_dir:{current_working_dir}"
        try:
            print_version_result = check_output(print_version_command)
            # print_version_result = cls.execute(print_version_command)
            print_version_result = f"{str(print_version_result)}:{print_version_command_string} succeeded"
        except subprocess.CalledProcessError as ex_called_process:
            error_string = ex_called_process.output
            print_version_result = str(print_version_result)
            if error_string is None:
                new_error_string = f": {print_version_command_string} succeeded with Exception"
                print_version_result = print_version_result + new_error_string

            else:
                print_version_result = print_version_result + \
                    f"Error: {error_string}"

        print_version_result = str(print_version_result)
        print(print_version_result)
        return print_version_result
