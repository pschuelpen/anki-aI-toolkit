#!/bin/bash

# Just some cool Message up top - but functionally stupid
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
echo ""
echo "Anki AI Toolkit - Setup Assistant - V1"
echo ""
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
echo ""

# Path to the configuration file
CONFIG_FILE="./src/config.yaml"

# Function to display usage instructions
usage() {
    echo "[Info] Usage: $0"
    echo "[Info] Run the script to configure the API key. If a config already exists, it will be used."
    exit 1
}

# Function to securely read API key input
read_api_key() {
    echo -n "[Setup] Enter your API key: "
    # Disable terminal echo to hide input
    stty -echo
    read -r API_KEY
    # Re-enable terminal echo
    stty echo
    echo
}

# Check if the configuration file already exists
if [ -f "$CONFIG_FILE" ]; then
    # Attempt to read the key from the existing file
    EXISTING_KEY=$(grep -oP '(?<=openai-api-key: ).*' "$CONFIG_FILE")
    if [ -n "$EXISTING_KEY" ]; then
        echo "[Setup] Config file '$CONFIG_FILE' already exists."
        echo "[Setup] Existing API key: *********** (hidden for privacy)"
        echo "[Setup] Exit"
        exit 0
    else
        echo "[Setup] Config file '$CONFIG_FILE' exists but no valid API key found."
    fi
else
    echo "[Setup] No existing configuration found."
fi

# Prompt the user to enter the API key
read_api_key

# Ensure the API key is not empty
if [ -z "$API_KEY" ]; then
    echo "[Error] Error: API key cannot be empty."
    exit 1
fi

# Write the API key to config.yaml
mkdir -p "$(dirname "$CONFIG_FILE")" # Ensure the directory exists
echo "[Setup] openai-api-key: $API_KEY" > "$CONFIG_FILE"
echo "[Setup] Config file '$CONFIG_FILE' created successfully."
