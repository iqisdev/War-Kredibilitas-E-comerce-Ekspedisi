<!DOCTYPE html>
<html lang="id">

<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>
        [5] Dashboard War Kredibilitas Brand: E-Commerce & Ekspedisi
    </title>

    <link rel="stylesheet"
          href="assets/css/style.css">

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

</head>

<body>

<!-- ================= SIDEBAR ================= -->

<aside class="sidebar">

    <div class="brand">

        <div class="brand-logo">
            .✦ ݁˖
        </div>

        <div>
            <h1>Dashboard</h1>
            <p>E-Commerce & Logistics</p>
        </div>

    </div>

     <nav class="menu">
            <a href="#overview" class="menu-item active"><span>●</span> Dashboard</a>
            <a href="#brand" class="menu-item"><span>●</span> Sentimen</a>
            <a href="#issue" class="menu-item"><span>●</span> Isu & Keluhan</a>
            <a href="#topic" class="menu-item"><span>●</span> Topic Modeling</a>
            <a href="#wordcloud" class="menu-item"><span>●</span> WordCloud</a>
            <a href="#sna" class="menu-item"><span>●</span> SNA</a>
            <a href="#data-table" class="menu-item"><span>●</span> Dataset</a>
        </nav>

        <div class="side-note">
            <p class="small-title">E-Commerce & Ekspedisi Analytics</p>
            <p>Analisis sentimen, tren ulasan, dan jaringan akun Twitter antar pengguna.</p>
        </div>
    </aside>

<!-- ================= MAIN ================= -->

<main class="main-content">

<!-- ================= TOPBAR ================= -->

<section class="topbar"
         id="overview">

    <div>

        <p class="eyebrow">
            DASHBOARD ANALYTICS
        </p>

        <h2>
            War Kredibilitas Brand:
            E-Commerce & Ekspedisi
        </h2>

        <p class="subtitle">

            Analisis Sentimen, Topic Modeling,
            Keluhan dan Social Network Analysis.

        </p>

    </div>

    <div class="top-actions">

        <div class="date-pill">
            Twitter / X Dataset
        </div>

        <button class="btn"
                id="btnExport">

            Export CSV

        </button>

    </div>

</section>

<!-- ================= FILTER ================= -->

<section class="filters">

    <div class="glass">

        <label>
            Brand
        </label>

        <select id="brandFilter">

            <option value="all">
                Semua Brand
            </option>

        </select>

    </div>

    <div class="glass">

        <label>
            Kategori
        </label>

        <select id="categoryFilter">

            <option value="all">
                Semua Kategori
            </option>

        </select>

    </div>

    <div class="glass">

        <label>
            Cari Tweet
        </label>

        <input type="text"
               id="searchInput"
               placeholder="paket, refund, kurir">

    </div>

</section>

<!-- ================= KPI ================= -->

<section class="kpi-grid">

    <div class="kpi-card green-card">
        <p>Total Tweet</p>
        <h3 id="kpiTotal">0</h3>
        <span>Tweet Analisis</span>
    </div>

    <div class="kpi-card">
        <p>Distribusi <br> Sentimen</p>
        <h3 id="kpiNegatif">0%</h3>
        <span>Persentase Tweet Negatif</span>
    </div>

    <div class="kpi-card">
        <p>Brand <br>Analisis</p>
        <h3 id="kpiBrand">4</h3>
        <span>Lazada, TikTok Shop, J&T, SiCepat</span>
    </div>

    <div class="kpi-card">
        <p>Top Issue</p>
        <h3 id="kpiIssue">0</h3>
        <span>Frekuensi Isu<br>Terbanyak</span>
    </div>

    <div class="kpi-card">
        <p>Akurasi <br>Model</p>
        <h3 id="kpiAccuracy">0%</h3>
        <span>Naive Bayes <br>+ TF-IDF</span>
    </div>

</section>

<!-- ================= BRAND ================= -->

<section class="dashboard-grid brand-sentiment-wrapper" id="brand">

    <!-- LEFT -->
    <article class="card">

        <div class="card-header">
            <div>
                <p class="eyebrow">BRAND ANALYSIS</p>
                <h3>Distribusi Sentimen per Brand</h3>
            </div>
        </div>

        <div class="brand-wrapper">

            <div class="brand-box">
                <h4 class="brand-title">E-Commerce</h4>
                <canvas id="brandChartEcommerce"></canvas>
            </div>

            <div class="brand-box">
                <h4 class="brand-title">Ekspedisi</h4>
                <canvas id="brandChartEkspedisi"></canvas>
            </div>

        </div>

        <div class="brand-legend">
            <div class="item"><span class="circle negative"></span>Negatif</div>
            <div class="item"><span class="circle neutral"></span>Netral</div>
            <div class="item"><span class="circle positive"></span>Positif</div>
        </div>

    </article>

    <!-- RIGHT (DONUT FIXED) -->
    <article class="card small-card donut-card">

        <div class="card-header compact">
            <div>
                <p class="eyebrow">KOMPOSISI</p>
                <h3>Sentimen <br> E-Commerce & Logistics</h3>
            </div>
        </div>

        <div class="donut-wrap">
            <canvas id="sentimentDonutChart"></canvas>
        </div>

        <!-- MINI BREAKDOWN (biar gak kosong) -->
        <div class="sentiment-mini-table">

    <div class="row">
        <div><span class="dot green"></span>Positif</div>
        <b id="miniPos">0</b>
    </div>

    <div class="row">
        <div><span class="dot gray"></span>Netral</div>
        <b id="miniNeu">0</b>
    </div>

    <div class="row">
        <div><span class="dot red"></span>Negatif</div>
        <b id="miniNeg">0</b>
    </div>

</div>

    </article>

</section>

<!-- ================= CATEGORY ================= -->

<section class="dashboard-grid issue-wrapper"
         id="issue">

    <!-- LEFT: CHART -->
    <article class="card issue-card">

        <div class="card-header issue-header">

            <div>
                <p class="eyebrow">TOP ISSUE</p>
                <h3>Isu Komplain Terbanyak</h3>
            </div>

            <div class="issue-pill">
                <span id="badgeEcommerce">E-Commerce 56.8%</span>
                <span>•</span>
                <span id="badgeEkspedisi">Ekspedisi 43.2%</span>
            </div>

        </div>

        <canvas id="issueChart"></canvas>

    </article>


    <!-- RIGHT: TWEET EVIDENCE -->
    <aside class="card tweet-side">

        <div class="evidence-heading">
            <p class="eyebrow">EVIDENCE TWEETS</p>
            <h3>Keluhan User</h3>
        </div>

        <div class="table-scroll evidence-table-wrap">

  <table class="soft-table evidence-table">

    <thead>
      <tr>
        <th>Kategori</th>
        <th>User</th>
        <th>Keluhan</th>
      </tr>
    </thead>

    <tbody id="evidenceTweetBody">
    </tbody>

  </table>

</div>

    </aside>

</section>

<!-- ================= TOPIC ================= -->

<section class="topic-model-section"
         id="topic">

    <div class="topic-left-stack">

        <article class="card topic-image-card">

            <div class="card-header">

                <div>

                    <p class="eyebrow">
                        TOPIC MODELING
                    </p>

                    <h3>
                        Klasterisasi Topik
                    </h3>

                </div>

            </div>

            <img class="cluster-img"
                 src="images/klasterisasi.png"
                 alt="Visualisasi klasterisasi topik">

            <div class="model-evaluation-panel">

                <div class="model-evaluation-head">

                    <div>
                        <p class="eyebrow">EVALUASI KLASIFIKASI SENTIMEN - TF-IDF</p>
                        <h4>Naive Bayes sebagai model terbaik</h4>
                    </div>

                    <strong>82.68%</strong>

                </div>

                <div class="metric-grid">

                    <div class="metric-item">
                        <span>F1 Macro</span>
                        <b>0.4246</b>
                    </div>

                    <div class="metric-item">
                        <span>F1 Weighted</span>
                        <b>0.7850</b>
                    </div>

                    <div class="metric-item">
                        <span>Support Test</span>
                        <b>381</b>
                    </div>

                </div>

                <p class="model-note">
                    Dipakai untuk membaca sentimen komparatif brand. Akurasi model tinggi, tetapi kelas netral masih perlu dibaca hati-hati karena jumlah datanya lebih kecil.
                </p>

            </div>

        </article>

        <article class="card image-card wordcloud-card"
                 id="wordcloud">

            <p class="eyebrow">
                WORDCLOUD
            </p>

            <h3>
                Wordcloud Isu Keluhan
            </h3>

            <img src="images/wordcloud.png"
                 alt="Wordcloud isu keluhan">

        </article>

    </div>

    <div class="topic-right-stack">

        <article class="card topic-interpretation-card">

            <div class="topic-score">
                <span>Silhouette Score</span>
                <strong id="silhouetteScore">0.5003</strong>
            </div>

            <h3>
                Interpretasi Topik
            </h3>

            <div id="topicCards"
                 class="topic-list interpretation-list">

            </div>

        </article>

    </div>

</section>

<!-- ================= SNA ================= -->

<section class="dashboard-grid"
         id="sna">

    <article class="card image-card">

        <p class="eyebrow">
            SOCIAL NETWORK ANALYSIS
        </p>

        <h3>
            Jaringan Akun
        </h3>

        <img class="network-img"
             src="images/sna_graph.png">

    </article>

    <article class="card centrality-card">

        <p class="eyebrow">
            CENTRALITY
        </p>

        <h3>
            Akun Prioritas
        </h3>

        <div class="centrality-summary">
            <div>
                <span>Prioritas Utama</span>
                <strong id="topCentralityAccount">-</strong>
            </div>

            <div>
                <span>Betweenness</span>
                <strong id="topCentralityScore">0</strong>
            </div>
        </div>

        <div class="centrality-toolbar">
            <input type="text"
                   id="accountPrioritySearch"
                   placeholder="Cari akun, brand, kategori">
        </div>

        <div class="table-wrap centrality-table-wrap">
            <table class="centrality-table">
                <thead>
                    <tr>
                        <th>Akun</th>
                        <th>Brand</th>
                        <th>Relasi</th>
                        <th>Betweenness</th>
                        <th>Urgensi</th>
                    </tr>
                </thead>

                <tbody id="priorityAccountsBody">
                </tbody>
            </table>
        </div>

    </article>

</section>

<!-- ================= TABLE ================= -->

<section class="card table-card"
         id="data-table">

    <div class="card-header">

        <div>

            <p class="eyebrow">
                DATA TWEET
            </p>

            <h3>
                Tweet Hasil Analisis
            </h3>

        </div>

        <span class="badge"
              id="rowCountBadge">

            0 data

        </span>

    </div>

    <div class="dataset-controls">

        <div class="dataset-control">
            <label for="datasetFocusFilter">Fokus Topik</label>
            <select id="datasetFocusFilter">
                <option value="all">Semua data</option>
                <option value="complaint"
                        selected>Komplain negatif</option>
                <option value="cluster-0">Paket hilang/rusak/refund</option>
                <option value="cluster-1">Promo, ongkir, pengiriman</option>
                <option value="cluster-2">Kurir, resi, status barang</option>
                <option value="ecommerce">E-Commerce</option>
                <option value="ekspedisi">Ekspedisi</option>
            </select>
        </div>

        <div class="dataset-control compact-control">
            <label for="rowsPerPageSelect">Tampil</label>
            <select id="rowsPerPageSelect">
                <option value="25">25 data</option>
                <option value="50">50 data</option>
                <option value="100">100 data</option>
            </select>
        </div>

        <div class="table-scroll-actions">
            <button type="button"
                    class="icon-btn"
                    id="scrollTableLeft"
                    aria-label="Geser tabel ke kiri">
                ‹
            </button>

            <button type="button"
                    class="icon-btn"
                    id="scrollTableRight"
                    aria-label="Geser tabel ke kanan">
                ›
            </button>
        </div>

    </div>

    <div class="table-wrap">

        <table>

            <thead>

                <tr>

                    <th>Username</th>

                    <th>Brand</th>

                    <th>Kategori</th>

                    <th>Sentimen</th>

                    <th>Topik</th>

                    <th>Tweet</th>

                </tr>

            </thead>

            <tbody id="reviewsTableBody">

            </tbody>

        </table>

    </div>

    <div class="table-pagination">
        <button type="button"
                class="pagination-btn"
                id="prevTweetPage">
            ‹ Prev
        </button>

        <span id="tweetPageInfo">Halaman 1 dari 1</span>

        <button type="button"
                class="pagination-btn"
                id="nextTweetPage">
            Next ›
        </button>
    </div>

</section>

</main>

<script src="assets/js/data.js?v=1.0.1"></script>
<script src="assets/js/app.js?v=1.0.1"></script>

</body>
</html>
