def classify_severity(score: int):
    if score >= 90:
        return "Healthy"
    elif score >= 70:
        return "Moderate"
    elif score >= 50:
        return "Risk"
    else:
        return "Critical"

def score_awr(features: dict):
    score = 100
    issues = []

    if features["db_cpu_pct"] and features["db_cpu_pct"] > 70:
        score -= 15
        issues.append(f"High DB CPU usage ({features['db_cpu_pct']}%)")

    if features["hard_parse_pct"] and features["hard_parse_pct"] > 5:
        score -= 10
        issues.append(f"High Hard Parse ratio ({features['hard_parse_pct']}%)")

    if "db file sequential read" in features["wait_events"]:
        score -= 15
        issues.append("High single block read waits detected")

    if "log file sync" in features["wait_events"]:
        score -= 10
        issues.append("Log file sync wait observed")

    if score < 0:
        score = 0

    return {
        "score": score,
        "severity": classify_severity(score),
        "issues": issues,
        "metrics": features
    }
