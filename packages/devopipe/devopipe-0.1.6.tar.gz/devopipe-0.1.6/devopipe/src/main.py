from typing import Dict, Optional

import typer
import os
import shutil
from pathlib import Path
from string import Template
from jinja2 import Environment, FileSystemLoader
import yaml
import subprocess
import random


app = typer.Typer()


@app.command()
def version():
    typer.echo(f"Typer version: {typer.__version__}")


@app.command()
def hello(name: str, iq: int, display_iq: bool = True, age: Optional[int] = None):
    print(f"Hello {name}")
    if display_iq:
        print(f"Your IQ is {iq}")
    if age:
        typer.echo(f"You have this age: {age}")
    else:
        typer.echo("Age not known!")




def choose_option(options: list):
    """
    Given a list of options, prompts the user to choose one and returns the chosen option.
    """
    for i, option in enumerate(options):
        typer.echo(f"{i + 1}: {option}")
    response = typer.prompt("Enter the number corresponding to your choice: ")
    try:
        index = int(response) - 1
        return options[index]
    except:
        typer.echo("Invalid choice. Please enter a number corresponding to an option.")
        return choose_option(options)
    


@app.command()
def init(file: str = None):
    """
    Prompts the user with a series of questions about setting up a CI/CD pipeline.
    """
    #with open("./src/templates/azure-pipelines.txt", 'r') as file:
    #    template_content = file.read()


    ci_system = "Azure Pipelines"
    tests = "Sonarqube"
    service_provider = "AWS"
    region = "us-east-1"
    name_cluster = "Devopipe"
    environment_names = ["test", "staging", "prod"]
    registry = "ECR (Elastic Container Registry)"
    repository_type = "Public" 
    data_migration = "Flyway"
    source_control = "Bitbucket"
    database = "Postgres"
    cd_tool = "Argocd"
    monitoring_stack = "ELK"


    if file is not None:
        yaml_values = read_yaml(file)
        
        print(yaml_values)



        ci_system = yaml_values["init"]["ci_system"]
        tests = yaml_values["init"]["tests"]
        service_provider = yaml_values["init"]["service_provider"]
        region = yaml_values["init"]["region"]
        environment_names = yaml_values["init"]["environment_names"]
        registry = yaml_values["init"]["registry"]
        repository_type = yaml_values["init"]["repository_type"]
        data_migration = yaml_values["init"]["data_migration"]
        source_control = yaml_values["init"]["source_control"]
        database = yaml_values["init"]["database"]
        cd_tool = yaml_values["init"]["cd_tool"]
        monitoring_stack = yaml_values["init"]["monitoring_stack"]


    else:
        print("else")
        ###########Give me: name of frontend, backend, databse, flyway image on docker compose,
        ########### What type of migration tool are you using
        ##########typer.echo("What CI will you use?")
        ##########ci_system = choose_option(["Azure Pipelines", "GitHub Actions"]) # For Pipeline
        ##########typer.echo("What tests plataform will you use?")
        ##########tests = choose_option(["Sonarqube", "Codacy"]) # For Kubernetes or Pipeline
        ##########typer.echo("What service provider will you use?")
        ##########service_provider = choose_option(["On-prem", "AWS", "Azure", "GCP"]) # For Kubernetes and Terraform
        ##########region = typer.prompt("Wich cloud region do you wanna use? ")
        ######################num_environments = int(typer.prompt("How many environments will you have? ")) # For kubernetes and Terraform
        ##########environment_names = typer.prompt("What are the names of your environments (separated by commas)? ") # For kubernetes and Terraform
        ##########registry = choose_option(["ECR (Elastic Container Registry)", "ACR (Azure Container Registry)", "Docker Hub"]) # For Pipeline and Kubernetes
        ##########typer.echo("Your repositories are:")
        ##########repository_type = choose_option(["Public", "Private"]) # For Pipeline and Terraform 
        ##########typer.echo("What migration tool will you use?")
        ##########monitoring_stack = choose_option(["Flyway", "Liquibase"]) # For Terraform
        ##########typer.echo("What stack do you wanna use for monitorization?")
        ###########Ask for Argocd
        ########### Bitbucket or github
        ##########typer.echo("What Source Control will you use?")
        ##########source_control = choose_option(["Bitbucket", "GitHub"]) # For Source Control
        ########### Qual base de dados
        ##########typer.echo("What Database will you use?")
        ##########database = choose_option(["Postgres"]) # For Source Control
        ##########typer.echo("Which Delievery tool will you use?")
        ##########cd_tool = choose_option(["Argocd"]) # For Source Control
        ##########typer.echo("Which Monitoring Stack will you use?")
        ##########monitoring_stack = choose_option(["ELK", "Prometheus + Loki"]) # For Terraform

    ## Create a template object
    #template = Template(template_content)

    ## Define the parameters
    #params = {'name': 'John', 'day': 'Monday'}

    ## Substitute the placeholders with actual values
    #filled_template = template.substitute(params)

    ## Print the filled template
    #print(filled_template)
    

    # Print out the answers for verification
    typer.echo(f"CI System: {ci_system}")
    typer.echo(f"Tests: {tests}")
    typer.echo(f"Service Provider: {service_provider}")
    typer.echo(f"Environment Names: {environment_names}")
    typer.echo(f"Registry: {registry}")
    typer.echo(f"Cluster name: {name_cluster}")
    typer.echo(f"Cloud Region: {region}")
    typer.echo(f"Repository Type: {repository_type}")
    typer.echo(f"Data Migration Tool: {data_migration}")
    typer.echo(f"Source Control: {source_control}")
    typer.echo(f"Database: {database}")
    typer.echo(f"Continuous Delievery Tool: {cd_tool}")
    typer.echo(f"Monitorization: {monitoring_stack}")

    if ci_system == "Azure Pipelines":
        template_dir = ["templates","ci-pipeline"]
        pipeline_frontend = mountAzurePipelineFrontend(registry, template_dir)
        typer.echo(type(pipeline_frontend))
        pipeline_backend = mountAzurePipelineBackend(registry, template_dir)
        #mountAzurePipeline(registry)
    folder_path = "./.azure-pipelines/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    #pipeline_frontend = ruamel.yaml.safe_load(pipeline_frontend)
    #pipeline_backend = ruamel.yaml.safe_load(pipeline_backend)

    #pipeline_frontend_formatted_yaml = yaml.dump(pipeline_frontend)
    #pipeline_backend_formatted_yaml = yaml.dump(pipeline_backend)
    
    save_template(pipeline_frontend, folder_path + "pipeline_frontend.yaml")
    save_template(pipeline_backend, folder_path + "pipeline_backend.yaml")

    # mount Terraform, Kubernetes
    if service_provider == "AWS":
        template_dir_terra = ["templates", "IaC", "aws"]
        template_dir_kubernetes = ["templates", "kubernetes"]
        template_dir_kubernetes_apps = ["templates", "kubernetes", "apps/"]
        template_dir_kub_cloud = ["templates", "kubernetes", "aws/"]
        
        arr = ["runnable", "terraform", "aws"]
        script_directory = os.path.dirname(os.path.abspath(__file__))
        #template_dir = os.path.join(script_directory, "templates","ci-pipeline")
        template_dir_source = os.path.join(script_directory, *arr)
        bucket_name = name_cluster.lower() + "-state-bucket-" + "".join([str(random.randint(0, 9)) for _ in range(6)])
        dynamodb_table = f'terraform-state-locking-{name_cluster.lower()}'
        create_aws_resources(template_dir_source, bucket_name, dynamodb_table ,region, name_cluster)
        mountTerraformAWS(name_cluster, environment_names, region, bucket_name, template_dir_terra)
        mountKubernetesAWS(name_cluster, environment_names, region, template_dir_kubernetes, template_dir_kubernetes_apps, template_dir_kub_cloud)


    # mount CD tool
    if cd_tool == "Argocd":
        template_dir_argocd = ["templates","IaC","aws", "argocd"]
        mountArgoCD(environment_names, template_dir_argocd)

    # mount test tool
    if tests == "Sonarqube":
        template_dir_sonarqube = ["templates", "tests"]
        mountSonarqube(service_provider, template_dir_sonarqube)



def mountSonarqube(service_provider, template_dir):
    if service_provider == "AWS":
        folder_path = "./kubernetes/aws/"
    
    if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    save_template(render_template(template_dir, "database-sonarqube.yaml", {}), folder_path + "database-sonarqube.yaml")
    save_template(render_template(template_dir, "deployment-sonarqube.yaml", {}), folder_path + "deployment-sonarqube.yaml")
    save_template(render_template(template_dir, "storage_sonarqube.yaml", {}), folder_path + "storage_sonarqube.yaml")



def mountArgoCD(environment_names, template_dir):
    template_dir_vcluster_values = ["templates", "IaC", "aws", "values"]
    folder_path = "./IaC/"
    folder_path_argocd = folder_path + "argocd/"
    if not os.path.exists(folder_path_argocd):
        os.makedirs(folder_path_argocd)

    save_template(render_template(template_dir, "argocd.yaml", {}), folder_path_argocd + "argocd.yaml")
    save_template(render_template(template_dir, "git-repo-secret.yaml", {}), folder_path_argocd + "git-repo-secret.yaml")

    folder_path_values = folder_path + "values/"
    if not os.path.exists(folder_path_values):
        os.makedirs(folder_path_values)
    
    save_template(render_template(template_dir, "argocd.yaml", {}), folder_path_values + "argocd.yaml")

    for i, env_name in enumerate(environment_names):
        save_template(render_template(template_dir_vcluster_values, "vcluster-config-init.yaml", {
            'url': "url_kubernetes",
            'username': "username",
            'password': "password",
            'argocd_name': env_name.lower() + "-apps",
            'argocd_path':  "environments/" + env_name.lower() + "/apps"
        }), folder_path_values + "vcluster-" + env_name.lower() + ".yaml")



def mountKubernetesAWS(name_cluster, environment_names, region, template_dir, template_dir_kubernetes_apps, template_dir_cloud):
    folder_path = "./kubernetes/"
    folder_path_aws = folder_path + "aws/"
    if not os.path.exists(folder_path_aws):
        os.makedirs(folder_path_aws)

    #mount Aws resources
    save_template(render_template(template_dir_cloud, "storage.yaml", {}), folder_path_aws + "storage.yaml")
    save_template(render_template(template_dir_cloud, "service-account.yaml", {}), folder_path_aws + "service-account.yaml")

    for i, env_name in enumerate(environment_names):
        save_template(render_template(template_dir_cloud, "ingress_aws.yaml", {
            'frontend_service': 'myapp-x-default-x-' + env_name.lower() +'-vcluster',
            'backend_service': 'myapp-backend-x-default-x-' + env_name.lower() +'-vcluster',
            'frontend_route': '/frontend/',
            'backend_route': '/api/v1/',
        }), folder_path_aws + "ingress_aws" + env_name.lower() + ".yaml")



    #mount environment resources
    for i, env_name in enumerate(environment_names):
        folder_path_env = folder_path + env_name.lower() + '/apps/'
        if not os.path.exists(folder_path_env):
            os.makedirs(folder_path_env)
        
        save_template(render_template(template_dir_kubernetes_apps, "deployment_backend.yaml", {}), folder_path_env + "/deployment_backend.yaml")
        save_template(render_template(template_dir_kubernetes_apps, "deployment_database.yaml", {}), folder_path_env + "/deployment_database.yaml")
        save_template(render_template(template_dir_kubernetes_apps, "deployment.yaml", {}), folder_path_env + "/deployment.yaml")
        save_template(render_template(template_dir_kubernetes_apps, "pgadmin-deploy.yaml", {}), folder_path_env + "/pgadmin-deploy.yaml")
        save_template(render_template(template_dir_kubernetes_apps, "pgadmin-secret.yaml", {}), folder_path_env + "/pgadmin-secret.yaml")




def mountTerraformAWS(name_cluster, environment_names, region, bucket_name, template_dir):
    folder_path = "./IaC/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    rendered_template_variables = render_template(template_dir, "variables.tf", {
        'cluster_name': name_cluster,
        'state_region': region,
        'bucket_name': bucket_name
    })

    rendered_template_namespaces = ""
    rendered_template_vclusters = ""

    for i, env_name in enumerate(environment_names):
        namespace_name = name_cluster.lower() + '-' + env_name.lower()
        rendered_template_namespaces += render_template(template_dir, "create-namespace.yaml", {
            'namespace_name': namespace_name
        })
        rendered_template_vclusters += render_template(template_dir, "create-vcluster.yaml", {
            'vcluster_name': env_name.lower() + "-vcluster",
            'namespace_name': namespace_name,
            'values_file': "values/" + namespace_name + ".yaml",
            'depends_on': "kubernetes_namespace." + namespace_name
        })

    
    save_template(rendered_template_variables, folder_path + "variables.tf")
    save_template(render_template(template_dir, "vpc-module.tf", {}), folder_path + "vpc-module.tf")
    save_template(render_template(template_dir, "main.tf", {}), folder_path + "main.tf")
    save_template(render_template(template_dir, "kubernetes-addons.tf", {
        'create_namespace': rendered_template_namespaces,
        'create_vcluster': rendered_template_vclusters
    }), folder_path + "kubernetes-addons.tf")
    save_template(render_template(template_dir, "developer-role.tf", {}), folder_path + "developer-role.tf")
    save_template(render_template(template_dir, "blueprints.tf", {}), folder_path + "blueprints.tf")





def mountAzurePipelineFrontend(registry, template_dir):
    phases_frontend = mountAzurePipeline(template_dir, registry, 'frontend_image', 'frontend_artifact', ['AWS_FRONTEND_REPOSITORY', 'frontend_react'] )

    rendered_template_frontend = render_template(template_dir, "azure-pipelines.yaml", {
        'set_artifacts_build': phases_frontend[0],
        'get_artifacts_deploy': phases_frontend[1],
        'deploy_artifact': phases_frontend[2]
    })
    
    typer.echo(rendered_template_frontend)

    return rendered_template_frontend


def mountAzurePipelineBackend(registry, template_dir):
    phases_api = mountAzurePipeline(template_dir, registry, 'backend_fastapi', 'Fastapi_Artifact', ['AWS_API_REPOSITORY', 'backend_fastapi'] )
    phases_data_migration = mountAzurePipeline(template_dir, registry, 'frontend_image', 'frontend_artifact', ['AWS_FLYWAY_REPOSITORY', 'migrations_flyway'] )

    rendered_template_backend = render_template(template_dir, "azure-pipelines.yaml", {
        'set_artifacts_build': phases_api[0] + phases_data_migration[0],
        'get_artifacts_deploy': phases_api[1] + phases_data_migration[1],
        'deploy_artifact': phases_api[2] + phases_data_migration[2]
    })
    
    typer.echo(rendered_template_backend)

    return rendered_template_backend




def mountAzurePipeline(template_dir, registry, artifact_tar, artifact_name, registry_variables ):
    

    pipeline_build_template = render_template(template_dir, "set-artifact.yaml", {
        'artifact_tar_name' : artifact_tar,
        'artifact_pipeline_name': artifact_name
    })
    pipeline_get_artifact_file = render_template(template_dir, "get-artifact.yaml", {
        'artifact_tar_name' : artifact_tar,
        'artifact_pipeline_name': artifact_name
    })
    
    if registry == "ECR (Elastic Container Registry)":
        deploy_artifact_file = render_template(template_dir, "deploy-artifacts-ecr.yaml", {
                'repository_variable' : registry_variables[0],
                'image_name' : registry_variables[1]
            })
    elif registry == "ACR (Azure Container Registry)":
        #To implement
        test = 1
    elif registry == "Docker Hub":
        deploy_artifact_file = render_template(template_dir, "deploy-artifacts-docker-hub.yaml", {
            'image_name' : registry_variables[0],
            'registry_username' : registry_variables[1],
            'registry_name' : registry_variables[2]
        })

    return [pipeline_build_template, pipeline_get_artifact_file, deploy_artifact_file]



#def load_template(template_file: str, variables: Dict[str, str]) -> str:
#    with open(template_file, "r") as file:
#        template = file.read()
#        filled_template = template.format(**variables)
#        return filled_template

# Helper function to save a filled template to a file
def save_template(template: str, output_file: str):
    with open(output_file, "w") as file:
        file.write(template)


def render_template(template_dir,template_file, context):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    template_dir_source = os.path.join(script_directory, *template_dir)

    file_loader = FileSystemLoader(template_dir_source)
    env = Environment(loader=file_loader)
    #current_directory_source = os.path.dirname(os.path.abspath(__file__))
    template = env.get_template(template_file)
    rendered_template = template.render(context)
    return rendered_template

#template_mappings = {
#    "azure-pipelines.yaml": {"tests": "tests"},
#    "steps_template.yaml": {}  # Add variables specific to the steps template
#    # Add mappings for other template files
#}
#
## Render the templates and save them to files
#for template_file, variables in template_mappings.items():
#    filled_template = load_template(template_file, variables)
#    output_file = f"{os.path.splitext(template_file)[0]}.yml"  # Output file name based on the template file
#    save_template(filled_template, output_file)




def create_aws_resources(file_path, bucket_name, dynamodb_table, region, project_name):
    # Run the Terraform command as a subprocess
    #subprocess.run(['terraform', 'apply', '-auto-approve', '-input=false', '-var', f'bucket_name={bucket_name}', '-var', f'region={region}', '-var', f'project_name={project_name}'], cwd=file_path)
    typer.echo(bucket_name)
    # Create S3 bucket
    subprocess.run(['aws', 's3api', 'create-bucket', '--bucket', bucket_name, '--region', region])

    # Enable versioning for the S3 bucket
    subprocess.run(['aws', 's3api', 'put-bucket-versioning', '--bucket', bucket_name, '--versioning-configuration', 'Status=Enabled'])

    # Create DynamoDB table
    subprocess.run(['aws', 'dynamodb', 'create-table', '--table-name', dynamodb_table, '--attribute-definitions', 'AttributeName=LockID,AttributeType=S', '--key-schema', 'AttributeName=LockID,KeyType=HASH', '--billing-mode', 'PAY_PER_REQUEST'])

    print(f'{project_name.lower()}_front')

    # Create ECR repositories
    subprocess.run(['aws', 'ecr', 'create-repository', '--repository-name', f'{project_name.lower()}_front'])
    subprocess.run(['aws', 'ecr', 'create-repository', '--repository-name', f'{project_name.lower()}_back'])
    subprocess.run(['aws', 'ecr', 'create-repository', '--repository-name', f'{project_name.lower()}_dbmigrations'])





def read_yaml(file_path):
    with open(file_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data


@app.command()
def testee():
    arr = ["templates","ci-pipeline"]
    script_directory = os.path.dirname(os.path.abspath(__file__))
    #template_dir = os.path.join(script_directory, "templates","ci-pipeline")
    template_dir_source = os.path.join(script_directory, *arr)
    typer.echo(script_directory)
    typer.echo(template_dir_source)

    file_loader = FileSystemLoader(template_dir_source)
    env = Environment(loader=file_loader)
    #current_directory_source = os.path.dirname(os.path.abspath(__file__))
    template = env.get_template("set-artifact.yaml")
    rendered_template = template.render({
        'artifact_tar_name' : "artifact_tar",
        'artifact_pipeline_name': "artifact_name"
    })
    typer.echo(rendered_template)


@app.command()
def te():
    random_numbers = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    print(random_numbers)
    print(type(random_numbers))





@app.command()
def template():
    source_file = "setup_template.yaml"
    destination_file = "downloaded_template.yaml"


    # Get the current working directory of the user
    current_directory = os.getcwd()
    
    # Get the current directory of the script
    current_directory_source = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path of the source and destination files
    source_path = os.path.join(current_directory_source, source_file)
    destination_path = os.path.join(current_directory, destination_file)
    
    # Copy the source file to the destination path
    shutil.copyfile(source_path, destination_path)
    
    print(f"Template created to: {destination_path}")





@app.command()
def goodbye():
    print("Goodbye")


if __name__ == "__main__":
    app()