#!/usr/bin/env python3
import os
import sys
import argparse
import pandas as pd
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

BASELINE_RESPONSE = (
    "This is a placeholder persuasive argument. In conclusion, "
    "the policy would benefit society. We should support this stance."
)

def word_count(text):
    if pd.isna(text) or not isinstance(text, str):
        return 0
    return len(text.strip().split())

def main():
    parser = argparse.ArgumentParser(description="Run model (or baseline) on input CSV.")
    parser.add_argument("--input_csv", type=str, default=None, help="Path to input CSV (prompts/tweets).")
    parser.add_argument("--output_csv", type=str, default=None, help="Path to output CSV.")
    parser.add_argument("--text_column", type=str, default=None, help="Column name for text (default: prompt_full_text or first column).")
    args = parser.parse_args()

    input_csv = args.input_csv or os.path.join(SCRIPT_DIR, "example_input.csv")
    output_csv = args.output_csv or os.path.join(RESULTS_DIR, "example_output.csv")
    text_col = args.text_column

    if not os.path.exists(input_csv):
        print(f"Error: input file not found: {input_csv}")
        sys.exit(1)

    df = pd.read_csv(input_csv)
    if text_col and text_col in df.columns:
        pass
    elif "prompt_full_text" in df.columns:
        text_col = "prompt_full_text"
    else:
        text_col = df.columns[0]
    print(f"Text column: {text_col}")

    # در حالت بدون مدل: پاسخ baseline برای هر سطر
    df["response"] = BASELINE_RESPONSE
    df["response_word_count"] = df["response"].apply(word_count)
    df["run_timestamp"] = datetime.now().isoformat()

    os.makedirs(os.path.dirname(output_csv) or ".", exist_ok=True)
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"Output saved: {output_csv} (n={len(df)})")
    return 0

if __name__ == "__main__":
    sys.exit(main())
