#!/bin/bash

PORT=5000
COMMAND_TO_CHECK_PORT="lsof -i :$PORT"
PROCESS_INFO=$(eval $COMMAND_TO_CHECK_PORT)

# Had some issues with port 5000 so wanted to just deal with it here
if [ ! -z "$PROCESS_INFO" ]; then
    echo "Port $PORT is in use."
    echo "Do you want to stop the process using port $PORT? (y/n)"
    read USER_INPUT
    if [ "$USER_INPUT" == "y" ]; then
        PID=$(echo $PROCESS_INFO | awk '{print $2}' | tail -1)
        if kill $PID; then
            echo "Process using port $PORT has been stopped."
        else
            echo "Failed to stop the process. Changing port in docker-compose.yml."
            sed -i '' "s/5000:5000/5001:5000/g" docker-compose.yml
        fi
    fi
fi

sudo docker-compose up --build -d

sleep 15

python test_api_script.py

echo "Do you want to stop the API and clean docker compose? (y/n)"
read STOP_API
if [ "$STOP_API" == "y" ]; then
    sudo docker-compose down --volumes --remove-orphans
    echo "API has been stopped."
fi
