"""
Utilitas ESG & estimasi jejak karbon komputasi (dummy).

Untuk produksi:
- Dapat menggunakan `codecarbon.OfflineEmissionsTracker` atau sistem internal
  untuk memonitor konsumsi energi & emisi CO2e.

Di prototype ini, fungsi hanya mengembalikan estimasi kasar yang aman dan murah.
"""

from __future__ import annotations

from typing import Optional

try:
    from codecarbon import OfflineEmissionsTracker  # type: ignore
except Exception:  # pragma: no cover
    OfflineEmissionsTracker = None  # type: ignore


def estimate_carbon_footprint_kg() -> float:
    """
    Estimasi kasar jejak karbon komputasi dalam kg CO2e.

    - Jika `codecarbon` tersedia dan lingkungan mendukung, fungsi akan
      men-start & stop tracker singkat lalu membaca emisi final.
    - Jika gagal, fallback ke nilai dummy kecil (~0.0001 kg).
    """
    fallback = 0.0001  # 0.1 gram CO2e sebagai dummy

    if OfflineEmissionsTracker is None:
        return fallback

    try:
        tracker = OfflineEmissionsTracker(
            country_iso_code="IDN",
            log_level="error",
            save_to_file=False,
        )
        tracker.start()
        emissions = tracker.stop()
        if emissions is None:
            return fallback
        # OfflineEmissionsTracker biasanya mengembalikan kg CO2e
        return float(max(emissions, fallback))
    except Exception:
        return fallback

