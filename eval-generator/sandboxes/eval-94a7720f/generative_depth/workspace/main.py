import random

def get_machine_configurations():
    """
    Returns a list of lists, where each inner list defines the resource
    types a machine can process.
    """
    # This configuration is designed for maximum resilience.
    # Each resource type is covered by exactly 3 machines.
    # Each machine has exactly 3 capabilities.
    # The distribution is balanced to provide multiple pathways for each resource.
    configurations = [
        ['A', 'B', 'C'],  # Machine 0
        ['A', 'B', 'D'],  # Machine 1
        ['A', 'C', 'E'],  # Machine 2
        ['B', 'D', 'E'],  # Machine 3
        ['C', 'D', 'E']   # Machine 4
    ]
    return configurations

def run_simulation(configurations):
    """
    Runs the factory simulation with the given machine configurations.
    """
    resource_types = ['A', 'B', 'C', 'D', 'E']
    num_machines = 5
    num_rounds = 100
    requests_per_round = 10
    total_successful_requests = 0

    for _ in range(num_rounds):
        # 1. Failure Event
        failed_machine_index = random.randint(0, num_machines - 1)
        available_machines = []
        for i in range(num_machines):
            if i != failed_machine_index:
                available_machines.append({
                    "id": i,
                    "capabilities": configurations[i]
                })

        # 2. Resource Requests
        resource_requests = [random.choice(resource_types) for _ in range(requests_per_round)]

        # 3. Fulfillment
        successful_requests_this_round = 0
        for request in resource_requests:
            is_fulfilled = False
            for machine in available_machines:
                if request in machine["capabilities"]:
                    is_fulfilled = True
                    break  # Request fulfilled by the first available machine
            if is_fulfilled:
                successful_requests_this_round += 1
        
        total_successful_requests += successful_requests_this_round

    return total_successful_requests / num_rounds

def main():
    """
    Main function to run the simulation and write results.
    """
    configurations = get_machine_configurations()
    
    # Validation checks
    if len(configurations) != 5:
        raise ValueError("The number of machine configurations must be exactly 5.")
    for i, config in enumerate(configurations):
        if not (1 <= len(config) <= 3):
            raise ValueError(f"Machine {i} must have between 1 and 3 capabilities.")
        if len(set(config)) != len(config):
            raise ValueError(f"Machine {i} has duplicate resource types in its configuration.")
        for resource in config:
            if resource not in ['A', 'B', 'C', 'D', 'E']:
                raise ValueError(f"Machine {i} has an invalid resource type: {resource}.")

    average_success = run_simulation(configurations)
    
    with open("results.txt", "w") as f:
        f.write(str(average_success))

if __name__ == "__main__":
    main()
