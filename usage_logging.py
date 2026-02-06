"""
Utility untuk logging anonymized usage.

Tujuan:
- Mencatat pola penggunaan secara agregat (mis. distribusi win rate, sektor favorit)
  tanpa menyimpan identitas asli user.
- File log disimpan lokal di folder `logs/usage_logs.csv`, siap diangkat ke
  data warehouse / lake untuk analitik SaaS.
"""

from __future__ import annotations

import csv
import datetime as _dt
import hashlib
import os
from typing import Any, Dict


def _anonymize_user(user_name: str) -> str:
    """
    Konversi nama user menjadi hash pendek yang tidak dapat dibalik.
    """
    if not user_name:
        user_name = "anonymous"
    h = hashlib.sha256(user_name.encode("utf-8")).hexdigest()
    return h[:12]


def log_usage_event(event_type: str, user_name: str, payload: Dict[str, Any]) -> None:
    """
    Tulis satu baris event ke CSV lokal.

    - event_type: jenis event (mis. 'analysis_run', 'order_simulation', dsb.).
    - user_name: nama asli user (akan di-hash).
    - payload: dict metrik tambahan (win_rate, sektor, timeframe, dsb.).
    """
    os.makedirs("logs", exist_ok=True)
    path = os.path.join("logs", "usage_logs.csv")

    timestamp = _dt.datetime.utcnow().isoformat()
    user_id = _anonymize_user(user_name)

    row: Dict[str, Any] = {
        "timestamp_utc": timestamp,
        "event_type": event_type,
        "user_id": user_id,
    }
    # Flatten payload (hanya level pertama)
    for key, value in payload.items():
        row[f"meta_{key}"] = value

    file_exists = os.path.exists(path)

    fieldnames = list(row.keys())

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

