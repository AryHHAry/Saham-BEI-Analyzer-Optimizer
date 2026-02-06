import streamlit as st
import datetime
import pandas as pd
import numpy as np
from PIL import Image
import os

# Import custom modules
import trading_engine as te
import visualizer as vis
import report_generator as rg
import dummy_data as dd
import integrations as intgr
from esg_utils import estimate_carbon_footprint_kg
from usage_logging import log_usage_event

# Configuration
st.set_page_config(
    page_title="Saham BEI Analyzer Optimizer",
    page_icon="📈",
    layout="wide",
)

# Load CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if os.path.exists("styles.css"):
    local_css("styles.css")

# --- UI Header & Navigation ---
def main():
    # Footer Credit (Persistent)
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            color: #6c757d;
            text-align: center;
            padding: 10px;
            font-size: 0.8rem;
            border-top: 1px solid #dee2e6;
            z-index: 100;
        }
        </style>
        <div class="footer">
            Created by <b>Ary HH</b> (aryhharyanto@proton.me) – Untuk saham BEI analyzer optimizer Indonesia
        </div>
        """,
        unsafe_allow_html=True
    )

    # Header
    st.title("📈 Saham BEI Analyzer Optimizer")
    
    # Vision Section
    with st.container():
        st.markdown("""
        <div class="vision-box">
            <h3>Vision</h3>
            <p>Tools ini bertujuan membangun micro SaaS <b>Saham BEI Analyzer</b> untuk Indonesia, 
            membantu trader optimasi siklus trading emiten BEI, dengan AI analisa/strategi/hold/buy/sell 
            untuk tren 2026 dan scale ke full platform.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer-box">
        ⚠️ Estimasi kasar, bukan saran trading, resiko kerugian, konsultasi finansial direkomendasikan.
    </div>
    """, unsafe_allow_html=True)

    # --- Sidebar: Global Parameters ---
    st.sidebar.header("User & Market Configuration")
    user_name = st.sidebar.text_input("Nama User/Trader", "Anonymous")
    trade_date = st.sidebar.date_input("Tanggal", datetime.date.today())
    
    initial_capital = st.sidebar.number_input("Modal Awal (Rp)", value=10000000, step=1000000)
    trading_style = st.sidebar.selectbox("Gaya Trading", ["Scalping", "Day", "Swing", "Position"], index=2)
    timeframe = st.sidebar.selectbox("Timeframe", ["1m", "1h", "1d", "1w"], index=2)
    
    stock_code = st.sidebar.text_input("Kode Emiten (e.g., BBCA/TLKM)", "BBCA").upper()
    selected_sector = st.sidebar.selectbox("Sektor", list(dd.SECTOR_PE_AVG.keys()))

    # --- Scenario Simulation (What-If) in Sidebar ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("Scenario Simulation")
    risk_pct = st.sidebar.slider("Risk Alignment (%)", 0.5, 5.0, 1.0, 0.25)
    
    # --- Data Retrieval ---
    with st.spinner('Fetching market data...'):
        df_prices = te.get_price_data(stock_code, timeframe)
        df_ind = te.compute_indicators(df_prices)

    if df_ind.empty:
        st.error("Data tidak tersedia untuk emiten ini. Silakan coba kode lain.")
        return

    # Logging
    log_usage_event("analysis_start", user_name, {"stock": stock_code, "capital": initial_capital})

    # --- MAIN TABS ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 1. Perencanaan", 
        "⚡ 2. Eksekusi", 
        "📈 3. Evaluasi", 
        "🤖 4. Analisa Emiten AI",
        "📥 5. Export & Status"
    ])

    # --- Tab 1: Perencanaan ---
    with tab1:
        st.header("Phase 1: Planning (Perencanaan Strategi)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Strategy Builder")
            st.multiselect("Pilih Indikator Utama", ["RSI", "MACD", "EMA", "Bollinger Bands"], default=["RSI", "EMA"])
            custom_algo = st.text_area("Custom Algorithm Logic", "If RSI < 30 and Price > EMA 20, Enter Long")
            
            st.subheader("Results: Backtesting Engine")
            metrics = te.simple_backtest(df_ind, initial_capital, risk_pct)
            m_col1, m_col2 = st.columns(2)
            m_col1.metric("Win Rate", f"{metrics['win_rate']:.1f}%")
            m_col2.metric("Profit Factor", f"{metrics['profit_factor']:.2f}")

        with col2:
            st.subheader("Risk Management Calculator")
            stop_loss_pct = st.slider("Stop Loss Distance (%)", 1.0, 10.0, 2.0)
            
            # Position Size Calculation
            last_price = df_ind['Close'].iloc[-1]
            risk_amount = initial_capital * (risk_pct / 100)
            stop_loss_val = last_price * (stop_loss_pct / 100)
            pos_size_shares = int(risk_amount // stop_loss_val) if stop_loss_val > 0 else 0
            
            st.info(f"Rekomendasi Position Size: **{pos_size_shares:,} Saham** (Rp {pos_size_shares * last_price:,.0f})")
            st.metric("Risk Amount per Trade", f"Rp {risk_amount:,.0f}")
            
            st.subheader("Fundamental Insights")
            fund = te.compute_fundamental_dummy(stock_code, selected_sector)
            st.write(f"**P/E Ratio:** {fund['pe']} (Avg Sektor: {fund['sector_pe_avg']})")
            st.write(f"**ROE:** {fund['roe']}% | **EPS:** Rp {fund['eps']}")

        st.markdown("---")
        st.subheader("Strategy Optimization (via PuLP)")
        opt = te.optimize_strategy_with_pulp(metrics)
        if opt:
            st.success(f"Saran Optimasi: Gunakan Risk {opt['risk_pct']}% untuk target Win Rate {opt['win_rate']}%")

    # --- Tab 2: Eksekusi ---
    with tab2:
        st.header("Phase 2: Execution (Eksekusi & Real-time)")
        
        # Charting
        fig_p, fig_m = vis.generate_performance_charts(df_ind, metrics)
        st.subheader("Advanced Charting")
        st.pyplot(fig_p)
        
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            st.subheader("Order Management")
            order_type = st.selectbox("Order Type", ["Limit", "Market", "Trailing Stop", "OCO"])
            order_qty = st.number_input("Quantity (Lots)", value=max(1, pos_size_shares//100))
            if st.button("Simulasikan Order"):
                st.toast(f"Order {order_type} for {order_qty} lots of {stock_code} placed (Simulated)")
            
            st.subheader("Sentiment Analysis")
            sent = te.compute_sentiment_dummy(stock_code)
            st.write(f"News: {sent['positive_news']}% Positive | Hype: {sent['social_hype']}%")
            st.progress(sent['sentiment_score']/100, text=f"Sentiment Score: {sent['sentiment_score']}")

        with col_ex2:
            st.subheader("Real-Time Alerts")
            price_target = st.number_input("Alert Trigger Price", value=float(last_price * 1.05))
            st.multiselect("Channels", ["Email", "Slack", "Zapier"], default=["Email"])
            if st.button("Set Alert"):
                st.success(f"Alert set at Rp {price_target:,.0f}")

    # --- Tab 3: Evaluasi ---
    with tab3:
        st.header("Phase 3: Evaluation (Evaluasi Kinerja)")
        
        col_ev1, col_ev2 = st.columns([2, 1])
        with col_ev1:
            st.subheader("Trading Journal Otomatis")
            journal_note = st.text_area("Catatan Trading", f"Eksekusi {stock_code} pada {trade_date}. Alasan: Breakout EMA.")
            if st.button("Save Journal"):
                st.success("Journal saved locally (Dummy)")

            st.subheader("Performance Analytics")
            st.pyplot(fig_m)
        
        with col_ev2:
            st.subheader("Correlation Matrix")
            corr = te.compute_correlation_dummy(df_ind)
            st.pyplot(vis.generate_correlation_heatmap(corr))
            st.metric("Correlation vs IHSG", f"{corr:.2f}")
        
        st.subheader("'What-If' 30-Day Projection")
        st.pyplot(vis.generate_multi_projection(df_ind))

    # --- Tab 4: Analisa Emiten AI ---
    with tab4:
        st.header("Rekomendasi AI: Hold / Buy / Sell")
        
        rec, conf = te.ml_recommendation(fund['pe'], fund['sector_pe_avg'], df_ind['RSI'].iloc[-1], sent['sentiment_score'])
        
        # UI Visual Comparator with Icons
        rec_color = "#2ca02c" if rec == "Buy" else "#d62728" if rec == "Sell" else "#ffbf00"
        st.markdown(f"""
            <div style="background-color:{rec_color}; padding:20px; border-radius:10px; color:white; text-align:center;">
                <h1 style="color:white; margin:0;">{rec}</h1>
                <p style="margin:0;">Confidence Score: {(conf*100):.1f}%</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Visual Comparator")
        comp1, comp2, comp3 = st.columns(3)
        comp1.write("📊 **Fundamental**")
        comp1.write("✅ P/E Undervalued" if fund['pe'] < fund['sector_pe_avg'] else "❌ P/E Rich")
        
        comp2.write("📈 **Teknikal**")
        comp2.write("✅ RSI Oversold" if df_ind['RSI'].iloc[-1] < 40 else "❌ RSI Overbought" if df_ind['RSI'].iloc[-1] > 70 else "⚖️ RSI Neutral")
        
        comp3.write("📰 **Sentimen**")
        comp3.write("✅ Positive Mojo" if sent['sentiment_score'] > 60 else "❌ Negative Vibe" if sent['sentiment_score'] < 40 else "⚖️ Neutral Hype")

        st.markdown("---")
        st.subheader("Actionable Recommendations")
        if rec == "Buy":
            st.write(f"💡 *Gunakan RSI 14 untuk swing {stock_code} tingkatkan win rate 15%*")
        elif rec == "Hold":
            st.write(f"💡 *Hold {stock_code} karena ROE >15% dan sentiment positive*")
        else:
            st.write(f"💡 *Exit {stock_code} segera karena market sentiment melemah dan RSI jenuh beli.*")

    # --- Tab 5: Export & Status ---
    with tab5:
        st.header("Laporan & Keamanan")
        
        col_st1, col_st2 = st.columns(2)
        with col_st1:
            st.subheader("Download Reports")
            
            # Prepare Export Data
            df_m = pd.DataFrame([metrics])
            
            csv_data = rg.generate_csv_data(df_m)
            if csv_data is not None and isinstance(csv_data, str):
                st.download_button(
                    "Export backtest to CSV",
                    data=csv_data,
                    file_name=f"Backtest_{stock_code}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("CSV data tidak tersedia.")

            pdf_data = rg.create_enhanced_pdf_report(user_name, stock_code, metrics, fund, sent, rec, conf)
            if pdf_data is not None and isinstance(pdf_data, bytes) and len(pdf_data) > 0:
                st.download_button(
                    "Download Laporan PDF",
                    data=pdf_data,
                    file_name=f"Report_{stock_code}.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning("PDF report tidak dapat dibuat. Cek data input atau hubungi admin.")

        with col_st2:
            st.subheader("Security & Compliance")
            st.write(f"🛡️ **Status:** {dd.COMPLIANCE_NOTES['Bappebti']}")
            st.write(f"🔒 **Enkripsi:** 2FA Dummy Enabled (Concept)")
            
            carbon = estimate_carbon_footprint_kg()
            st.write(f"🌱 **ESG Carbon Estimate:** {carbon:.6f} kg CO2e")

    # Threshold Alerts
    if metrics['max_drawdown_pct'] > 20:
        st.sidebar.error("⚠️ ALERT: Drawdown > 20%!")
    if sent['sentiment_score'] < 50:
        st.sidebar.warning("⚠️ Sentiment is weak (< 50)")

if __name__ == "__main__":
    main()
