#----------------------------------------#
import sys
import jaydebeapi
import pandas as pd
from getpass import getpass
import re
import itertools
import warnings
from base64 import b64encode
from base64 import b64decode
import hashlib
import uuid
import requests
from github import Github
import uuid
import os
import base64
import urllib
import os.path
import yaml
import requests
import json
from sqlalchemy import create_engine
from datetime import datetime
from datetime import *
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
from Cryptodome.Hash import SHA256
from getpass import getpass
import logging
from logging.handlers import RotatingFileHandler
from ndp_deployment.fetch_metastore import object_deployment
#from ipynb.fs.full.fetch_metastore import *
#----------------------------------------#
# Instantiating a Logger to log info+ data with a 1.5 GB max file size.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
maxByteSize = 1.5*1024*1024
file_handler = RotatingFileHandler('Migration.log', maxBytes=maxByteSize,backupCount=10)
file_format = logging.Formatter('%(asctime)s: %(message)s', datefmt='%d-%m-%Y || %I:%M:%S %p')
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)
#----------------------------------------#
warnings.filterwarnings("ignore")
dt = datetime.now()
ts = datetime.timestamp(dt)
#----------------------------------------#
def set_api_base_url(url:str):
    global api_url
    api_url = url

def get_auth(token:str=None):
    if token == None:
        global bearer_token
        token = bearer_token
    return {
        "Authorization": token,
        "X-Request-ID": str(uuid.uuid1())
      }

def basic_auth(username:str,password:str):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

def login(username:str,password:str):
    global bearer_token
    global refresh_token
    auth=get_auth(basic_auth(username, password))
    response = requests.get(url=f'{api_url}/api/v1.0/auth/login',headers=auth)
    response = json.loads(response.text)
    bearer_token = f"Bearer {response['idToken']}"
    refresh_token = f"Bearer {response['refreshToken']}"

def refresh_tokens():
    global bearer_token
    global refresh_token
    auth = get_auth(refresh_token)
    response = requests.get(url=f'{api_url}/api/v1.0/auth/refresh',headers=auth)
    response = json.loads(response.text)
    bearer_token = f"Bearer {response['idToken']}"
    refresh_token = f"Bearer {response['refreshToken']}"

def get_pipeline_containers():
    auth = get_auth()
    response = requests.get(url=f'{api_url}/api/v1.0/pipeline/containers',headers=auth)
    response = json.loads(response.text)
    return response

def get_pipeline_relations(pipeline_container_id:int):
    auth = get_auth()
    response = requests.get(url=f'{api_url}/api/v1.0/pipeline/containers/{pipeline_container_id}/relations',headers=auth)
    response = json.loads(response.text)
    return response

def execute_pipeline(pipeline_container_id:int, pipeline_relation_id:int, pageLimit:int):
    auth = get_auth()
    body = json.dumps({
    "pageLimit": pageLimit
    })
    response = requests.post(url=f'{api_url}/api/v1.0/pipeline/containers/{pipeline_container_id}/relations/{pipeline_relation_id}/execute',headers=auth,data=body)
    print(response.text)
    response = json.loads(response.text)
    return response

def open_sql_query(sql_query:str, pageLimit:int):
    auth = get_auth()
    body = json.dumps({
    "select": sql_query,
    "pageLimit": pageLimit
    })
    response = requests.post(url=f'{api_url}/api/v1.0/query/sql/start',headers=auth,data=body)
    response = json.loads(response.text)
    return response

def register_table(datasource_name:str, table_name:str):
    auth = get_auth()
    body = json.dumps({
    "dataSourceName": datasource_name,
      "tableName": table_name
    })
    response = requests.post(url=f'{api_url}/api/v1.0/query/sql/register-table',headers=auth,data=body)
    response = json.loads(response.text)
    return response

def generic_query(sql_query:str):
    auth = get_auth()
    body = json.dumps({
    "sql": sql_query
    })
    response = requests.post(url=f'{api_url}/api/v1.0/query/sql/generic-query',headers=auth,data=body)
    response = json.loads(response.text)
    return response

def page_sql_query(queryToken:str, pageLimit:int, pageNumber:int):
    auth = get_auth()
    params = {
    "queryToken": queryToken,
    "pageLimit": pageLimit,
    "pageNumber": pageNumber
    }
    response = requests.get(url=f'{api_url}/api/v1.0/query/sql/page',headers=auth,params=params)
    response = json.loads(response.text)
    return response

def close_sql_query(query_token:str):
    auth = get_auth()
    requests.delete(url=f'{api_url}/api/v1.0/query/sql/close/{query_token}',headers=auth)

def clear_query_cache(username:str):
    auth = get_auth()
    requests.delete(url=f'{api_url}/api/v1.0/query/sql/clear/{username}',headers=auth)
#----------------------------------------#
#GET ORD ID FROM EMAIL
def get_org_id_from_email(lightning_username):
    orgId_query = 'select fk_organisation_id as id from metastore.lightning_user where lower(trim(email))='+"\'"+str(lightning_username)+"\'"
    x = open_sql_query(orgId_query,100)
    orgid_dict = x['records']
    if isinstance(orgid_dict[0],dict):
        orgId = orgid_dict[0]['id']
    return orgId
#----------------------------------------#
def run_fetch_metastore(api_url,lightning_username,lightning_pass,folder_path,option_for_backup,container_name,object_name):
    object_deployment(api_url,lightning_username,lightning_pass,folder_path,option_for_backup,container_name,object_name)
#----------------------------------------#
def migrate_other_env(source_org_id,target_api_url,folder_path,target_user_id,target_password,object_type,con_name,pipe_name,option_type):
    try:
        set_api_base_url(target_api_url)
        print('API BASE URL SET FOR TARGET')
        login(target_user_id,target_password)
        print("Target Host Connection successful")
        target_org_id=get_org_id_from_email(target_user_id)
        print('Target Org Id: '+str(target_org_id))
        print('Target Org Id Received from API')
        if (str(object_type).lower().strip()=='views'):
            print('Migrate Views Function call')
            filename_to_open=str(folder_path).strip()+'Migration_Data_Objects/'+str(con_name).lower().strip()+'-permanent_view-'+str(source_org_id)+'.sql'
        elif (str(object_type).lower().strip()=='pipelines'):
            print('Migration Pipelines Function call')
            if (option_type=='2' or option_type=='4'):
                print('Individual Pipeline')
                filename_to_open=str(folder_path).strip()+'Migration_Data_Objects/'+str(con_name).lower().strip()+'-'+str(pipe_name).lower().strip()+'-pipeline-'+str(source_org_id)+'.sql'
            elif (option_type=='1' or option_type=='3'):
                print('Pipeline Container')
                filename_to_open=str(folder_path).lower().strip()+'Migration_Data_Objects/'+str(con_name).lower().strip()+'-pipeline-'+str(source_org_id)+'.sql'
        elif (str(object_type).lower().strip()=='data_marts'):
            print('Migrate Data Marts Function call')
            if (option_type=='5'):
                print('Data Mart')
                filename_to_open=str(folder_path).strip()+'Migration_Data_Objects/'+str(con_name).lower().strip()+'-datamart-'+str(source_org_id)+'.sql'
            elif (option_type=='6'):
                print('Data Mart Table')
                filename_to_open=str(folder_path).strip()+'Migration_Data_Objects/'+str(con_name).lower().strip()+'-'+str(pipe_name).lower().strip()+'-datamart-'+str(source_org_id)+'.sql'
        logger.info(filename_to_open)
        file_read = open(filename_to_open,'r')
        print('File Found successfully : '+str(filename_to_open))
        data_read = file_read.read()
        mylist = data_read.split('INSERT INTO')
        mylist = [value for value in mylist if value]
        if(len(mylist)<2):
            mylist = data_read.split('\n')
        for line in mylist:
            line = 'INSERT INTO'+str(line)
            if line.lower().strip().startswith('insert into metastore.pipeline_container ') or line.lower().strip().startswith('insert into metastore.schema_store_view ') or line.lower().strip().startswith('insert into metastore.data_mart '):
                parts = line.strip().rsplit(',', 1)
                newlistparts=[]
                for fiorg in parts:
                    if fiorg==str(source_org_id)+')':
                        fiorg=','+str(target_org_id)+')'
                        newlistparts.append(fiorg)
                    else:
                        fiorg = fiorg
                        newlistparts.append(fiorg)
                    line = ''.join(newlistparts)
            else:
                line = line
            if (line.strip()!=''):
                if (line.strip())[-1]==';':
                    print(line)
                    generic_query(line.strip()[:-1])
                else:
                    print(line)
                    generic_query(line.strip())
        print('Migration Successful')
    except Exception as e:
        print(e)
        logger.info('Migration to Target Environment - Not Successful. Please Check Logs.')
        logger.info(e)
#----------------------------------------#
def migration_data_objects(lightning_username,lightning_pass,folder_path,api_url,option_for_backup,target_api_url,target_user_id,target_password,con_name,pipe_name,object_type):
    try:
        print('Fetch data object from source')
        set_api_base_url(api_url)
        login(lightning_username,lightning_pass)
        print('Login to source successful')
        source_org_id=get_org_id_from_email(lightning_username)
        run_fetch_metastore(str(api_url),str(lightning_username),str(lightning_pass),str(folder_path).strip(),str(option_for_backup).strip(),str(con_name).strip(),str(pipe_name).strip())
        print('Successfully fetched data object from source')
        print('Migrating to target environment')
        migrate_other_env(str(source_org_id),str(target_api_url),str(folder_path).strip(),str(target_user_id),str(target_password),str(object_type).strip(),str(con_name).strip(),str(pipe_name).strip(),str(option_for_backup).strip())
    except Exception as e:
        print(e)
#----------------------------------------#