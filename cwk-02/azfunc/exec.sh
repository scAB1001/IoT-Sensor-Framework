#!/bin/bash

# IoT Framework Script - COMP3211 CWK2

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

BASE_URL="https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/api"

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


compile_query_db() {
    print_info "Querying database for verification..."
    cd ../java-db/
    ./build.sh exec QueryDB.java
    cd ../azfunc/
}

query_db() {
    print_info "Querying database for verification..."
    cd ../java-db/
    java QueryDB.java
    cd ../azfunc/
}

check() {
    print_header "Checking Data Transfer Dependencies"

    # Check for curl or wget
    if ! command -v curl &> /dev/null && ! command -v wget &> /dev/null
    then
        print_error "Neither curl nor wget could be found. Please install one of them to proceed."
        exit
    elif command -v curl &> /dev/null; then
        print_success "curl is installed."
        print_indent "$(curl --version | head -n 1)"
    else
        print_success "wget is installed."
        print_indent "$(wget --version | head -n 1)"
    fi

    print_header "Checking Virtual Environment Status"
    source ./setup.sh is_activated

    print_header "Checking Azure SQL Database Status"
    compile_query_db
}

curl_response() {
    local response="$1"
    local success_msg="$2"
    local failure_msg="$3"

    # Default messages if none given
    success_msg="${success_msg:-Request successful}"
    failure_msg="${failure_msg:-Request failed}"

    # Check using curl
    if echo "$response" | python3 -c "import json, sys; json.load(sys.stdin); print('valid')" 2>/dev/null | grep -q "valid"; then
        echo "$response" | python3 -m json.tool
        print_success "$success_msg"
        return 0
    else
        echo "$response"
        print_error "$failure_msg"
        return 1
    fi
}

deploy_functions() {
    print_header "DEPLOYING FUNCTIONS TO AZURE"
    print_info "This may take a few minutes..."

    if func azure functionapp publish func-app-sc222ab --python; then
        print_success "Deployment completed successfully!"
    else
        print_error "Deployment failed"
    fi
}

check_azure_status() {
    print_header "Checking Azure Functions and Database Status"

    # Test by calling statistics endpoint with dummy request

    # Test by calling simulate-data endpoint with dummy request
}

test_task1() {
    check

    print_header "TASK 1: Testing Sensor Data Simulation"
    print_info "Generating data for 20 sensors..."

    # If $2 is provided, use it as sensor count
    if [ -n "$2" ]; then
        SENSOR_COUNT=$2
        echo "Using sensor count: ${SENSOR_COUNT}"
        response=$(curl -s "${BASE_URL}/simulate-data?sensor_count=${SENSOR_COUNT}")
    else
       response=$(curl -s "${BASE_URL}/simulate-data")
    fi

    # Check response with curl
    curl_response "$response" "Task 1 - Data generation successful" "Task 1 - Failed to generate data"

    if [ $? -ne 0 ]; then
        # show_usage
        exit
    else
        print_success "Azure Functions: ONLINE"
        print_success "Database Connection: ONLINE"
        # Check using java-db
        print_info "Verifying data insertion in database..."
        query_db
    fi
}

test_task2() {
    print_header "TASK 2: Testing Statistics Calculation"
    print_info "Calculating statistics from database..."

    response=$(curl -s "${BASE_URL}/statistics")

    # Check response with curl
    curl_response "$response" "Task 2 - Statistics calculation successful" "Task 2 - Failed to calculate statistics"

    # Check using java-db
    print_info "Verifying data insertion in database..."
    query_db
}

# TODO:
test_task3() {
    print_header "TASK 3: Testing Automated Pipeline"

    print_info "Step 3(a): Generating data to trigger automation..."
    response=$(curl -s "${BASE_URL}/simulate-data?sensor_count=3")

    if echo "$response" | python3 -c "import json, sys; json.load(sys.stdin); print('valid')" 2>/dev/null | grep -q "valid"; then
        print_success "Step 3(a) - Data generated successfully"

        print_info "Step 3(b/c): Checking database (automatic trigger should run in background)..."
        sleep 3

        # Check statistics to verify pipeline worked
        stats_response=$(curl -s "${BASE_URL}/statistics")
        if echo "$stats_response" | python3 -c "import json, sys; data=json.load(sys.stdin); print('valid' if data.get('data_analyzed', 0) > 0 else 'empty')" 2>/dev/null | grep -q "valid"; then
            print_success "Task 3 - Automated pipeline working!"
            echo "Latest statistics:"
            data_analyzed=$(echo "$stats_response" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('data_analyzed', 0))")
            echo "$data_analyzed"
        else
            print_warning "Task 3 - Pipeline may need time to trigger (check Azure logs)"
        fi
    else
        print_error "Task 3 - Failed to generate test data"
    fi
}


show_usage() {
    echo -e "${CYAN}IoT Framework Test Script${NC}"
    echo
    echo "Usage: $0 [command]"
    echo
    echo -e "${BLUE}Commands:${NC}"
    echo -e "  check, ch                - Check for required dependencies"
    echo -e "  task1, t1                - Test Task 1 (Data Simulation)"
    echo -e "  task2, t2                - Test Task 2 (Statistics)"
    echo -e "  task3, t3                - Test Task 3 (Automated Pipeline)"
    echo -e "  deploy, dep              - Deploy functions to Azure"
    echo -e "  query, q                 - Query database for verification"
    echo -e "  status, st               - Check azure status"
    echo -e "  all, a                   - Run all tests"
    print_info "Base URL: $BASE_URL"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo "  $0 check"
    echo "  $0 task1 | task2 | task3"
    echo "  $0 deploy"
    echo "  $0 query"
    echo "  $0 status"
    echo "  $0 all"
}

case "${1:-}" in
    "t1"|"task1")
        test_task1
        ;;
    "t2"|"task2")
        test_task2
        ;;
    "t3"|"task3")
        test_task3
        ;;
    "dep"|"deploy")
        deploy_functions
        ;;
    "q"|"query")
        query_db
        ;;
    "st"|"status")
        show_status
        ;;
    "a"|"all")
        test_task1
        echo
        test_task2
        echo
        test_task3
        ;;
    *)
        show_usage
        ;;
esac