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

test_task1() {
    print_header "TASK 1: Testing Sensor Data Simulation"
    print_info "Generating data for 20 sensors..."

    response=$(curl -s "${BASE_URL}/simulate-data?sensor_count=20")

    if echo "$response" | python3 -c "import json, sys; json.load(sys.stdin); print('valid')" 2>/dev/null | grep -q "valid"; then
        print_success "Task 1 - Data generation successful"
        echo "$response" | python3 -m json.tool
    else
        print_error "Task 1 - Failed to generate data"
        echo "$response"
    fi
}

test_task2() {
    print_header "TASK 2: Testing Statistics Calculation"
    print_info "Calculating statistics from database..."

    response=$(curl -s "${BASE_URL}/statistics?data_limit=10")

    if echo "$response" | python3 -c "import json, sys; json.load(sys.stdin); print('valid')" 2>/dev/null | grep -q "valid"; then
        print_success "Task 2 - Statistics calculation successful"
        echo "$response" | python3 -m json.tool
    else
        print_error "Task 2 - Failed to calculate statistics"
        echo "$response"
    fi
}

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

query_db() {
    print_info "Querying database for verification..."
    cd ../java-db-setup/
    java QueryDB
    cd ../azfunc/
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

show_status() {
    print_header "CURRENT SYSTEM STATUS"

    # Test basic connectivity
    if curl -s "${BASE_URL}/simulate-data?sensor_count=1" > /dev/null; then
        print_success "Azure Functions: ONLINE"
    else
        print_error "Azure Functions: OFFLINE"
    fi

    # Check database connectivity via statistics
    stats=$(curl -s "${BASE_URL}/statistics?data_limit=1")
    if echo "$stats" | python3 -c "import json, sys; data=json.load(sys.stdin); print('connected' if 'data_analyzed' in data else 'error')" 2>/dev/null | grep -q "connected"; then
        print_success "Database Connection: ONLINE"
    else
        print_warning "Database Connection: CHECKING..."
    fi
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
    "all")
        test_task1
        echo
        test_task2
        echo
        test_task3
        ;;
    *)
        echo -e "${CYAN}IoT Framework Test Script${NC}"
        echo
        echo "Usage: $0 [command]"
        echo
        echo "Commands:"
        echo -e "  ${GREEN}task1${NC}    - Test Task 1 (Data Simulation)"
        echo -e "  ${GREEN}task2${NC}    - Test Task 2 (Statistics)"
        echo -e "  ${GREEN}task3${NC}    - Test Task 3 (Automated Pipeline)"
        echo -e "  ${GREEN}deploy${NC}   - Deploy functions to Azure"
        echo -e "  ${GREEN}query${NC}    - Query database for verification"
        echo -e "  ${GREEN}status${NC}   - Check system status"
        echo -e "  ${GREEN}all${NC}      - Run all tests"
        echo
        print_info "Base URL: $BASE_URL"
        ;;
esac