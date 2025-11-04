#!/usr/bin/env bash

SELENIUM_URL=$1
RETRIES=$2
DELAY=$3

check_selenium_service() {
  # Try health check endpoint
  response=$(curl --write-out "%{http_code}" --silent --output /dev/null "$SELENIUM_URL/status")
  
  if [[ "$response" -eq 200 ]]; then
    echo "Selenium service is up and running."
    return 0
  else
    echo "Selenium service is not responding. HTTP Status: $response"
    return 1
  fi
}

attempt=1
while [[ $attempt -le $RETRIES ]]
do
  echo "Attempt $attempt of $RETRIES to check Selenium service..."
  if check_selenium_service; then
    echo "Selenium service is available."
    exit 0
  else
    echo "Retrying in $DELAY seconds..."
    sleep $DELAY
    attempt=$((attempt + 1))
  fi
done

echo "Selenium service is still down after $RETRIES attempts. Exiting..."
exit 1