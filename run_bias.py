"""
run_bias.py - Root wrapper for domains.hiring.runner
"""
import sys
from domains.hiring.runner import run_hiring_audit

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--control", action="store_true")
    parser.add_argument("--fixed", action="store_true")
    args = parser.parse_args()

    mode = "control" if args.control else ("fixed" if args.fixed else "standard")
    run_hiring_audit(mode=mode)
