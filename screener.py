"""
screener.py - Root wrapper for domains.hiring.screener
"""
from domains.hiring.screener import screen
from core.parser import extract_json_safely as _extract_json_safely

if __name__ == "__main__":
    with open("jd.txt", "r") as f:
        jd = f.read()
    res = screen("Python Developer with SQL, Git, and Docker experience.", jd)
    print("Screen result:", res)
