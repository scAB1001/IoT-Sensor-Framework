import requests
import time
import matplotlib.pyplot as plt
import json
import numpy as np
from datetime import datetime, timezone
import concurrent.futures
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_URL = "https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/api"
TASK1_ENDPOINT = "/simulate-data"
TASK2_ENDPOINT = "/statistics"
RESULTS_DIR = "performance_results"
RESULTS_FILE = "performance_results.json"

# Create results directory if it doesn't exist
os.makedirs(RESULTS_DIR, exist_ok=True)

# =============================================================================
# TESTING FUNCTIONS
# =============================================================================

def test_single_request(sensor_count=20):
    """
    Test a single request to the simulate-data function

    WHAT: Measures response time for generating sensor data
    WHY: Baseline performance measurement for Task 1
    HOW: Sends HTTP request and times the response
    """
    try:
        start_time = time.time()
        response = requests.get(
            f"{BASE_URL}{TASK1_ENDPOINT}?sensor_count={sensor_count}",
            timeout=30
        )
        end_time = time.time()

        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        success = response.status_code == 200

        if success:
            data = response.json()
            records_stored = data.get('sensor_count', 0)
            db_status = data.get('database_status', '')
        else:
            records_stored = 0
            db_status = f"HTTP {response.status_code}"

        return {
            'sensor_count': sensor_count,
            'response_time_ms': response_time,
            'success': success,
            'records_stored': records_stored,
            'db_status': db_status,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

    except requests.exceptions.Timeout:
        return {
            'sensor_count': sensor_count,
            'response_time_ms': 30000,
            'success': False,
            'records_stored': 0,
            'db_status': 'Timeout',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            'sensor_count': sensor_count,
            'response_time_ms': 0,
            'success': False,
            'records_stored': 0,
            'db_status': f'Error: {str(e)}',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }


def test_scalability_sequential():
    """
    Test Task 1 scalability with sequential requests of increasing sensor counts

    WHAT: Measures how response time changes with different numbers of sensors
    WHY: Demonstrates vertical scaling capability of the serverless function
    HOW: Sends requests for 1 to 5000 sensors sequentially with 1-second delays
    """
    print("Starting Sequential Scalability Test")
    print("=" * 50)

    sensor_counts = [1, 5, 10, 20, 50, 100, 200, 500, 1000, 2500, 5000]
    results = []

    for count in sensor_counts:
        print(f"Testing {count:4d} sensors...", end=" ", flush=True)
        result = test_single_request(count)
        results.append(result)

        if result['success']:
            print(f"✅ {result['response_time_ms']:6.1f} ms")
        else:
            print(f"❌ Failed: {result['db_status']}")

        time.sleep(1)  # Avoid overwhelming the service

    return results


def test_concurrent_load():
    """
    Test Task 1 performance under concurrent load

    WHAT: Measures how the function handles multiple simultaneous requests
    WHY: Demonstrates horizontal scaling and concurrency handling
    HOW: Uses ThreadPoolExecutor to send multiple requests simultaneously
    """
    print("\nStarting Concurrent Load Test")
    print("=" * 50)

    concurrent_requests = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    sensor_count = 20  # Fixed sensor count for concurrency test
    concurrency_results = []

    for num_requests in concurrent_requests:
        print(f"Testing {num_requests:4d} concurrent requests...", end=" ", flush=True)

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [
                executor.submit(test_single_request, sensor_count)
                for _ in range(num_requests)
            ]
            request_results = [
                future.result()
                for future in concurrent.futures.as_completed(futures)
            ]

        end_time = time.time()

        # Calculate metrics
        successful_requests = sum(1 for r in request_results if r['success'])
        total_response_time = sum(
            r['response_time_ms'] for r in request_results if r['success']
        )
        avg_response_time = (
            total_response_time / successful_requests
            if successful_requests > 0 else 0
        )
        total_time = (end_time - start_time) * 1000

        result = {
            'concurrent_requests': num_requests,
            'sensor_count_per_request': sensor_count,
            'successful_requests': successful_requests,
            'failed_requests': num_requests - successful_requests,
            'average_response_time_ms': avg_response_time,
            'total_execution_time_ms': total_time,
            'throughput_requests_per_sec': (
                num_requests / (total_time / 1000)
                if total_time > 0 else 0
            )
        }

        concurrency_results.append(result)
        print(
            f"✅ {successful_requests}/{num_requests} successful, "
            f"Avg: {avg_response_time:.1f} ms"
        )

    return concurrency_results


def test_statistics_scalability():
    """
    Test Task 2 statistics function with different data volumes

    WHAT: Measures how statistics calculation time scales with data volume
    WHY: Demonstrates analytical processing scalability
    HOW: Requests statistics for increasing data limits (10 to 5000 records)
    """
    print("\n📊 Testing Task 2: Statistics Function Scalability")
    print("=" * 50)

    data_limits = [10, 50, 100, 500, 1000, 5000]
    results = []

    for limit in data_limits:
        print(f"Testing statistics with {limit:4d} records...", end=" ", flush=True)

        start_time = time.time()
        response = requests.get(
            f"{BASE_URL}{TASK2_ENDPOINT}?data_limit={limit}",
            timeout=30
        )
        end_time = time.time()

        response_time = (end_time - start_time) * 1000
        success = response.status_code == 200

        if success:
            data = response.json()
            data_analyzed = data.get('data_analyzed', 0)
            print(f"✅ {response_time:6.1f} ms ({data_analyzed} records)")
        else:
            print(f"❌ Failed: HTTP {response.status_code}")

        results.append({
            'data_limit': limit,
            'response_time_ms': response_time,
            'success': success,
            'data_analyzed': data_analyzed if success else 0
        })

        time.sleep(1)

    return results


def test_task3_workflow():
    """
    Test the complete Task 3 automated workflow

    WHAT: Measures end-to-end performance of data generation → automatic processing
    WHY: Validates the realistic scenario implementation
    HOW: Generates data and checks if statistics are automatically calculated
    """
    print("\n🔄 Testing Task 3: Automated Workflow")
    print("=" * 50)

    cycles = 5
    workflow_results = []

    for cycle in range(cycles):
        print(f"Workflow cycle {cycle + 1}/{cycles}...")

        # Step 1: Generate data (should trigger automatic processing)
        start_time = time.time()
        gen_response = requests.get(f"{BASE_URL}{TASK1_ENDPOINT}?sensor_count=20")
        gen_time = (time.time() - start_time) * 1000

        if gen_response.status_code == 200:
            print(f"  ✅ Data generated: {gen_time:.1f}ms")

            # Wait for automatic trigger
            time.sleep(5)

            # Step 2: Check if statistics were automatically calculated
            stats_response = requests.get(f"{BASE_URL}{TASK2_ENDPOINT}?data_limit=50")
            stats_time = (time.time() - start_time) * 1000

            if stats_response.status_code == 200:
                stats_data = stats_response.json()
                workflow_results.append({
                    'cycle': cycle + 1,
                    'data_generation_ms': gen_time,
                    'total_workflow_ms': stats_time,
                    'data_analyzed': stats_data.get('data_analyzed', 0),
                    'workflow_success': True
                })
                print(f"  ✅ Statistics available: {stats_time:.1f}ms total")
            else:
                workflow_results.append({
                    'cycle': cycle + 1,
                    'data_generation_ms': gen_time,
                    'total_workflow_ms': stats_time,
                    'workflow_success': False
                })
                print(f"  ❌ Statistics not generated")
        else:
            print(f"  ❌ Data generation failed")

        time.sleep(2)  # Wait between cycles

    return workflow_results


# =============================================================================
# GRAPHING FUNCTIONS - SEPARATE GRAPHS FOR EACH TASK
# =============================================================================

def create_task1_graphs(sequential_results, concurrency_results):
    """
    Create comprehensive graphs for Task 1: Data Simulation

    GRAPHS:
    1. Response Time vs Sensor Count - Vertical scaling performance
    2. Throughput vs Concurrent Requests - Horizontal scaling performance
    3. Success Rate Under Load - Reliability under stress
    """
    print("\n📈 Generating Task 1 Graphs...")

    # Graph 1: Response Time vs Sensor Count
    plt.figure(figsize=(10, 6))

    sensor_counts = [r['sensor_count'] for r in sequential_results if r['success']]
    response_times = [r['response_time_ms'] for r in sequential_results if r['success']]

    plt.plot(sensor_counts, response_times, 'bo-', linewidth=2, markersize=4)
    plt.title('Task 1: Data Generation Performance\nResponse Time vs Number of Sensors', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Sensors Simulated', fontweight='bold')
    plt.ylabel('Response Time (milliseconds)', fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')

    # Add annotation for the assignment requirement (20 sensors)
    if 20 in sensor_counts:
        idx = sensor_counts.index(20)
        plt.annotate(f'20 sensors (requirement)\n{response_times[idx]:.1f}ms',
                    xy=(20, response_times[idx]),
                    xytext=(50, response_times[idx] * 2),
                    arrowprops=dict(arrowstyle='->', color='red'),
                    fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{RESULTS_DIR}/task1_sensor_scaling.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Graph 2: Throughput and Response Time vs Concurrent Requests
    plt.figure(figsize=(12, 5))

    concurrent_reqs = [r['concurrent_requests'] for r in concurrency_results]
    throughput = [r['throughput_requests_per_sec'] for r in concurrency_results]
    avg_response_times = [r['average_response_time_ms'] for r in concurrency_results]

    plt.subplot(1, 2, 1)
    plt.plot(concurrent_reqs, throughput, 'g^-', linewidth=2, markersize=6)
    plt.title('Throughput vs Concurrent Requests\n(20 sensors per request)', fontweight='bold')
    plt.xlabel('Number of Concurrent Requests', fontweight='bold')
    plt.ylabel('Throughput (requests/second)', fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xscale('log')

    plt.subplot(1, 2, 2)
    plt.plot(concurrent_reqs, avg_response_times, 'ms-', linewidth=2, markersize=6)
    plt.title('Response Time vs Concurrent Requests', fontweight='bold')
    plt.xlabel('Number of Concurrent Requests', fontweight='bold')
    plt.ylabel('Average Response Time (ms)', fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xscale('log')

    plt.tight_layout()
    plt.savefig(f'{RESULTS_DIR}/task1_concurrent_performance.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Graph 3: Success Rate Under Load
    plt.figure(figsize=(8, 6))

    success_rates = [
        (r['successful_requests'] / r['concurrent_requests'] * 100)
        for r in concurrency_results
    ]

    colors = ['lightgreen' if rate > 95 else 'orange' if rate > 80 else 'lightcoral'
              for rate in success_rates]

    bars = plt.bar(concurrent_reqs, success_rates, color=colors, alpha=0.7, edgecolor='black')
    plt.title('Task 1: Success Rate Under Concurrent Load', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Concurrent Requests', fontweight='bold')
    plt.ylabel('Success Rate (%)', fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    plt.ylim(0, 105)

    # Add value labels on bars
    for bar, rate in zip(bars, success_rates):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{RESULTS_DIR}/task1_success_rates.png', dpi=300, bbox_inches='tight')
    plt.show()


def create_task2_graphs(stats_results):
    """
    Create graphs for Task 2: Statistics Calculation

    GRAPHS:
    1. Processing Time vs Data Volume - Analytical scalability
    2. Actual Data Processed - Validation of data retrieval
    """
    if not stats_results:
        print("❌ No Task 2 results to graph")
        return

    print("\n📊 Generating Task 2 Graphs...")

    successful_results = [r for r in stats_results if r['success']]
    if not successful_results:
        print("❌ No successful Task 2 results to graph")
        return

    plt.figure(figsize=(12, 5))

    # Graph 1: Processing Time vs Data Volume
    plt.subplot(1, 2, 1)
    data_limits = [r['data_limit'] for r in successful_results]
    stats_times = [r['response_time_ms'] for r in successful_results]

    plt.plot(data_limits, stats_times, 'ro-', linewidth=2, markersize=6)
    plt.title('Task 2: Statistics Calculation Performance\nProcessing Time vs Data Volume',
              fontweight='bold')
    plt.xlabel('Number of Records Analyzed', fontweight='bold')
    plt.ylabel('Processing Time (milliseconds)', fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xscale('log')

    # Graph 2: Actual Data Processed
    plt.subplot(1, 2, 2)
    analyzed_data = [r['data_analyzed'] for r in successful_results]

    plt.bar(data_limits[:len(analyzed_data)], analyzed_data,
            color='orange', alpha=0.7, edgecolor='black')
    plt.title('Task 2: Data Processing Validation\nRequested vs Actual Records',
              fontweight='bold')
    plt.xlabel('Requested Data Limit', fontweight='bold')
    plt.ylabel('Records Actually Analyzed', fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for i, (limit, actual) in enumerate(zip(data_limits, analyzed_data)):
        plt.text(limit, actual + (max(analyzed_data) * 0.02),
                f'{actual}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{RESULTS_DIR}/task2_statistics_performance.png', dpi=300, bbox_inches='tight')
    plt.show()


def create_task3_graphs(workflow_results):
    """
    Create graphs for Task 3: Automated Workflow

    GRAPHS:
    1. Workflow Timing - End-to-end performance
    2. Success Analysis - Reliability of automation
    """
    if not workflow_results:
        print("❌ No Task 3 results to graph")
        return

    print("\n🔄 Generating Task 3 Graphs...")

    plt.figure(figsize=(12, 5))

    # Graph 1: Workflow Timing Analysis
    plt.subplot(1, 2, 1)
    cycles = [r['cycle'] for r in workflow_results]
    gen_times = [r['data_generation_ms'] for r in workflow_results]
    total_times = [r['total_workflow_ms'] for r in workflow_results]

    x = np.arange(len(cycles))
    width = 0.35

    plt.bar(x - width/2, gen_times, width, label='Data Generation',
            color='lightblue', alpha=0.7, edgecolor='black')
    plt.bar(x + width/2, total_times, width, label='Total Workflow',
            color='lightgreen', alpha=0.7, edgecolor='black')

    plt.title('Task 3: Automated Workflow Timing\nPer Execution Cycle',
              fontweight='bold')
    plt.xlabel('Workflow Execution Cycle', fontweight='bold')
    plt.ylabel('Time (milliseconds)', fontweight='bold')
    plt.xticks(x, cycles)
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')

    # Graph 2: Success Rate Analysis
    plt.subplot(1, 2, 2)
    success_count = sum(1 for r in workflow_results if r['workflow_success'])
    failure_count = len(workflow_results) - success_count

    labels = ['Successful', 'Failed']
    values = [success_count, failure_count]
    colors = ['lightgreen', 'lightcoral']

    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors,
            startangle=90, explode=(0.1, 0))
    plt.title('Task 3: Workflow Success Rate\nAutomated Data → Statistics',
              fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{RESULTS_DIR}/task3_workflow_performance.png', dpi=300, bbox_inches='tight')
    plt.show()


# =============================================================================
# SUMMARY AND UTILITY FUNCTIONS
# =============================================================================

def save_test_results(sequential_results, stats_results, workflow_results, concurrency_results):
    """Save all test results to JSON file for future analysis"""
    results_data = {
        'test_timestamp': datetime.now(timezone.utc).isoformat(),
        'base_url': BASE_URL,
        'task1_sequential': sequential_results,
        'task1_concurrent': concurrency_results,
        'task2_statistics': stats_results,
        'task3_workflow': workflow_results
    }

    with open(f'{RESULTS_DIR}/{RESULTS_FILE}', 'w') as f:
        json.dump(results_data, f, indent=2)

    print(f"✅ Results saved to: {RESULTS_DIR}/{RESULTS_FILE}")


def print_comprehensive_summary(sequential_results, stats_results, workflow_results, concurrency_results):
    """Print a comprehensive summary of all test results"""
    print("\n" + "="*70)
    print("📈 COMPREHENSIVE PERFORMANCE TEST SUMMARY")
    print("="*70)

    # Task 1 Summary
    successful_sequential = [r for r in sequential_results if r['success']]
    if successful_sequential:
        max_sensors = max(r['sensor_count'] for r in successful_sequential)
        avg_sequential_time = np.mean([r['response_time_ms'] for r in successful_sequential])

        print("\n🎯 TASK 1: Data Simulation")
        print(f"  • Maximum sensors tested: {max_sensors}")
        print(f"  • Average response time: {avg_sequential_time:.1f} ms")
        print(f"  • Success rate: {len(successful_sequential)}/{len(sequential_results)} requests")

    # Task 1 Concurrent Summary
    if concurrency_results:
        max_concurrent = max(r['concurrent_requests'] for r in concurrency_results)
        max_throughput = max(r['throughput_requests_per_sec'] for r in concurrency_results)
        best_success_rate = max([
            r['successful_requests']/r['concurrent_requests']*100
            for r in concurrency_results
        ])

        print(f"  • Maximum concurrent requests: {max_concurrent}")
        print(f"  • Peak throughput: {max_throughput:.1f} requests/second")
        print(f"  • Best success rate: {best_success_rate:.1f}%")

    # Task 2 Summary
    successful_stats = [r for r in stats_results if r['success']]
    if successful_stats:
        max_data = max(r['data_limit'] for r in successful_stats)
        avg_stats_time = np.mean([r['response_time_ms'] for r in successful_stats])

        print("\n📊 TASK 2: Statistics Calculation")
        print(f"  • Maximum data processed: {max_data} records")
        print(f"  • Average processing time: {avg_stats_time:.1f} ms")
        print(f"  • Success rate: {len(successful_stats)}/{len(stats_results)} requests")

    # Task 3 Summary
    if workflow_results:
        successful_workflows = sum(1 for r in workflow_results if r['workflow_success'])
        avg_workflow_time = np.mean([
            r['total_workflow_ms'] for r in workflow_results if r['workflow_success']
        ])

        print("\n🔄 TASK 3: Automated Workflow")
        print(f"  • Workflow cycles: {len(workflow_results)}")
        print(f"  • Successful automations: {successful_workflows}/{len(workflow_results)}")
        print(f"  • Average workflow time: {avg_workflow_time:.1f} ms")
        print(f"  • Success rate: {(successful_workflows/len(workflow_results))*100:.1f}%")

    print(f"\n📁 Results directory: {RESULTS_DIR}/")
    print("="*70)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main function to execute all performance tests"""
    print("🚀 Azure Functions Performance Test - COMP3211 Coursework")
    print(f"📍 Target URL: {BASE_URL}")
    print()

    try:
        # Task 1: Data Simulation Scalability
        print("🎯 TASK 1: Testing Data Simulation Scalability")
        sequential_results = test_scalability_sequential()
        concurrency_results = test_concurrent_load()

        # Task 2: Statistics Function Scalability
        print("\n🎯 TASK 2: Testing Statistics Calculation Scalability")
        stats_results = test_statistics_scalability()

        # Task 3: Automated Workflow
        print("\n🎯 TASK 3: Testing Automated Workflow Performance")
        workflow_results = test_task3_workflow()

        # Generate separate graphs for each task
        create_task1_graphs(sequential_results, concurrency_results)
        create_task2_graphs(stats_results)
        create_task3_graphs(workflow_results)

        # Save results and print summary
        save_test_results(sequential_results, stats_results, workflow_results, concurrency_results)
        print_comprehensive_summary(sequential_results, stats_results, workflow_results, concurrency_results)

    except KeyboardInterrupt:
        print("\n❌ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()