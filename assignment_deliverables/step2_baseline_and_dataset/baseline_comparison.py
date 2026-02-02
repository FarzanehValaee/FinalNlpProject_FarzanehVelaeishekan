import os
import sys
import pandas as pd
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# مسیر خروجی مدل (پایلوت) و دیتاست سیاسی
MODEL_RESPONSES_PATH = os.path.join(REPO_ROOT, "pilot", "data", "completions", "pythia-160m_responses.csv")
POLITICAL_PROMPTS_PATH = os.path.join(REPO_ROOT, "pilot", "data", "prompts_political_5.csv")
OUTPUT_COMPARISON = os.path.join(RESULTS_DIR, "baseline_comparison.csv")
OUTPUT_SUMMARY = os.path.join(RESULTS_DIR, "baseline_comparison_summary.csv")

# Baseline: پاسخ ثابت (متن کوتاه ثابت به‌جای تولید مدل)
BASELINE_RESPONSE = (
    "This is a placeholder persuasive argument. In conclusion, "
    "the policy would benefit society. We should support this stance."
)

def word_count(text):
    if pd.isna(text) or not isinstance(text, str):
        return 0
    return len(text.strip().split())

def main():
    rows = []

    # بارگذاری خروجی مدل
    if os.path.exists(MODEL_RESPONSES_PATH):
        df_model = pd.read_csv(MODEL_RESPONSES_PATH)
        if "response" in df_model.columns and "prompt_full_text" in df_model.columns:
            for idx, row in df_model.iterrows():
                model_resp = row.get("response", "")
                prompt = row.get("prompt_full_text", "")[:80]
                wc_model = word_count(model_resp)
                wc_baseline = word_count(BASELINE_RESPONSE)
                rows.append({
                    "prompt_short": prompt + "..." if len(str(prompt)) > 80 else prompt,
                    "model_response_word_count": wc_model,
                    "baseline_response_word_count": wc_baseline,
                    "difference_word_count": wc_model - wc_baseline,
                    "source": "pilot_prompts",
                })
    else:
        print(f"Warning: model file not found: {MODEL_RESPONSES_PATH}")
        print("Comparison uses baseline only.")

    # اگر دیتاست سیاسی وجود دارد، برای آن هم baseline اضافه کن (بدون خروجی مدل واقعی، فقط baseline)
    if os.path.exists(POLITICAL_PROMPTS_PATH):
        df_pol = pd.read_csv(POLITICAL_PROMPTS_PATH)
        col = "prompt_full_text" if "prompt_full_text" in df_pol.columns else df_pol.columns[0]
        for idx, row in df_pol.iterrows():
            prompt = row[col][:80] if isinstance(row[col], str) else str(row[col])[:80]
            wc_baseline = word_count(BASELINE_RESPONSE)
            rows.append({
                "prompt_short": prompt + "..." if len(str(prompt)) > 80 else prompt,
                "model_response_word_count": None,
                "baseline_response_word_count": wc_baseline,
                "difference_word_count": None,
                "source": "political_5",
            })

    if not rows:
        # حداقل یک سطر نمونه
        rows.append({
            "prompt_short": "sample prompt",
            "model_response_word_count": 0,
            "baseline_response_word_count": word_count(BASELINE_RESPONSE),
            "difference_word_count": -word_count(BASELINE_RESPONSE),
            "source": "sample",
        })

    df_out = pd.DataFrame(rows)
    df_out.to_csv(OUTPUT_COMPARISON, index=False, encoding="utf-8-sig")
    print(f"Comparison table saved: {OUTPUT_COMPARISON}")

    # خلاصه: میانگین طول پاسخ مدل vs baseline (فقط جایی که مدل داریم)
    with_model = df_out[df_out["model_response_word_count"].notna()]
    if len(with_model) > 0:
        summary = pd.DataFrame([{
            "metric": "mean_model_word_count",
            "value": with_model["model_response_word_count"].mean(),
        }, {
            "metric": "mean_baseline_word_count",
            "value": with_model["baseline_response_word_count"].mean(),
        }, {
            "metric": "mean_difference_word_count",
            "value": with_model["difference_word_count"].mean(),
        }, {
            "metric": "n_prompts_with_model",
            "value": len(with_model),
        }])
        summary.to_csv(OUTPUT_SUMMARY, index=False, encoding="utf-8-sig")
        print(f"Summary saved: {OUTPUT_SUMMARY}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
