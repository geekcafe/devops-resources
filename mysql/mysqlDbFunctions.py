
#!/usr/bin/python
 
###########################################################
#
# This python script is used for mysql database backup
# using mysqldump and gzip utility.
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


def backup_mysql_db(host, port, userName, password, databaseName, folderPath, compress = True, showProgress = True):
    
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
        
            progress_options = " --verbose "
            dump_options = " --default-character-set=utf8 --skip-triggers  --single-transaction --skip-lock-tables  --compress "
            dumpcmd = "mysqldump  --user=" + userName + " --host=" + host + " --protocol=tcp --port=" + port + " --password=" + password + dump_options + " " + databaseName + " " + progress_options + "  > " + pipes.quote(path)
            
            
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

def restore_mysql_db(host, port, userName, password, databaseName, filePath, compress = True, showProgress = True):
    errors = False

    # check to see if the file exists
    try:
        print("checking directory path for " + filePath)
        if not os.path.isfile(filePath) :
            print("file does not exist")
            errors = True 
        
    except:
        print("Error checking for backup file")
        errors = True

    if not errors:
        
        connectCommand = "mysql  --user=" + userName + "  --host=" + host + "  --protocol=tcp --port=" + port + "  --password=" + password

        try:
            #drop the db 
            print("\t[Database] [" + databaseName + "][Dropping]")
            
            
            dropDbCommand = " -e \" drop database " + databaseName + "\""

            response = os.system(connectCommand + dropDbCommand)

            outcome = "NA"
            if response==0:
                outcome = "Succeeded"
            else: 
                outcome = "Failed"
                #it's possible the database didn't exist so don't set the flag errors flag here

            print("\t[Database][" + databaseName + "][Drop][" + outcome +"]")
        except:
            print("\tException Occured Dropping Db")

        
        try:
            
            print("\t[Database] [" + databaseName + "][Creating]")
            
            
            dropDbCommand = " -e \" create database " + databaseName + "\""

            response = os.system(connectCommand + dropDbCommand)

            # create the db
            outcome = "NA"
            if response==0:
                outcome = "Succeeded"
            else: 
                outcome = "Failed"                
                # if we can't create it we should set the errors flag
                outcome=True

            print("\t[Database][" + databaseName + "][Create][" + outcome +"]")

        except:
            print("\tException Occured Creating Db")


      


        if not errors:
            try:
                
                progressCmd = "pv " + filePath + " | "

                restoreCmd =  connectCommand + "  " + databaseName

                if showProgress:
                    restoreCmd = progressCmd + " " + restoreCmd
                else:
                    restoreCmd = restoreCmd + "  < " + pipes.quote(filePath) 

                # let's do a backup
                response = os.system(restoreCmd)

                if response!=0:
                    errors = True

            except:
                print("\tException Occured")

        
        if not errors:
            outocme = "Completed Successfully"
        else: 
            outocme = "Failed With Errors"                
            

        print("[Database][" + databaseName + "][Restore][" + outcome +"]")