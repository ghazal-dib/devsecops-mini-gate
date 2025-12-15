import os
import sys
import json


def secret_leak_scanning(path="app.log"):
    patterns = ["API_KEY", "PASSWORD", "AWS_SECRET"]

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                for p in patterns:
                    if p in line:
                        return True  # leak found
    except FileNotFoundError:
        print("BLOCK: app.log missing")
        return True 

    return False  # no leak


def analyze_report(path="report.json"):
    high_count = 0
    has_critical = False

    try:
        with open(path, "r", encoding="utf-8") as file:
            report = json.load(file)
    except FileNotFoundError:
        print("BLOCK: report.json missing")
        return 0, True
    except json.JSONDecodeError:
        print("BLOCK: report.json invalid JSON")
        return 0, True

    results = report.get("Results", [])
    for result in results:
        vulns = result.get("Vulnerabilities", [])
        for v in vulns:
            severity = v.get("Severity", "UNKNOWN")
            if severity == "CRITICAL":
                has_critical = True
            elif severity == "HIGH":
                high_count += 1

    return high_count, has_critical


def decide(high_count, has_critical):
    if has_critical:
        return "BLOCK"
    if high_count >= 2:
        return "BLOCK"
    if high_count == 1:
        return "WARN"
    return "OK"


def main():
    # A) Secret check
    api_key = os.environ.get("API_KEY")
    if not api_key:
        print("BLOCK: API_KEY missing")
        sys.exit(1)

    # B) Secret leak scanning
    has_leak = secret_leak_scanning("app.log")
    if has_leak:
        print("BLOCK: Secret leak detected")
        sys.exit(1)

    # C) JSON vulnerabilities
    high_count, has_critical = analyze_report("report.json")

    # D) Decision
    final_decision = decide(high_count, has_critical)

    if final_decision == "BLOCK":
        print("BLOCK")
        sys.exit(1)
    elif final_decision == "WARN":
        print("WARN")
        sys.exit(0)
    else:
        print("OK")
        sys.exit(0)


if __name__ == "__main__":
    main()
