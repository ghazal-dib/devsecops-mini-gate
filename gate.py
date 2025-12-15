import os
import sys

def analyze_log(path="scan.log"):
    high_count = 0
    has_critical = False

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "CRITICAL" in line:
                has_critical = True
            if "HIGH" in line:
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
    # 1) Secret check 
    api_key = os.environ.get("API_KEY")
    if not api_key:
        print("BLOCK: API_KEY missing")
        sys.exit(1)

    # 2) Analyze log
    high_count, has_critical = analyze_log("scan.log")

    # 3) Final decision
    final_decision = decide(high_count, has_critical)

    if final_decision == "BLOCK":
        print("BLOCK: Critical found or too many HIGH")
        sys.exit(1)
    elif final_decision == "WARN":
        print("WARNING: HIGH found")
        sys.exit(0)
    else:
        print("OK: No blocking issues")
        sys.exit(0)


if __name__ == "__main__":
    main()
