import shutil,os
from .resource_creation import create_workspace,create_compute,create_environment
from .logger import Logger
try:
    import sklearn
    from azureml.core import Workspace,Experiment,Environment,ScriptRunConfig
    from azureml.core.model import Model
    from azureml.core.resource_configuration import ResourceConfiguration
except:
    pass


class DwcAzureTrain:
    def __init__(self,workspace=None,workspace_args=None,experiment=None,experiment_args=None,compute_type=None,compute=None,compute_args=None,environment=None,environment_type=None,environment_args=None):

        try:
            
            #get the logger instance
            self.logger = Logger.get_instance()

            #creation of workspace
            self.workspace=self._create_workspace(workspace,workspace_args)

            #creation of experiment
            self.experiment=self._create_experiment(experiment,experiment_args)

            #creation of compute_target
            self.compute=self._create_compute_target(compute,compute_args,compute_type)
            
            #creation of environment
            self.environment=self._create_environment(environment,environment_type,environment_args)

        except Exception:
            raise    
    
    def _create_workspace(self,workspace=None,workspace_args=None):
        try:
            if workspace is None:
                return create_workspace(workspace_args)
            else:
                if isinstance(workspace,Workspace):
                    self.logger.info("Assigning Workspace.")
                    return workspace
                else:
                    raise Exception("The parameter 'workspace' should be specified and must be of type class 'Workspace'.")
        except Exception as e:
            self.logger.error(e)
            raise

    
    def _create_compute_target(self,compute=None,compute_args=None,compute_type=None):
        try:
            if compute:
               self.logger.info("Assigning compute.")
               return compute
            elif compute_args is not None or compute_type is not None:
                if compute_args is not None and compute_type is not None:
                    return create_compute(self.workspace,compute_type,compute_args)
                else:
                    self.logger.info("The parameters 'compute_type' and 'compute_args' are required for creating a new compute.")
            else:
                self.logger.info("The parameters 'compute', 'compute_args' and 'compute_type' are missing. No compute is created. If a compute needs to be assigned, the parameter 'compute' needs to be specified. The parameters 'compute_type' and 'compute_args' are required for creating a new compute.")
                
        except Exception as e:
            self.logger.error(e)
            raise
    

    
    def _create_environment(self,environment=None,environment_type=None,environment_args=None):
        try:
            if environment is None:
                return create_environment(self.workspace,environment_type,environment_args)
            else:
                if isinstance(environment,Environment):
                    self.logger.info("Assigning Environment.")
                    return environment
                else:raise Exception("The parameter 'environment' should be of type class 'Environment'.")
        
        except TypeError as t:
            self.logger.error("Specify the correct parameters and correct parameter values for 'environment_args'.")
            self.logger.error(t)
            raise

        except Exception as e:
            self.logger.error(e)
            raise
    
    def _create_experiment(self,experiment=None,experiment_args=None):
        try:
            if experiment is None:
                if experiment_args is None or not isinstance(experiment_args,dict):
                    raise Exception("The parameter 'experiment_args' must be specified and should be of type 'dict'.")
                return self._create_new_experiment(**experiment_args)
            else:
                if isinstance(experiment,Experiment):
                    return experiment
                else:
                    raise Exception("The parameter 'Experiment' should be of type class 'Experiment'.")
        except Exception as e:
            self.logger.error(e)
            raise
    
    def _create_new_experiment(self, name=None, _skip_name_validation=False, _id=None, _archived_time=None, _create_in_cloud=True, _experiment_dto=None,**kwargs):
    
        try:
            if name is None:
                raise Exception("The parameter 'name' must be specified.")
            self.logger.info("Creating Experiment")
            return Experiment(workspace=self.workspace, 
                            name=name,
                            _skip_name_validation=_skip_name_validation,
                            _id=_id,
                            _archived_time=_archived_time,
                            _create_in_cloud=_create_in_cloud,
                            _experiment_dto=_experiment_dto,
                            **kwargs)
        except Exception as e:
            self.logger.error(e)
            raise

    
    def update_compute(self,compute=None,compute_args=None,compute_type=None):
        try:
            self.logger.info("Updating compute")
            self.compute=self._create_compute_target(compute,compute_args,compute_type)
        except Exception as e:
            self.logger.error(e)
            raise


    
    def update_environment(self,environment=None,environment_type=None,environment_args=None):
    
        try:
            self.logger.info("Updating environment")
            self.environment=self._create_environment(environment,environment_type,environment_args)
        except Exception as e:
            self.logger.error(e)
            raise

    
    def update_experiment(self,experiment=None,experiment_args=None):
        try:
            self.logger.info("Updating experiment")
            self.experiment=self._create_experiment(experiment,experiment_args)
        except Exception as e:
            self.logger.error(e)
            raise
    
    def _generate_script_run_config(self,source_directory=None, script=None, arguments=None, run_config=None, _telemetry_values=None, compute_target=None, environment=None, distributed_job_config=None, resume_from=None, max_run_duration_seconds=2592000, command=None, docker_runtime_config=None):
        try:
            if source_directory is None:
                raise Exception("The parameter 'source_directory' must be specified.")
            
            if not os.path.isdir(source_directory):
                raise Exception("The 'source_directory' is not accessible.")
            
            if not os.path.isfile(source_directory+'/'+script):
                raise Exception("The script does not exist in the source directory.")
            
            return ScriptRunConfig(source_directory=source_directory,
                                        script=script,
                                        arguments=arguments,
                                        run_config=run_config,
                                        _telemetry_values=_telemetry_values,
                                        compute_target=compute_target,
                                        environment=environment,
                                        distributed_job_config=distributed_job_config,
                                        resume_from=resume_from,
                                        max_run_duration_seconds=max_run_duration_seconds,
                                        command=command,
                                        docker_runtime_config=docker_runtime_config
                                        )
        except Exception as e:
            self.logger.error(e)
            raise
            

    def copy_config_file(self,config_file_path,script_directory):
        try:
            self.logger.info("Copying config file for db connection to script_directory %s",script_directory)

            if os.path.isfile(config_file_path):
                if not os.path.isdir(script_directory):
                    os.makedirs(script_directory, exist_ok=True)
                shutil.copy(config_file_path, script_directory)
            else:
                raise Exception("There was a problem copying the db config file 'config.json' from config_directory {} to script_directory {}. Check the config file path ".format(config_file_path,script_directory))

        except shutil.SameFileError:
            pass
            
        except Exception as e:
            self.logger.error("There was a problem copying the db config file 'config.json' from config_directory to script_directory. Create a db config file 'config.json' for connecting to SAP DWC and provide the path for the config file 'config_file_path', if not already created.")
            self.logger.error(e)              
            raise
    
    def generate_run_config(self,config_args,is_dwc_connection_required=True,config_file_path=None):

        try:
                self.logger.info("Generating script run config.")
                if 'source_directory' not in config_args:
                    raise Exception("The parameter 'source_directory' must be specified.")
                
                if is_dwc_connection_required:

                    if config_file_path is None:
                        raise Exception("The parameter 'config_file_path' must be specified. This parameter specifies the path for the 'config.json' file for SAP DWC connection.")

                    #copy config file for db connection to source_directory
                    self.copy_config_file(config_file_path=config_file_path,script_directory=config_args['source_directory'])
                else:
                    self.logger.info("Skipping the copy of db connection config 'config.json' to 'source_directory'.")

                config_args['compute_target']=self.compute
                config_args['environment']=self.environment

                return self._generate_script_run_config(**config_args)

        except Exception as e:
            self.logger.error(e) 
            raise
    
    def download_files(self,run,prefix='outputs', output_directory=None, output_paths=None, batch_size=100, append_prefix=True):
        try:
            self.logger.info("Downloading the required files.")

            if output_directory is None:
                output_directory='outputs'+'/'+str(self.experiment.name)+'/'+str(run.id)

            self.logger.info("Downloading the files to %s.",output_directory)

            run.download_files(prefix=prefix,
                               output_directory=output_directory,
                               output_paths=output_paths,
                               batch_size=batch_size,
                               append_prefix=append_prefix)

        except Exception as e:
            self.logger.error(e)
    
    
    def submit_run(self,run_config,is_download=False,download_args=None,show_output=True,tags=None, **kwargs):
        try:
            self.logger.info("Submitting training run.")
            run = self.experiment.submit(run_config,tags,**kwargs)
            run.wait_for_completion(show_output)

            if is_download:
                if download_args is not None and isinstance(download_args,dict):
                    self.download_files(run=run,**download_args)
                else:
                    self.download_files(run=run)
            return run
        except Exception as e:
            self.logger.error(e)
            raise
    
    def _create_resource_config(self,cpu=None, memory_in_gb=None, gpu=None):
        try:
            return ResourceConfiguration(cpu=cpu, 
                                         memory_in_gb=memory_in_gb, 
                                         gpu=gpu)
        except Exception as e:
            self.logger.error(e)
            raise
    
    def _register_model(self,run=None,model_name=None, model_path=None, tags=None, properties=None, model_framework=None, model_framework_version=None, description=None, datasets=None, sample_input_dataset=None, sample_output_dataset=None, resource_configuration=None, **kwargs):
        try:

            if model_name is None:
                raise Exception("The parameter 'model_name' must be specified.")

            return run.register_model(model_name=model_name, 
                                model_path=model_path, 
                                tags=tags, 
                                properties=properties, 
                                model_framework=model_framework, 
                                model_framework_version=model_framework_version, 
                                description=description, 
                                datasets=datasets, 
                                sample_input_dataset=sample_input_dataset, 
                                sample_output_dataset=sample_output_dataset, 
                                resource_configuration=resource_configuration, 
                                **kwargs)
        except Exception as e:
            self.logger.error(e)
            raise

    
    def register_model(self,run,model_args,resource_config_args=None,is_sklearn_model=False):
        try:
            self.logger.info("Registering the model.")
            if is_sklearn_model:
                self.logger.info("Configuring parameters for sklearn model.")
                model_args["model_framework"]=Model.Framework.SCIKITLEARN
                if 'model_framework_version' not in model_args:
                    model_args["model_framework_version"]=sklearn.__version__

            if resource_config_args is not None:
                if isinstance(resource_config_args,dict):
                    model_args["resource_configuration"]=self._create_resource_config(**resource_config_args)
                else:
                    raise Exception("The parameter 'resource_config' must be of type 'dict'.")

            return self._register_model(run=run,**model_args)


        except Exception as e:
            self.logger.error(e)
            raise
