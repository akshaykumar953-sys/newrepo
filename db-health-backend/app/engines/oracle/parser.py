import re
from app.engines.oracle.schema import empty_feature_schema

def extract_percentage(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except:
            return None
    return None

def parse_awr(text: str):
    features = empty_feature_schema()

    features["db_cpu_pct"] = extract_percentage(r"DB CPU.*?(\d+\.\d+)", text)
    features["hard_parse_pct"] = extract_percentage(r"Hard Parse.*?(\d+\.\d+)", text)
    features["buffer_cache_hit_pct"] = extract_percentage(r"Buffer Cache Hit Ratio.*?(\d+\.\d+)", text)

    if "db file sequential read" in text.lower():
        features["wait_events"].append("db file sequential read")

    if "log file sync" in text.lower():
        features["wait_events"].append("log file sync")

    return features
