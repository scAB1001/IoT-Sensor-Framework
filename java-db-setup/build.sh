#!/bin/bash

# README #
# Run `chmod +x ./build.sh` to make this file executable

# Divide class paths (-cp adds them to the classpath), look at cur dir, then run jar file
javac -cp ".:../sqljdbc_12.8.1.0_enu/sqljdbc_12.8/enu/jars/mssql-jdbc-12.8.1.jre11.jar" *.java

# Execute the class (executable) file
java CreateDB
java QueryDB