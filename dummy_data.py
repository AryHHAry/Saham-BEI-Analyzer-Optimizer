"""
Centralized dummy data and constants for Saham BEI Analyzer Optimizer.
"""

IDX_STOCKS = {
    "BBCA": {"name": "Bank Central Asia Tbk.", "sector": "Banking"},
    "BBRI": {"name": "Bank Rakyat Indonesia Tbk.", "sector": "Banking"},
    "TLKM": {"name": "Telkom Indonesia Tbk.", "sector": "Telecommunications"},
    "ASII": {"name": "Astra International Tbk.", "sector": "Consumer"},
    "ADRO": {"name": "Adaro Energy Indonesia Tbk.", "sector": "Energy"},
    "UNTR": {"name": "United Tractors Tbk.", "sector": "Mining"},
    "GOTO": {"name": "GoTo Gojek Tokopedia Tbk.", "sector": "Technology"},
}

SECTOR_PE_AVG = {
    "Banking": 15.4,
    "Telecommunications": 18.2,
    "Consumer": 20.1,
    "Energy": 9.5,
    "Mining": 11.2,
    "Technology": 25.0,
    "Other": 15.0
}

COMPLIANCE_NOTES = {
    "Bappebti": "Sesuai regulasi Bappebti No. 1 2026 tentang instrumen derivatif dan saham.",
    "IDX": "Mengikuti panduan keterbukaan informasi Bursa Efek Indonesia.",
    "ESG": "Analisa emisi komputasi disertakan dalam laporan evaluasi.",
}
