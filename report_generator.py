import io
import datetime
from fpdf import FPDF
import pandas as pd
from typing import Dict

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "SAHAM BEI ANALYZER OPTIMIZER - REPORT", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()} | Created by Ary HH (aryhharyanto@proton.me)", 0, 0, "C")

def create_enhanced_pdf_report(
    user_name: str,
    stock_code: str,
    metrics: Dict[str, float],
    fund: Dict[str, float],
    sentiment: Dict[str, float],
    recommendation: str,
    confidence: float,
    charts: list = None
) -> bytes:
    """Buat laporan PDF yang lebih kaya dengan data dan visual."""
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", "", 10)
    
    # Data Umum
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, f"Trader: {user_name} | Emiten: {stock_code} | Date: {datetime.date.today()}", 1, 1, "L", True)
    pdf.ln(5)
    
    # Analisa AI
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Rekomendasi AI & Sentimen", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, f"Rekomendasi Utama: {recommendation} (Confidence: {confidence*100:.1f}%)", 0, 1)
    pdf.cell(0, 8, f"Sentiment Score: {sentiment['sentiment_score']} (News: {sentiment['positive_news']}%, Hype: {sentiment['social_hype']}%)", 0, 1)
    pdf.ln(5)
    
    # Performa Strategi
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. Performa Strategi (Backtest)", 0, 1)
    pdf.set_font("Arial", "", 10)
    col_width = 45
    pdf.cell(col_width, 8, "Win Rate", 1)
    pdf.cell(col_width, 8, f"{metrics['win_rate']:.2f}%", 1, 1)
    pdf.cell(col_width, 8, "Profit Factor", 1)
    pdf.cell(col_width, 8, f"{metrics['profit_factor']:.2f}", 1, 1)
    pdf.cell(col_width, 8, "Total Trades", 1)
    pdf.cell(col_width, 8, f"{metrics['total_trades']}", 1, 1)
    pdf.ln(5)
    
    # Fundamental
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "3. Data Fundamental", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 8, f"P/E Ratio: {fund['pe']} (Sektor: {fund['sector_pe_avg']})\nROE: {fund['roe']}%\nEPS: Rp {fund['eps']}\nDER: {fund['de_ratio']}")
    
    pdf.ln(10)
    pdf.set_font("Arial", "I", 8)
    pdf.multi_cell(0, 5, "DISCLAIMER: Laporan ini bersifat edukatif dan bukan merupakan saran investasi. Penulis tidak bertanggung jawab atas kerugian yang timbul dari penggunaan data ini.")
    
    try:
        pdf_data = pdf.output(dest="S")
        if isinstance(pdf_data, str):
            return pdf_data.encode("latin-1")
        elif isinstance(pdf_data, bytes):
            return pdf_data
        else:
            return b""  # fallback empty bytes
    except Exception:
        return b""  # fallback jika error

def generate_csv_data(df_metrics: pd.DataFrame) -> str:
    return df_metrics.to_csv(index=False)

def generate_excel_data(df_metrics: pd.DataFrame, df_prices: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_metrics.to_excel(writer, index=False, sheet_name="Summary")
        df_prices.to_excel(writer, index=True, sheet_name="PriceData")
    return output.getvalue()
