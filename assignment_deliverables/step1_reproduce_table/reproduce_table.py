import os
import sys
import pandas as pd
import numpy as np

# مسیر ریشهٔ پروژه (دو سطح بالاتر از این اسکریپت)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# مسیر دادهٔ نهایی مقاله
DATA_PATH = os.path.join(REPO_ROOT, "main_study", "code", "analysis", "final_data_with_metrics.csv")
OUTPUT_PATH = os.path.join(RESULTS_DIR, "reproduced_table.csv")

# عنوان‌های فارسی برای چاپ جداول
TABLE_1_TITLE = "جدول ۱ — ضرایب رگرسیون (اقناع‌پذیری ~ log(parameter count))"
TABLE_2_TITLE = "جدول ۲ — خلاصه به‌ازای هر مدل (تعداد، میانگین اقناع‌پذیری، میانگین log پارامتر)"


def print_table(title: str, df: pd.DataFrame) -> None:
    """چاپ یک عنوان و جدول در کنسول."""
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)
    print(df.to_string(index=False))
    print()


def main():
    if not os.path.exists(DATA_PATH):
        print(f"Error: data file not found: {DATA_PATH}")
        print("Adjust path in script or run from project root.")
        sys.exit(1)

    df = pd.read_csv(DATA_PATH)
    # فقط شرط AI (مدل‌ها)
    df = df[df["condition"] == "AI"].copy()
    df = df.dropna(subset=["parameters", "dv_response_mean"])
    df["parameters"] = pd.to_numeric(df["parameters"], errors="coerce")
    df = df[df["parameters"] > 0]
    df["log_param_count"] = np.log(df["parameters"] * 1e9)

    # رگرسیون ساده: dv_response_mean ~ log(parameter count)
    from sklearn.linear_model import LinearRegression
    X = df[["log_param_count"]].values
    y = df["dv_response_mean"].values
    reg = LinearRegression().fit(X, y)
    intercept = reg.intercept_
    slope = reg.coef_[0]
    r2 = reg.score(X, y)

    # خلاصه به‌ازای هر مدل (میانگین persuasion و پارامترها)
    summary = (
        df.groupby("model", as_index=False)
        .agg(
            n=("dv_response_mean", "count"),
            mean_persuasion=("dv_response_mean", "mean"),
            mean_log_param=("log_param_count", "mean"),
        )
        .round(4)
    )

    # جدول بازتولیدشده: ضرایب رگرسیون + خلاصه
    table_rows = [
        {"term": "intercept", "estimate": round(intercept, 4), "note": "reproduced from paper data"},
        {"term": "log(parameter count)", "estimate": round(slope, 4), "note": "effect of model size"},
        {"term": "R_squared", "estimate": round(r2, 4), "note": "simple linear"},
    ]
    table_df = pd.DataFrame(table_rows)
    summary_path = os.path.join(RESULTS_DIR, "reproduced_summary_by_model.csv")

    # اول ذخیرهٔ نتایج (حتی اگر چاپ بعداً خطا بدهد)
    table_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    summary.to_csv(summary_path, index=False, encoding="utf-8-sig")

    # چاپ جداول در کنسول (در صورت خطای encoding نادیده گرفته می‌شود)
    try:
        print("Output: two tables. Table 1: regression coefficients. Table 2: summary by model.")
        print_table(TABLE_1_TITLE, table_df)
        print_table(TABLE_2_TITLE, summary)
        print("Saved:", OUTPUT_PATH, summary_path)
    except (UnicodeEncodeError, UnicodeDecodeError):
        print("Results saved. (Console print skipped due to encoding.)")
        print("Files:", OUTPUT_PATH, summary_path)
    return 0

if __name__ == "__main__":
    sys.exit(main())
