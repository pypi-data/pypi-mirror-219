import os
from json import load
from pkg_resources import resource_stream
from abc import ABC, abstractmethod
from .logger import Logger
try:
    from azureml.core import Environment
    from azureml.core.conda_dependencies import CondaDependencies
except:
    pass

class AmlEnvironment(ABC):
    
    @abstractmethod
    def create_environment(self):
           pass


class EnvironmentFactory:
    
    @staticmethod
    def get_environment(environment_type):
        logger = Logger.get_instance()
        try:
            if environment_type.lower()=='condapackageenvironment':
                return CondaPackageEnvironment()
            
            elif environment_type.lower()=='condaspecificationenvironment':
                return CondaSpecificationEnvironment()
            
            else:
                raise Exception("Specify the correct parameter 'environment_type'. The 'environment_type' supported are 'CondaPackageEnvironment', 'CondaSpecificationEnvironment'.")
        
        except Exception as e:
            logger.error(e)
            raise

class CondaPackageEnvironment(AmlEnvironment):

    def __init__(self):
        self.logger = Logger.get_instance()

    def create_environment(self,workspace,name=None,python_version=None,conda_packages=None,pip_packages=None,pip_indexurl=None,pin_sdk_version=True,pip_wheel_files=None):
        try:
            configs = load(resource_stream('fedml_azure', 'internal_config.json'))
            function_configs=configs["environment_creation"]["CondaPackageEnvironment"]["create_environment"]

            if python_version is None:
                python_version=function_configs["python_version"]

            default_conda_packages=function_configs["conda_packages"]
            default_pip_packages=function_configs["pip_packages"]

            pip_wheels=[]

            if name is None:
                raise Exception("The parameter 'name' must be specified in 'environment_args'.")
            
            if conda_packages is not None and not isinstance(conda_packages,list):
                    raise Exception("The parameter 'conda_packages' must be of type list.")
            
            if pip_packages is not None and not isinstance(pip_packages,list):
                    raise Exception("The parameter 'pip_packages' must be of type list.")
            
            if pip_wheel_files is not None:
                if not isinstance(pip_wheel_files,list):
                    raise Exception("The parameter 'pip_wheel_files' must be of type 'list'.")

                for pip_wheel_file in pip_wheel_files:
                    pip_wheels.append(Environment.add_private_pip_wheel(workspace=workspace,file_path = pip_wheel_file,exist_ok=True))

            environment = Environment(name=name)
            environment.python.conda_dependencies = CondaDependencies.create(
                                                                            python_version=python_version,
                                                                            conda_packages=default_conda_packages+ (conda_packages if (conda_packages is not None) else []), 
                                                                            pip_packages=default_pip_packages + (pip_packages if (pip_packages is not None) else []) + pip_wheels,
                                                                            pip_indexurl=pip_indexurl,
                                                                            pin_sdk_version=pin_sdk_version
                                                                            )

            return environment
        
        except Exception as e:
            self.logger.error(e)
            raise

class CondaSpecificationEnvironment(AmlEnvironment):

    def __init__(self):
        self.logger = Logger.get_instance()

    def create_environment(self,workspace,name=None, file_path=None,pip_wheel_files=None):
        try:

            if name is None or file_path is None:
                raise Exception("The parameters 'name', 'file_path' must be specified in 'environment_args'.")
            
            if not os.path.isfile(file_path):
                raise Exception("The dependency file could not be read from the 'file_path' location.")
            
            environment=Environment.from_conda_specification(name = name, file_path = file_path)

            if pip_wheel_files is not None:
                if not isinstance(pip_wheel_files,list):
                    raise Exception("The parameter 'pip_wheel_files' must be of type 'list'.")

                for pip_wheel_file in pip_wheel_files:
                    environment.python.conda_dependencies.add_pip_package(Environment.add_private_pip_wheel(workspace=workspace,file_path = pip_wheel_file,exist_ok=True))
                    
            return environment

        except Exception as e:
            self.logger.error(e)
            raise
        





        