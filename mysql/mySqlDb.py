
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

class mySqlDb:
    def __init__(self, host, port, userName, password, databaseName):
        self.host = host
        self.port = port
        self.userName = userName
        self.password = password
        self.databaseName = databaseName
    
    def export(self, folderPath, compress = True):
        # generate a backup name with a timestamp
        timestamp = time.strftime('%Y%m%d-%H%M%S')
        fileName = self.databaseName + '-' + timestamp + ".dump"
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
                print("Backing up " + self.databaseName + " to " + path)
                # some options
                dump_options = " --default-character-set=utf8 --skip-triggers  --single-transaction --skip-lock-tables  --compress "
                dumpcmd = "mysqldump  --user=" + self.userName + " --host=" + self.host + " --protocol=tcp --port=" + self.port + " --password=" + self.password + dump_options + " " +databaseName + " > " + pipes.quote(path)
                
                
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
    

    def restore_mysql_db(self, filePath):
        
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
            try:
                # 3.7 syntax - string interpolation
                restoreCmd = f"mysql  --user={self.userName} --host={self.host} --protocol=tcp --port={self.port} --password={self.password} {self.databaseName} < {pipes.quote(filePath)} "
                # let's do a backup
                response = os.system(restoreCmd)

                if response!=0:
                    errors = True

            except:
                print("Exception Occured")

        
        if not errors:
            print("Db Restored Succesfully")