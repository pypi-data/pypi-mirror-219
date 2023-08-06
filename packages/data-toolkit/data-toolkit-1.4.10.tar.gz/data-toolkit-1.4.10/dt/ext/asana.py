import asana
import json
import os
# import request
import pandas as pd
import time
import sys
pd.options.display.width = 0

# disable pandas warning
pd.options.mode.chained_assignment = None

# pandas set max column width
pd.set_option('display.max_colwidth', 75)

def get_subtask_name(row):
    # [[{'gid': '947951982649945', 'resource_type': 'task'}, {'gid': '947951982649946', 'resource_type': 'task'}]]
    pass

def user_select_option(message, options):
    option_lst = list(options)
    print_(message)
    for i, val in enumerate(option_lst):
        print_(i, ': ' + val['name'])
    index = int(input("Enter choice (default 0): ") or 0)
    return option_lst[index]

def get_oauth_token(config):
    '''Get an OAuth token from Asana'''
    asana_client_id = config['asana_client_id']
    asana_client_secret = config['asana_client_secret']
    # create a client with the OAuth credentials:
    client = asana.Client.oauth(
        client_id=asana_client_id,
        client_secret=asana_client_secret,
        # this special redirect URI will prompt the user to copy/paste the code.
        # useful for command line scripts and other non-web apps
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )

    # get an authorization URL:
    (url, state) = client.session.authorization_url()
    try:
        # in a web app you'd redirect the user to this URL when they take action to
        # login with Asana or connect their account to Asana
        import webbrowser
        webbrowser.open(url)
    except Exception as e:
        print("Open the following URL in a browser to authorize:")
        print(url)

    print("Copy and paste the returned code from the browser and press enter:")

    code = sys.stdin.readline().strip()
    # exchange the code for a bearer token
    token = client.session.fetch_token(code=code)

    print("token=", json.dumps(token))
    print("authorized=", client.session.authorized)
    # print("me=", client.users.me())

    # normally you'd persist this token somewhere
    os.environ['ASANA_TOKEN'] = json.dumps(token) # (see below)
    
    # save token to ~/.dt_config.json
    with open(os.path.expanduser('~/.dt_config.json'),"r+") as f:
        config = json.load(f)
        config['asana_token'] = token
        # overwrite json file
        f.seek(0)
        f.write(json.dumps(config, indent=4))
        f.truncate()
        
    return token, client


def get_config():
    with open(os.path.expanduser('~/.dt_config.json')) as f:
        # before loading strip all lines starting with // after leading whitespace is stripped
        f = '\n'.join([line for line in f.read().splitlines() if not line.strip().startswith('//')])
        config = dict(json.loads(f))
    return config

def get_client(oauth=False):
    config = get_config()
    
    # check if asana api key exists
    if 'asana_api_key' in config.keys():
        api_key = config['asana_api_key']
        
        # create asana client
        client = asana.Client.access_token(api_key)
    else:
        
        try:
            client = asana.Client.access_token(config['asana_token']['access_token'])
        except KeyError:
            print("Insufficient token found. Getting new token...")
            token, client = get_oauth_token(config)
            
        
        if client.session.authorized == False:
            print("Insufficient token found. Getting new token")
            token, client = get_oauth_token(config)
        else:
            try:
                client = asana.Client.access_token(config['asana_token']['access_token'])
                print(f"Token found. Using token: {client.users.me()}")
            except asana.error.NoAuthorizationError:
                print("Insufficient token found. Getting new token...")
                token, client = get_oauth_token(config)

    return client


def asana_list_todos(project_name,filtering):
    if filtering is None: filtering = 'due'    
    
    df = asana_get_todos(project_name,filtering)
    df = df[['gid','name',"due_on", "completed", "notes", "subtasks"]] # projects
    
    # get all subtasks
    
    if filtering == 'done':
        df = df[df['completed'] == True]
        print(df)
        
    if filtering == 'due':
        df = df[df['completed'] == False]
        print(df)
    
    if filtering == 'all':
        print(df)
        
    if filtering == 'everyone':
        df = asana_get_todos(workspace_name,filtering)
        print(df)
        
def asana_list_workspaces(filtering):
    client = get_client(True)

    me = client.users.me()
    workspace_id = me['workspaces'][0]['gid']
    projects = list(client.projects.get_projects_for_workspace(workspace_id))
    
    workspaces_df = pd.DataFrame(projects)
    
    print(workspaces_df)
    
    
def asana_get_todos(project_name,filtering):
     # read api key from ~/.dt_config.json
    client = get_client(True)
    (url, state) = client.session.authorization_url()
        
    me = client.users.me()
    workspace_id = me['workspaces'][0]['gid']
    
    # {'param': 'value', 'param': 'value'}
    # https://developers.asana.com/docs/get-tasks-from-a-project
    # print requests that python is making

    opt_fields='name,due_on,completed,projects,notes,subtasks'
    if filtering!='everyone':
        tasks = list(client.tasks.find_all({"opt_fields":opt_fields}, 
                                           workspace=workspace_id, assignee='me'))
    else:
        project_id = list(client.projects.get_projects_for_workspace(workspace_id))[0]['gid']
        tasks = list(client.tasks.find_all({"opt_fields":opt_fields, "project_id": project_id}, 
                                           project=project_id))
    df = pd.DataFrame(tasks)
    return df
    
def add_todo(task_text, expected_duration, workspace_id, project_id):
    tm = time.localtime()
    config = get_config()
    
    if expected_duration is None:
        tar_date = f"{tm.tm_year}-{tm.tm_mon:02d}-{tm.tm_mday+1:02d}"
    else:
        day = tm.tm_mday+int(expected_duration)
        tar_date = f"{tm.tm_year}-{tm.tm_mon:02d}-{day:02d}"
    
    
    client = get_client(True)
    me = client.users.me()
    
    if workspace_id is None: workspace_id = me['workspaces'][0]['gid']
    
    # if 'asana_projects' in config:
    #     asana_projects = config['asana_projects']
    # else: asana_projects = None
    # asana_projects = asana_projects if asana_projects is not None else {}
    
    
    # if project_name not in asana_projects.keys():
    #     projects = list(client.projects.get_projects_for_workspace(workspace_id))
    #     if project_name == 0:
    #         # here project_name is id
    #         project_id = projects[int(project_name)]['gid']
    #     else:
    #         try:
    #             # filter s.t. project id that matches the project name
    #             project_id = list(filter(lambda x: x['name'] == project_name, projects))[0]['gid']
    #             import ipdb; ipdb.set_trace()
    #             # project_id = [ w['gid'] for w in projects if w['name'] == project_name][0]
    #             print(f"project_id of project name {project_name}: {project_id}")
    #         except IndexError:
    #             print(f"Project {project_name} not found. But this could also be a bug.")
    # else:
    #     project_id = asana_projects[project_name]
        
    # docs https://developers.asana.com/docs/create-a-task
        
    data =  {'name': task_text,
        "resource_subtype": "default_task",
        "assignee": me['gid'],
        "due_on": tar_date,
        "projects": project_id,
        # 'notes': 'Note: This is a test task created with the python-asana client.',
        # 'projects': [workspace_id]
    }
    
    # if project_name == '-1':
    #     del data['projects']
        
    print("posting", data)
    result = client.tasks.create_in_workspace(workspace_id, data)

    print(json.dumps(result, indent=4))
    
def done_todo(task_id):
    client = get_client(True)
    data =  {'completed': True}
    result = client.tasks.update_task(task_id, data)
    print(json.dumps(result, indent=4))

def fix_past_due(project_name):
    df = asana_get_todos(project_name,None)
    client = get_client(True)
    
    # select all that are past due
    df = df[df['completed'] == False]
    df = df[df['due_on'].notnull()]
    df['due_on'] = pd.to_datetime(df['due_on'])
    df = df[df['due_on'] < pd.Timestamp.today()]
    
    # asana update task to today
    all_tasks = []
    
    for i in df.index:
        task_id = df.loc[i,'gid']
        data =  {'due_on': pd.Timestamp.today().strftime("%Y-%m-%d")}
        result = client.tasks.update_task(task_id, data)
        # print(json.dumps(result, indent=4))
        all_tasks.append(result)
        
    df = pd.DataFrame(all_tasks)
    cols = ['gid', 'completed', 'due_on', 'name', 'notes']
    print(df[cols])