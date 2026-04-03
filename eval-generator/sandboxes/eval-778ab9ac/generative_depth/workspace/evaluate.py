
import json

def evaluate_resilience(systems_file, disruptions_file, report_file):
    """
    Evaluates the resilience of systems against disruptions and generates a report.
    """
    with open(systems_file, 'r') as f:
        systems = json.load(f)
    with open(disruptions_file, 'r') as f:
        disruptions = json.load(f)

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

    with open(report_file, 'w') as f:
        json.dump(report, f, indent=4)

def check_survival(system, unavailable_skills):
    """
    Checks if a system survives a given disruption.
    """
    # 1. Check fixed obligations
    for obligation in system['fixed_obligations']:
        if obligation in unavailable_skills:
            return False

    # 2. Check essential needs
    current_skills = [s for s in system['available_skills'] if s not in unavailable_skills]
    
    for need, required_skills in system['essential_needs'].items():
        if not any(skill in current_skills for skill in required_skills):
            return False

    return True

if __name__ == "__main__":
    evaluate_resilience('systems.json', 'disruptions.json', 'survival_report.json')
