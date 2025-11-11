#!/bin/bash

# Divide classpaths (-cp adds them to the classpath), look at cur dir, then run jar file
javac -cp ".:../sqljdbc_12.8.1.0_enu/sqljdbc_12.8/enu/jars/mssql-jdbc-12.8.1.jre11.jar" *.java #CreateDB.java QueryDB.java

# Create database from CSV file
# java -cp ".:../sqljdbc_12.8.1.0_enu/sqljdbc_12.8/enu/jars/mssql-jdbc-12.8.1.jre11.jar" CreateDB students.csv

# Run query on database
java -cp ".:../sqljdbc_12.8.1.0_enu/sqljdbc_12.8/enu/jars/mssql-jdbc-12.8.1.jre11.jar" QueryDB # Michael
