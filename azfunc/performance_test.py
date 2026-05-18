import requests
import time
import matplotlib.pyplot as plt
import numpy as np
import concurrent.futures
import os

# Configuration
BASE_URL = "https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/api"
RESULTS_DIR = "performance_results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def test_single_request(endpoint, params=None):
    """Generic function to test a single request"""
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=30)
        end_time = time.time()

        return {
            'response_time_ms': (end_time - start_time) * 1000,
            'success': response.status_code == 200,
            'data': response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        return {'response_time_ms': 0, 'success': False, 'error': str(e)}

def test_task1_scalability():
    """Task 1: Two scalability tests for data generation"""
    print("Testing Task 1: Data Generation Scalability")

    # Test 1: Vertical scaling (sensor count)
    print("1. Vertical Scaling: Sensor Count Impact")
    sensor_counts = [1, 5, 20, 50, 100, 150, 200, 250, 500, 750, 1000]
    vertical_results = []

    for count in sensor_counts:
        result = test_single_request("/simulate-data", {"sensor_count": count})
        vertical_results.append({
            'sensor_count': count,
            'response_time': result['response_time_ms'],
            'success': result['success']
        })
        print(f"  {count} sensors: {result['response_time_ms']:.1f}ms")
        time.sleep(0.5)

    # Test 2: Horizontal scaling (concurrent requests)
    print("2. Horizontal Scaling: Concurrent Load")
    concurrent_levels = [1, 2, 5, 10, 20, 50, 100, 150, 250, 500, 1000]
    concurrency_results = []

    for num_requests in concurrent_levels:
        start_time = time.time()
        successful = 0
        total_time = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(test_single_request, "/simulate-data", {"sensor_count": 20})
                      for _ in range(num_requests)]

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result['success']:
                    successful += 1
                    total_time += result['response_time_ms']

        avg_time = total_time / successful if successful > 0 else 0
        throughput = successful / ((time.time() - start_time) or 1)

        concurrency_results.append({
            'concurrent_requests': num_requests,
            'success_rate': (successful / num_requests) * 100,
            'avg_response_time': avg_time,
            'throughput': throughput
        })
        print(f"  {num_requests} concurrent: {successful}/{num_requests} successful, {avg_time:.1f}ms avg")

    return vertical_results, concurrency_results

def test_task2_scalability():
    """Task 2: Two scalability tests for statistics calculation"""
    print("Testing Task 2: Statistics Calculation Scalability")

    # Test 1: Data volume impact
    print("1. Data Volume Impact")
    data_limits = [1, 10, 50, 100, 250, 500, 1000, 2500, 5000]
    volume_results = []

    for limit in data_limits:
        result = test_single_request("/statistics", {"data_limit": limit})
        data_analyzed = result['data'].get('data_analyzed', 0) if result['data'] else 0
        volume_results.append({
            'data_limit': limit,
            'response_time': result['response_time_ms'],
            'data_analyzed': data_analyzed,
            'success': result['success']
        })
        print(f"  {limit} records: {result['response_time_ms']:.1f}ms ({data_analyzed} analyzed)")
        time.sleep(0.5)

    # Test 2: Concurrent statistics requests
    print("2. Concurrent Statistics Requests")
    concurrent_levels = [1, 2, 5, 10, 20, 50, 100, 150, 250, 500, 1000]
    stats_concurrency_results = []

    for num_requests in concurrent_levels:
        start_time = time.time()
        successful = 0
        total_time = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(test_single_request, "/statistics", {"data_limit": 100})
                      for _ in range(num_requests)]

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result['success']:
                    successful += 1
                    total_time += result['response_time_ms']

        avg_time = total_time / successful if successful > 0 else 0

        stats_concurrency_results.append({
            'concurrent_requests': num_requests,
            'success_rate': (successful / num_requests) * 100,
            'avg_response_time': avg_time
        })
        print(f"  {num_requests} concurrent: {successful}/{num_requests} successful, {avg_time:.1f}ms avg")

    return volume_results, stats_concurrency_results

def test_task3_workflow():
    """Task 3: Two tests for automated workflow"""
    print("Testing Task 3: Automated Workflow Performance")

    # Test 1: Workflow timing analysis
    print("1. Workflow Timing Analysis")
    workflow_timings = []
    sensor_counts = [1, 5, 20, 50, 100, 150, 200, 250, 500, 750, 1000]  # Test different loads

    for count in sensor_counts:
        # Time data generation
        gen_start = time.time()
        gen_result = test_single_request("/simulate-data", {"sensor_count": count})
        gen_time = (time.time() - gen_start) * 1000

        if gen_result['success']:
            # Wait for automatic processing
            time.sleep(5)

            # Check if statistics are available
            stats_result = test_single_request("/statistics", {"data_limit": 100})

            workflow_timings.append({
                'sensor_count': count,
                'data_generation_time': gen_time,
                'stats_available': stats_result['success'],
                'total_time': gen_time + 5000  # Include wait time
            })
            print(f"  {count} sensors: {gen_time:.1f}ms generation, stats available: {stats_result['success']}")
        else:
            print(f"  {count} sensors: Generation failed")

        time.sleep(2)

    # Test 2: Workflow reliability
    print("2. Workflow Reliability")
    reliability_results = []
    cycles = 10

    successful_workflows = 0
    for cycle in range(cycles):
        # Generate data
        gen_result = test_single_request("/simulate-data", {"sensor_count": 20})

        if gen_result['success']:
            # Wait for automation
            time.sleep(5)

            # Verify statistics were generated
            stats_result = test_single_request("/statistics", {"data_limit": 50})
            workflow_success = stats_result['success']

            if workflow_success:
                successful_workflows += 1

            reliability_results.append({
                'cycle': cycle + 1,
                'success': workflow_success
            })

        time.sleep(1)

    reliability_rate = (successful_workflows / cycles) * 100
    print(f"  Workflow success rate: {reliability_rate:.1f}% ({successful_workflows}/{cycles})")

    return workflow_timings, reliability_results, reliability_rate

def create_consolidated_graphs(task1_results, task2_results, task3_results):
    """Create 3 consolidated graphs with 2 subplots each"""

    # Extract results
    vertical_results, concurrency_results = task1_results
    volume_results, stats_concurrency_results = task2_results
    workflow_timings, reliability_results, reliability_rate = task3_results

    # Graph 1: Task 1 - Data Generation Scalability
    plt.figure(figsize=(15, 5))

    # Subplot 1: Vertical Scaling
    plt.subplot(1, 2, 1)
    sensor_counts = [r['sensor_count'] for r in vertical_results if r['success']]
    response_times = [r['response_time'] for r in vertical_results if r['success']]

    plt.plot(sensor_counts, response_times, 'bo-', linewidth=2, markersize=6)
    plt.title('Task 1: Response Time vs Sensor Count', fontweight='bold', fontsize=12)
    plt.xlabel('Number of Sensors', fontweight='bold')
    plt.ylabel('Response Time (ms)', fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xscale('log')

    # Highlight assignment requirement
    if 20 in sensor_counts:
        idx = sensor_counts.index(20)
        plt.annotate(f'20 sensors\n{response_times[idx]:.1f}ms',
                    xy=(20, response_times[idx]), xytext=(50, response_times[idx] * 1.5),
                    arrowprops=dict(arrowstyle='->', color='red'),
                    fontweight='bold', ha='center')

    # Subplot 2: Horizontal Scaling
    plt.subplot(1, 2, 2)
    concurrent_reqs = [r['concurrent_requests'] for r in concurrency_results]
    throughput = [r['throughput'] for r in concurrency_results]
    success_rates = [r['success_rate'] for r in concurrency_results]

    plt.plot(concurrent_reqs, throughput, 'g^-', linewidth=2, markersize=6, label='Throughput')
    plt.plot(concurrent_reqs, success_rates, 'ro-', linewidth=2, markersize=6, label='Success Rate')
    plt.title('Task 1: Concurrent Performance', fontweight='bold', fontsize=12)
    plt.xlabel('Concurrent Requests', fontweight='bold')
    plt.ylabel('Throughput (req/s) / Success Rate (%)', fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xscale('log')

    plt.tight_layout()
    plt.savefig(f'{RESULTS_DIR}/task1_consolidated.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Graph 2: Task 2 - Statistics Calculation Scalability
    plt.figure(figsize=(15, 5))

    # Subplot 1: Data Volume Impact
    plt.subplot(1, 2, 1)
    data_limits = [r['data_limit'] for r in volume_results if r['success']]
    stats_times = [r['response_time'] for r in volume_results if r['success']]

    plt.plot(data_limits, stats_times, 'mo-', linewidth=2, markersize=6)
    plt.title('Task 2: Processing Time vs Data Volume', fontweight='bold', fontsize=12)
    plt.xlabel('Number of Records', fontweight='bold')
    plt.ylabel('Processing Time (ms)', fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xscale('log')

    # Subplot 2: Concurrent Statistics
    plt.subplot(1, 2, 2)
    stats_concurrent = [r['concurrent_requests'] for r in stats_concurrency_results]
    stats_response_times = [r['avg_response_time'] for r in stats_concurrency_results]
    stats_success = [r['success_rate'] for r in stats_concurrency_results]

    plt.plot(stats_concurrent, stats_response_times, 'co-', linewidth=2, markersize=6, label='Response Time')
    plt.plot(stats_concurrent, stats_success, 'yo-', linewidth=2, markersize=6, label='Success Rate')
    plt.title('Task 2: Concurrent Statistics Performance', fontweight='bold', fontsize=12)
    plt.xlabel('Concurrent Requests', fontweight='bold')
    plt.ylabel('Response Time (ms) / Success Rate (%)', fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'{RESULTS_DIR}/task2_consolidated.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Graph 3: Task 3 - Automated Workflow
    plt.figure(figsize=(15, 5))

    # Subplot 1: Workflow Timing
    plt.subplot(1, 2, 1)
    sensor_counts_wf = [r['sensor_count'] for r in workflow_timings]
    gen_times = [r['data_generation_time'] for r in workflow_timings]

    plt.bar(sensor_counts_wf, gen_times, color='lightblue', alpha=0.7, edgecolor='black')
    plt.title('Task 3: Data Generation Time by Load', fontweight='bold', fontsize=12)
    plt.xlabel('Number of Sensors', fontweight='bold')
    plt.ylabel('Generation Time (ms)', fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for i, (count, time_val) in enumerate(zip(sensor_counts_wf, gen_times)):
        plt.text(count, time_val + (max(gen_times) * 0.05), f'{time_val:.0f}ms',
                ha='center', va='bottom', fontweight='bold')

    # Subplot 2: Workflow Reliability
    plt.subplot(1, 2, 2)
    labels = ['Successful', 'Failed']
    success_count = sum(1 for r in reliability_results if r['success'])
    failure_count = len(reliability_results) - success_count
    sizes = [success_count, failure_count]
    colors = ['lightgreen', 'lightcoral']

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors,
            startangle=90, explode=(0.1, 0))
    plt.title(f'Task 3: Workflow Reliability\n({reliability_rate:.1f}% Success Rate)',
              fontweight='bold', fontsize=12)

    plt.tight_layout()
    plt.savefig(f'{RESULTS_DIR}/task3_consolidated.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Main execution function"""
    print("COMP3211 Scalability Testing - Consolidated Analysis")
    print("=" * 60)

    try:
        # Run all tests
        task1_results = test_task1_scalability()
        print()

        task2_results = test_task2_scalability()
        print()

        task3_results = test_task3_workflow()
        print()

        # Generate consolidated graphs
        create_consolidated_graphs(task1_results, task2_results, task3_results)

        print("Testing completed successfully!")
        print(f"Graphs saved to: {RESULTS_DIR}/")

    except Exception as e:
        print(f"Testing failed: {str(e)}")

if __name__ == "__main__":
    main()