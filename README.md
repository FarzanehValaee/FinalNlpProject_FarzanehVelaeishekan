# Scaling language model size yields diminishing returns for single-message political persuasion

**ارائه‌دهنده:** فرزانه ولایی شکن (۴۰۴۱۵۸۷۴)

این پروژه بر اساس مقالهٔ فوق انجام شده است.

---

## محل قرارگیری مطالب

| مورد                                       | مسیر                                                                                                  |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **نتایج و تحلیل پروژه**  | پوشه`assignment_deliverables/`و زیرپوشه `assignment_deliverables/results/` |
| **مقالهٔ اصلی**                | پوشه`papers/` — فایل `مقاله اصلی.pdf`                                           |
| **خلاصهٔ تحلیلی مقاله** | پوشه`papers/` — فایل `خلاصه تحلیلی مقاله.pdf`                            |

---

## تحویل پروژه و تحلیل‌ها (`assignment_deliverables`)

تحویلی پروژه سه مرحله دارد: (۱) بازتولید جدول نتیجهٔ مقاله، (۲) دیتاست جدید سیاسی و مقایسه با baseline، (۳) اسکریپت اجرا روی فایل CSV ورودی. خروجی هر مرحله در `assignment_deliverables/results/` ذخیره شده است.

---

### مرحله ۱: بازتولید جدول نتیجهٔ مقاله

**هدف:** مقاله اثر **اندازهٔ مدل** (تعداد پارامترها) را روی **میزان متقاعدسازی** (persuasion) با رگرسیون گزارش می‌کند. این مرحله همان رابطه را از روی دادهٔ نهایی مقاله برآورد و به صورت جدول ذخیره می‌کند.

**روش:**

- ورودی: فایل `main_study/code/analysis/final_data_with_metrics.csv` (دادهٔ نهایی مطالعهٔ اصلی).
- فیلتر: فقط ردیف‌های شرط **AI** (خروجی مدل‌ها)، با مقادیر معتبر برای `parameters` و `dv_response_mean`.
- متغیرها: `log_param_count = log(parameters × 10⁹)` و `dv_response_mean` (میانگین پاسخ شرکت‌کنندگان به پیام متقاعدکننده).
- مدل: رگرسیون خطی ساده **dv_response_mean ~ log(parameter count)** با `sklearn.linear_model.LinearRegression`.

**خروجی‌ها:**

- **`reproduced_table.csv`**: ضرایب مدل — `intercept` (حدود ۵٫۴۵)، `log(parameter count)` (حدود ۱٫۲۶، یعنی با بزرگ‌تر شدن مدل، persuasion بیشتر می‌شود)، و `R_squared` (حدود ۰٫۱۲).
- **`reproduced_summary_by_model.csv`**: خلاصه به‌ازای هر مدل — تعداد مشاهدات، میانگین persuasion و میانگین `log_param_count` (مثلاً pythia-160m، pythia-410m، Llama-2-7b، falcon-7b و غیره).

**تفسیر:** ضریب مثبت برای `log(parameter count)` با نتیجهٔ مقاله هم‌خوان است: مدل‌های بزرگ‌تر در میانگین پیام متقاعدکننده‌تری تولید می‌کنند؛ R² نسبتاً کم نشان می‌دهد بخش زیادی از واریانس به عوامل دیگر (مثلاً موضوع، فرمول‌بندی پرامپت) وابسته است.

---

### مرحله ۲: دیتاست جدید سیاسی و مقایسه با baseline

**هدف:** (۱) استفاده از یک **دیتاست جدید با پرامپت‌های صریح سیاسی**؛ (۲) تعریف یک **baseline ساده** (پاسخ ثابت بدون مدل) و مقایسهٔ آن با خروجی مدل از نظر طول پاسخ.

**دیتاست جدید سیاسی:**فایل `pilot/data/prompts_political_5.csv` شامل **۵ پرامپت** با موضوعات صریح سیاسی است:

- الغای electoral college و انتخاب رئیس‌جمهور با آرای مردمی
- محدودیت دوره برای کنگره (term limits)
- برگرداندن Citizens United و محدود کردن هزینهٔ شرکت‌ها در انتخابات
- ایالت شدن واشنگتن دی.سی.
- الزام ارائه کارت شناسایی با عکس برای رای‌گیری

**Baseline:** یک متن ثابت کوتاه (حدود ۱۴ کلمه) به‌عنوان «پاسخ قالب» بدون استفاده از مدل.

**روش مقایسه:**

- ورودی‌ها: خروجی مدل pythia-160m روی پرامپت‌های پایلوت (`pilot/data/completions/pythia-160m_responses.csv`) و لیست پرامپت‌های سیاسی بالا.
- برای هر پرامپت: شمارش تعداد کلمهٔ پاسخ مدل و پاسخ baseline، و محاسبهٔ اختلاف.
- خلاصه: میانگین طول پاسخ مدل، میانگین طول baseline، و میانگین اختلاف.

**خروجی‌ها:**

- **`baseline_comparison.csv`**: هر سطر یک پرامپت (خلاصهٔ متن)، `model_response_word_count`، `baseline_response_word_count`، `difference_word_count`، و منبع (pilot_prompts یا political_5).
- **`baseline_comparison_summary.csv`**: متریک‌های کلی — مثلاً `mean_model_word_count` (حدود ۱۸۷)، `mean_baseline_word_count` (۱۴)، `mean_difference_word_count` (حدود ۱۷۳)، و تعداد پرامپت‌هایی که خروجی مدل دارند.

**تفسیر:** پاسخ‌های مدل به‌طور میانگین بسیار طولانی‌تر از baseline ثابت هستند؛ این اختلاف نشان می‌دهد مدل واقعاً متن تولید می‌کند و baseline فقط یک حد پایهٔ ساده است.

---

### مرحله ۳: اسکریپت اجرا روی فایل ورودی CSV

**هدف:** یک اسکریپت ساده که یک فایل CSV ورودی (مثلاً پرامپت‌ها یا توییت‌ها) بگیرد و یک فایل CSV خروجی با ستون‌های پاسخ و تعداد کلمه تولید کند.

**ورودی:** CSV با حداقل یک ستون متنی — ترجیحاً `prompt_full_text` یا در غیر این صورت اولین ستون.

**خروجی:** همان سطرهای ورودی به‌اضافهٔ ستون‌های:

- `response`: متن پاسخ (در حالت پیش‌فرض همان baseline ثابت؛ برای خروجی مدل واقعی از اسکریپت اصلی پروژه استفاده شود).
- `response_word_count`: تعداد کلمهٔ پاسخ.
- `run_timestamp`: زمان اجرا.

**فایل‌های نمونه:**

- **`example_input.csv`**: دو پرامپت نمونه (انرژی تجدیدپذیر، بودجهٔ مدارس).
- **`example_output.csv`**: خروجی همان دو پرامپت با پاسخ baseline و تعداد کلمه.

**لاگ اجرا:** فایل `assignment_deliverables/run_log.txt` شامل خروجی ترمینال برای هر سه مرحله است.

---

## نحوهٔ ران گرفتن ( `assignment_deliverables`)

همهٔ دستورات از **ریشهٔ پروژه** اجرا شوند.

### پیش‌نیاز

```bash
pip install pandas numpy scikit-learn
```

### مرحله ۱: بازتولید جدول نتیجهٔ مقاله

```bash
python assignment_deliverables/step1_reproduce_table/reproduce_table.py
```

خروجی: `assignment_deliverables/results/reproduced_table.csv` و `reproduced_summary_by_model.csv`.

### مرحله ۲: baseline و دیتاست سیاسی

```bash
python assignment_deliverables/step2_baseline_and_dataset/baseline_comparison.py
```

خروجی: `assignment_deliverables/results/baseline_comparison.csv` و `baseline_comparison_summary.csv`.

### مرحله ۳: اسکریپت اجرا روی فایل ورودی CSV

```bash
python assignment_deliverables/run_on_input.py --input_csv assignment_deliverables/example_input.csv --output_csv assignment_deliverables/results/example_output.csv
```

خروجی: `assignment_deliverables/results/example_output.csv` (ستون‌های پاسخ و تعداد کلمه).

پارامترهای اختیاری: `--input_csv`، `--output_csv`، `--text_column` (نام ستون متن).

---

## Citation

```bibtex
@misc{hackenburg2024evidence,
      title={Scaling language model size yields diminishing returns for single-message political persuasion},
      author={Kobi Hackenburg and Ben M. Tappin and Paul Röttger and Scott Hale and Jonathan Bright and Helen Margetts},
      year={2024},
      eprint={2406.14508},
      archivePrefix={arXiv},
}
```
