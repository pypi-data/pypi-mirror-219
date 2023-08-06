from datetime import datetime
import pandas as pd
from faker import Faker

# generate notional data in this schema
target_cols = {'ID': "number",
 'Customer': "string",
 'Sector': "categorical",
 'Market_capitalisation': "number",
 'Sales_employee_handing_case': "string",
 'Additional_priority': "categorical",
 'Region_of_service': "categorical",
 'Type_of_company': "categorical",
 'current_status': "categorical",
 'team_handling_current_status': "categorical",
 'group_ID_handling_current_status': "categorical",
 'last_status_update_at': "date",
 'path_length': "number",
 'full_path_string_filter_one': "string",
 'full_path_string_filter_two': "string",
 'days_since_last_update': "number",
 'expected_path': "string",
 'stages_missed': "number",
 'core_stages_missed': "number",
 'main_stage_for_notification': "categorical",
 'team_for_final_notification': "categorical",
 'group_ID_for_final_notification': "string",
}
'''
team_handling_job	palantir_group_ID_handling_job
Admin	ba0e063f-47d0-49bf-9e1e-b38be1c62c69
KYC	a38e0da6-e551-4cd4-b610-f119aa4ac7b0
DD	bceef7dc-44be-4826-b76a-a9a8d2fbba21
Enablement	e49b2181-3596-4d18-8283-ec6ff6da8615


'''

NOTE_TYPES = {
    "Account Activation by Bank": [
        "Account activated successfully.",
        "Customer can start using the account now.",
        "Account activation process completed."
    ],
    "Due Dilligence": [
        "All due diligence checks passed successfully.",
        "No issues found during the due diligence process.",
        "Customer cleared the due diligence process."
    ],
    "Account Rejection by Bank": [
        "Account opening request rejected by the bank.",
        "Account does not meet the bank's criteria for opening.",
        "Bank unable to open the account at this time."
    ],
    "Account Opening Request": [
        "Account opening request received.",
        "Request is being processed.",
        "Account will be opened soon."
    ],
    "KYC Requirements": [
        "KYC requirements completed successfully.",
        "Customer's KYC documents verified successfully.",
        "KYC process completed."
    ],
    "Enhanced Due Dilligence": [
        "Enhanced due diligence required for the account.",
        "Additional information needed for due diligence purposes.",
        "Customer's account flagged for enhanced due diligence."
    ],
    "Client Documentation & Paperwork": [
        "Customer's documentation and paperwork received.",
        "Customer's paperwork approved successfully.",
        "Customer's documentation is complete."
    ],
    "Account Frozen": [
        "Account frozen due to non-compliance with KYC requirements.",
        "Account temporarily suspended for further due diligence.",
        "Account frozen due to suspicious activities."
    ],
    "Account Closed": [
        "Account closed successfully.",
        "Account closed due to inactivity.",
        "Account closed due to non-compliance with bank's policies."
    ],
    "Additional Information Required": [
        "Additional information required to complete the account opening request.",
        "Additional documentation needed for the KYC process.",
        "Further details needed on customer's source of income."
    ],
    "Account Verification": [
        "Account verification completed successfully.",
        "Customer's account verified for transaction purposes.",
        "Verification process completed."
    ],
    "Client Interview Required": [
        "Client interview required to complete the due diligence process.",
        "Interview scheduled with the customer.",
        "Interview completed successfully."
    ],
    "Documentation & Paperwork": [
        "Customer's documentation pending for further processing.",
        "Documentation received but awaiting verification.",
        "Documents under review."
    ],
    "Document Verification Pending": [
        "Customer's documents pending verification.",
        "Documents being reviewed by the bank.",
        "Verification process pending."
    ],
    "KYC Pending": [
        "KYC process pending completion.",
        "Further KYC checks required.",
        "KYC process delayed."
    ],
    "Enhanced Due Diligence Pending": [
        "Enhanced due diligence pending for the account.",
        "Additional information needed for due diligence purposes.",
        "Customer's account flagged for enhanced due diligence."
    ],
    "Rejected During Enhanced Due Diligence": [
        "Account opening request rejected during enhanced due diligence.",
        "Customer failed to meet the requirements for enhanced due diligence.",
        "Enhanced due diligence process completed with rejection."
    ],
    "Client Information Update Required": [
        "Customer's information needs to be updated.",
        "Information provided by the customer is outdated.",
        "Customer's account on hold until information is updated."
    ],
    "Risk Assessment Required": [
        "Risk assessment required for the account.",
        "Customer's risk profile under review.",
        "Account opening request pending risk assessment."
    ]
}

def generate_log_data(n=100):
    companies_df = generate_company_data(n=n)
    companies = list(companies_df.Customer.values)
    
    fake = Faker()
    
    all_logs = []
    
    current_status = ['Account Activation by Bank',"Due Dilligence",'Account Rejection by Bank', 'Account Opening Request',
                      "KYC Requirements","Enhanced Due Dilligence","Client Documentation & Paperwork"]
    
    teams = ["Enablement","DD","Admin",'KYC']
    # map teams to stages
    team_responsible = {
        "Account Activation by Bank": "Enablement",
        "Due Dilligence": "DD",
        "Account Rejection by Bank": "Admin",
        "Account Opening Request": "Admin",
        "KYC Requirements": "KYC",
        "Enhanced Due Dilligence": "DD",
        "Documentation & Paperwork": "KYC"
    }

    
    expected_string = ["Account Opening Request","Documentation & Paperwork","KYC Requirements",
                       "Due Dilligence","Account Rejection by Bank","Account Activation by Bank"]
    
    # define a transition graph where .6-.8% of the time we go to the next stage, and .1-.2% we get rejected
    # and .1-.2% we go to a random stage
    transition_graph = {
        'Account Opening Request': {
            'Documentation & Paperwork': .6,
            'KYC Requirements': .1,
            'Due Dilligence': .1,
            'Account Rejection by Bank': .1,
            'Account Activation by Bank': .1,
        },
        'Documentation & Paperwork': {
            'KYC Requirements': .8,
            'Due Dilligence': .1,
            'Account Rejection by Bank': .1,
        },
        'KYC Requirements': {
            'Due Dilligence': .8,
            'Account Rejection by Bank': .1,
            'Account Activation by Bank': .1,
        },
        'Due Dilligence': {
            'Account Rejection by Bank': .8,
            'Account Activation by Bank': .2,
        },
        'Account Rejection by Bank': {
            'Account Rejection by Bank': 1,
        },
        'Account Activation by Bank': {
            'Account Activation by Bank': 1,
        },
    }
    
    
    for comp,idx in enumerate(companies):
        num_steps = fake.pyint(min_value=1, max_value=25)
        start_time = fake.date_time_between(start_date="-1y", end_date="now")
         
        path = []
        comments = []
    
        current_stage = 'Account Opening Request'
        transition_time = start_time
        
        
        # use the transition graph to generate a path to take the number of (unique) steps as define above
        for i in range(num_steps):
            transition_probs = transition_graph[current_stage]
            
            # make min difference 6 hours 
            next_time = timedelta(hours=6) + transition_time
            
            
            transition_time = fake.date_time_between(start_date=next_time, end_date="now")
            rand = fake.pyfloat(min_value=0, max_value=1)
            # loop through the transitions and determine if the random number falls within the range for that transition
            for stage, prob in transition_probs.items():
                data = {
                            "id": idx,
                            "company_id": comp,
                            "stage": current_stage,
                            "time": transition_time,
                            "team_handling_job": team_responsible[current_stage],
                            "comments": fake.random_element(NOTE_TYPES[current_stage]),
                }
                
                if rand <= prob:
                    current_stage = stage
                
                path.append(data)
            
            # also break if the stage is 'Account Rejection by Bank' or 'Account Activation by Bank'
            if current_stage in ['Account Rejection by Bank', 'Account Activation by Bank']:
                break
        
        df = pd.DataFrame(path)
        all_logs.append(df)
        path = []


    print(pd.concat(all_logs,axis=0))

def generate_company_data(n=100):
    # generate fake data
    fake = Faker()
    
    sectors = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Consumer Goods', 'Real Estate', 'Transportation', 'Utilities',
               'Retail', 'Telecommunications', 'Media', 'Entertainment', 'Manufacturing', 'Construction', 'Education', 'Hospitality', 'Agriculture']
    
    data_generated = []

    for n in range(int(n)):
        last_status_update_at = fake.date_time_between(start_date="-1y", end_date="now"),
        days_since_last_update = (datetime.now() - last_status_update_at[0]).days
        path_length = fake.pyint(min_value=1, max_value=7)
        # full_path_string_filter_one = "-".join(fake.random_elements(elements=current_status, length=path_length, unique=True)),
        country = fake.random_element(elements=['US', 'EU','UK', 'ME', 'China'])
        country_mapping = {
            "US": "15864041",
            "UK": "15601741",
            "EU": "",
            "China": "3084336",
            "ME": "15536130",
        }
        
        data = {
            'ID': fake.pyint(),
            "Customer": fake.company(),
            # sector as categorical from list
            "Sector": fake.random_element(elements=sectors),
            "Revenue": fake.pyfloat(min_value=1_000_000, max_value=10_000_000_000, right_digits=2),
            "Sales_employee_handing_case": fake.name(),
            "Additional_priority": fake.random_element(elements=['Yes', 'No']),
            "Region_of_service": country,
            "Region_of_service_mapbox_id": country_mapping[country],
            "Type_of_company": fake.random_element(elements=['Public', 'Private', 'NGO']),
            # "current_status": fake.random_element(elements=current_status),
            # "team_handling_current_status": fake.random_element(elements=teams),
            # "group_ID_for_final_notification": fake.uuid4(),
            # "group_ID_handling_current_status": fake.uuid4(),
            # "last_status_update_at": last_status_update_at,
            # "path_length": path_length,
            # # full path string is a combination of stages in current_status string joined together by '-'
            # # why was that chosen?
            # "full_path_string_filter_one": full_path_string_filter_one, 
            # # what is this one meant to mean?
            # "full_path_string_filter_two": "-".join(fake.random_elements(elements=current_status, length=path_length, unique=True)),
            # # this is a number of days since last update as calculated in difference now - "last_status_update_at"
            # "days_since_last_update": fake.pyint(min_value=1, max_value=365),
            # "last_status_update_at": last_status_update_at,
            # # make expected path of equal length as current full_path_string_filter_one
            # "expected_path": "-".join(fake.random_elements(elements=expected_string, length=min(path_length,5), unique=True)),
            # # see stages missed by difference between set(expected_path) and set(full_path_string_filter_one)
            # "stages_missed": len(set(expected_string) - set(full_path_string_filter_one)),
            # "core_stages_missed": len(set(expected_string[:5]) - set(full_path_string_filter_one[:5]))==0,
            # "main_stage_for_notification": fake.random_element(elements=['Account Opening Request', 'Documentation & Paperwork', 'KYC Requirements', 'Due Dilligence', 'Account Rejection by Bank', 'Account Activation by Bank']),
            # "team_for_final_notification": fake.random_element(elements=['Enablement', 'DD', 'Admin', 'KYC']),
            # "group_ID_for_final_notification": fake.uuid4()
        }
        
        data_generated.append(data)
        
        
        
    df = pd.DataFrame(data_generated)
    
    return df 
    
    
def generate_group_data(n):
    fake = Faker()
    
    target_cols = {"Status": "string",
     "Team_handling_job": "string",
     "Team_group_ID": "string",
     "primary_key": "string",}
    
    current_status = ['Account Activation by Bank',"Due Dilligence",'Account Rejection by Bank', 'Account Opening Request',
                      "KYC Requirements","Enhanced Due Dilligence","Client Documentation & Paperwork"]
    
    collected_data = []
    
    for i in range(n):
        status = fake.random_element(elements=current_status)
        team_id = fake.uuid4()
        
        data = {
            "Status": status,
            "Team_handling_job": fake.random_element(elements=['Enablement', 'DD', 'Admin', 'KYC']),
            "Team_group_ID": team_id,
            # is concat of status and team_group_ID "-"
            "primary_key":" - ".join([status, team_id])
        }
        
        collected_data.append(data) 
   
   
    df = pd.DataFrame(collected_data)
    return df
   
    
if __name__ == "__main__":
    generate_log_data(n=100)