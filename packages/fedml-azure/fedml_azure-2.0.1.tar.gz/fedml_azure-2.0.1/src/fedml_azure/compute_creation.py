from abc import ABC, abstractmethod
from .logger import Logger
try:
    from azureml.core.compute import ComputeTarget, AmlCompute, ComputeInstance, AksCompute
    from azureml.core.compute_target import ComputeTargetException
except:
    pass

class AmlComputeTargets(ABC):

    @abstractmethod
    def create_compute_target(self):
           pass

class ComputeFactory:

    @staticmethod
    def get_compute(compute_type):
        logger = Logger.get_instance()
        try:
            if compute_type.lower()=='amlcomputecluster':
                return AmlComputeCluster()
            
            elif compute_type.lower()=='amlcomputeinstance':
                return AmlComputeInstance()
            
            elif compute_type.lower()=='aks':
                return Aks()
            
            else:
                raise Exception("Specify correct parameter 'compute_type'. The compute types supported are 'AmlComputeCluster', 'AmlComputeInstance' and 'AKS'.")
        
        except Exception as e:
            logger.error(e)
            raise
            


class AmlComputeCluster(AmlComputeTargets):

    def __init__(self):
        self.logger = Logger.get_instance()

    def create_compute_target(self,ws,compute_name=None,vm_size='', vm_priority='dedicated', min_nodes=0, max_nodes=None, idle_seconds_before_scaledown=1800, admin_username=None, admin_user_password=None, admin_user_ssh_key=None, vnet_resourcegroup_name=None, vnet_name=None, subnet_name=None, tags=None, description=None, remote_login_port_public_access='NotSpecified', identity_type=None, identity_id=None, location=None,show_output=True, min_node_count=None, timeout_in_minutes=20):
        try:

            if compute_name is None:
                raise Exception("The parameter 'compute_name' must be specified in 'compute_args'.")

            if compute_name in ws.compute_targets:
                compute_target = ws.compute_targets[compute_name]
                if compute_target and type(compute_target) is AmlCompute:
                    self.logger.info('Found compute target. just use it. %s',compute_name)
                    return compute_target
            else:
                self.logger.info('Creating a new compute target...')
                provisioning_config = AmlCompute.provisioning_configuration(vm_size=vm_size,
                                                                            vm_priority=vm_priority, 
                                                                            min_nodes=min_nodes, 
                                                                            max_nodes=max_nodes, 
                                                                            idle_seconds_before_scaledown=idle_seconds_before_scaledown, 
                                                                            admin_username=admin_username, 
                                                                            admin_user_password=admin_user_password, 
                                                                            admin_user_ssh_key=admin_user_ssh_key, 
                                                                            vnet_resourcegroup_name=vnet_resourcegroup_name, 
                                                                            vnet_name=vnet_name, 
                                                                            subnet_name=subnet_name, 
                                                                            tags=tags, 
                                                                            description=description, 
                                                                            remote_login_port_public_access=remote_login_port_public_access, 
                                                                            identity_type=identity_type, 
                                                                            identity_id=identity_id,
                                                                            location=location
                                                                            )

                # create the cluster
                compute_target = ComputeTarget.create(ws, compute_name, provisioning_config)
                
                # can poll for a minimum number of nodes and for a specific timeout. 
                # if no min node count is provided it will use the scale settings for the cluster
                compute_target.wait_for_completion(show_output=show_output, min_node_count=min_node_count, timeout_in_minutes=timeout_in_minutes)
                
                # For a more detailed view of current AmlCompute status, use get_status()
                self.logger.info(compute_target.get_status().serialize())
                return compute_target
        
        
        except Exception as e:
            self.logger.error(e)
            raise


class AmlComputeInstance(AmlComputeTargets):

    def __init__(self):
        self.logger = Logger.get_instance()

    def create_compute_target(self,ws,compute_name=None,vm_size='', ssh_public_access=False, admin_user_ssh_public_key=None, vnet_resourcegroup_name=None, vnet_name=None, subnet_name=None, tags=None, description=None, assigned_user_object_id=None, assigned_user_tenant_id=None,show_output=True):
        try:
            if compute_name is None:
                raise Exception("The parameter 'compute_name' must be specified in 'compute_args'.")

            instance = ComputeInstance(workspace=ws, name=compute_name)
            self.logger.info('Found existing instance, using it.')
            return instance

        except ComputeTargetException:
            compute_config = ComputeInstance.provisioning_configuration(
                                                                        vm_size=vm_size,
                                                                        ssh_public_access=ssh_public_access,
                                                                        admin_user_ssh_public_key=admin_user_ssh_public_key,
                                                                        vnet_resourcegroup_name=vnet_resourcegroup_name,
                                                                        vnet_name=vnet_name,
                                                                        subnet_name=subnet_name,
                                                                        tags=tags,
                                                                        description=description,
                                                                        assigned_user_object_id=assigned_user_object_id,
                                                                        assigned_user_tenant_id=assigned_user_tenant_id
                                                                    )
            instance = ComputeInstance.create(ws, compute_name, compute_config)
            instance.wait_for_completion(show_output=show_output)
            return instance

        except Exception as e:
            self.logger.error(e)
            raise

def _assign_ssl_configs(prov_config,ssl_cname=None, ssl_cert_pem_file=None, ssl_key_pem_file=None, leaf_domain_label=None, overwrite_existing_domain=False):
    prov_config.enable_ssl(ssl_cname=ssl_cname,
                           ssl_cert_pem_file=ssl_cert_pem_file,
                           ssl_key_pem_file=ssl_key_pem_file,
                           leaf_domain_label=leaf_domain_label,
                           overwrite_existing_domain=overwrite_existing_domain
                           )


class Aks(AmlComputeTargets):
    def __init__(self):
        self.logger = Logger.get_instance()

    def create_compute_target(self,ws,compute_name=None,enable_ssl=False,ssl_args=None,agent_count=None, vm_size=None, ssl_cname=None, ssl_cert_pem_file=None, ssl_key_pem_file=None, location=None, vnet_resourcegroup_name=None, vnet_name=None, subnet_name=None, service_cidr=None, dns_service_ip=None, docker_bridge_cidr=None, cluster_purpose=None, load_balancer_type=None, load_balancer_subnet=None):
        try:
            if compute_name is None:
                raise Exception("The parameter 'compute_name' must be specified in 'compute_args'.")

            # Verify that cluster does not exist already
            try:
                aks_target = ComputeTarget(workspace=ws, name=compute_name)
                self.logger.info('Found existing cluster, use it.')
            except ComputeTargetException:
                # Use the default configuration (can also provide parameters to customize)
                prov_config = AksCompute.provisioning_configuration(agent_count=agent_count,
                                                                    vm_size=vm_size,
                                                                    ssl_cname=ssl_cname,
                                                                    ssl_cert_pem_file=ssl_cert_pem_file,
                                                                    ssl_key_pem_file=ssl_key_pem_file,
                                                                    location=location,
                                                                    vnet_resourcegroup_name=vnet_resourcegroup_name,
                                                                    vnet_name=vnet_name,
                                                                    subnet_name=subnet_name,
                                                                    service_cidr=service_cidr,
                                                                    dns_service_ip=dns_service_ip,
                                                                    docker_bridge_cidr=docker_bridge_cidr,
                                                                    cluster_purpose=cluster_purpose,
                                                                    load_balancer_type=load_balancer_type,
                                                                    load_balancer_subnet=load_balancer_subnet)
                
                if enable_ssl:
                    if ssl_args is None or not isinstance(ssl_args,dict):
                        self.logger.info("The parameter 'ssl_args' is missing or it is not of type 'dict'.")
                        _assign_ssl_configs(prov_config=prov_config)
                    else:
                        ssl_args['prov_config']=prov_config
                        _assign_ssl_configs(**ssl_args)

                # Create the cluster
                aks_target = ComputeTarget.create(workspace = ws, 
                                                name = compute_name, 
                                                provisioning_configuration = prov_config)

            if aks_target.get_status() != "Succeeded":
                aks_target.wait_for_completion(show_output=True)

            return aks_target

        except Exception as e:
            self.logger.error(e)
            raise