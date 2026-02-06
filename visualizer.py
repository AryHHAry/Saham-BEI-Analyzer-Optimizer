import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Tuple

def generate_performance_charts(df: pd.DataFrame, metrics: dict) -> Tuple[plt.Figure, plt.Figure]:
    """Buat chart harga dan ringkasan kinerja."""
    # Fig 1: Prices & Indicators
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(df.index, df["Close"], label="Close", color="#1f77b4", linewidth=1.5)
    if "EMA" in df.columns:
        ax1.plot(df.index, df["EMA"], label="EMA", color="#ff7f0e", alpha=0.8)
    if "BB_upper" in df.columns and "BB_lower" in df.columns:
        ax1.fill_between(df.index, df["BB_lower"], df["BB_upper"], color="gray", alpha=0.1, label="Bollinger Bands")
    
    ax1.set_title("Advanced Charting (Technical Analysis Overlay)", fontsize=12)
    ax1.legend(loc="upper left")
    ax1.grid(True, alpha=0.2)
    plt.tight_layout()

    # Fig 2: Key Metrics Bar Chart
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    labels = ["Win Rate (%)", "Profit Factor", "Drawdown (%)"]
    values = [metrics.get("win_rate", 0), metrics.get("profit_factor", 0), metrics.get("max_drawdown_pct", 0)]
    colors = ["#2ca02c", "#1f77b4", "#d62728"]
    
    bars = ax2.bar(labels, values, color=colors, alpha=0.8)
    ax2.set_title("Strategy Performance Metrics", fontsize=11)
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.1, round(yval, 2), ha='center', va='bottom')
    
    plt.tight_layout()
    return fig1, fig2

def generate_correlation_heatmap(corr_value: float) -> plt.Figure:
    """Heatmap korelasi sederhana."""
    fig, ax = plt.subplots(figsize=(4, 4))
    data = np.array([[1.0, corr_value], [corr_value, 1.0]])
    im = ax.imshow(data, cmap="RdYlGn", vmin=-1, vmax=1)
    
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Emiten", "IHSG"])
    ax.set_yticklabels(["Emiten", "IHSG"])
    
    # Text annotations
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center", color="black" if abs(data[i, j]) < 0.7 else "white")
            
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("Correlation: Emiten vs IHSG")
    plt.tight_layout()
    return fig

def generate_multi_projection(df: pd.DataFrame) -> plt.Figure:
    """Simulasi proyeksi multi-emiten (dummy)."""
    fig, ax = plt.subplots(figsize=(10, 4))
    last_price = df["Close"].iloc[-1]
    x = np.arange(30) # 30 days projection
    
    # 3 Scenarios
    rng = np.random.default_rng(42)
    ax.plot(x, last_price * (1 + 0.002 * x + rng.normal(0, 0.01, 30)), label="Bullish Case", color="green")
    ax.plot(x, last_price * (1 + 0.00 * x + rng.normal(0, 0.01, 30)), label="Base Case", color="blue")
    ax.plot(x, last_price * (1 - 0.002 * x + rng.normal(0, 0.01, 30)), label="Bearish Case", color="red")
    
    ax.set_title("30-Day 'What-If' Price Projection")
    ax.set_ylabel("Price (Rp)")
    ax.set_xlabel("Days Ahead")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig
