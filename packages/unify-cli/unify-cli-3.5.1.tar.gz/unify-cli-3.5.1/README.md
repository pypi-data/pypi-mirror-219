# Element Unify CLI

The Unify CLI is a command line interface to Element Unify. It aims to supports all major APIs in Element Unify,
and all common OSes (Mac, Windows, Linux). 

It uses the command line tool library Click. https://click.palletsprojects.com/en/7.x/

## Installation

The Unify CLI needs Python as a prerequisite. Therefore the installation instructions are divided in two main sections:

1. [Python Installation](#python-installation)
2. [CLI Installation](#unify-cli-installation)

### Python Installation

The best way to get a Python environment up is using a Python virtual environment:

1. ```brew install pyenv```
2. ```brew install pyenv-virtualenv```
3. Initialize virtual environment, this can be accomplish in two ways:
    
    **Option 1: Edit your Terminal profile (persistent)**
    
    3.1.1 If you're using bash, append the following to the end of `~/.bashrc`
    ```
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    ```
    
    3.1.2 If you're using ZSH, append the following to the end of `~/.zshrc`
    ```
    eval "$(pyenv init -)"
    ```
    
    **Option 2: Initialize virtualenv for your current session (temporary)**
    
    3.2 Or, run this command to initialize the virtualenv 
    ```pyenv init```

4. ```source ~/.bashrc```
5. ```pyenv install 3.8.0```
6. ```pyenv virtualenv 3.8.0 unify-cli```

### Unify CLI Installation

1. activate the virtualenv

    ``` pyenv activate unify-cli ```

2. ``` pip install unify-cli ```

3. Run a test command to ensure things are working!

    ``` unify cluster add --help ```

## Configuration

To get started with Unify CLI, first add your instance of Unify. Note that a cluster represents a deployment of Element Unify.

    unify cluster add

1. Remote is the URL of Unify. For example, https://app001-aws.elementanalytics.com/.
2. Username is your Unify username (email).
3. Password is your Unify password.
4. Name is a name for this instance. For subsequent examples, ```unify``` is used

You will be prompted to save your credentials to keyring.

Next log in to this instance

    unify cluster login --remote=unify

You may be prompted to access your credentials from keyring.

## Basic Commands

An Unify CLI command has the following structure

    unify <command group> <command> [options and parameters]

For example, to list all orgs in Unify:

    unify org list --remote=unify

## Main Command Groups

Each of these has a set of commands that goes with it.

### Cluster
- Get
- List
- Delete
- Set defaults (org, cluster, user)

### Org
- Get
- Upcert
- List
- Delete
- Grant

### User
- Get
- Upcert
- List
- Delete

### Template
- Get
- Upcert
- List
- Delete

### Dataset
- Get
- Upcert
- List
- Delete

### Datastream
- Simulate

### Pipeline (include map-attributes)
- Get
- Upcert
- List
- Delete
- Run
- Evergreen (turn on and off, Maybe part of the upcert?)

### Access
- Databases
- Execute

## Configure CLI

Follow the steps below to set up the Unify CLI:

- Add a new cluster 
    - Help
        -   ```unify cluster add --help```           
    - Client will prompt for parameters 
        -   ```unify cluster add```
    - All parameters inline 
        -   ``` unify cluster add --remote "https://app001-aws.elementanalytics.com/" --username "yourusername" --password "yourpassword" --name "unify" ```

- Set cluster as default
    - Help
        -   ```unify cluster default --help```
    -   Client will prompt for parameters
        -   ``` unify cluster default ```
    -   All commands inline
        -   ``` unify cluster default --remote unify ```
- Log in to cluster
    - Help
        -   ```unify cluster login --help```
    - Client will prompt for parameters

## Workflow activities
Workflows commands perform bulk operations to help facilitate common operations such as copying pipelines or templates from one organization to another.

- Element Unify Instance Management              
    - Delete existing cluster
        - Help
            -   ```unify cluster disconnect --help```        
        -   All parameters inline
            -   ```unify cluster disconnect --remote unify```
        -   Client will prompt for parameters
            -   ``` unify cluster disconnect ```
            
    - List all Unify instances
        - Help
            -   ```unify cluster list --help```
        -   ```unify cluster list ```            

- Organization Management
    - Create Organization
        -   All Parameters inline to default cluster
            -  ``` unify org add --name "New Organization Name" ```
        
        -   All Parameters inline to different cluster
            -  ``` unify org add --name "New Organization Name" --remote "cluster_name"  ```
        
        -   Client will prompt for parameters ot default cluster
            -   ``` unify org add ```
        
        -   Client will prompt to different cluster
            -  ``` unify org add --remote "cluster_name"  ```
    
    - List all org available for current in user
        
        -   List from default cluster
            -  ``` unify org list ```                    

        -   List from different cluster
            -  ``` unify org list --remote "cluster name" ```
    
    -   Delete org from cluster
        
        - Delete org from default cluster
            
            -  ``` unify org delete --orgid ###### ```                           

        - Delete org from different cluster
            
            -  ``` unify org delete --orgid ###### --remote cluster_name ```   
                                                      
  - Create Users
    
    - Add Admin user to an existing org in default cluster
        -   ``` unify user add --orgid ###### --email "user_email@email.com" --name "User Name" --role Admin --remote unify  ```

    - Add Contributor user to an existing org in default cluster
        -   ``` unify user add --orgid ###### --email "user_email@email.com" --name "User Name" --role Contributor --remote unify  ```
    
    - Add user to an existing org to different cluster
        -   ``` unify user add --orgid ###### --email "user_email@email.com" --name "User Name" --role Admin --remote cluster_name  ```
    
    - Add Contributor user to an existing org in default cluster
        -   ``` unify user add --orgid ###### --email "user_email@email.com" --name "User Name" --role Contributor --remote cluster_name  ```

  - Data Workflow
    -   This group gives the user the ability to export and import various types of data from templates, sources and pipelines
    
    - Templates
        - Export: This gives the functionality to export all templates from a given ORG, the output will be in standard output.
        
            - ``` unify wf export-template --org ##### --remote cluster_name ```
            
            - Export output into file  ``` unify wf export-template --org ##### --remote cluster_name ```
        
        - Import: This will import templates contents into a given org of a cluster
            - ``` unify wf import-template --org ##### --remote cluster_name templates.csv```                 
        
        - Combine import and export into a single line
            - ``` unify wf export-template --org ##### --remote origin_cluster_name | unify wf import-template --org ##### --remote destination_cluster_name ```
    
    - Pipelines
        - Export: this gives the functionality of exporting all necessary data (except sources) to export a pipelien structure. This command will even include map templates and map attributes
        
            - ``` unify wf export-pipeline --remote origin_cluster_name --org ##### --pipeline ####  ```  
        
        - Import: This will import a pipeline into a given organization of the cluster. This will need a big file as input that can be generated with ```unify wf export-pipeline```
        
            - ```unify wf import-pipeline --remote destination_cluster_name --org #####   ```
            
        - Import and Export combined using command line pipe
            - ``` unify wf export-pipeline --remote origin_cluster_name --org org_origin_id --pipeline pipeline_id_to_be_copied |  unify wf import-pipeline --remote destination_cluster_name --org destination_org_id ```

    - Graphs
        - List: this gives you the list of all graphs on a given org
        
            - ``` unify graph list --remote origin_cluster_name --org ##### ```  
        
        - Query: This will give you the ability to create cypher queries to a given graph
        
            - ```unify graph query --org ### --remote origin_cluster_name --graph "GRAPH ID" "Cypher Query" -j```
            - ```unify graph query --org #### --remote platad --graph ##### "MATCH (n)-[r]->(g) RETURN *" -j```
            
           

### Example: Migrate an organization ###

The simplest way to fully migrate an org is to chain together several commands in a single bash script, the following .sh script can do the job.

```
#!/bin/sh

ORIGIN_ORG="5024"
ORIGIN_ENV="unify"
DESTINATION_ORG="10824"
DESTINATION_ENV="unify"

# Login to the origin unify cluster
unify cluster login --remote $ORIGIN_ENV

# Login to the destination unify cluster
unify cluster login --remote $DESTINATION_ENV

# Export the templates from the origin env and imported to the destination env
unify wf export-template --remote $ORIGIN_ENV --org $ORIGIN_ORG | unify wf import-template --remote $DESTINATION_ENV --org $DESTINATION_ORG

echo "Templates were migrated"

# Retrieves the datasets lists into a json array
DATASETS=$(unify dataset list --org $ORIGIN_ORG --remote $ORIGIN_ENV)

# Iterates over the current datasets
jq -c '.[]' <<< $DATASETS | while read js; do
  code_val=$(jq -r '.id' <<< "$js")

  # Export each dataset from the origin env and imported to the destination env
  unify wf export-dataset --remote $ORIGIN_ENV --org $ORIGIN_ORG --id $code_val | unify wf import-dataset --remote $DESTINATION_ENV --org $DESTINATION_ORG
done


# Retrieves the pipeline lists into a json array
PIPELINES=$(unify pipeline list --org $ORIGIN_ORG --remote $ORIGIN_ENV)

# Iterates over the current Pipelines
jq -c '.[]' <<< $PIPELINES | while read jss; do
  code_val=$(jq -r '.id' <<< "$jss")
  # Export each pipeline from the origin env and imported to the destination env
  unify wf export-pipeline --remote $ORIGIN_ENV --org $ORIGIN_ORG --pipeline $code_val --skip datasets --skip templates |  unify wf import-pipeline --remote $DESTINATION_ENV --org $DESTINATION_ORG --skip datasets --skip templates
done

```

# Developers Section

Info for people developing against the CLI

## Running the tests

1. Initialize your virtual environment, either using virtualenv, pyenv & pyvenv-virtualenv, or however you have it set up.
2. Install the test requirements: ``` pip install -r tests/requirements.txt ```
3. Set the environment variables with cluster credentials (note, this should be a testing cluster for tests as it may not clean up after itself). These env var names may be edited in `tests/local.ini` if you like (don't check in the changes of course). Values for these can be found in 1password in the Engineering vault.
    * LOCAL_API_URL
    * LOCAL_ADMIN_NAME
    * LOCAL_ADMIN_PASSWORD
4. Run the tests: ``` nosetests --tc-file tests/local.ini --nocapture -v tests/ ```

