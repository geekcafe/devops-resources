from mysqlDbFunctions import backup_mysql_db



# example execution
backup_mysql_db("127.0.0.1", "3306", "username", "password", "database_name", "/tmp/db/bk")
