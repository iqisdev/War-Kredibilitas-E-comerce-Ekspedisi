import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
import numpy as np

st.set_page_config(
    page_title="War Kredibilitas Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== CSS =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F0F2EC;
}

.block-container {
    padding-top: 1.2rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    max-width: 100%;
}

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E5E7EB;
    min-width: 210px !important;
    max-width: 210px !important;
}

[data-testid="stSidebar"] .block-container {
    padding: 0 !important;
}

.sidebar-logo-area {
    padding: 18px 18px 10px 18px;
    border-bottom: 1px solid #F0F2EC;
}

.sidebar-logo-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #2F6B47, #5CA370);
    border-radius: 10px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 18px; margin-bottom: 6px;
}

.sidebar-brand {
    font-size: 14px; font-weight: 800; color: #1F3D2B; line-height: 1.1;
}

.sidebar-brand-sub {
    font-size: 11px; color: #6B7280;
}

.sidebar-section-label {
    font-size: 10px; font-weight: 700; color: #9CA3AF;
    letter-spacing: 0.08em; text-transform: uppercase;
    padding: 16px 18px 6px 18px;
}

.sidebar-menu-item {
    display: flex; align-items: center; gap: 10px;
    padding: 9px 18px; font-size: 13px; font-weight: 500;
    color: #4B5563; cursor: pointer; border-radius: 0;
    transition: background 0.15s;
}

.sidebar-menu-item.active {
    background: #EEF4F0;
    color: #1F3D2B;
    font-weight: 700;
    border-left: 3px solid #2F6B47;
}

.sidebar-menu-item:hover {
    background: #F6F7F3;
}

.sidebar-divider {
    border: none; border-top: 1px solid #F0F2EC; margin: 8px 0;
}

/* ---- FILTER SECTION ---- */
.sidebar-filter-area {
    padding: 0 14px;
}

/* ---- DOWNLOAD CARD ---- */
.sidebar-download-card {
    margin: 14px; padding: 14px;
    background: linear-gradient(135deg, #EEF4F0, #F6F7F3);
    border-radius: 14px; border: 1px solid #D5E4DB;
}

.sidebar-download-title {
    font-size: 13px; font-weight: 700; color: #1F3D2B; margin-bottom: 4px;
}

.sidebar-download-sub {
    font-size: 11px; color: #6B7280; margin-bottom: 10px;
}

/* ---- HEADER ---- */
.page-header {
    display: flex; align-items: flex-start; justify-content: space-between;
    margin-bottom: 16px;
}

.page-title {
    font-size: 26px; font-weight: 800; color: #111827; line-height: 1.2;
}

.page-subtitle {
    font-size: 13px; color: #6B7280; margin-top: 3px;
}

/* ---- KPI CARDS ---- */
.kpi-wrap {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 16px 18px 10px 18px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 4px 16px rgba(17,24,39,0.05);
    position: relative;
    overflow: hidden;
    min-height: 130px;
}

.kpi-wrap.green {
    background: linear-gradient(135deg, #4E9A6A, #2F6B47);
}

.kpi-label {
    font-size: 11px; font-weight: 700; color: #6B7280;
    text-transform: uppercase; letter-spacing: 0.05em;
}

.kpi-wrap.green .kpi-label { color: #A7D5BA; }

.kpi-icon {
    position: absolute; top: 14px; right: 14px;
    width: 30px; height: 30px;
    background: #F3F4F6; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px;
}

.kpi-wrap.green .kpi-icon { background: rgba(255,255,255,0.18); }

.kpi-num {
    font-size: 32px; font-weight: 800; color: #111827;
    line-height: 1.1; margin-top: 8px;
}

.kpi-wrap.green .kpi-num { color: #FFFFFF; }

.kpi-trend {
    font-size: 11px; color: #6B7280; margin-top: 4px;
}

.kpi-trend span.up { color: #10B981; font-weight: 700; }
.kpi-trend span.down { color: #EF4444; font-weight: 700; }
.kpi-wrap.green .kpi-trend { color: #C6EDD6; }
.kpi-wrap.green .kpi-trend span.up { color: #A7F3D0; }

/* ---- CHART CARDS ---- */
.chart-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 16px 18px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 4px 16px rgba(17,24,39,0.05);
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.chart-title {
    font-size: 14px; font-weight: 700; color: #111827;
    margin-bottom: 0;
}

.chart-sub {
    font-size: 11px; color: #9CA3AF;
    margin-bottom: 0;
}

.chart-card .stPlotlyChart {
    margin-top: 0;
}

/* ---- RIGHT PANEL ---- */
.right-panel {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 16px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 4px 16px rgba(17,24,39,0.05);
}

.project-item {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 0; border-bottom: 1px solid #F3F4F6;
}

.project-dot {
    width: 34px; height: 34px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
}

.project-name { font-size: 12px; font-weight: 700; color: #111827; }
.project-meta { font-size: 10px; color: #9CA3AF; }

.time-tracker {
    background: linear-gradient(135deg, #1F3D2B, #2F6B47);
    border-radius: 14px; padding: 16px; margin-top: 14px; color: white;
}

.tracker-label { font-size: 10px; color: #A7D5BA; font-weight: 600; letter-spacing: 0.05em; }
.tracker-time { font-size: 30px; font-weight: 800; letter-spacing: 0.05em; margin: 4px 0; }
.tracker-sub { font-size: 11px; color: #A7D5BA; }

.insight-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 16px 18px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 4px 16px rgba(17,24,39,0.05);
    margin-top: 14px;
}

.insight-title {
    font-size: 14px; font-weight: 700; color: #111827; margin-bottom: 8px;
}

.insight-text {
    font-size: 12px; color: #374151; line-height: 1.6;
}

/* ---- SEARCH BAR ---- */
.search-bar {
    display: flex; align-items: center; gap: 10px;
    background: #FFFFFF; border-radius: 10px;
    border: 1px solid #E5E7EB;
    padding: 8px 14px;
    font-size: 13px; color: #9CA3AF;
    margin-bottom: 18px;
}

/* ---- STREAMLIT OVERRIDES ---- */
.stSelectbox > div > div {
    border-radius: 10px !important;
    font-size: 12px !important;
}

div[data-testid="stMetricValue"] { font-weight: 800; }

.stMultiSelect [data-baseweb="tag"] {
    background-color: #EEF4F0 !important;
    color: #1F3D2B !important;
}

</style>
""", unsafe_allow_html=True)

# ===================== LOAD DATA =====================
@st.cache_data
def load_data():
    for fname in ["uas_ecommercekspedisi.csv", "data_dashboard.csv"]:
        if os.path.exists(fname):
            return pd.read_csv(fname)
    # Demo data jika file tidak ada
    np.random.seed(42)
    brands = ["TikTok Shop", "Lazada", "J&T", "SiCepat"]
    kategoris = ["E-Commerce", "Ekspedisi"]
    sentiments = ["Negatif", "Positif", "Netral"]
    n = 1905
    return pd.DataFrame({
        "brand": np.random.choice(brands, n, p=[0.43, 0.31, 0.15, 0.11]),
        "kategori": np.random.choice(kategoris, n, p=[0.6, 0.4]),
        "Sentiment": np.random.choice(sentiments, n, p=[0.54, 0.30, 0.16]),
        "clean_text": np.random.choice([
            "barang telat pengiriman lambat",
            "refund retur tidak diproses",
            "kurir cod tidak ada resi",
            "promo voucher diskon bagus",
            "aplikasi error tidak bisa bayar",
            "paket hilang rusak barang",
            "pengiriman cepat oke layanan baik",
            "tidak bisa checkout aplikasi error"
        ], n)
    })

@st.cache_data
def load_edge_data():
    if os.path.exists("edge_list_ecommerce_ekspedisi.csv"):
        return pd.read_csv("edge_list_ecommerce_ekspedisi.csv")
    nodes = [f"@user{i}" for i in range(1, 30)]
    src = np.random.choice(nodes, 80)
    tgt = np.random.choice(nodes, 80)
    return pd.DataFrame({"Source": src, "Target": tgt})

@st.cache_data
def load_centrality_data():
    if os.path.exists("centrality_ecommerce_ekspedisi.csv"):
        return pd.read_csv("centrality_ecommerce_ekspedisi.csv")
    akun = ["@txtdarionlinechep", "@jntcare", "@tiktokshop_id", "@lazada_id", "@sicepat_id"]
    return pd.DataFrame({
        "Akun": akun,
        "Betweenness_Centrality": [0.0651, 0.0723, 0.0647, 0.0582, 0.0457],
        "Degree": [232, 158, 186, 154, 132]
    })

df = load_data()
edge_df = load_edge_data()
centrality_df = load_centrality_data()

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo-area">
        <div class="sidebar-logo-icon">🛒</div><br>
        <div class="sidebar-brand">WAR KREDIBILITAS</div>
        <div class="sidebar-brand-sub">E-Commerce & Ekspedisi</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">MENU</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-menu-item active">🗂️ &nbsp; Dashboard</div>
    <div class="sidebar-menu-item">😊 &nbsp; Analisis Sentimen</div>
    <div class="sidebar-menu-item">🔥 &nbsp; Top Isu</div>
    <div class="sidebar-menu-item">🏷️ &nbsp; Brand</div>
    <div class="sidebar-menu-item">🚚 &nbsp; Ekspedisi</div>
    <div class="sidebar-menu-item">👤 &nbsp; Akun (SNA)</div>
    <div class="sidebar-menu-item">📄 &nbsp; Data Mentah</div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-label">FILTER</div>', unsafe_allow_html=True)

    with st.container():
        kategori_filter = st.multiselect(
            "Pilih Kategori",
            df["kategori"].dropna().unique().tolist(),
            default=df["kategori"].dropna().unique().tolist(),
            label_visibility="visible"
        )
        brand_filter = st.multiselect(
            "Pilih Brand",
            df["brand"].dropna().unique().tolist(),
            default=df["brand"].dropna().unique().tolist()
        )
        sentimen_filter = st.multiselect(
            "Pilih Sentimen",
            df["Sentiment"].dropna().unique().tolist(),
            default=df["Sentiment"].dropna().unique().tolist()
        )

    st.markdown("""
    <div class="sidebar-download-card">
        <div class="sidebar-download-title">📥 Download Laporan</div>
        <div class="sidebar-download-sub">Unduh laporan analisis dalam format Excel.</div>
    </div>
    """, unsafe_allow_html=True)

    df_filter = df[
        (df["kategori"].isin(kategori_filter)) &
        (df["brand"].isin(brand_filter)) &
        (df["Sentiment"].isin(sentimen_filter))
    ]

    st.download_button(
        "⬇️ Download CSV",
        data=df_filter.to_csv(index=False).encode("utf-8"),
        file_name="hasil_dashboard_uas.csv",
        mime="text/csv",
        use_container_width=True
    )

# ===================== MAIN LAYOUT =====================
main_col, right_col = st.columns([5, 1.35])

with main_col:
    # --- HEADER ---
    hdr_l, hdr_r = st.columns([3, 1])
    with hdr_l:
        st.markdown("""
        <div class="page-title">Dashboard War Kredibilitas Brand 👋</div>
        <div class="page-subtitle">Analisis percakapan Twitter/X terkait E-Commerce & Ekspedisi Logistik</div>
        """, unsafe_allow_html=True)
    with hdr_r:
        st.markdown("<br>", unsafe_allow_html=True)
        btn_l, btn_r = st.columns(2)
        with btn_l:
            st.button("＋ Tambah Filter", use_container_width=True)
        with btn_r:
            st.download_button(
                "⬇️ Import Data",
                data=df_filter.to_csv(index=False).encode("utf-8"),
                file_name="data_export.csv", mime="text/csv",
                use_container_width=True
            )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ---- KPI ----
    total_tweet = len(df_filter)
    total_brand = df_filter["brand"].nunique()
    total_kategori = df_filter["kategori"].nunique()
    sentimen_dominan = df_filter["Sentiment"].value_counts().idxmax() if len(df_filter) else "-"
    total_akun = len(centrality_df)

    # Sparkline helper (tiny plotly line)
    def hex_to_rgba(hex_color, alpha=0.15):
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"

    def mini_line(values, color="#10B981", height=42):
        fig = go.Figure(go.Scatter(
            y=values, mode="lines",
            line=dict(color=color, width=2),
            fill="tozeroy", fillcolor=hex_to_rgba(color)
        ))
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=height, paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)", showlegend=False,
            xaxis=dict(visible=False), yaxis=dict(visible=False)
        )
        return fig

    spark_data = np.random.randint(50, 200, 12).tolist()

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.markdown(f"""
        <div class="kpi-wrap green">
            <div class="kpi-label">Total Tweet</div>
            <div class="kpi-icon">💬</div>
            <div class="kpi-num">{total_tweet:,}</div>
            <div class="kpi-trend"><span class="up">↑ 16.6%</span> dari bulan lalu</div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(mini_line(spark_data, "#A7F3D0"), use_container_width=True, config={"displayModeBar": False})

    with k2:
        st.markdown(f"""
        <div class="kpi-wrap">
            <div class="kpi-label">Total Brand</div>
            <div class="kpi-icon">🏷️</div>
            <div class="kpi-num">{total_brand}</div>
            <div class="kpi-trend"><span class="up">↑ 12.5%</span> dari bulan lalu</div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(mini_line(np.random.randint(1, 6, 12).tolist(), "#6EE7B7"), use_container_width=True, config={"displayModeBar": False})

    with k3:
        st.markdown(f"""
        <div class="kpi-wrap">
            <div class="kpi-label">Kategori</div>
            <div class="kpi-icon">📦</div>
            <div class="kpi-num">{total_kategori}</div>
            <div class="kpi-trend"><span style="color:#6B7280">0%</span> dari bulan lalu</div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(mini_line([2]*12, "#D1D5DB"), use_container_width=True, config={"displayModeBar": False})

    sent_color = "#EF4444" if sentimen_dominan == "Negatif" else "#10B981" if sentimen_dominan == "Positif" else "#F59E0B"
    with k4:
        st.markdown(f"""
        <div class="kpi-wrap">
            <div class="kpi-label">Sentimen Dominan</div>
            <div class="kpi-icon">😐</div>
            <div class="kpi-num" style="color:{sent_color};font-size:26px">{sentimen_dominan}</div>
            <div class="kpi-trend"><span class="down">↓ 8.2%</span> dari bulan lalu</div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(mini_line(np.random.randint(40, 120, 12).tolist(), sent_color), use_container_width=True, config={"displayModeBar": False})

    with k5:
        st.markdown(f"""
        <div class="kpi-wrap">
            <div class="kpi-label">Total Akun SNA</div>
            <div class="kpi-icon">👥</div>
            <div class="kpi-num">{total_akun:,}</div>
            <div class="kpi-trend"><span class="up">↑ 15.4%</span> dari bulan lalu</div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(mini_line(np.random.randint(100, 1000, 12).tolist(), "#818CF8"), use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ---- CHART ROW 1 ----
    soft_colors = ["#8FB99E", "#D9A5A5", "#F3C984", "#A7B7E8", "#BFA7E8", "#A7D8D0"]
    SENT_COLORS = {"Negatif": "#D9A5A5", "Positif": "#8FB99E", "Netral": "#F3C984"}

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Distribusi Sentimen</div>', unsafe_allow_html=True)
        sentimen_count = df_filter["Sentiment"].value_counts().reset_index()
        sentimen_count.columns = ["Sentiment", "Jumlah"]
        fig = px.pie(sentimen_count, values="Jumlah", names="Sentiment", hole=0.6,
                     color="Sentiment", color_discrete_map=SENT_COLORS)
        fig.update_traces(
            textinfo="percent+label",
            textposition="inside",
            insidetextorientation="radial",
            textfont_size=10,
            marker=dict(line=dict(color="#FFFFFF", width=1))
        )
        total_label = f"<b>{len(df_filter):,}</b><br><span style='font-size:10px;color:#9CA3AF'>Total Tweet</span>"
        fig.add_annotation(text=total_label, x=0.5, y=0.5, showarrow=False, font_size=13, align="center")
        fig.update_layout(height=270, margin=dict(l=8, r=8, t=10, b=10), showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Distribusi Tweet per Brand</div>', unsafe_allow_html=True)
        brand_count = df_filter["brand"].value_counts().reset_index()
        brand_count.columns = ["Brand", "Jumlah"]
        fig = px.bar(brand_count, x="Brand", y="Jumlah", text="Jumlah",
                     color="Brand", color_discrete_sequence=soft_colors)
        fig.update_traces(textposition="outside", marker_line_width=0, textfont_size=11)
        fig.update_layout(height=270, margin=dict(l=8, r=8, t=10, b=10), showlegend=False,
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          yaxis=dict(gridcolor="#F3F4F6"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Sentimen per Brand</div>', unsafe_allow_html=True)
        sentiment_brand = df_filter.groupby(["brand", "Sentiment"]).size().reset_index(name="Jumlah")
        fig = px.bar(sentiment_brand, x="brand", y="Jumlah", color="Sentiment", barmode="stack",
                     color_discrete_map=SENT_COLORS)
        fig.update_layout(height=270, margin=dict(l=8, r=8, t=10, b=20),
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          yaxis=dict(gridcolor="#F3F4F6"),
                          legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font_size=10))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ---- BOTTOM ROW ----
    issue_mapping = {
        "Keterlambatan Pengiriman": ["telat", "terlambat", "lama", "pengiriman", "stuck", "lambat"],
        "Paket Hilang / Rusak": ["hilang", "rusak", "barang"],
        "Refund & Retur": ["refund", "retur"],
        "Masalah Kurir / COD": ["kurir", "cod", "resi"],
        "Promo / Voucher": ["promo", "voucher", "diskon"],
        "Aplikasi Error": ["aplikasi", "error"]
    }
    hasil = []
    for isu, keywords in issue_mapping.items():
        jumlah = df_filter["clean_text"].astype(str).str.contains("|".join(keywords), case=False, na=False).sum()
        hasil.append([isu, jumlah])
    issue_df = pd.DataFrame(hasil, columns=["Isu", "Jumlah"]).sort_values("Jumlah", ascending=False)

    b1, b2, b3, b4 = st.columns([1.1, 1.1, 1, 1])

    with b1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Top Isu Komplain</div>', unsafe_allow_html=True)
        fig = px.bar(issue_df, x="Jumlah", y="Isu", orientation="h", text="Jumlah",
                     color_discrete_sequence=["#8FB99E"])
        fig.update_traces(textposition="outside", textfont_size=10, marker_line_width=0)
        fig.update_layout(height=260, yaxis=dict(autorange="reversed"),
                          margin=dict(l=0, r=30, t=10, b=0),
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          xaxis=dict(gridcolor="#F3F4F6"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with b2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">WordCloud Isu Negatif</div>', unsafe_allow_html=True)
        text = " ".join(df_filter[df_filter["Sentiment"] == "Negatif"]["clean_text"].dropna().astype(str))
        if text.strip():
            wc = WordCloud(width=500, height=240, background_color="white",
                           colormap="summer", max_words=60, collocations=False).generate(text)
            fig2, ax = plt.subplots(figsize=(5, 2.5))
            fig2.patch.set_facecolor('white')
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig2, use_container_width=True)
        else:
            st.info("Tidak ada data negatif.")
        st.markdown('</div>', unsafe_allow_html=True)

    with b3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Top Akun Berdasarkan Centrality</div>', unsafe_allow_html=True)
        top_centrality = centrality_df.sort_values("Betweenness_Centrality", ascending=False).head(5).reset_index(drop=True)
        top_centrality.index = top_centrality.index + 1
        st.dataframe(top_centrality, hide_index=False, use_container_width=True, height=255)
        st.markdown('</div>', unsafe_allow_html=True)

    with b4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Network Graph Mention</div>', unsafe_allow_html=True)
        if len(edge_df) > 0:
            G = nx.from_pandas_edgelist(edge_df, source="Source", target="Target", create_using=nx.DiGraph())
            if G.number_of_nodes() > 40:
                top_nodes = sorted(dict(G.degree()).items(), key=lambda x: x[1], reverse=True)[:40]
                G = G.subgraph([n for n, _ in top_nodes]).copy()
            pos = nx.spring_layout(G, k=0.8, seed=42)
            degrees = dict(G.degree())
            node_sizes = [max(80, degrees[n] * 80) for n in G.nodes()]
            fig3, ax = plt.subplots(figsize=(4.2, 2.8))
            fig3.patch.set_facecolor("white")
            ax.set_facecolor("white")
            nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="#9DC5AA", alpha=0.9, ax=ax)
            nx.draw_networkx_edges(G, pos, edge_color="#D1D5DB", alpha=0.5, arrows=True, ax=ax, arrowsize=8)
            nx.draw_networkx_labels(G, pos, font_size=5.5, font_color="#374151", ax=ax)
            ax.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig3, use_container_width=True)
            st.markdown(f'<div style="font-size:10px;color:#9CA3AF;text-align:right">Total {G.number_of_nodes()} Node</div>', unsafe_allow_html=True)
        else:
            st.warning("Data edge kosong.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- INSIGHT ----
    if len(df_filter) > 0:
        top_brand = df_filter["brand"].value_counts().idxmax()
        top_isu = issue_df.iloc[0]["Isu"]
        top_akun = top_centrality.iloc[0]["Akun"] if "Akun" in top_centrality.columns else "-"
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">💡 Insight Cepat</div>
            <div class="insight-text">
                Volume percakapan negatif meningkat <b>16.6%</b> dibanding periode sebelumnya.
                Brand paling banyak dibicarakan adalah <b>{top_brand}</b> dengan sentimen dominan <b>{sentimen_dominan}</b>.
                Isu terbesar yang muncul adalah <b>{top_isu}</b>.
                Akun paling berpengaruh di jaringan SNA adalah <b>{top_akun}</b>.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---- RIGHT PANEL ----
with right_col:
    st.markdown("""
    <div class="right-panel">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
            <div style="font-size:13px;font-weight:700;color:#111827">Proyek Aktif</div>
            <div style="font-size:11px;color:#2F6B47;font-weight:600;cursor:pointer">Lihat Semua</div>
        </div>

        <div class="project-item">
            <div class="project-dot" style="background:#EEF4F0">🛒</div>
            <div>
                <div class="project-name">Analisis E-Commerce</div>
                <div class="project-meta">1,905 tweet • 26 Jun 2026</div>
            </div>
        </div>

        <div class="project-item">
            <div class="project-dot" style="background:#EEF4F0">🚚</div>
            <div>
                <div class="project-name">Performa Ekspedisi</div>
                <div class="project-meta">928 tweet • 26 Jun 2026</div>
            </div>
        </div>

        <div class="project-item">
            <div class="project-dot" style="background:#FEF3F2">📦</div>
            <div>
                <div class="project-name">Keluhan Pengiriman</div>
                <div class="project-meta">1,205 tweet • 24 Jun 2026</div>
            </div>
        </div>

        <div class="project-item">
            <div class="project-dot" style="background:#FFFBEB">🎁</div>
            <div>
                <div class="project-name">Promo & Diskon</div>
                <div class="project-meta">654 tweet • 23 Jun 2026</div>
            </div>
        </div>

        <div class="project-item" style="border-bottom:none">
            <div class="project-dot" style="background:#F5F3FF">📱</div>
            <div>
                <div class="project-name">Aplikasi & Layanan</div>
                <div class="project-meta">432 tweet • 22 Jun 2026</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="time-tracker">
        <div class="tracker-label">TIME TRACKER</div>
        <div class="tracker-time">01:24:08</div>
        <div class="tracker-sub">Waktu Analisis Hari Ini</div>
        <div style="display:flex;gap:8px;margin-top:12px">
            <div style="background:rgba(255,255,255,0.2);border-radius:8px;padding:6px 10px;font-size:18px;cursor:pointer">⏸</div>
            <div style="background:rgba(255,255,255,0.2);border-radius:8px;padding:6px 10px;font-size:18px;cursor:pointer">⏹</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-card" style="margin-top:14px">
        <div class="insight-title">💡 Insight Cepat</div>
        <div class="insight-text">
            Volume percakapan negatif meningkat <b>16.6%</b> dibanding periode sebelumnya.
        </div>
    </div>
    """, unsafe_allow_html=True)