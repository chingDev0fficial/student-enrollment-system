#!/usr/bin/env bash

# Print a header message
print_header() {
    echo -e "\n=============================="
    echo -e "  $1"
    echo -e "==============================\n"
}

# Log messages
log_message() {
    echo -e "[INFO] $1"
}

# Handle errors and exit
handle_error() {
    echo -e "[ERROR] $1"
    exit 1
}

# Check for required commands
check_requirements() {
    for cmd in "$@"; do
        if ! command -v "$cmd" &> /dev/null; then
            handle_error "Missing required command: $cmd"
        fi
    done
}

# Activate virtual environment
activate_venv() {
    if [ -d ".venv" ]; then
        log_message "Activating virtual environment..."
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
            source .venv/Scripts/activate || handle_error "Failed to activate virtual environment"
        else
            source .venv/bin/activate || handle_error "Failed to activate virtual environment"
        fi
    else
        handle_error "Virtual environment not found. Run setup first."
    fi
}
