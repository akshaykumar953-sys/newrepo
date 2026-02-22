from bs4 import BeautifulSoup
from typing import Dict, Any


def parse_structured_awr(html: str) -> Dict[str, Any]:

    soup = BeautifulSoup(html, "lxml")

    data = {}

    data["top_events"] = extract_top_events(soup)
    data["wait_classes"] = extract_wait_classes(soup)
    data["host_cpu"] = extract_host_cpu(soup)
    data["load_profile"] = extract_load_profile(soup)
    data["instance_efficiency"] = extract_instance_efficiency(soup)
    data["platform"] = detect_platform(soup)

    return data


# -------------------------------------------------
# Utility: find table by summary keyword
# -------------------------------------------------
def find_table_by_summary(soup, keyword: str):
    for table in soup.find_all("table"):
        summary = table.get("summary", "")
        if keyword.lower() in summary.lower():
            return table
    return None


# -------------------------------------------------
# Top 10 Wait Events
# Summary text from your AWR:
# "This table displays top 10 wait events by total wait time"
# -------------------------------------------------
def extract_top_events(soup):

    table = find_table_by_summary(
        soup,
        "top 10 wait events"
    )

    if not table:
        return {}

    rows = table.find_all("tr")[1:]
    events = []

    for row in rows:
        cols = [c.text.strip() for c in row.find_all("td")]

        if len(cols) >= 5:
            events.append({
                "event": cols[0],
                "waits": cols[1],
                "time_sec": cols[2],
                "avg_wait": cols[3],
                "pct_db_time": cols[4]
            })

    return events

# -------------------------------------------------
# Foreground Wait Class
# Summary text:
# "This table displays wait class statistics ordered by total wait time"
# -------------------------------------------------
def extract_wait_classes(soup):

    table = find_table_by_summary(
        soup,
        "wait class statistics ordered by total wait time"
    )

    if not table:
        return {}

    rows = table.find_all("tr")[1:]
    wait_data = {}

    for row in rows:
        cols = [c.text.strip() for c in row.find_all("td")]

        if len(cols) >= 5:
            wait_data[cols[0]] = {
                "waits": cols[1],
                "time_sec": cols[2],
                "avg_wait": cols[3],
                "pct_db_time": cols[4]
            }

    return wait_data

# -------------------------------------------------
# Host CPU
# Summary text:
# "This table displays some detailed operating systems statistics"
# -------------------------------------------------
def extract_host_cpu(soup):

    table = find_table_by_summary(
        soup,
        "operating systems statistics"
    )

    if not table:
        return {}

    rows = table.find_all("tr")[1:]

    cpu_data = {}

    for row in rows:
        cols = [c.text.strip() for c in row.find_all("td")]

        if len(cols) >= 2:
            cpu_data[cols[0]] = cols[1]

    return cpu_data


# -------------------------------------------------
# Load Profile
# Summary text:
# "This table displays load profile"
# -------------------------------------------------
def extract_load_profile(soup):

    table = find_table_by_summary(
        soup,
        "load profile"
    )

    if not table:
        return {}

    rows = table.find_all("tr")[1:]

    load_data = {}

    for row in rows:
        cols = [c.text.strip() for c in row.find_all("td")]

        if len(cols) >= 2:
            load_data[cols[0]] = cols[1]

    return load_data


# -------------------------------------------------
# Instance Efficiency Percentages
# Summary text:
# "This table displays instance efficiency percentages"
# -------------------------------------------------
def extract_instance_efficiency(soup):

    table = find_table_by_summary(
        soup,
        "instance efficiency percentages"
    )

    if not table:
        return {}

    rows = table.find_all("tr")[1:]

    eff_data = {}

    for row in rows:
        cols = [c.text.strip() for c in row.find_all("td")]

        if len(cols) >= 2:
            eff_data[cols[0]] = cols[1]

    return eff_data


# -------------------------------------------------
# Platform Detection (Generic vs Exadata)
# -------------------------------------------------
def detect_platform(soup):

    html_text = soup.text.lower()

    if (
        "cell single block physical read" in html_text or
        "cell smart table scan" in html_text or
        "cell multiblock physical read" in html_text
    ):
        return "exadata"

    return "generic"
