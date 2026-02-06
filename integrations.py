"""
Stub integrasi eksternal untuk prototype Saham BEI Analyzer Optimizer.

Modul ini sengaja dibuat sebagai *hook*:
- Endpoint email / Slack / Zapier / broker masih dummy (tidak ada network call nyata).
- Data BEI/IDX, Yahoo Finance, CNBC/Investing juga masih dummy.

Saat sistem di-upgrade menjadi platform produksi (mis. dengan backend Flask/FastAPI),
fungsi-fungsi di sini dapat diisi dengan implementasi nyata dan autentikasi yang aman.
"""

from __future__ import annotations

from typing import Any, Dict, List


def simulate_email_alert(to_address: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Dummy pengiriman email alert.

    Untuk produksi:
    - Integrasikan dengan provider email (SendGrid, SES, SMTP internal, dsb.).
    - Tambahkan rate limiting & audit logging.
    """
    return {
        "channel": "email_dummy",
        "to": to_address,
        "subject": subject,
        "preview": body[:120],
        "status": "queued_dummy",
    }


def simulate_slack_alert(channel: str, message: str) -> Dict[str, Any]:
    """
    Dummy pengiriman alert ke Slack/Teams.

    Untuk produksi:
    - Gunakan webhook URL yang tersimpan di konfigurasi aman (env/secret manager).
    """
    return {
        "channel": "slack_dummy",
        "target": channel,
        "message": message[:200],
        "status": "queued_dummy",
    }


def simulate_zapier_webhook(event_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dummy trigger Zapier untuk integrasi ke broker / CRM / Notion, dsb.
    """
    return {
        "channel": "zapier_dummy",
        "event": event_name,
        "payload_keys": list(payload.keys()),
        "status": "queued_dummy",
    }


def dummy_idx_price_feed(symbol: str) -> Dict[str, Any]:
    """
    Dummy hook ke feed harga BEI/IDX.

    Untuk produksi:
    - Hubungkan ke data provider resmi (IDX, broker, atau vendor data), perhatikan
      SLA, rate limit, dan regulasi Bappebti/OJK.
    """
    return {
        "source": "idx_dummy",
        "symbol": symbol.upper(),
        "note": "Data real-time belum diaktifkan; gunakan yfinance/random walk di sisi analitik.",
    }


def dummy_news_sentiment(symbol: str) -> Dict[str, Any]:
    """
    Dummy agregator sentimen berita CNBC/Investing/sosial media.
    """
    return {
        "source": "news_dummy",
        "symbol": symbol.upper(),
        "note": "Integrasi scraping/API berita & social media dapat ditambahkan di fase berikutnya.",
    }


def record_broker_signal_dummy(
    broker_name: str,
    symbol: str,
    side: str,
    size: float,
    tags: List[str] | None = None,
) -> Dict[str, Any]:
    """
    Dummy pencatatan sinyal kirim ke broker (market/limit/OCO, dsb.).

    Untuk produksi:
    - Mapping ke API broker (HTTP/FIX/Socket).
    - Validasi order (risk, compliance, MAX position).
    """
    return {
        "broker": broker_name,
        "symbol": symbol.upper(),
        "side": side,
        "size": size,
        "tags": tags or [],
        "status": "recorded_dummy",
    }

