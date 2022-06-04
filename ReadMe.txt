
Purpose
-----------
This script is used to delete the folders in Jfrog from a given path (specified in JSON)
Script will skip the latest folders and delete other folders from the given path

How to run
-----------
1. Make sure you have created a user in Jfrog with appropriate permission to delete the artifacts
2. Update the username and password in the python script (Later we can think, how to secure this depending on where we going to run this script)
3. Fill the JSON file 
    keep_minimum: Minimum Folders that needs to be kept
4. Run the script as "python Delete_Artifacts_Folders.py"


Developer - K.Janarthanan
