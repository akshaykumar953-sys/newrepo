import re


# ---------------------------------------------
# Remove commas and convert to float safely
# ---------------------------------------------
def to_float(value: str):
    if not value:
        return 0.0

    value = value.replace(",", "").strip()

    try:
        return float(value)
    except:
        return 0.0


# ---------------------------------------------
# Convert time strings to seconds
# Supports ns, us, ms, s
# ---------------------------------------------
def time_to_seconds(value: str):

    if not value:
        return 0.0

    value = value.strip()

    # Extract numeric part
    number = re.findall(r"[\d\.E\+\-]+", value)
    if not number:
        return 0.0

    number = float(number[0])

    if "ns" in value:
        return number / 1_000_000_000
    elif "us" in value:
        return number / 1_000_000
    elif "ms" in value:
        return number / 1_000
    else:
        return number  # already seconds


# ---------------------------------------------
# Normalize Top Events
# ---------------------------------------------
def normalize_top_events(events):

    normalized = []

    for e in events:

        normalized.append({
            "event": e["event"],
            "waits": int(to_float(e.get("waits", "0"))),
            "time_sec": to_float(e.get("time_sec", "0")),
            "avg_wait_sec": time_to_seconds(e.get("avg_wait", "")),
            "pct_db_time": to_float(e.get("pct_db_time", "0"))
        })

    return normalized


# ---------------------------------------------
# Normalize Wait Classes
# ---------------------------------------------
def normalize_wait_classes(wait_classes):

    normalized = {}

    for k, v in wait_classes.items():

        normalized[k] = {
            "waits": int(to_float(v.get("waits", "0"))),
            "time_sec": to_float(v.get("time_sec", "0")),
            "avg_wait_sec": time_to_seconds(v.get("avg_wait", "")),
            "pct_db_time": to_float(v.get("pct_db_time", "0"))
        }

    return normalized


# ---------------------------------------------
# Normalize Load Profile
# ---------------------------------------------
def normalize_load_profile(load_profile):

    normalized = {}

    for k, v in load_profile.items():
        normalized[k] = to_float(v)

    return normalized


# ---------------------------------------------
# Normalize Instance Efficiency
# ---------------------------------------------
def normalize_efficiency(eff):

    normalized = {}

    for k, v in eff.items():
        normalized[k] = to_float(v)

    return normalized
