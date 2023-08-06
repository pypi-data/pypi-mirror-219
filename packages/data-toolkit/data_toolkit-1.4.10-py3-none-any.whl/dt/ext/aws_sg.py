#/bin/python
'''
TODO: fix

botocore.exceptions.ClientError: An error occurred (InvalidPermission.Duplicate) 
when calling the AuthorizeSecurityGroupIngress operation: the specified rule "peer: 86.16.93.195/32, TCP, from port: 8501, 
to port: 8501, ALLOW" already exists

  File "/Users/jlangr/code/data-toolkit/dt/controllers/base.py", line 101, in sg
    update_sg_to_ip(sg_name=sg_name, profile=profile,
  File "/Users/jlangr/code/data-toolkit/dt/ext/aws_sg.py", line 111, in update_sg_to_ip
    data = ec2.authorize_security_group_ingress(
'''

import boto3
import pandas as pd
import os 

try:
    term_wdith = os.get_terminal_size().columns
except OSError:
    term_wdith = 70

# pd.set_option('display.max_colwidth',term_wdith - 40)
pd.set_option('display.max_colwidth',30)

def get_public_ip():
    from urllib.request import urlopen
    import re
    data = str(urlopen('http://checkip.dyndns.com/').read())
    # data = '<html><head><title>Current IP Check</title></head><body>Current IP Address: 65.96.168.198</body></html>\r\n'
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

def get_sg(profile: str, sid: int, sg_name = None, region='eu-west-1'):
    
    # decide if use security group name or security group id
    if sid:
        # get relevant row from security group df
        sg_name = list_security_groups(profile=profile, region=region).iloc[sid]['GroupName']
    else:
        sg_name = 'default'
    
    ec2 = boto3.session.Session(profile_name=profile, region_name=region).client('ec2')
    resp = ec2.describe_security_groups()
    target_sg_dict = list(filter(lambda x: x['GroupName']==sg_name, resp['SecurityGroups']))
    return target_sg_dict

def check_if_exists(ip_ranges: list, descriptions: list):
    # for each description check if there is a description in the existing permissions with the same description
    try:
        # TODO: why is 'ip_ranges' not defined?
        return any([ ip_ranges['Description']==d for d in descriptions ])
        # *** NameError: name 'ip_ranges' is not defined
        # return 'Aux' in ip_ranges['IpRanges'][0]['Description']
    except IndexError as e:
        assert ip_ranges['IpRanges']==[]
        return False
    except KeyError as e:
        return False

def update_sg_to_ip(sg_name='jakub', # ip='2.222.105.71/32',
                    ports=[22, 8888, 8501, 8889, 5432], profile='default',
                    messages='', region='eu-west-1'):
    import boto3

    ip = f"{get_public_ip()}/32"

    try:
        group_name = list_security_groups(profile=profile, region=region)
        sid = group_name.index[group_name.GroupName==sg_name].tolist()[0]
    except IndexError:
        raise ValueError(f"Security group called {sg_name} does not exist")
    ec2 = boto3.session.Session(profile_name=profile, region_name=region).client('ec2')

    target_sg_dict = get_sg(sg_name=sg_name, sid=sid, profile=profile, region=region)[0]
    ec2_res = boto3.session.Session(profile_name=profile, region_name=region).resource('ec2')
    sg_res = ec2_res.SecurityGroup(target_sg_dict['GroupId'])

    # determine what the new sg rules should be either default or custom
    if messages=='':
        print('Warning messages are empty. Skipping')
        descriptions = {
                22: 'Jakub Aux SSH',
                80: 'Web',
                8888: 'Jakub Aux Jupyter',
                8501: 'Jakub Aux Streamlit',
                8889: 'Jakub Aux Jupyter2',
                5432: 'Jakub Aux Postgres'
            }
    else:
        items = [ i for i in messages.split(',')]
        descriptions = { int(k.split(':')[0]):k.split(':')[1] for k in items } 
        ports = [ int(i.split(':')[0]) for i in items ] 

    # TODO: allow for more than just 1 port setting
    target_ports = [ [ s['ToPort']==p for p in ports ]
                    for s in sg_res.ip_permissions if 'ToPort' in s.keys()]
    # flatten target_ports list take all True values and merge into one list
    # [[True, False, False],[False, False True]] -> [True, False, True]
    target_ports = [ any(i) for i in zip(*target_ports) ]
     
    # loop using description to only remove already existing and replace them later
    # effectiely overwriting them
    permissions_to_revoke = []
    for i in range(len(sg_res.ip_permissions)):
        if target_ports[i]:
            ipr = sg_res.ip_permissions[i]
            ip_ranges_to_revoke = [ s for s in ipr['IpRanges'] if check_if_exists(s, list(descriptions.values())) ]
            permissions_to_revoke.append({ 
                **ipr,
                'IpRanges': ip_ranges_to_revoke })

    # Removes all relevant permissions from this group (originally as `jakub`)
    if sg_res.ip_permissions!=[] and permissions_to_revoke==[]:
        print('No permissions to revoke. Skipping.')
    else:
        sg_res.revoke_ingress(IpPermissions=permissions_to_revoke)
        print(f'Removed permissions {permissions_to_revoke}')

    # assign new rules   
    ip_perms = [ {
        'IpProtocol': 'tcp',
        'FromPort': ports[i],
        'ToPort': ports[i],
        'IpRanges': [{'CidrIp': ip, 'Description': descriptions[ports[i]] }]}
            for i in range(len(ports)) ]
    
    data = ec2.authorize_security_group_ingress(
            GroupId=target_sg_dict['GroupId'],
            IpPermissions=ip_perms )
    print(f'Ingress Successfully Set {ip_perms} to {sg_name}')

# lists all security groups
def list_security_groups(region: str = 'eu-west-1', profile: str = 'default'):
    # define a boto3 client with a region eu-est
    boto3.setup_default_session(profile_name=profile)
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_security_groups()
    security_group_df = pd.DataFrame(response['SecurityGroups'])

    # extract keys from Tags column
    # [ x for x in df.Tags if not np.all(pd.isna(x)) ] 

    # generate a mask for terms that have FILTER_TERMS in them
    FILTER_TERMS = ['LIW']
    mask = security_group_df.Description.apply(lambda x: any(term in x for term in FILTER_TERMS))
    security_group_df = security_group_df[~mask]

    # display all columns except FILTER_COLS
    FILTER_COLS = ['VpcId', 'Tags','OwnerId']
    security_group_df = security_group_df[security_group_df.columns.difference(FILTER_COLS)]

    # create an Ingress dataframe by filtering on IpPermissions not empty
    df_ingress = security_group_df[security_group_df.IpPermissions.notnull()]
    ip_permissions_df = pd.DataFrame.from_dict([x[0] for x in df_ingress.IpPermissions.values])
    
    df_ingress = df_ingress.reset_index().drop('index',axis=1)
    
    viewable_df = pd.concat([ip_permissions_df,df_ingress],axis=1).drop(['Ipv6Ranges','IpPermissions'],axis=1)
    # viewable_df.Description = viewable_df.Description.str[:30]

    # reorders columns 
    order = "GroupName FromPort IpProtocol ToPort UserIdGroupPairs PrefixListIds Description IpRanges IpPermissionsEgress GroupId".split()
    viewable_df = viewable_df[order]

    return viewable_df

