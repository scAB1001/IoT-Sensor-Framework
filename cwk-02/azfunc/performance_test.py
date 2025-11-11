import requests
import time
import matplotlib.pyplot as plt
import json
import numpy as np
from datetime import datetime, timezone
import os

# Configuration
BASE_URL = "https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/api"
RESULTS_FILE = "performance_results.json"


def test_single_request(sensor_count):
    """Test a single request and return timing data"""
    try:
        start_time = time.time()
        response = requests.get(
            f"{BASE_URL}/simulate-data?sensor_count={sensor_count}", timeout=30)
        end_time = time.time()

        response_time = (end_time - start_time) * \
            1000  # Convert to milliseconds
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
            'response_time_ms': 30000,  # 30 seconds timeout
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
    """Test scalability with sequential requests"""
    print("🚀 Starting Sequential Scalability Test")
    print("=" * 50)

    # Test different sensor counts - starting small and scaling up
    sensor_counts = [1, 5, 10, 20, 50, 100, 200, 500]
    results = []

    for count in sensor_counts:
        print(f"Testing {count:3d} sensors...", end=" ", flush=True)

        result = test_single_request(count)
        results.append(result)

        if result['success']:
            print(f"✅ {result['response_time_ms']:6.1f} ms")
        else:
            print(f"❌ Failed: {result['db_status']}")

        # Small delay between requests to avoid overwhelming the service
        time.sleep(1)

    return results


def test_concurrent_load():
    import shutil
    import concurrent.futures
    """Test concurrent requests to measure parallel scalability"""
    print("\n🔥 Starting Concurrent Load Test")
    print("=" * 50)

    concurrent_requests = [1, 2, 5, 10]
    sensor_count = 20  # Fixed sensor count for concurrency test
    concurrency_results = []

    for num_requests in concurrent_requests:
        print(f"Testing {num_requests} concurrent requests...",
              end=" ", flush=True)

        start_time = time.time()
        successful_requests = 0
        total_response_time = 0

        # Use ThreadPoolExecutor for concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(test_single_request, sensor_count)
                       for _ in range(num_requests)]
            request_results = [future.result()
                               for future in concurrent.futures.as_completed(futures)]

        end_time = time.time()

        # Calculate metrics
        successful_requests = sum(1 for r in request_results if r['success'])
        total_response_time = sum(r['response_time_ms']
                                  for r in request_results if r['success'])
        avg_response_time = total_response_time / \
            successful_requests if successful_requests > 0 else 0
        total_time = (end_time - start_time) * 1000

        result = {
            'concurrent_requests': num_requests,
            'sensor_count_per_request': sensor_count,
            'successful_requests': successful_requests,
            'failed_requests': num_requests - successful_requests,
            'average_response_time_ms': avg_response_time,
            'total_execution_time_ms': total_time,
            'throughput_requests_per_sec': (num_requests / (total_time / 1000)) if total_time > 0 else 0
        }

        concurrency_results.append(result)
        print(
            f"✅ {successful_requests}/{num_requests} successful, Avg: {avg_response_time:.1f} ms")

    return concurrency_results


def generate_scalability_graphs(sequential_results, concurrency_results):
    """Generate comprehensive scalability graphs"""
    print("\n📊 Generating Scalability Graphs...")

    # Create results directory if it doesn't exist
    os.makedirs('performance_results', exist_ok=True)

    # Graph 1: Response Time vs Sensor Count
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    sensor_counts = [r['sensor_count'] for r in sequential_results]
    response_times = [r['response_time_ms'] for r in sequential_results]
    successes = [r['success'] for r in sequential_results]

    # Plot successful and failed requests with different colors
    success_counts = [sc for sc, success in zip(
        sensor_counts, successes) if success]
    success_times = [rt for rt, success in zip(
        response_times, successes) if success]
    fail_counts = [sc for sc, success in zip(
        sensor_counts, successes) if not success]
    fail_times = [rt for rt, success in zip(
        response_times, successes) if not success]

    plt.plot(success_counts, success_times, 'go-',
             linewidth=2, markersize=6, label='Successful')
    if fail_counts:
        plt.plot(fail_counts, fail_times, 'ro-',
                 linewidth=2, markersize=6, label='Failed')

    plt.title('Task 1: Response Time vs Sensor Count\n(Sequential Requests)')
    plt.xlabel('Number of Sensors')
    plt.ylabel('Response Time (ms)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.yscale('log')  # Log scale for better visualization of large ranges

    # Graph 2: Throughput vs Concurrent Requests
    plt.subplot(2, 2, 2)
    concurrent_reqs = [r['concurrent_requests'] for r in concurrency_results]
    throughput = [r['throughput_requests_per_sec']
                  for r in concurrency_results]

    plt.plot(concurrent_reqs, throughput, 'bo-', linewidth=2, markersize=6)
    plt.title('Throughput vs Concurrent Requests\n(20 sensors per request)')
    plt.xlabel('Number of Concurrent Requests')
    plt.ylabel('Throughput (requests/second)')
    plt.grid(True, alpha=0.3)

    # Graph 3: Average Response Time vs Concurrent Requests
    plt.subplot(2, 2, 3)
    avg_response_times = [r['average_response_time_ms']
                          for r in concurrency_results]

    plt.plot(concurrent_reqs, avg_response_times,
             'mo-', linewidth=2, markersize=6)
    plt.title('Average Response Time vs Concurrent Requests')
    plt.xlabel('Number of Concurrent Requests')
    plt.ylabel('Average Response Time (ms)')
    plt.grid(True, alpha=0.3)

    # Graph 4: Success Rate
    plt.subplot(2, 2, 4)
    success_rates = [(r['successful_requests'] / r['concurrent_requests'] * 100)
                     for r in concurrency_results]

    plt.bar(concurrent_reqs, success_rates, color='lightgreen', alpha=0.7)
    plt.title('Success Rate vs Concurrent Requests')
    plt.xlabel('Number of Concurrent Requests')
    plt.ylabel('Success Rate (%)')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 105)

    # Add value labels on bars
    for i, v in enumerate(success_rates):
        plt.text(concurrent_reqs[i], v + 2,
                 f'{v:.1f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('performance_results/scalability_analysis.png',
                dpi=300, bbox_inches='tight')
    plt.show()

    # Save detailed results
    results_data = {
        'test_timestamp': datetime.now(timezone.utc).isoformat(),
        'base_url': BASE_URL,
        'sequential_results': sequential_results,
        'concurrency_results': concurrency_results
    }

    with open(f'performance_results/{RESULTS_FILE}', 'w') as f:
        json.dump(results_data, f, indent=2)

    print("✅ Graphs saved to 'performance_results/' directory")


def print_summary(sequential_results, concurrency_results):
    """Print a comprehensive test summary"""
    print("\n" + "="*60)
    print("📈 PERFORMANCE TEST SUMMARY")
    print("="*60)

    # Sequential test summary
    successful_sequential = [r for r in sequential_results if r['success']]
    if successful_sequential:
        max_sensors = max(r['sensor_count'] for r in successful_sequential)
        avg_response_time = np.mean(
            [r['response_time_ms'] for r in successful_sequential])
        print(f"Sequential Tests:")
        print(f"  • Maximum successful sensor count: {max_sensors}")
        print(f"  • Average response time: {avg_response_time:.1f} ms")
        print(
            f"  • Success rate: {len(successful_sequential)}/{len(sequential_results)} requests")

    # Concurrency test summary
    if concurrency_results:
        max_concurrent = max(r['concurrent_requests']
                             for r in concurrency_results)
        max_throughput = max(r['throughput_requests_per_sec']
                             for r in concurrency_results)
        print(f"Concurrent Tests:")
        print(f"  • Maximum concurrent requests tested: {max_concurrent}")
        print(f"  • Peak throughput: {max_throughput:.1f} requests/second")
        print(
            f"  • Best success rate: {max([r['successful_requests']/r['concurrent_requests']*100 for r in concurrency_results]):.1f}%")

    print(f"\n📁 Results saved to: performance_results/")
    print("="*60)


def main():
    """Main function to run all performance tests"""
    print("Azure Functions Performance Test - Task 1 Scalability")
    print(f"Target URL: {BASE_URL}")
    print()

    try:
        # Run sequential scalability test
        sequential_results = test_scalability_sequential()

        # Run concurrent load test
        concurrency_results = test_concurrent_load()

        # Generate graphs and save results
        generate_scalability_graphs(sequential_results, concurrency_results)

        # Print summary
        print_summary(sequential_results, concurrency_results)

    except KeyboardInterrupt:
        print("\n❌ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")


if __name__ == "__main__":
    main()
