# performance_test.py
import requests
import time
import matplotlib.pyplot as plt
import concurrent.futures


def test_scalability():
    base_url = "http://localhost:5007/api/sensors"
    sensor_counts = [1, 50, 250, 500, 750, 1000, 1500, 2000, 2500, 3000, 4000, 5000]
    response_times = []

    for count in sensor_counts:
        start_time = time.time()
        response = requests.get(f"{base_url}/{count}")
        end_time = time.time()

        response_time = (end_time - start_time) * 1000
        response_times.append(response_time)
        print(f"Sensors: {count}, Response Time: {response_time:.2f}ms")

    # Generate graph
    plt.figure(figsize=(10, 6))
    plt.plot(sensor_counts, response_times, 'bo-')
    plt.title('Azure Function Scalability: Response Time vs Sensor Count')
    plt.xlabel('Number of Sensors')
    plt.ylabel('Response Time (ms)')
    plt.grid(True)
    plt.savefig('scalability_graph.png')
    plt.show()


test_scalability()
