#!/bin/bash

# ./env.sh -e    # To encrypt
# ./env.sh -d    # To decrypt

ENV_FILE=".env"
ENC_FILE=".env.enc"

# Function to encrypt the .env file
encrypt_env() {
    # Check if .env exists
    if [ ! -f "$ENV_FILE" ]; then
        echo "Error: $ENV_FILE does not exist."
        exit 1
    fi

    echo "Encrypting $ENV_FILE to $ENC_FILE..."

    # Encrypt the file with OpenSSL (AES-256-CBC)
    openssl enc -aes-256-cbc -salt -in "$ENV_FILE" -out "$ENC_FILE"

    # Check if encryption was successful
    if [ $? -eq 0 ]; then
        echo "Encryption successful! File saved as $ENC_FILE"
        
        # Ask if original file should be deleted
        read -p "Do you want to delete the original .env file? (y/n): " delete_original
        if [[ $delete_original == "y" || $delete_original == "Y" ]]; then
            rm "$ENV_FILE"
            echo "Original .env file deleted."
        fi
        
        echo "IMPORTANT: Don't forget the password used for encryption!"
    else
        echo "Encryption failed."
        exit 1
    fi
}

# Function to decrypt the .env.enc file
decrypt_env() {
    # Check if encrypted file exists
    if [ ! -f "$ENC_FILE" ]; then
        echo "Error: $ENC_FILE does not exist."
        exit 1
    fi

    # Check if .env already exists to prevent accidental overwrite
    if [ -f "$ENV_FILE" ]; then
        read -p "Warning: $ENV_FILE already exists. Overwrite? (y/n): " overwrite
        if [[ $overwrite != "y" && $overwrite != "Y" ]]; then
            echo "Decryption cancelled."
            exit 0
        fi
    fi

    echo "Decrypting $ENC_FILE to $ENV_FILE..."

    # Decrypt the file with OpenSSL
    openssl enc -aes-256-cbc -d -in "$ENC_FILE" -out "$ENV_FILE"

    # Check if decryption was successful
    if [ $? -eq 0 ]; then
        echo "Decryption successful! File saved as $ENV_FILE"
        
        # Set proper permissions for the .env file
        chmod 600 "$ENV_FILE"
        echo ".env file permissions set to 600 (read/write for owner only)"
    else
        echo "Decryption failed. Make sure you're using the correct password."
        # Remove potentially corrupted output file
        if [ -f "$ENV_FILE" ]; then
            rm "$ENV_FILE"
        fi
        exit 1
    fi
}

# Process command line arguments
if [ "$1" == "-e" ] || [ "$1" == "--encrypt" ]; then
    encrypt_env
elif [ "$1" == "-d" ] || [ "$1" == "--decrypt" ]; then
    decrypt_env
else
    # If no valid argument provided, prompt user for action
    echo "What would you like to do?"
    echo "1) Encrypt .env file"
    echo "2) Decrypt .env.enc file"
    read -p "Enter your choice (1 or 2): " choice
    
    case $choice in
        1)
            encrypt_env
            ;;
        2)
            decrypt_env
            ;;
        *)
            echo "Invalid choice. Please run again and select 1 or 2."
            exit 1
            ;;
    esac
fi
