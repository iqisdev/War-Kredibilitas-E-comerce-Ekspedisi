import pandas as pd
import json

# ======================
# LOAD DATA CSV
# ======================
df = pd.read_csv("data/hasil_utama.csv")

# ======================
# CLEANING BASIC
# ======================
df.columns = [col.lower() for col in df.columns]

# pastikan kolom ada
if "sentimen" not in df.columns:
    df["sentimen"] = "netral"

# ======================
# KPI DASHBOARD
# ======================
total_tweet = len(df)
positif = len(df[df["sentimen"] == "positif"])
negatif = len(df[df["sentimen"] == "negatif"])
netral = len(df[df["sentimen"] == "netral"])

akun_unik = df["username"].nunique() if "username" in df.columns else 0

# ======================
# TOP ISSUE
# ======================

try:

    issue_df = pd.read_csv("data/issue.csv")

    # rapikan nama kolom
    issue_df.columns = issue_df.columns.str.strip()

    # sesuaikan kapitalisasi
    if "Isu" not in issue_df.columns:
        issue_df.rename(columns={"issue": "Isu"}, inplace=True)

    if "Jumlah" not in issue_df.columns:
        issue_df.rename(columns={"jumlah": "Jumlah"}, inplace=True)

    # urutkan berdasarkan jumlah terbesar
    issue_df = issue_df.sort_values(
        by="Jumlah",
        ascending=False
    )

    # ambil Top 5
    issue_df = issue_df.head(5)

    top_issue = issue_df.to_dict(orient="records")

except Exception as e:

    print(e)

    top_issue = []
# ======================
# WORDCLOUD DATA
# ======================
if "tweet" in df.columns:
    words = " ".join(df["tweet"].astype(str)).split()
else:
    words = []

word_freq = {}
for w in words:
    w = w.lower()
    if len(w) > 2:
        word_freq[w] = word_freq.get(w, 0) + 1

wordcloud_data = word_freq

# ======================
# STRUCTURE DASHBOARD JSON
# ======================
dashboard_data = {
    "overview": {
        "total_tweet": total_tweet,
        "positif": positif,
        "negatif": negatif,
        "netral": netral,
        "akun_unik": akun_unik
    },
    "topIssues": top_issue,
    "wordcloud": wordcloud_data
}

# ======================
# SAVE JSON
# ======================
with open("dashboard_data.json", "w", encoding="utf-8") as f:
    json.dump(dashboard_data, f, indent=4)

print("Export selesai -> dashboard_data.json berhasil dibuat")