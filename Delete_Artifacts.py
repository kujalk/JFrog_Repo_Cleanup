import requests
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s :: [%(module)s] :: [%(levelname)s] :: %(message)s",
    handlers=[
        logging.FileHandler("Delete.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('log')

def read_all_folders(artifactory_url,config,auth):
    """
    To read all folders and print its modified state
    """

    try:
        for folder in config.get('folders'):
            for path in folder.get('path'):

                url = f'{artifactory_url}'
                logger.info(f"Working on path - {folder.get('repo')}/{path}")

                aql_query = f'items.find({{"type":"folder","repo":{{"$eq":"{folder.get("repo")}"}},"path":"{path}"}})'

                response = requests.post(url+'/api/search/aql', headers=headers, data=aql_query, auth=auth)

                if(response.status_code == 200):
                    results=json.loads(response.text)
                    for item in results.get('results'):
                        logger.info(f"Path -> {item['repo']}/{item['path']}/{item['name']} and Modified Date -> {item['modified']}")
                else:
                    logger.error(f"Response code is {response.status_code} while accessing url {folder.get('repo')}/{path} and error is {response.text}")
                    
    except Exception as e:
        logger.error(f"Failed to read files {e}")


def get_delete_folders(artifactory_url,config,auth):
    """
    To get all delete folers and their urls sorted by modified date
    """

    try:
        tracker=[]
        
        for folder in config.get('folders'):
            for path in folder.get('path'):

                path_tracker=[]
                url = f'{artifactory_url}'
                logger.info(f"Working on path - {folder.get('repo')}/{path}")

                aql_query = f'items.find({{"type":"folder","repo":{{"$eq":"{folder.get("repo")}"}},"path":"{path}"}})'

                response = requests.post(url+'/api/search/aql', headers=headers, data=aql_query, auth=auth)

                if(response.status_code == 200):
                    results=json.loads(response.text)
                    for item in results.get('results'):
                        artifact={}
                        artifact['Path'] = f"{item['repo']}/{item['path']}/{item['name']}"
                        artifact['Modified'] = item['modified']
                        path_tracker.append(artifact)
                        
                        logger.info(f"Path -> {item['repo']}/{item['path']}/{item['name']} and Modified Date -> {item['modified']}")
                    
                    delete_list = sorted(path_tracker, key=lambda d: d['Modified']) 
                    tracker.append(delete_list[:-folder.get("keep_minimum")])
                    
                else:
                    logger.error(f"Response code is {response.status_code} while accessing url {folder.get('repo')}/{path} and error is {response.text}")
    
        return tracker
    
    except Exception as e:
        logger.error(f"Failed to read files {e}")


def delete_artifacts(artifactory_url,filter_results,auth):  
    """
    Loop and delete the artifacts folders
    """ 
    
    try:
        count=0
        for entry in filter_results:         
            for url in entry:

                try:
                    count+=1
                    delete_url = f"{artifactory_url}/{url['Path']}"
                    logger.info(f"Deleting {delete_url}")

                    # response = requests.delete(delete_url, auth=auth)

                    # if(response.status_code == 204):
                    #      logger.info("Deletion is successful")
                    # else:
                    #     raise Exception (f"Deletion failed with response code - {response.status_code}")

                except Exception as e:
                    logger.error(f"Failed to delete the {url} - {e}")
                    
        logger.info(f"Completed deleting. Deleted {count} items totally")

    except Exception as e:
        logger.error(f"Failed in Deleting urls - {e}")



#Main
with open (r'Cleanup.json', "r") as file:
    config=json.loads(file.read())

artifactory_url = config.get('artifactory_url')
headers = {"content-type": "text/plain"}
username = 'testuser'
password = 'testpassword'
auth=(username, password)

logger.info("Starting script")
read_all_folders(artifactory_url,config,auth)

logger.info("Getting Delete urls")
delete_urls=get_delete_folders(artifactory_url,config,auth)

logger.info("Starting deleting artifacts")
delete_artifacts(artifactory_url,delete_urls,auth)

logger.info("Completed script")
