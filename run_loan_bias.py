"""
run_loan_bias.py - Root wrapper for domains.lending.runner
"""
import sys
from domains.lending.runner import run_lending_audit

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--control", action="store_true")
    parser.add_argument("--fixed", action="store_true")
    args = parser.parse_args()

    mode = "control" if args.control else ("fixed" if args.fixed else "standard")
    run_lending_audit(mode=mode)
