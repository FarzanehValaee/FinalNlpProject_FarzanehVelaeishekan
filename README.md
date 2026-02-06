# Scaling language model size yields diminishing returns for single-message political persuasion

**ارائه‌دهنده:** فرزانه ولایی شکن (۴۰۴۱۵۸۷۴)

این پروژه بر اساس مقالهٔ فوق انجام شده است.

---

## محل قرارگیری مطالب

| مورد | مسیر |
|------|------|
| **نتایج و تحلیل پروژه** | پوشهٔ `assignment_deliverables/` و زیرپوشهٔ `assignment_deliverables/results/` |
| **مقالهٔ اصلی** | پوشهٔ `papers/` — فایل `مقاله اصلی.pdf` |
| **خلاصهٔ تحلیلی مقاله** | پوشهٔ `papers/` — فایل `خلاصه تحلیلی مقاله.pdf` |

---

## تحویل پروژه و تحلیل‌ها (`assignment_deliverables`)

تحویل پروژه سه مرحله دارد: (۱) بازتولید جدول نتیجهٔ مقاله، (۲) مقایسهٔ اقناع‌پذیری برای پرامپت‌های سیاسی و ذخیرهٔ ۱۰ پرامپت سیاسی، (۳) اسکریپت اجرا روی فایل CSV ورودی. خروجی هر مرحله در `assignment_deliverables/results/` ذخیره می‌شود.

---

### مرحله ۱: بازتولید جدول نتیجهٔ مقاله

**هدف:** مقاله اثر **اندازهٔ مدل** (تعداد پارامترها) را روی **میزان متقاعدسازی** (persuasion) با رگرسیون گزارش می‌کند. این مرحله همان رابطه را از روی دادهٔ نهایی مقاله برآورد و به صورت جدول ذخیره می‌کند.

**روش:**

- ورودی: فایل `main_study/code/analysis/final_data_with_metrics.csv` (دادهٔ نهایی مطالعهٔ اصلی).
- فیلتر: فقط ردیف‌های شرط **AI** (خروجی مدل‌ها)، با مقادیر معتبر برای `parameters` و `dv_response_mean`.
- متغیرها: `log_param_count = log(parameters × 10⁹)` و `dv_response_mean` (میانگین پاسخ شرکت‌کنندگان به پیام متقاعدکننده).
- مدل: رگرسیون خطی ساده **dv_response_mean ~ log(parameter count)** با `sklearn.linear_model.LinearRegression`.

**خروجی‌ها:**

- **`reproduced_table.csv`**: ضرایب مدل — `intercept`، `log(parameter count)` (اثر اندازهٔ مدل)، و `R_squared`.
- **`reproduced_summary_by_model.csv`**: خلاصه به‌ازای هر مدل — تعداد مشاهدات، میانگین persuasion و میانگین `log_param_count` (برای همهٔ مدل‌های موجود در داده، از جمله pythia، Llama، Qwen، Yi، falcon و غیره).

اسکریپت علاوه بر ذخیرهٔ CSV، هر دو جدول را در کنسول هم چاپ می‌کند.

**تفسیر:** ضریب مثبت برای `log(parameter count)` با نتیجهٔ مقاله هم‌خوان است: مدل‌های بزرگ‌تر به‌طور میانگین پیام متقاعدکننده‌تری تولید می‌کنند؛ R² نسبتاً کم نشان می‌دهد بخش زیادی از واریانس به عوامل دیگر (مثلاً موضوع، فرمول‌بندی پرامپت) وابسته است.

---

### مرحله ۲: ۱۰ پرامپت سیاسی و مقایسهٔ اقناع‌پذیری

**هدف:** (۱) تعریف **۱۰ پرامپت سیاسی** و ذخیرهٔ آن‌ها در یک فایل CSV؛ (۲) مقایسهٔ **اقناع‌پذیری** (persuasiveness) وقتی فقط موضوعات متناظر با این ۱۰ پرامپت استفاده می‌شوند در برابر همهٔ پرامپت‌های پروژه — یعنی بررسی اینکه آیا «پرامپت سیاسی‌تر» دادن بر اقناع‌پذیری تأثیر می‌گذارد یا خیر.

**۱۰ پرامپت سیاسی:** موضوعات شامل الغای electoral college، محدودیت دورهٔ کنگره، شرط کار برای مدیکید، بهداشت وتران‌ها، حقوق بازنشستگی، کمک خارجی، حبس انفرادی، مرز/خودکشی، حق رای محکومان، و اقدام مثبت هستند. متن کامل هر پرامپت در خروجی ذخیره می‌شود.

**روش مقایسه:**

- ورودی: فایل `main_study/code/analysis/final_data_with_metrics.csv` (شرط AI، متغیر `dv_response_mean` به‌عنوان نمرهٔ اقناع‌پذیری).
- دو گروه: (الف) همهٔ مشاهدات شرط AI؛ (ب) فقط مشاهداتی که `issue_short` آن‌ها با ۹ موضوع متناظر ۱۰ پرامپت سیاسی (در دیتاست پروژه) مطابقت دارد.
- محاسبه: میانگین `dv_response_mean` برای هر گروه و تفاوت آن‌ها؛ در صورت تفاوت ناچیز، نتیجه «بدون اثر» در نظر گرفته می‌شود.

**خروجی‌ها:**

- **`top10_political_prompts.csv`**: لیست ۱۰ پرامپت سیاسی با ستون‌های `rank` (۱ تا ۱۰) و `prompt_full_text` (متن کامل).
- **`persuasiveness_comparison.csv`**: جدول مقایسه — میانگین اقناع‌پذیری برای «همهٔ پرامپت‌های پروژه»، برای «موضوعات ۱۰ پرامپت سیاسی»، تفاوت، و نتیجه (آیا ۱۰ پرامپت سیاسی‌تر تأثیری بر اقناع‌پذیری گذاشته‌اند یا خیر).

**تفسیر:** در تحلیل انجام‌شده، استفاده از موضوعات متناظر با ۱۰ پرامپت سیاسی‌تر نسبت به همهٔ پرامپت‌های پروژه تفاوت معنادار یا قابل‌توجهی در اقناع‌پذیری ایجاد نکرده است (نتیجهٔ ذخیره‌شده: بدون اثر یا تفاوت ناچیز).

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

**لاگ اجرا:** فایل `assignment_deliverables/run_log.txt` شامل خروجی ترمینال برای مراحل اجرا است.

---

## اجرای یک‌جا و ذخیرهٔ نتایج

اسکریپت **`assignment_deliverables/run_and_save_results.py`** منطق مرحلهٔ ۱ و ۲ را با هم اجرا می‌کند و همهٔ خروجی‌ها را در `results/` ذخیره می‌کند:

- `reproduced_table.csv`
- `reproduced_summary_by_model.csv`
- `top10_political_prompts.csv`
- `persuasiveness_comparison.csv`

برای به‌روزرسانی نتایج با یک دستور:

```bash
python assignment_deliverables/run_and_save_results.py
```

---

## نحوهٔ ران گرفتن (`assignment_deliverables`)

همهٔ دستورات از **ریشهٔ پروژه** اجرا شوند.

### پیش‌نیاز

```bash
pip install pandas numpy scikit-learn
```

### مرحله ۱: بازتولید جدول نتیجهٔ مقاله

```bash
python assignment_deliverables/step1_reproduce_table/reproduce_table.py
```

خروجی: `assignment_deliverables/results/reproduced_table.csv` و `reproduced_summary_by_model.csv` (و چاپ همان جداول در کنسول).

### مرحله ۲: ۱۰ پرامپت سیاسی و مقایسهٔ اقناع‌پذیری

```bash
python assignment_deliverables/step2_baseline_and_dataset/baseline_comparison.py
```

خروجی: `assignment_deliverables/results/top10_political_prompts.csv` و `persuasiveness_comparison.csv`.

### مرحله ۳: اسکریپت اجرا روی فایل ورودی CSV

```bash
python assignment_deliverables/run_on_input.py --input_csv assignment_deliverables/example_input.csv --output_csv assignment_deliverables/results/example_output.csv
```

خروجی: `assignment_deliverables/results/example_output.csv` (ستون‌های پاسخ و تعداد کلمه).

پارامترهای اختیاری: `--input_csv`، `--output_csv`، `--text_column` (نام ستون متن).

---

## فایل‌های خروجی در `results/`

| فایل | منبع | محتوا |
|------|------|--------|
| `reproduced_table.csv` | مرحله ۱ | ضرایب رگرسیون (intercept، log parameter count، R²) |
| `reproduced_summary_by_model.csv` | مرحله ۱ | خلاصه به‌ازای هر مدل (n، mean_persuasion، mean_log_param) |
| `top10_political_prompts.csv` | مرحله ۲ | ۱۰ پرامپت سیاسی (rank، prompt_full_text) |
| `persuasiveness_comparison.csv` | مرحله ۲ | مقایسهٔ اقناع‌پذیری (همهٔ پرامپت‌ها vs ۱۰ پرامپت سیاسی) و نتیجه |
| `example_output.csv` | مرحله ۳ | خروجی نمونه برای دو پرامپت (response، response_word_count، timestamp) |

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
