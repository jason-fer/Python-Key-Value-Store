#!/bin/bash
# Install the python dependencies needed for this application
# Will need root permission to run if you don't have the --user 
# option below. 
pip install Flask     	--user   #for the webserver
pip install requests   	--user   #for the client
pip install sqlite3   	--user   #for sqlite backend
pip install hash_ring 	--user   #for consistent hashing
