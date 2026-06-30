from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
IMAGE_DIR = BASE_DIR / "images"

SENTIMENT_COLORS = {
    "Negatif": "#ef4444",
    "Netral": "#94a3b8",
    "Positif": "#2563eb",
}

TOPIC_SUMMARY = [
    {
        "title": "Paket Hilang, Rusak, dan Refund",
        "count": "1.238 tweet",
        "description": "Paket rusak atau hilang, refund lambat, uang tertahan, dan kecewa pada layanan brand.",
        "keywords": ["hilang", "paket", "rusak", "telat", "refund", "uang", "kecewa", "brand"],
    },
    {
        "title": "Promo, Ongkir, dan Pengiriman",
        "count": "97 tweet",
        "description": "Diskusi promo aplikasi, ongkir, diskon, dan aktivitas event belanja.",
        "keywords": ["kirim", "paket", "ongkir", "diskon", "aplikasi", "promo", "spesial"],
    },
    {
        "title": "Kurir, Resi, dan Status Barang",
        "count": "570 tweet",
        "description": "Keluhan operasional tentang kurir, resi, status pengiriman, dan respons bantuan.",
        "keywords": ["kurir", "resi", "barang", "hilang", "dikirim", "kak", "gratis"],
    },
]


st.set_page_config(
    page_title="Dashboard War Kredibilitas Brand",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_DIR / "hasil_utama.csv")
    issues = pd.read_csv(DATA_DIR / "issue.csv")
    accounts = pd.read_csv(DATA_DIR / "top_accounts.csv")
    edges = pd.read_csv(DATA_DIR / "edge_list.csv")
    return df, issues, accounts, edges


df, issue_df, top_accounts_df, edges_df = load_data()

for column in ["brand", "kategori", "Sentiment", "topic_label", "username", "full_text"]:
    if column in df.columns:
        df[column] = df[column].fillna("-")


def fmt_int(value):
    return f"{int(value):,}".replace(",", ".")


def fmt_pct(value):
    return f"{value:.1f}%"


def short_text(value, limit=135):
    text = " ".join(str(value).split())
    return f"{text[:limit]}..." if len(text) > limit else text


def section_title(eyebrow, title, anchor=None):
    anchor_html = f" id='{anchor}'" if anchor else ""
    st.markdown(
        f"""
        <div{anchor_html} class="section-head">
            <div class="eyebrow">{eyebrow}</div>
            <h2>{title}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, note, primary=False):
    kind = " primary" if primary else ""
    st.markdown(
        f"""
        <div class="metric-card{kind}">
            <span>{label}</span>
            <strong>{value}</strong>
            <p>{note}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_image(path):
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.info(f"Gambar belum tersedia: {path.name}")


def chart_config():
    return {"displayModeBar": False, "responsive": True}


def make_brand_chart(data):
    grouped = (
        data.groupby(["kategori", "brand", "Sentiment"])
        .size()
        .reset_index(name="Jumlah")
    )
    fig = px.bar(
        grouped,
        x="brand",
        y="Jumlah",
        color="Sentiment",
        facet_col="kategori",
        barmode="group",
        color_discrete_map=SENTIMENT_COLORS,
        category_orders={"Sentiment": ["Negatif", "Netral", "Positif"]},
    )
    fig.for_each_annotation(lambda item: item.update(text=item.text.split("=")[-1]))
    fig.update_layout(
        height=270,
        margin=dict(l=8, r=8, t=34, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        legend_title_text="",
        legend=dict(orientation="h", y=-0.24, x=0.25),
        font=dict(color="#596a62", size=12),
    )
    fig.update_xaxes(title=None, tickangle=0)
    fig.update_yaxes(title=None, gridcolor="#edf1ed")
    return fig


def make_sentiment_chart(data):
    sentiment = (
        data["Sentiment"]
        .value_counts()
        .reindex(["Positif", "Netral", "Negatif"])
        .fillna(0)
        .reset_index()
    )
    sentiment.columns = ["Sentiment", "Jumlah"]
    fig = px.pie(
        sentiment,
        names="Sentiment",
        values="Jumlah",
        hole=0.62,
        color="Sentiment",
        color_discrete_map=SENTIMENT_COLORS,
    )
    fig.update_layout(
        height=230,
        margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        font=dict(color="#596a62", size=12),
    )
    return fig, sentiment


def make_issue_chart(data, issues):
    filtered_issues = issues.copy()
    if set(data["kategori"].unique()) != set(df["kategori"].unique()):
        filtered_issues = filtered_issues[filtered_issues["Kategori"].isin(data["kategori"].unique())]
    fig = px.bar(
        filtered_issues.sort_values("Jumlah", ascending=True),
        x="Jumlah",
        y="Isu",
        color="Kategori",
        orientation="h",
        color_discrete_map={"E-Commerce": "#1d4ed8", "Ekspedisi": "#60a5fa"},
    )
    fig.update_layout(
        height=270,
        margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        legend_title_text="",
        legend=dict(orientation="h", y=1.1, x=0.52),
        font=dict(color="#596a62", size=12),
    )
    fig.update_xaxes(title=None, gridcolor="#edf1ed")
    fig.update_yaxes(title=None)
    return fig


def enrich_accounts(accounts, edges):
    edge_stats = {}
    for _, edge in edges.iterrows():
        for account in [edge.get("Source"), edge.get("Target")]:
            if pd.isna(account) or not account:
                continue
            key = str(account).lower()
            stats = edge_stats.setdefault(key, {"relations": 0, "brands": set(), "categories": set()})
            stats["relations"] += 1
            if pd.notna(edge.get("Brand")):
                stats["brands"].add(edge.get("Brand"))
            if pd.notna(edge.get("Kategori")):
                stats["categories"].add(edge.get("Kategori"))

    enriched = accounts.sort_values("Betweenness", ascending=False).copy()
    keys = enriched["Akun"].str.lower()
    enriched["Relasi"] = keys.map(lambda key: edge_stats.get(key, {}).get("relations", 0))
    enriched["Brand"] = keys.map(lambda key: ", ".join(sorted(edge_stats.get(key, {}).get("brands", []))) or "-")
    enriched["Kategori"] = keys.map(lambda key: ", ".join(sorted(edge_stats.get(key, {}).get("categories", []))) or "-")
    enriched["Urgensi"] = [
        "Tinggi" if index < 3 and row.Betweenness > 0 else "Sedang" if index < 10 and row.Betweenness > 0 else "Monitor"
        for index, row in enumerate(enriched.itertuples())
    ]
    enriched["Betweenness"] = enriched["Betweenness"].map(lambda value: f"{value:.6f}")
    enriched["Akun"] = "@" + enriched["Akun"].astype(str)
    return enriched


st.markdown(
    """
    <style>
    :root{
        --bg:#eef4ff;
        --panel:#ffffff;
        --text:#172033;
        --muted:#66758a;
        --line:#dbe7f6;
        --green:#2563eb;
        --green-dark:#1d4ed8;
        --green-soft:#dbeafe;
        --shadow:0 18px 42px rgba(30,64,175,.10);
    }

    .stApp{
        background:linear-gradient(140deg,#eef4ff 0%,#f8fbff 44%,#edf6ff 100%);
    }

    html, body, [class*="css"]{
        font-family:Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color:var(--text);
    }

    .main .block-container{
        max-width:1220px;
        padding:18px 22px 44px;
    }

    header[data-testid="stHeader"]{
        background:transparent;
    }

    section[data-testid="stSidebar"]{
        background:transparent;
    }

    section[data-testid="stSidebar"] > div{
        background:#fff;
        border:1px solid rgba(255,255,255,.95);
        border-radius:30px;
        box-shadow:var(--shadow);
        margin:18px 10px 18px 18px;
        padding:20px 16px;
    }

    .sidebar-brand{
        display:flex;
        align-items:center;
        gap:14px;
        margin:4px 0 18px;
    }

    .sidebar-logo{
        width:48px;
        height:48px;
        border-radius:16px;
        display:grid;
        place-items:center;
        background:var(--green);
        color:#fff;
        font-weight:900;
        box-shadow:0 14px 28px rgba(37,99,235,.22);
    }

    .sidebar-title{
        font-size:21px;
        font-weight:900;
        letter-spacing:-.03em;
        line-height:1.05;
    }

    .sidebar-subtitle{
        color:#7c8b84;
        font-size:13px;
        margin-top:4px;
    }

    .nav-link{
        display:block;
        padding:8px 12px;
        border-radius:14px;
        color:#53665d !important;
        text-decoration:none !important;
        font-weight:800;
        margin-bottom:4px;
    }

    .nav-link:hover{
        background:#eff6ff;
        color:var(--green-dark) !important;
    }

    .side-note{
        margin-top:14px;
        padding:14px;
        border-radius:20px;
        background:#eff6ff;
        border:1px solid #dbeafe;
        color:#63756d;
        line-height:1.45;
        font-size:13px;
    }

    .side-note strong{
        display:block;
        color:var(--green-dark);
        font-size:15px;
        margin-bottom:6px;
    }

    .hero-card,
    .metric-card{
        background:#fff;
        border:1px solid rgba(255,255,255,.95);
        border-radius:26px;
        box-shadow:var(--shadow);
    }

    .hero-card{
        display:flex;
        justify-content:space-between;
        align-items:center;
        gap:18px;
        padding:22px 26px;
        margin-bottom:14px;
    }

    .hero-card h1{
        margin:6px 0 8px;
        color:var(--text);
        font-size:32px;
        font-weight:900;
        line-height:1.12;
        letter-spacing:-.035em;
    }

    .hero-card p{
        margin:0;
        color:var(--muted);
        font-size:15px;
        font-weight:600;
    }

    .dataset-pill{
        flex:0 0 auto;
        padding:13px 17px;
        border-radius:999px;
        background:#f8fbff;
        border:1px solid var(--line);
        color:#40554b;
        font-size:13px;
        font-weight:900;
    }

    .metric-card{
        min-height:112px;
        padding:16px 18px;
        position:relative;
        overflow:hidden;
    }

    .metric-card:after{
        content:"";
        position:absolute;
        right:-36px;
        top:-36px;
        width:92px;
        height:92px;
        border-radius:50%;
        background:var(--green-soft);
    }

    .metric-card.primary{
        background:linear-gradient(145deg,#2563eb 0%,#1d4ed8 100%);
        color:#fff;
    }

    .metric-card.primary:after{
        background:rgba(255,255,255,.17);
    }

    .metric-card span{
        display:block;
        color:#6b7b73;
        font-size:12px;
        font-weight:900;
        margin-bottom:12px;
    }

    .metric-card.primary span,
    .metric-card.primary p{
        color:#eff6ff;
    }

    .metric-card strong{
        display:block;
        font-size:29px;
        font-weight:900;
        line-height:1;
        letter-spacing:-.05em;
        margin-bottom:9px;
        color:inherit;
    }

    .metric-card p{
        margin:0;
        color:var(--green-dark);
        font-size:13px;
        line-height:1.35;
        font-weight:900;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]{
        border:1px solid rgba(255,255,255,.94);
        border-radius:22px;
        background:#fff;
        box-shadow:var(--shadow);
        height:auto !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] > div{
        padding:16px 18px;
        height:auto !important;
        min-height:0 !important;
    }

    div[data-testid="stHorizontalBlock"]{
        align-items:flex-start;
        gap:1rem;
    }

    .section-head{
        margin-bottom:10px;
    }

    .eyebrow{
        color:var(--green);
        font-size:12px;
        font-weight:900;
        letter-spacing:.14em;
        text-transform:uppercase;
        margin-bottom:6px;
    }

    .section-head h2{
        margin:0;
        color:var(--text);
        font-size:26px;
        font-weight:900;
        line-height:1.18;
        letter-spacing:-.035em;
    }

    .topic-panel{
        padding:18px;
        border-radius:22px;
        background:linear-gradient(145deg,#2563eb 0%,#1e40af 100%);
        color:#fff;
        box-shadow:var(--shadow);
        margin-bottom:12px;
    }

    .score-row{
        display:flex;
        justify-content:space-between;
        gap:12px;
        margin-bottom:18px;
        font-weight:900;
    }

    .score-row strong{
        font-size:24px;
    }

    .topic-card{
        padding:14px;
        border-radius:18px;
        background:#fff;
        color:var(--text);
        border:1px solid rgba(255,255,255,.92);
        box-shadow:0 10px 24px rgba(30,64,175,.08);
        margin-bottom:10px;
    }

    .topic-card h3{
        margin:0 0 8px;
        font-size:18px;
        font-weight:900;
        line-height:1.22;
    }

    .topic-card p{
        margin:0 0 10px;
        color:#64756d;
        font-size:14px;
        font-weight:600;
        line-height:1.45;
    }

    .topic-count{
        float:right;
        padding:5px 8px;
        border-radius:999px;
        background:var(--green-soft);
        color:var(--green-dark);
        font-size:11px;
        font-weight:900;
        margin-left:8px;
    }

    .tag{
        display:inline-block;
        margin:3px 3px 0 0;
        padding:6px 9px;
        border-radius:999px;
        background:var(--green-soft);
        color:var(--green-dark);
        font-size:11px;
        font-weight:900;
    }

    .summary-grid{
        display:grid;
        grid-template-columns:repeat(3,minmax(0,1fr));
        gap:10px;
        margin:10px 0;
    }

    .summary-grid.two{
        grid-template-columns:repeat(2,minmax(0,1fr));
    }

    .summary-box{
        padding:12px;
        border-radius:16px;
        border:1px solid var(--line);
        background:#f8fbff;
    }

    .summary-box span{
        display:block;
        margin-bottom:8px;
        color:#65736c;
        font-size:12px;
        font-weight:900;
        text-transform:uppercase;
        letter-spacing:.06em;
    }

    .summary-box strong{
        display:block;
        overflow:hidden;
        color:var(--text);
        font-size:19px;
        font-weight:900;
        white-space:nowrap;
        text-overflow:ellipsis;
    }

    .stPlotlyChart{
        border-radius:18px;
        overflow:hidden;
    }

    div[data-testid="stDataFrame"]{
        border-radius:16px;
        overflow:hidden;
    }

    [data-testid="stImage"] img{
        border-radius:16px;
        border:1px solid var(--line);
        background:#fff;
        max-height:360px;
        object-fit:contain;
    }

    div[data-testid="stImage"]{
        text-align:center;
    }

    div[data-testid="stDataFrame"]{
        max-width:100%;
    }

    div[data-testid="stElementContainer"]{
        margin-bottom:.45rem;
    }

    @media (max-width:900px){
        .hero-card{
            align-items:flex-start;
            flex-direction:column;
        }

        .summary-grid,
        .summary-grid.two{
            grid-template-columns:1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">.✦ ݁˖</div>
            <div>
                <div class="sidebar-title">Dashboard</div>
                <div class="sidebar-subtitle">E-Commerce & Logistics</div>
            </div>
        </div>
        <a class="nav-link" href="#dashboard-analytics">Dashboard</a>
        <a class="nav-link" href="#brand-analysis">Sentimen</a>
        <a class="nav-link" href="#top-issue">Isu & Keluhan</a>
        <a class="nav-link" href="#topic-modeling">Topic Modeling</a>
        <a class="nav-link" href="#wordcloud">WordCloud</a>
        <a class="nav-link" href="#social-network-analysis">SNA</a>
        <a class="nav-link" href="#data-tweet">Dataset</a>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.caption("Filter global")
    selected_categories = st.multiselect(
        "Kategori",
        sorted(df["kategori"].dropna().unique()),
        default=sorted(df["kategori"].dropna().unique()),
    )
    selected_brands = st.multiselect(
        "Brand",
        sorted(df["brand"].dropna().unique()),
        default=sorted(df["brand"].dropna().unique()),
    )
    selected_sentiments = st.multiselect(
        "Sentimen",
        ["Negatif", "Netral", "Positif"],
        default=["Negatif", "Netral", "Positif"],
    )
    keyword = st.text_input("Cari tweet / user")

    st.markdown(
        """
        <div class="side-note">
            <strong>E-Commerce & Ekspedisi Analytics</strong>
            Filter di atas mengubah KPI, chart, evidence, dan tabel.
        </div>
        """,
        unsafe_allow_html=True,
    )


filtered_df = df[
    df["kategori"].isin(selected_categories)
    & df["brand"].isin(selected_brands)
    & df["Sentiment"].isin(selected_sentiments)
].copy()

if keyword:
    query = keyword.lower()
    mask = (
        filtered_df["full_text"].astype(str).str.lower().str.contains(query, regex=False)
        | filtered_df["username"].astype(str).str.lower().str.contains(query, regex=False)
    )
    filtered_df = filtered_df[mask]

if filtered_df.empty:
    st.warning("Tidak ada data untuk kombinasi filter ini.")
    st.stop()


total_tweets = len(filtered_df)
negative_total = int((filtered_df["Sentiment"] == "Negatif").sum())
negative_share = negative_total / total_tweets * 100 if total_tweets else 0
brand_count = filtered_df["brand"].nunique()
top_issue = issue_df.sort_values("Jumlah", ascending=False).iloc[0]
top_account = top_accounts_df.sort_values("Betweenness", ascending=False).iloc[0]

st.markdown(
    """
    <div id="dashboard-analytics" class="hero-card">
        <div>
            <div class="eyebrow">Dashboard Analytics</div>
            <h1>War Kredibilitas Brand: E-Commerce & Ekspedisi</h1>
            <p>Analisis sentimen, topic modeling, keluhan, dan Social Network Analysis.</p>
        </div>
        <div class="dataset-pill">Twitter / X Dataset</div>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(5)
with metric_cols[0]:
    metric_card("Total Tweet", fmt_int(total_tweets), "Tweet sesuai filter", primary=True)
with metric_cols[1]:
    metric_card("Distribusi Sentimen", fmt_pct(negative_share), "Tweet negatif")
with metric_cols[2]:
    metric_card("Brand Analysis", str(brand_count), "Brand aktif")
with metric_cols[3]:
    metric_card("Top Issue", fmt_int(top_issue["Jumlah"]), f"{top_issue['Isu']} terbanyak")
with metric_cols[4]:
    metric_card("Akurasi Model", "82.68%", "Naive Bayes + TF-IDF")

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

left, right = st.columns([1.65, 1], gap="medium")
with left.container(border=True):
    section_title("Brand Analysis", "Distribusi Sentimen per Brand", "brand-analysis")
    st.plotly_chart(make_brand_chart(filtered_df), use_container_width=True, config=chart_config())

with right.container(border=True):
    section_title("Komposisi", "Sentimen E-Commerce & Logistics")
    sentiment_fig, sentiment_table = make_sentiment_chart(filtered_df)
    st.plotly_chart(sentiment_fig, use_container_width=True, config=chart_config())
    st.dataframe(sentiment_table, hide_index=True, use_container_width=True, height=140)

left, right = st.columns([1.65, 1], gap="medium")
with left.container(border=True):
    section_title("Top Issue", "Isu Komplain Terbanyak", "top-issue")
    st.plotly_chart(make_issue_chart(filtered_df, issue_df), use_container_width=True, config=chart_config())

with right.container(border=True):
    section_title("Evidence Tweets", "Keluhan User")
    evidence = (
        filtered_df[filtered_df["Sentiment"].eq("Negatif")]
        .sort_values("favorite_count", ascending=False)
        .head(8)
    )
    if evidence.empty:
        st.info("Tidak ada tweet negatif pada filter ini.")
    else:
        evidence_table = evidence.assign(
            User="@" + evidence["username"].astype(str),
            Tweet=evidence["full_text"].map(lambda value: short_text(value, 82)),
        )[["kategori", "User", "Tweet"]]
        st.dataframe(evidence_table, hide_index=True, use_container_width=True, height=270)

left, right = st.columns([1.65, 1], gap="medium")
with left.container(border=True):
    section_title("Topic Modeling", "Klasterisasi Topik", "topic-modeling")
    show_image(IMAGE_DIR / "klasterisasi.png")
    st.markdown(
        """
        <div class="eyebrow" style="margin-top:14px">Evaluasi Klasifikasi Sentimen - TF-IDF</div>
        <div class="summary-grid">
            <div class="summary-box"><span>F1 Macro</span><strong>0.4246</strong></div>
            <div class="summary-box"><span>F1 Weighted</span><strong>0.7850</strong></div>
            <div class="summary-box"><span>Support Test</span><strong>381</strong></div>
        </div>
        <p style="color:#61736b;line-height:1.45;margin:0">
            Dipakai untuk membaca sentimen komparatif brand. Kelas netral tetap perlu dibaca hati-hati karena jumlah datanya lebih kecil.
        </p>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
        <div class="topic-panel">
            <div class="score-row">
                <span>Silhouette Score</span>
                <strong>0.5003</strong>
            </div>
            <h2 style="margin:0;font-size:24px">Interpretasi Topik</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for index, topic in enumerate(TOPIC_SUMMARY, start=1):
        tags = "".join(f"<span class='tag'>{item}</span>" for item in topic["keywords"])
        st.markdown(
            f"""
            <div class="topic-card">
                <span class="topic-count">{topic["count"]}</span>
                <h3>Topik {index}: {topic["title"]}</h3>
                <p>{topic["description"]}</p>
                {tags}
            </div>
            """,
            unsafe_allow_html=True,
        )

with st.container(border=True):
    section_title("WordCloud", "Wordcloud Isu Keluhan", "wordcloud")
    show_image(IMAGE_DIR / "wordcloud.png")

centrality_df = enrich_accounts(top_accounts_df, edges_df)

left, right = st.columns([1.65, 1], gap="medium")
with left.container(border=True):
    section_title("Social Network Analysis", "Jaringan Akun", "social-network-analysis")
    show_image(IMAGE_DIR / "sna_graph.png")

with right.container(border=True):
    section_title("Centrality", "Akun Prioritas")
    st.markdown(
        f"""
        <div class="summary-grid two">
            <div class="summary-box"><span>Prioritas Utama</span><strong>@{top_account["Akun"]}</strong></div>
            <div class="summary-box"><span>Betweenness</span><strong>{top_account["Betweenness"]:.6f}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    account_query = st.text_input("Cari akun, brand, kategori", key="account_search")
    shown_accounts = centrality_df
    if account_query:
        query = account_query.lower()
        shown_accounts = centrality_df[
            centrality_df.astype(str).apply(
                lambda row: row.str.lower().str.contains(query, regex=False).any(),
                axis=1,
            )
        ]
    st.dataframe(
        shown_accounts[["Akun", "Brand", "Relasi", "Betweenness", "Urgensi"]].head(12),
        hide_index=True,
        use_container_width=True,
        height=300,
    )

with st.container(border=True):
    section_title("Data Tweet", "Tweet Hasil Analisis", "data-tweet")
    table_controls = st.columns([1.2, 1.2, 1])
    with table_controls[0]:
        topic_filter = st.selectbox(
            "Fokus Topik",
            [
                "Data sesuai filter global",
                "Komplain negatif",
                "Paket hilang/rusak/refund",
                "Promo, ongkir, pengiriman",
                "Kurir, resi, status barang",
            ],
        )
    with table_controls[1]:
        table_search = st.text_input("Cari dalam tabel")
    with table_controls[2]:
        row_limit = st.selectbox("Tampil", [25, 50, 100], index=0)

    table_df = filtered_df.copy()
    if topic_filter == "Komplain negatif":
        table_df = table_df[table_df["Sentiment"].eq("Negatif")]
    elif topic_filter != "Data sesuai filter global":
        topic_map = {
            "Paket hilang/rusak/refund": "Paket hilang/rusak/refund",
            "Promo, ongkir, pengiriman": "Promo, ongkir, dan pengiriman",
            "Kurir, resi, status barang": "Kurir, resi, dan status barang",
        }
        table_df = table_df[
            table_df["topic_label"].astype(str).str.contains(topic_map[topic_filter], case=False, na=False)
        ]

    if table_search:
        query = table_search.lower()
        table_df = table_df[
            table_df.astype(str).apply(
                lambda row: row.str.lower().str.contains(query, regex=False).any(),
                axis=1,
            )
        ]

    display_df = table_df.head(row_limit).assign(
        Username=lambda data: "@" + data["username"].astype(str),
        Tweet=lambda data: data["full_text"].map(short_text),
    )
    st.caption(f"{fmt_int(len(table_df))} data sesuai filter")
    st.dataframe(
        display_df[["Username", "brand", "kategori", "Sentiment", "topic_label", "Tweet"]],
        hide_index=True,
        use_container_width=True,
        height=430,
    )
