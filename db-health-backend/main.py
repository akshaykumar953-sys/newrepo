from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_percentage(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except:
            return None
    return None


@app.post("/analyze/oracle")
async def analyze_oracle(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode(errors="ignore")

    score = 100
    issues = []

    # -------------------------
    # Extract DB CPU %
    # -------------------------
    db_cpu = extract_percentage(r"DB CPU.*?(\d+\.\d+)%", text)

    if db_cpu:
        if db_cpu > 70:
            score -= 15
            issues.append(f"High DB CPU usage ({db_cpu}%)")

    # -------------------------
    # Extract Hard Parse %
    # -------------------------
    hard_parse = extract_percentage(r"Hard Parse.*?(\d+\.\d+)%", text)

    if hard_parse:
        if hard_parse > 5:
            score -= 10
            issues.append(f"High Hard Parse ratio ({hard_parse}%)")

    # -------------------------
    # Detect Top Wait Events
    # -------------------------
    if "db file sequential read" in text.lower():
        score -= 15
        issues.append("High single block read waits detected")

    if "log file sync" in text.lower():
        score -= 10
        issues.append("Log file sync wait observed")

    if "direct path read" in text.lower():
        score -= 10
        issues.append("Direct path read wait observed")

    # -------------------------
    # Buffer Cache Hit Ratio
    # -------------------------
    buffer_hit = extract_percentage(r"Buffer Cache Hit Ratio.*?(\d+\.\d+)%", text)

    if buffer_hit:
        if buffer_hit < 90:
            score -= 10
            issues.append(f"Low Buffer Cache Hit Ratio ({buffer_hit}%)")

    # Prevent negative
    if score < 0:
        score = 0

    return {
        "score": score,
        "issues": issues,
        "metrics": {
            "db_cpu": db_cpu,
            "hard_parse": hard_parse,
            "buffer_cache_hit": buffer_hit
        }
    }
