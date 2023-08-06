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
# Instantiating a Logger to log info+ data with a 1.5 GB max file size.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
maxByteSize = 1.5*1024*1024
file_handler = RotatingFileHandler('execute_versioncontrol.log', maxBytes=maxByteSize,backupCount=10)
file_format = logging.Formatter('%(asctime)s: %(message)s', datefmt='%d-%m-%Y || %I:%M:%S %p')
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)
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

def get_pipeline_containers_api():
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
#CALL FETCH METASTORE PIP LIBRARY
def run_fetch_metastore(api_url,lightning_username,lightning_pass,folder_path,option_for_backup,container_name,object_name):
    object_deployment(api_url,lightning_username,lightning_pass,folder_path,option_for_backup,container_name,object_name)
#----------------------------------------# 
#EXECUTE QUERY PASSED TO THIS FUNCTION AND RETURN RESULTS VIA API
def exec_query_get_res(sql_query_res):
    page_limit = 100
    x = open_sql_query(sql_query_res,page_limit)
    res = x['records']
    query_token = x['queryToken']
    max_pages = x['totalPages']
    for i in range(2,max_pages+1):
        page_data=page_sql_query(query_token,page_limit,i)
        res += page_data['records']
    return res
#----------------------------------------# 
#GET ORD ID FROM EMAIL
def get_org_id_from_email(lightning_username):
    orgId_query = 'select id from metastore.organisation where lower(trim(email))='+"\'"+str(lightning_username)+"\'"
    x = open_sql_query(orgId_query,100)
    orgid_dict = x['records']
    if isinstance(orgid_dict[0],dict):
        orgId = orgid_dict[0]['id']
    return orgId
#----------------------------------------#
#BACKUP OF PIPELINES AT INDIVIDUAL LEVEL
def get_individual_pipelines(folder_path,lightning_username,lightning_pass,api_url):
    logger.info('Backup of Pipelines at an individual level')
    orgId = get_org_id_from_email(lightning_username)
    sql_ind_pipeline="select r.name as rname,c.name as cname from metastore.pipeline_relation r inner join metastore.pipeline_container c on c.id=r.fk_pipeline_container_id where c.fk_organisation_id="+str(orgId).strip()
    res = exec_query_get_res(sql_ind_pipeline)
    if isinstance(res[0],dict):
        for dic in res:
            con_name=list(dic.values())[0]
            pipe_name=list(dic.values())[1]
            if (len(str(pipe_name))>1):
                print(str(pipe_name)+'.'+str(con_name))
                run_fetch_metastore(str(api_url),str(lightning_username),str(lightning_pass),str(folder_path).strip(),"2",str(pipe_name),str(con_name))

#BACKUP OF PIPELINES AT CONTAINER LEVEL
def get_pipeline_containers(folder_path,lightning_username,lightning_pass,api_url):
    logger.info('Backup of Pipelines at container level')
    orgId = get_org_id_from_email(lightning_username)
    sql_query_pipeline="select name from metastore.pipeline_container where fk_organisation_id="+str(orgId).strip()
    res = exec_query_get_res(sql_query_pipeline)
    if isinstance(res[0],dict):
        for i in res:
            name = str(i['name'])
            print(name)
            run_fetch_metastore(str(api_url),str(lightning_username),str(lightning_pass),str(folder_path).strip(),"1",str(name),"")

#BACKUP OF PERMANENT VIEWS
def get_data_views(folder_path,lightning_username,lightning_pass,api_url):
    logger.info('Backup of Permanent Views')
    orgId = get_org_id_from_email(lightning_username)
    sql_query_view="select name from metastore.schema_store_view where fk_organisation_id="+str(orgId).strip()
    res = exec_query_get_res(sql_query_view)
    if isinstance(res[0],dict):
        for i in res:
            name = str(i['name'])
            print(name)
            run_fetch_metastore(str(api_url),str(lightning_username),str(lightning_pass),str(folder_path).strip(),"7",str(name),"")

#BACKUP OF DATA MARTS AT CONTAINER LEVEL
def get_data_marts(folder_path,lightning_username,lightning_pass,api_url):
    logger.info('Backup of Data Marts')
    orgId = get_org_id_from_email(lightning_username)
    sql_query_mart="select name from metastore.data_mart where fk_organisation_id="+str(orgId).strip()
    res = exec_query_get_res(sql_query_mart)
    if isinstance(res[0],dict):
        for i in res:
            name = str(i['name'])
            print(name)
            run_fetch_metastore(str(api_url),str(lightning_username),str(lightning_pass),str(folder_path).strip(),"5",str(name),"")
#----------------------------------------#
#GENERATE FILE NAME FOR RESTORE FUCNTIONALITY
def generate_file_name(arg1,arg2,object_type,type_of_restore,folder_path,api_url):
    logger.info('Inside Generate File Function...')
    if (type_of_restore=='full'):
        filename_restore=str(folder_path).strip()+'versioncontrol/backup/'+str(arg1)+''+str(arg2)+''+str(object_type)+'.sql'
        if(os.path.exists(filename_restore)):
            logger.info('File exists for restore, now executing the commands for restore\n')
            execute_sql_file(filename_restore)
        else:
            logger.info('Restore: File does not exist')
    elif (type_of_restore=='individual'):
        filename_restore=str(folder_path).strip()+'versioncontrol/restore/'+str(arg1)+''+str(arg2)+''+str(object_type)+'.sql'
        logger.info(filename_restore)
        if(os.path.exists(filename_restore)):
            logger.info('File exists for restore, now executing the commands for restore\n')
            execute_sql_file(filename_restore)
        else:
            logger.info('Restore: File does not exist')
#----------------------------------------#
#RESTORE VIEWS FUNCTION
def restore_views(arg1,folder_path,lightning_username):
    orgId = get_org_id_from_email(lightning_username)
    if len(str(arg1))>=1:
        sql_query_view="select name from metastore.schema_store_view where lower(name)='"+str(arg1)+"'"
        res = exec_query_get_res(sql_query_view)
        if isinstance(res[0],dict):
            for i in res:
                name = str(i['name'])
                #DROP VIEWS IF ALREADY EXISTING
                sql_query_drop_view="Drop Permanent View "+name
                generic_query(sql_query_drop_view)
            #GENERATE FILE AND EXECUTE THE QUERY TO RESTORE VIEW
            generate_file_name(arg1,'','-permanent_view-'+str(orgId),'individual',folder_path,api_url)
        else:
            #GENERATE FILE AND EXECUTE THE QUERY TO RESTORE THE VIEW WITHOUT DROPPING, SINCE IT DOESN'T EXIST ALREADY
            generate_file_name(arg1,'','-permanent_view-'+str(orgId),'individual',folder_path,api_url)
    else:
        sql_query_view="select name from metastore.schema_store_view where fk_organisation_id="+str(orgId).strip()
        res = exec_query_get_res(sql_query_view)
        if isinstance(res[0],dict):
            for i in res:
                name = str(i['name'])
                #DROP VIEWS IF ALREADY EXISTING
                sql_query_drop_view="Drop Permanent View "+name
                generic_query(sql_query_drop_view)
            #GENERATE FILE AND EXECUTE THE QUERY TO RESTORE VIEW
            generate_file_name('','','views-'+str(orgId),'full',folder_path,api_url)
        else:
            #GENERATE FILE AND EXECUTE THE QUERY TO RESTORE THE VIEW WITHOUT DROPPING, SINCE IT DOESN'T EXIST ALREADY
            generate_file_name('','','views-'+str(orgId),'full',folder_path,api_url)
#----------------------------------------#
#RESTORE DATAMARTS FUNCTION
def restore_datamarts(orgId,arg1,folder_path,api_url,lightning_username):
    orgId = get_org_id_from_email(lightning_username)
    if len(str(arg1))>=1:
        sql_query_mart="select name from metastore.data_mart where lower(name)='"+str(arg1)+"' and fk_organisation_id="+str(orgId).strip()
        res = exec_query_get_res(sql_query_mart)
        if isinstance(res[0],dict):
            for i in res:
                name = str(i['name'])
                #DROP DATA MART IF ALREADY EXISTING
                sql_query_drop_datamart="Drop Datamart "+name
                generic_query(sql_query_drop_datamart)
            #GENERATE FILE AND EXECUTE THE QUERY TO RESTORE DATAMART
            generate_file_name(arg1,'','-datamart-'+str(orgId),'individual',folder_path,api_url)
        else:
            #GENERATE FILE AND EXECUTE THE QUERY TO RESTORE THE DATAMART WITHOUT DROPPING, SINCE IT DOESN'T EXIST ALREADY 
            generate_file_name(arg1,'','-datamart-'+str(orgId),'individual',folder_path,api_url)
    else:
        sql_query_mart="select name from metastore.data_mart where fk_organisation_id="+str(orgId).strip()
        res = exec_query_get_res(sql_query_mart)
        if isinstance(res[0],dict):
            for i in res:
                name = str(i['name'])
                #DROP DATA MART IF ALREADY EXISTING
                sql_query_drop_datamart="Drop Datamart "+name
                generic_query(sql_query_drop_datamart)
            #GENERATE FILE AND EXECUTE THE QUERY TO RESTORE DATAMART
            generate_file_name('','','data_marts-'+str(orgId),'full',folder_path,api_url)
        else:
            #GENERATE FILE AND EXECUTE THE QUERY TO RESTORE THE DATAMART WITHOUT DROPPING, SINCE IT DOESN'T EXIST ALREADY 
            generate_file_name('','','data_marts-'+str(orgId),'full',folder_path,api_url)
#----------------------------------------#
#RESTORE PIPELINES FUNCTION
def restore_pipelines(arg1,arg2,folder_path,api_url,lightning_username):
    orgId = get_org_id_from_email(lightning_username)
    if len(str(arg1))>0 and len(str(arg2))>0:
        sql_query_pipeline="select r.name as rname,c.name as cname from metastore.pipeline_relation r inner join metastore.pipeline_container c on c.id=r.fk_pipeline_container_id where r.name='%s' and c.name='%s' and c.fk_organisation_id=%s"%(arg2,arg1,str(orgId).strip())
        logger.info(sql_query_pipeline)
        res = exec_query_get_res(sql_query_pipeline)
        if isinstance(res[0],dict):
            name = str(arg1.lower())+"."+str(arg2.lower())
            #DROP DATA PIPELINE IF ALREADY EXISTING
            sql_query_drop_pipeline="Drop Pipeline Relation "+name
            generic_query(sql_query_drop_pipeline)
            #GENERATE FILE AND EXECUTE THE QUERY TO RESTORE DATA PIPELINE
            generate_file_name(arg1,'-'+str(arg2),'-pipeline-'+str(orgId),'individual',folder_path,api_url)
        else:
            #GENERATE FILE AND EXECUTE THE QUERY TO RESTORE DATA PIPELINE WITHOUT DROPPING, SINCE IT DOESN'T EXIST
            generate_file_name(arg1,'-'+str(arg2),'-pipeline-'+str(orgId),'individual',folder_path,api_url)
    elif len(str(arg1))>0 and len(str(arg2))==0:
        sql_query_pipeline="select name from metastore.pipeline_container where lower(name)='"+str(arg1)+"' and fk_organisation_id="+str(orgId).strip()
        res = exec_query_get_res(sql_query_pipeline)
        if isinstance(res[0],dict):
            for i in res:
            #DROP DATA PIPELINE CONTAINER IF ALREADY EXISTING
                name = str(i['name'])
                sql_query_drop_pipeline="Drop Pipeline Container "+name
                generic_query(sql_query_drop_pipeline)
            #GENERATE FILE AND EXECUTE THE QUERY TO RESTORE DATA PIPELINE CONTAINER
            generate_file_name(arg1,'','-pipeline-'+str(orgId),'individual',folder_path,api_url)
        else:
            #GENERATE FILE AND EXECUTE THE QUERY TO RESTORE DATA PIPELINE CONTAINER WITHOUT DROPPING, SINCE IT DOESN'T EXIST
            generate_file_name(arg1,'','-pipeline-'+str(orgId),'individual',folder_path,api_url)
    else:
        sql_query_pipeline="select name from metastore.pipeline_container where fk_organisation_id="+str(orgId).strip()
        res = exec_query_get_res(sql_query_pipeline)
        if isinstance(res[0],dict):
            for i in res:
                name = str(i['name'])
            #DROP ALL DATA PIPELINE CONTAINERS IF ALREADY EXISTING..IF ANY
                sql_query_drop_pipeline="Drop Pipeline Container "+name
                generic_query(sql_query_drop_pipeline)
            #GENERATE FILE AND EXECUTE THE QUERY TO RESTORE ALL DATA PIPELINE CONTAINERS
            generate_file_name('','','pipelines-'+str(orgId),'full',folder_path,api_url)
        else:
            #GENERATE FILE AND EXECUTE THE QUERY TO RESTORE ALL DATA PIPELINE CONTAINERS WITHOUT DROPPING, SINCE IT DOESN'T EXIST
            generate_file_name('','','pipelines-'+str(orgId),'full',folder_path,api_url)
#----------------------------------------#
#EXECUTE ALL THE QUERIES INSIDE THE FILE GENERATED BY THE RESTORE FUCNTION
def execute_sql_file(filename):
    logger.info(filename)
    logger.info("\n")
    fd = open(filename, 'r')
    sqlFile = fd.read()
    sqlCommands = sqlFile.split(';')[:-1]
    for query in sqlCommands:
        logger.info(query)
        #EXECUTE ALL THE INSERT STATEMENTS IN THE FILE
        generic_query(query)
    fd.close()
    restore_msg="\nRestore finished for the file "+str(filename)
    logger.info(restore_msg)
#----------------------------------------#
#MAIN FUNCTION FOR THIS FILE. CALLS RELEVANT FUNCTIONS BASED ON RESTORE AND BACKUP OPTIONS.
def object_versioncontrol(folder_path,lightning_username,lightning_pass,api_url,vcarg1,vcarg2,vcarg3,vcarg4):
    #SET API URL AND PASS LOGIN CREDENTIALS TO THE API
    set_api_base_url(api_url)
    login(lightning_username,lightning_pass)
    #IF THE USER WANTS BACKUP, PERFORM THE BELOW OPERATIONS
    if str(vcarg1).lower().strip()=='backup':
        #CALL BACKUP PIPELINES FUNCTION AT AN INDIVIDUAL LEVEL
        print('Backup of INDIVIDUAL PIPELINES - PROCESS BEGUN')
        get_individual_pipelines(folder_path,lightning_username,lightning_pass,api_url)
        print('Backup of INDIVIDUAL PIPELINES - PROCESS END')
        #CALL BACKUP PIPELINES FUNCTION AT A CONTAINER LEVEL
        print('Backup of PIPELINES CONTAINER - PROCESS BEGUN')
        get_pipeline_containers(folder_path,lightning_username,lightning_pass,api_url)
        print('Backup of PIPELINES CONTAINER - PROCESS END')
        #CALL BACKUP PERMANENT DATA VIEWS FUNCTION
        print('Backup of PERMANENT VIEWS - PROCESS BEGUN')
        get_data_views(folder_path,lightning_username,lightning_pass,api_url)
        print('Backup of PERMANENT VIEWS - PROCESS END')
        #CALL BACKUP DATA MARTS FUNCTION
        print('Backup of DATA MARTS - PROCESS BEGUN')
        get_data_marts(folder_path,lightning_username,lightning_pass,api_url)
        print('Backup of DATA MARTS - PROCESS END')
        
    #IF THE USER WANTS RESTORE, PERFORM THE BELOW OPERATIONS
    elif str(vcarg1).lower().strip()=='restore':
        if (len(str(vcarg2).lower().strip())>0 and len(str(vcarg3).lower().strip())==0 and len(str(vcarg4).lower().strip())==0):
            try:
                #CALL RESTORE PIPELINES IF THE USER WANTS TO RESTORE ALL PIPELINES
                if str(vcarg2).lower().strip()=='pipelines':
                    logger.info("Restoring All Pipelines")
                    restore_pipelines('','',folder_path,api_url,lightning_username)
                #CALL RESTORE DATA MARTS IF THE USER WANTS TO RESTORE ALL DATA MARTS
                elif str(vcarg2).lower().strip()=='data_marts':
                    logger.info("Restoring All DataMarts")
                    restore_datamarts('',folder_path,api_url,lightning_username)
                #CALL RESTORE VIEWS IF THE USER WANTS TO RESTORE ALL DATA VIEWS
                elif str(vcarg2).lower().strip()=='views':
                    logger.info("Restoring All Views")
                    restore_views('',folder_path,api_url,lightning_username)
            #EXIT IF NO OPTION IS MENTIONED OR PARAMETERS ARE PASSED INCORRECTLY
            except:
                exit()
        elif (len(str(vcarg2).lower().strip())>0 and len(str(vcarg3).lower().strip())>0 and len(str(vcarg4).lower().strip())==0):
            try:
                #CALL RESTORE PIPELINES IF THE USER WANTS TO RESTORE PIPELINES AT CONTAINER LEVEL
                if str(vcarg2).lower().strip()=='pipelines':
                    logger.info("Restoring Pipeline Container")
                    restore_pipelines(str(vcarg3).lower().strip(),'',folder_path,api_url,lightning_username)
                #CALL RESTORE DATA MARTS IF THE USER WANTS TO RESTORE DATA MARTS AT CONTAINER LEVEL
                elif str(vcarg2).lower().strip()=='data_marts':
                    logger.info("Restoring DataMart")
                    restore_datamarts(str(vcarg3).lower().strip(),folder_path,api_url,lightning_username)
                #CALL RESTORE VIEWS IF THE USER WANTS TO RESTORE ANY OF THE PERMANENT VIEWS
                elif str(vcarg2).lower().strip()=='views':
                    logger.info("Restoring View")
                    restore_views(str(vcarg3).lower().strip(),folder_path,api_url,lightning_username)
            #EXIT IF NO OPTION IS MENTIONED OR PARAMETERS ARE PASSED INCORRECTLY
            except:
                exit()
        elif (len(str(vcarg2).lower().strip())>0 and len(str(vcarg3).lower().strip())>0 and len(str(vcarg4).lower().strip())>0):
            try:
                #CALL RESTORE PIPELINES IF THE USER WANTS TO RESTORE PIPELINES AT INDIVIDUAL LEVEL
                if str(vcarg2).lower().strip()=='pipelines':
                    logger.info("Restoring Individual Pipelines")
                    restore_pipelines(str(vcarg3).lower().strip(),str(vcarg4).lower().strip(),folder_path,api_url,lightning_username)
            #EXIT IF NO OPTION IS MENTIONED OR PARAMETERS ARE PASSED INCORRECTLY
            except:
                exit()
        else:
            #RESTORE ALL THE DATA OBJECTS
            logger.info("Restoring All")
            #RESTORE ALL THE DATA PIPELINES
            restore_pipelines('','',folder_path,api_url,lightning_username)
            #RESTORE ALL THE DATA MARTS
            restore_datamarts('',folder_path,api_url,lightning_username)
            #RESTORE ALL THE DATA/PERMANENT VIEWS
            restore_views('',folder_path,api_url,lightning_username)
#----------------------------------------#