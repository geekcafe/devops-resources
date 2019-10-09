
#!/usr/bin/python
 
###########################################################
#
# This python script is used for mysql database backup
# using mysqldump and tar utility.
#
# Written by : Eric Wilson
# Website: http://www.geekcafe.com
# Created date: October 8, 2019
# Last modified: 
# Tested with : Python 2.7.15 & Python 3.5
# Script Revision: 1.0
#
##########################################################
import os
import time
import datetime
import pipes


def backup_mysql_db(host, port, userName, password, databaseName, folderPath):
    
    # generate a backup name with a timestamp
    timestamp = time.strftime('%Y%m%d-%H%M%S')
    fileName = databaseName + '-' + timestamp + ".dump"
    path = os.path.join(folderPath, fileName)
    errors = False

    # Checking if backup folder already exists or not. If not exists will create it.
    try:
        print("checking directory path for " + folderPath)
        if not os.path.exists(folderPath):
            print("Creating folder path")
            os.makedirs(folderPath)
        else:
            print("Path Exists")
        print()
    except:
        print("Error on making directory")
        
    try:        
        print("Backing up " + databaseName + " to " + path)
        dump_options = " --default-character-set=utf8 --skip-triggers  --single-transaction --skip-lock-tables  --compress "
        dumpcmd = "mysqldump  --user=" + userName + " --host=" + host + " --protocol=tcp --port=" + port + " --password=" + password + dump_options + " " +databaseName + " > " + pipes.quote(path)
        #dumpcmd = "mysqldump --protocol=tcp --host=" + host + " --user=" + userName + " -p " + password + " --port=" + port + " " + databaseName + " > " + pipes.quote(path)
        
        print("Executing " + dumpcmd)

        os.system(dumpcmd)
        gzipcmd = "gzip " + pipes.quote(path)
        os.system(gzipcmd)
    except:
        print("Error Generating a backup")

    if not errors:
        print ("")
        print ("Backup script completed")
        print ("Your backups have been created in '" + path + "' directory")
    else:
        print("Backup Failed")

