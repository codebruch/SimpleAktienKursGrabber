#!/bin/bash

# Start the first process

python /app/wsserver.py &

# Start the second process
python /app/webscraper.py &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?