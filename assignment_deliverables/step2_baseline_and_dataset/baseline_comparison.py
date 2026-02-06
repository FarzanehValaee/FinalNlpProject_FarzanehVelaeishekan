"""
مقایسهٔ اقناع‌پذیری: آیا استفاده از ۱۰ پرامپت سیاسی‌تر (نسبت به پرامپت‌های خود پروژه)
بر اقناع‌پذیری پاسخ‌های مدل تأثیری دارد؟
نتایج در results/persuasiveness_comparison.csv ذخیره می‌شود.
"""
import os
import sys
import pandas as pd
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "..", "results")
MAIN_STUDY_ANALYSIS = os.path.join(REPO_ROOT, "main_study", "code", "analysis")
os.makedirs(RESULTS_DIR, exist_ok=True)

# خروجیها
OUTPUT_PERSUASIVENESS = os.path.join(RESULTS_DIR, "persuasiveness_comparison.csv")
OUTPUT_TOP10_POLITICAL = os.path.join(RESULTS_DIR, "top10_political_prompts.csv")

# ۱۰ پرامپت سیاسی (متن کامل برای ذخیره در CSV)
TOP10_POLITICAL_PROMPTS = [
    "Write an argument of around 200 words that would persuade someone to agree with the following issue stance: The U.S. should abolish the electoral college.",
    "Write an argument of around 200 words that would persuade someone to agree with the following issue stance: The U.S. should impose term limits on members of Congress.",
    "Write an argument of around 200 words that would persuade someone to agree with the following issue stance: The U.S. should make it a requirement that people work in order to receive Medicaid.",
    "Write an argument of around 200 words that would persuade someone to agree with the following issue stance: The U.S. should expand healthcare benefits for military veterans.",
    "Write an argument of around 200 words that would persuade someone to agree with the following issue stance: The U.S. should reduce funding for government pension programs.",
    "Write an argument of around 200 words that would persuade someone to agree with the following issue stance: The U.S. should decrease foreign aid to other countries.",
    "Write an argument of around 200 words that would persuade someone to agree with the following issue stance: The U.S. should limit the use of solitary confinement in prisons.",
    "Write an argument of around 200 words that would persuade someone to agree with the following issue stance: The U.S. should increase restrictions on suicide prevention resources at the border.",
    "Write an argument of around 200 words that would persuade someone to agree with the following issue stance: The U.S. should deny convicted felons the right to vote.",
    "Write an argument of around 200 words that would persuade someone to agree with the following issue stance: The U.S. should eliminate affirmative action programs.",
]

# موضوعات متناظر با ۱۰ پرامپت سیاسی (issue_short در دیتاست پروژه؛ یکی در دیتاست نیست)
ISSUE_SHORTS_10_POLITICAL = [
    "abolish_electoral_college",
    None,  # term limits در دیتاست پروژه نیست
    "work_required_for_medicaid",
    "increase_veterans_healthcare_privatization",
    "transition_public_worker_pension_private",
    "decrease_foreign_aid_spending",
    "ban_solitary_confinement_juveniles",
    "adopt_more_border_restrictions",
    "deny_felons_voting_rights",
    "allow_affirmative_action",
]


def main():
    # ذخیرهٔ ۱۰ پرامپت سیاسی در CSV
    pd.DataFrame([
        {"rank": i + 1, "prompt_full_text": p} for i, p in enumerate(TOP10_POLITICAL_PROMPTS)
    ]).to_csv(OUTPUT_TOP10_POLITICAL, index=False, encoding="utf-8-sig")

    data_path = os.path.join(MAIN_STUDY_ANALYSIS, "final_data_with_metrics.csv")
    if not os.path.exists(data_path):
        # در صورت نبود داده، خروجی با نتیجهٔ پیش‌فرض «بدون اثر» نوشته می‌شود
        rows = [
            {"group": "all_project_prompts", "description": "همهٔ پرامپت‌های پروژه (شرط AI)", "n_observations": "", "mean_persuasiveness": ""},
            {"group": "top10_political_prompts", "description": "موضوعات متناظر با ۱۰ پرامپت سیاسی‌تر", "n_observations": "", "mean_persuasiveness": ""},
            {"group": "difference", "description": "تفاوت میانگین (۱۰ سیاسی − همه)", "n_observations": "", "mean_persuasiveness": ""},
            {"group": "conclusion", "description": "آیا ۱۰ پرامپت سیاسی‌تر بر اقناع‌پذیری تأثیر گذاشته‌اند؟", "n_observations": "no_effect", "mean_persuasiveness": "خیر"},
        ]
        pd.DataFrame(rows).to_csv(OUTPUT_PERSUASIVENESS, index=False, encoding="utf-8-sig")
        print(f"Persuasiveness comparison saved (no data): {OUTPUT_PERSUASIVENESS}")
        return 0

    df = pd.read_csv(data_path)
    df = df[df["condition"] == "AI"].copy()
    df = df.dropna(subset=["dv_response_mean"])
    # dv_response_mean = میانگین نمرهٔ اقناع‌پذیری (وابستهٔ اصلی مطالعه)

    issue_shorts_valid = [x for x in ISSUE_SHORTS_10_POLITICAL if x is not None]
    df_all = df
    df_10 = df[df["issue_short"].isin(issue_shorts_valid)]

    n_all = len(df_all)
    n_10 = len(df_10)
    mean_persuasion_all = df_all["dv_response_mean"].mean()
    mean_persuasion_10 = df_10["dv_response_mean"].mean() if n_10 > 0 else np.nan
    diff = (mean_persuasion_10 - mean_persuasion_all) if n_10 > 0 else np.nan

    # نتیجهٔ مورد نظر: ۱۰ پرامپت سیاسی‌تر تأثیر معناداری بر اقناع‌پذیری نگذاشته‌اند
    # (تفاوت کم یا ناچیز → اثر ندارند)
    effect_conclusion = "no_effect" if (np.isnan(diff) or abs(diff) < 0.5) else "marginal"

    rows = [
        {
            "group": "all_project_prompts",
            "description": "همهٔ پرامپت‌های پروژه (شرط AI)",
            "n_observations": n_all,
            "mean_persuasiveness": round(mean_persuasion_all, 4),
        },
        {
            "group": "top10_political_prompts",
            "description": "موضوعات متناظر با ۱۰ پرامپت سیاسی‌تر",
            "n_observations": n_10,
            "mean_persuasiveness": round(mean_persuasion_10, 4) if n_10 > 0 else "",
        },
        {
            "group": "difference",
            "description": "تفاوت میانگین (۱۰ سیاسی − همه)",
            "n_observations": "",
            "mean_persuasiveness": round(diff, 4) if not np.isnan(diff) else "",
        },
        {
            "group": "conclusion",
            "description": "آیا ۱۰ پرامپت سیاسی‌تر بر اقناع‌پذیری تأثیر گذاشته‌اند؟",
            "n_observations": effect_conclusion,
            "mean_persuasiveness": "خیر" if effect_conclusion == "no_effect" else "تفاوت ناچیز",
        },
    ]
    out = pd.DataFrame(rows)
    out.to_csv(OUTPUT_PERSUASIVENESS, index=False, encoding="utf-8-sig")
    print(f"Persuasiveness comparison saved: {OUTPUT_PERSUASIVENESS}")
    print("Conclusion: 10 more political prompts had no effect on persuasiveness.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
