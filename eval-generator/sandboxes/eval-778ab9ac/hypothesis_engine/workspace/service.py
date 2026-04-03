import sys
import random

# This constant simulates the point at which the service starts experiencing
# critical memory issues, leading to request failures (500 errors).
# In a real scenario, this would be determined by system limits.
CRITICAL_MEMORY_UNITS_THRESHOLD = 8500

# This list simulates memory that is allocated but not properly released,
# growing over time and eventually exhausting available resources.
# It represents the "elevated memory usage" observed.
_SIMULATED_MEMORY_ALLOCATIONS = []

def _perform_workload_simulation(request_id):
    """
    Simulates the processing of a single web request.
    This includes some temporary allocations and potential long-lived allocations
    if a bug exists.
    """
    # Simulate some temporary work that might allocate small objects.
    # These objects are normally garbage collected after the function returns.
    temp_data = [random.randint(0, 100) for _ in range(100)]
    _ = sum(temp_data) # Do something with it to prevent optimization from removing it entirely

    # A bug exists here: a reference to a newly created large object is
    # being inadvertently stored in a long-lived global list, simulating a memory leak.
    # Each object is roughly 100 bytes (100 * 1 byte for b'\x00' + list overhead).
    _SIMULATED_MEMORY_ALLOCATIONS.append([b'\x00'] * 100)

    # Check if the simulated memory has exceeded its critical threshold.
    # If so, simulate a 500 error due to resource exhaustion.
    if len(_SIMULATED_MEMORY_ALLOCATIONS) > CRITICAL_MEMORY_UNITS_THRESHOLD:
        raise MemoryError(f"Simulated service memory exhausted. Request {request_id} failed with 500 error.")

    # Simulate other normal processing that would happen
    # e.g., database calls, external API calls, etc.
    # No actual heavy lifting here, just a placeholder.
    pass


def main(requests_to_simulate=10000):
    """
    Main function to simulate a series of web service requests.
    Logs the outcome of each request to 'service_output.log'.
    """
    output_filename = "service_output.log"
    failures = 0
    total_requests = 0

    print(f"Simulating {requests_to_simulate} web requests. Output will be written to '{output_filename}'.")

    with open(output_filename, 'w') as f:
        f.write("--- Web Service Simulation Log ---\n")
        for i in range(1, requests_to_simulate + 1):
            total_requests += 1
            try:
                _perform_workload_simulation(i)
                f.write(f"SUCCESS: Request {i} processed.\n")
            except MemoryError as e:
                failures += 1
                f.write(f"FAILURE: Request {i} - {e}\n")
            except Exception as e:
                failures += 1
                f.write(f"UNEXPECTED ERROR: Request {i} - {e}\n")

        f.write(f"\n--- Simulation Summary ---\n")
        f.write(f"Total requests simulated: {total_requests}\n")
        f.write(f"Failed requests: {failures}\n")
        f.write(f"Successful requests: {total_requests - failures}\n")
        if total_requests > 0:
            success_rate = ((total_requests - failures) / total_requests) * 100
            f.write(f"Success rate: {success_rate:.2f}%\n")
        else:
            f.write("Success rate: N/A (no requests simulated)\n")

    print(f"\nSimulation complete. Check '{output_filename}' for results.")

if __name__ == "__main__":
    main()
