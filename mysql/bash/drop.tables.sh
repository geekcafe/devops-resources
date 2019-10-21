#!/bin/bash
MUSER="$1"
MPASS="$2"
MDB="$3"
HOST="$4"
PORT="$5"
 
# Detect paths
MYSQL=$(which mysql)
AWK=$(which awk)
GREP=$(which grep)
 
if [ $# -ne 5 ]
then
	echo "Usage: $0 {MySQL-User-Name} {MySQL-User-Password} {MySQL-Database-Name} {Host} {Port}"
	echo "Drops all tables from a MySQL"
	exit 1
fi

CONNECTION = "" 
TABLES=$($MYSQL -u $MUSER -p$MPASS $MDB --host=$HOST --port=$PORT -e 'show tables' | $AWK '{ print $1}' | $GREP -v '^Tables' )
 
for t in $TABLES
do
	echo "Deleting $t table from $MDB database..."
	$MYSQL -u $MUSER -p$MPASS $MDB --host=$HOST --port=$PORT -e "drop table $t"
done