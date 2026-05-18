#!/bin/bash

# Run `chmod +x setup.sh` to make this file executable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_indent() {
    echo -e "    $1"
}

# Check dependencies
check() {
    print_header "Checking Python Dependencies"
    if ! command -v python3 &> /dev/null
    then
        print_error "python3 could not be found. Please install Python 3 to proceed."
        exit
    else
        print_success "python3 found:"
        print_indent "$(python3 --version)"
    fi
}

is_activated() {
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        print_success "Virtual environment is activated."
        print_info "Use command 'deactivate' to exit the virtual environment."
        return 0
    else
        print_error "Virtual environment is not activated. Please run 'source .venv/bin/activate' first."
        return 1
    fi
}

init_venv() {
    print_header "Setting up Python Virtual Environment"
    if [ -d ".venv" ]; then
        print_warning "Virtual environment '.venv' already exists. Skipping creation."
    else
        print_info "Creating virtual environment '.venv'..."
        python3 -m venv .venv
        print_success "Virtual environment created."
    fi

    print_info "Activating virtual environment..."
    source .venv/bin/activate

    # Verify activation
    if ! is_activated; then
        print_error "Failed to activate the virtual environment."
        exit 1
    fi
}

populate_venv() {
    # Check if virtual environment is activated
    if ! is_activated; then
        exit 1
    fi

    print_header "Populating Python Virtual Environment"
    print_info "Upgrading pip to the latest version..."
    pip install --upgrade pip
    print_success "pip is using the latest version."

    print_info "Installing required packages from `requirements.txt`..."
    pip install -r requirements.txt
    print_success "Required packages installed."

    print_info "Verifying installation by listing installed packages..."
    pip list
}

show_usage() {
    echo -e "${CYAN}Usage: $0 [command]${NC}"
    echo -e "${BLUE}Commands:${NC}"
    echo "  check, ch                           - Check for required dependencies"
    echo "  init, in                            - Initialize the Python virtual environment"
    echo "  is_activated, ia                   - Check if the virtual environment is activated"
    echo "  populate, pop                       - Populate the virtual environment with required packages"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo "  $0 check"
    echo "  source $0 init"                     - Source is needed to activate venv in current shell
    echo "  $0 populate"
}

case $1 in
    "ch"|"check")
        check
        ;;
    "in"|"init")
        init_venv
        ;;
    "ia"|"is_activated")
        is_activated
        ;;
    "pop"|"populate")
        populate_venv
        ;;
    *)
        print_error "Invalid argument. Use 'check', 'init', 'is_activated', or 'populate'."
        show_usage
        ;;
esac
