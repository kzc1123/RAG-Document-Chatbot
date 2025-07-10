#!/bin/bash

# Define the base URL of your FastAPI application
BASE_URL="http://0.0.0.0:8000"

# Test GET request
echo "Testing GET "$BASE_URL'/'
response=$(curl -X GET $BASE_URL'/')
echo "Response: >>$response<<"
# Optionally, check something in the response, e.g., status or a field
echo $response | jq '.id, .name'  # adjust fields according to your API response

echo "--------------------------------------------------"

# Test POST request
echo "Testing POST /items"
post_data='{"name": "sample item", "description": "This is a sample item."}'
response=$(curl -s -X POST "$BASE_URL/items" -H "Content-Type: application/json" -d "$post_data")
echo "Response: $response"
# Optionally, check something in the response, e.g., status or a field
echo $response | jq '.id, .message'  # adjust fields according to your API response

# Check for specific response codes or values if needed
# You can add if conditions to check response and exit with non-zero status on failure
