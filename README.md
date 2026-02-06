# Saham BEI Analyzer Optimizer

**Saham BEI Analyzer Optimizer** adalah prototype web app / micro SaaS berbasis Streamlit untuk membantu trader individu, freelancer, dan small business di Indonesia menganalisa dan mengoptimasi siklus trading saham BEI (Perencanaan → Eksekusi → Evaluasi) dalam satu dashboard.

Aplikasi ini:

- Menggabungkan indikator teknikal (RSI, EMA, Bollinger Bands, MACD) dengan backtest sederhana.
- Menyediakan kalkulator risk management (position sizing) dan metrik kinerja (win rate, profit factor, max drawdown, risk-to-reward).
- Menyajikan insight fundamental dummy (P/E, EPS, ROE, Debt/Equity) dan analisa sentimen dummy (berita + hype sosial).
- Memberikan rekomendasi **Hold/Buy/Sell** berbasis rule + ML dummy (Logistic Regression sintetis) dengan confidence score.
- Menampilkan visual: chart harga dengan indikator overlay, ringkasan kinerja, dan correlation matrix dummy emiten vs IHSG.
- Menyediakan fitur export CSV/Excel/PDF untuk backtest, metrik, dan laporan analisa emiten.

> **Catatan**: Ini adalah prototype edukatif, **bukan** platform trading produksi dan **tidak terhubung ke broker**. Semua data real-time, integrasi API (IDX/Yahoo/CNBC, Zapier, broker), enkripsi/2FA, dan compliance resmi belum diaktifkan.

---

### Fitur Utama

- **Perencanaan**
  - Strategy builder (pemilihan indikator + catatan algoritma custom).
  - Backtesting sederhana (1 emiten, 1 strategi dummy: buy saat Close > EMA & RSI > 50).
  - Risk management calculator (risk per trade %, stop-loss %, position size, nilai posisi).
  - Fundamental insights dummy: P/E, sector P/E avg, EPS, ROE, Debt/Equity.
  - Strategy optimization dummy dengan **PuLP** (pilih konfigurasi risk % yang memaksimalkan expected profit dengan constraint risk ≤ 2%, win rate ≥ 50%).

- **Eksekusi**
  - Advanced charting dummy: harga + EMA + Bollinger Bands (matplotlib).
  - Order management dummy (Market/Limit/Trailing Stop/OCO) **tanpa** koneksi broker.
  - Real-time alerts dummy: input threshold harga + channel (Email/Slack/Zapier) sebagai hook integrasi.
  - Sentiment analysis dummy dari skor berita & social hype sintetis.

- **Evaluasi**
  - Trading journal otomatis (template teks untuk alasan entry/exit dan catatan emosi).
  - Performance analytics: win rate, profit factor, max drawdown, risk-to-reward.
  - Comparator vs benchmark (IHSG dummy) dan correlation matrix dummy emiten vs IHSG.

- **Analisa Emiten AI**
  - Rekomendasi Hold / Buy / Sell berbasis:
    - P/E vs sektor, RSI terakhir, sentiment score.
    - Model **Logistic Regression (scikit-learn)** dengan data sintetis.
  - Actionable insights (narasi praktis untuk optimasi strategi).
  - Data liquidity dummy (average volume & traded value).
  - Catatan keamanan & kepatuhan (enkripsi, 2FA, compliance Bappebti/IDX) sebagai konsep desain.

- **Export & Integrasi**
  - Export **CSV** dan **Excel** (via `pandas` + `openpyxl`) untuk metrik & data harga + indikator.
  - Export **PDF report** (via `fpdf2`) berisi ringkasan strategi, fundamental, sentiment, dan rekomendasi.
  - Penjelasan hook untuk future API (IDX/Bappebti, Yahoo Finance, CNBC/Investing.com, Zapier/broker).

---

### Struktur Proyek

Aplikasi ini telah dimodularisasi untuk skalabilitas:

- `app.py`: Entry point utama dan UI layout.
- `trading_engine.py`: Perhitungan teknikal, backtest, dan logika AI.
- `visualizer.py`: Modul pembuatan chart (Matplotlib).
- `report_generator.py`: Modul ekspor PDF, Excel, dan CSV.
- `dummy_data.py`: Centralized dummy data untuk emiten dan sektor.
- `styles.css`: Custom styling untuk tampilan premium.

---

### Teknologi & Dependency

- **Backend/UI**: Python + Streamlit.
- **Data & Analitik**: `numpy`, `pandas`, `matplotlib`, `TA-Lib` (fallback manual tersedia).
- **Optimasi**: `PuLP` (linear programming).
- **Data historis**: `yfinance`.
- **Statistik & ML**: `statsmodels`, `scikit-learn`.
- **Export**: `fpdf2` (PDF), `openpyxl` (Excel), `Pillow`.

---

### Cara Menjalankan Secara Lokal

1. **Clone / buka folder proyek**

   Buka folder:

   - `Saham BEI Analyzer Optimizer`

2. **Buat & aktifkan virtual environment (opsional tapi disarankan)**

   Di PowerShell:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependency**

   ```bash
   pip install -r requirements.txt
   ```

   > Jika instalasi `TA-Lib` gagal di Windows, Anda dapat:
   > - Menginstall wheel binary TA-Lib yang sesuai secara manual, atau
   > - Sementara menghapus baris `TA-Lib` dari `requirements.txt`.  
   >   Aplikasi tetap jalan dengan fallback perhitungan indikator sederhana (tanpa TA-Lib).

4. **Jalankan aplikasi Streamlit**

   ```bash
   streamlit run app.py
   ```

5. **Buka di browser**

   Biasanya Streamlit akan membuka browser otomatis di:

   - `http://localhost:8501`

---

### Bahasa & UX

- Bahasa utama antarmuka: **Indonesia**.
- Tersedia opsi **English** untuk judul dan section vision.
- UI responsif, layout lebar (`wide`) dengan sidebar untuk parameter umum & simulasi skenario.
- Terdapat **warning box** yang menjelaskan bahwa semua estimasi bersifat kasar dan edukatif.

---

### Vision Project

Tools ini bertujuan membangun **micro SaaS Saham BEI Analyzer** khusus pasar Indonesia:

- Mengintegrasikan siklus **Perencanaan → Eksekusi → Evaluasi** trading saham BEI dalam satu ekosistem.
- Menyediakan fondasi untuk:
  - Edukasi trader (workflow yang terstruktur & data-driven).
  - Optimasi campaign & insight produk (via logging anonymized usage dan analisa sektor).
  - Ekstensi ke **full trading platform** dengan AI prediksi tren & automated order.
- Menargetkan potensi monetisasi (MRR) mirip tools internasional seperti Yahoo Finance / platform IDX tools,
  namun fokus ke kebutuhan dan regulasi lokal (Bappebti/IDX, ESG, dll).

---

### Non-Open-Source & Hak Cipta

- Proyek ini **bukan open-source**.
- Tidak ada lisensi open-source yang melekat.
- Tidak ada section kontribusi, governance, atau call-to-action kolaborasi publik.
- Seluruh hak desain, branding, dan pengembangan lanjutan berada pada pemilik proyek.

---

### Kredit

Created by **Ary HH** (`aryhharyanto@proton.me`) – Untuk saham BEI analyzer optimizer Indonesia.
