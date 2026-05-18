#!/bin/bash

# Run `chmod +x ./build.sh` to make this file executable

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
    print_header "Checking Java Dependencies"
    if ! command -v javac &> /dev/null
    then
        print_error "javac could not be found. Please install JDK to proceed."
        exit
    else
        print_success "javac found:"
        print_indent "$(javac --version)"
    fi

    if ! command -v java &> /dev/null
    then
        print_error "java could not be found. Please install JDK to proceed."
        exit
    else
        print_success "java found:"
        print_indent "$(java --version)"
    fi

    jdbc_path=$(find . -name "*jre11.jar" -type f | head -n1)
    if [ -z "$jdbc_path" ]; then
        print_error "JDBC Driver not found. Please ensure the path is correct."
        exit 1
    else
        JDBC_JAR="$jdbc_path"
        JDBC_DIR=$(dirname "$jdbc_path")
        print_success "JDBC Driver found at $JDBC_JAR"
        print_info "Located in directory: $JDBC_DIR"
    fi
}


compile_all() {
    print_info "Compiling all Java files..."
    javac -cp ".:$JDBC_JAR" *.java

    # Verify compilation
    if [ $? -eq 0 ]; then
        print_success "Compilation successful"
    else
        print_error "Compilation failed"
        exit 1
    fi
}

compile_specific() {
    local file="$1"
    print_info "Compiling $file..."
    javac -cp ".:$JDBC_JAR" $file

    # Verify compilation
    if [ $? -eq 0 ]; then
        print_success "Compilation successful"
    else
        print_error "Compilation failed"
        exit 1
    fi
}

execute() {
    # Convert .java to class name by removing .java
    local file="$1"
    class_name="${file%.java}"
    print_info "Executing: $class_name"

    java "$class_name"
    # Verify execution
    if [ $? -eq 0 ]; then
        print_success "Execution of $class_name successful"
    else
        print_error "Execution of $class_name failed"
        exit 1
    fi
}

show_usage() {
    echo -e "${CYAN}Usage: $0 [command] [filename]${NC}"
    echo ""
    echo -e "${BLUE}Commands:${NC}"
    echo "  check, ch                           - Check for required dependencies"
    echo "  clean, cl                           - Delete all .class files"
    echo "  compile, comp                       - Compile all Java files"
    echo "  compile [filename]                  - Compile specific Java file"
    echo "  all                                 - Clean and compile all files"
    echo "  execute, exec [file]                - Compile and execute specific Java file"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo "  $0 check"
    echo "  $0 clean"
    echo "  $0 compile"
    echo "  $0 compile CreateDB.java"
    echo "  $0 all"
    echo "  $0 exec CreateDB.java"
}


case "$1" in
    "ch"|"check")
        check
        ;;
    "cl"|"clean")
        print_header "Cleaning previous build"
        find . -name "*.class" -delete 2>/dev/null
        print_success "Cleaned previous build"
        ;;
    "comp"|"compile")
        print_header "Compiling Java source files"
        if [ -n "$2" ]; then
            compile_specific "$2"
        else
            compile_all
        fi
        ;;
    "all")
        print_header "Full Build: Clean and Compile"
        compile_all
        ;;
    "exec"|"execute")
        if [ -n "$2" ]; then
            print_header "Building and Executing $2"
            compile_specific "$2"

            if [ $? -eq 0 ]; then
                execute "$2"
            else
                print_error "Compilation failed"
                exit 1
            fi

        else
            print_warning "No files specified to run."
            show_usage
            exit 1
        fi
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
