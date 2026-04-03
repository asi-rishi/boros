
import json

def check_survival(system, unavailable_skills):
    """
    Checks if a system survives a given disruption based on survival criteria.
    """
    # 1. All fixed obligations must be maintained.
    # A system fails if any of its fixed obligations are in the list of unavailable skills.
    if any(obligation in unavailable_skills for obligation in system.get('fixed_obligations', [])):
        return False

    # 2. All essential needs must be met.
    # Calculate the system's remaining skills after the disruption.
    remaining_skills = set(system.get('available_skills', [])) - set(unavailable_skills)

    # For every essential need, check if there is at least one available skill to satisfy it.
    for need, required_skills in system.get('essential_needs', {}).items():
        # A need is met if at least one of the skills that can satisfy it is in the remaining skills.
        if not any(skill in remaining_skills for skill in required_skills):
            return False  # If any need is not met, the system fails.

    # If all checks pass, the system survives.
    return True

def main():
    """
    Main function to read data, evaluate systems, and write the report.
    """
    try:
        with open('systems.json', 'r') as f:
            systems = json.load(f)
    except FileNotFoundError:
        print("Error: systems.json not found.")
        return

    try:
        with open('disruptions.json', 'r') as f:
            disruptions = json.load(f)
    except FileNotFoundError:
        print("Error: disruptions.json not found.")
        return

    report = {}
    total_disruptions = len(disruptions)

    for system_name, system_data in systems.items():
        survived_count = 0
        for disruption_name, unavailable_skills in disruptions.items():
            if check_survival(system_data, unavailable_skills):
                survived_count += 1
        
        survival_rate = survived_count / total_disruptions if total_disruptions > 0 else 0
        
        report[system_name] = {
            "survived_count": survived_count,
            "total_disruptions": total_disruptions,
            "survival_rate": round(survival_rate, 4)
        }

    with open('survival_report.json', 'w') as f:
        json.dump(report, f, indent=4)

if __name__ == "__main__":
    main()
