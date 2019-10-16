
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


def backup_mysql_db(host, port, userName, password, databaseName, folderPath, compress = True):
    
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
        errors = True
    
    if not errors:
        try:        
            print("Backing up " + databaseName + " to " + path)
            # some options
            dump_options = " --default-character-set=utf8 --skip-triggers  --single-transaction --skip-lock-tables  --compress "
            dumpcmd = "mysqldump  --user=" + userName + " --host=" + host + " --protocol=tcp --port=" + port + " --password=" + password + dump_options + " " +databaseName + " > " + pipes.quote(path)
            
            
            print("Executing " + dumpcmd)

            response = os.system(dumpcmd)

            if response==0:
                # zip the file
                if compress:
                    gzipcmd = "gzip " + pipes.quote(path)
                    path = path + ".gz"
                    os.system(gzipcmd)
            else:
                print("Error Returned by mysql during the backup")
                errors=True
                # remove the file created by the backup process
                if os.path.exists(path):
                    os.remove(path)
        except:
            print("Error Generating a backup")
            errors = True

    if not errors:
        print ("")
        print ("Backup script completed")
        print ("Your backup have been created.  It can found here: [" + path + "]")
    else:
        print("Backup Failed")

def restore_mysql_db(host, port, userName, password, databaseName, folderPath, compress = True):
    print(host)