import datetime
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional

try:
    import talib
except Exception:
    talib = None

try:
    import yfinance as yf
except Exception:
    yf = None

try:
    from sklearn.linear_model import LogisticRegression
except Exception:
    LogisticRegression = None

try:
    import statsmodels.api as sm
except Exception:
    sm = None

try:
    import pulp
except Exception:
    pulp = None

def get_price_data(
    symbol: str, 
    timeframe: str, 
    period_days: int = 365,
) -> pd.DataFrame:
    """Ambil data harga (yfinance + fallback dummy)."""
    end = datetime.datetime.today()
    start = end - datetime.timedelta(days=period_days)
    idx_symbol = symbol.strip().upper()
    yf_symbol = idx_symbol if idx_symbol.endswith(".JK") else f"{idx_symbol}.JK"
    
    df: Optional[pd.DataFrame] = None
    if yf is not None:
        try:
            data = yf.download(yf_symbol, start=start, end=end, progress=False, auto_adjust=True)
            if not data.empty:
                # Ensure it's a 1D dataframe and columns are simple
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)
                df = data.rename(columns=str.capitalize)
        except Exception:
            df = None

    if df is None or df.empty:
        dates = pd.date_range(start=start, end=end, freq="B")
        n = len(dates)
        rng = np.random.default_rng(abs(hash(symbol)) % (2**32))
        prices = 10000 + np.cumsum(rng.normal(0, 100, size=n))
        prices = np.maximum(prices, 500)
        df = pd.DataFrame({
            "Open": prices * (1 + rng.normal(0, 0.002, size=n)),
            "High": prices * (1 + rng.normal(0.005, 0.003, size=n)),
            "Low": prices * (1 - rng.normal(0.005, 0.003, size=n)),
            "Close": prices,
            "Volume": rng.integers(1e5, 5e6, size=n),
        }, index=dates)

    rule = {"1m": "15min", "1h": "1H", "1d": "1D", "1w": "1W"}.get(timeframe, "1D")
    return df.resample(rule).last().dropna()

def compute_indicators(df: pd.DataFrame, rsi_period=14, ema_period=20, bb_period=20) -> pd.DataFrame:
    """Hitung RSI, EMA, Bollinger Bands, MACD."""
    close = df["Close"]
    
    if talib is not None:
        rsi = talib.RSI(close, timeperiod=rsi_period)
        ema = talib.EMA(close, timeperiod=ema_period)
        upper, middle, lower = talib.BBANDS(close, timeperiod=bb_period, nbdevup=2, nbdevdn=2)
        macd, macd_signal, _ = talib.MACD(close)
    else:
        # Fallback manual
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(rsi_period).mean()
        rs = gain / (loss + 1e-9)
        rsi = 100 - (100 / (1 + rs))
        ema = close.ewm(span=ema_period, adjust=False).mean()
        mid = close.rolling(bb_period).mean()
        std = close.rolling(bb_period).std()
        upper, middle, lower = mid + 2*std, mid, mid - 2*std
        m_fast = close.ewm(span=12).mean()
        m_slow = close.ewm(span=26).mean()
        macd = m_fast - m_slow
        macd_signal = macd.ewm(span=9).mean()

    df_ind = df.copy()
    df_ind["RSI"], df_ind["EMA"] = rsi, ema
    df_ind["BB_upper"], df_ind["BB_middle"], df_ind["BB_lower"] = upper, middle, lower
    df_ind["MACD"], df_ind["MACD_signal"] = macd, macd_signal
    return df_ind.dropna()

def simple_backtest(df: pd.DataFrame, initial_capital: float, risk_pct: float) -> Dict[str, float]:
    """Simulasi backtest sederhana."""
    cash, pos_shares, trades = initial_capital, 0, []
    prices, ema, rsi = df["Close"].values, df["EMA"].values, df["RSI"].values

    for i in range(1, len(df)):
        if pos_shares == 0:
            if prices[i] > ema[i] and rsi[i] > 50:
                risk_val = cash * (risk_pct / 100.0)
                risk_per_share = max(prices[i] * 0.02, 1.0)
                shares = int(risk_val // risk_per_share)
                if shares > 0:
                    pos_shares, entry_p = shares, prices[i]
                    cash -= shares * entry_p
        else:
            if prices[i] < ema[i] or rsi[i] < 45:
                cash += pos_shares * prices[i]
                trades.append((entry_p, prices[i]))
                pos_shares = 0
    
    if pos_shares > 0:
        cash += pos_shares * prices[-1]
        trades.append((entry_p, prices[-1]))

    wins = [t for t in trades if t[1] > t[0]]
    losses = [t for t in trades if t[1] <= t[0]]
    win_sum = sum(t[1]-t[0] for t in wins)
    loss_sum = sum(abs(t[1]-t[0]) for t in losses)
    
    return {
        "final_equity": float(cash),
        "win_rate": (len(wins)/len(trades)*100) if trades else 0.0,
        "profit_factor": (win_sum/loss_sum) if loss_sum > 0 else (win_sum if win_sum > 0 else 1.0),
        "total_trades": float(len(trades)),
        "max_drawdown_pct": 12.5, # Dummy MDD
        "risk_to_reward": 2.0
    }

def compute_fundamental_dummy(symbol: str, sector: str) -> Dict[str, float]:
    base_pe = {"Banking": 15, "Mining": 10, "Energy": 12, "Telecommunications": 18, "Consumer": 20}.get(sector, 15)
    rng = np.random.default_rng(abs(hash(symbol)) % (2**32))
    return {
        "pe": round(float(base_pe + rng.normal(0, 2)), 2),
        "sector_pe_avg": float(base_pe),
        "eps": round(float(rng.normal(400, 50)), 2),
        "roe": round(float(rng.normal(18, 4)), 2),
        "de_ratio": round(float(abs(rng.normal(0.6, 0.2))), 2)
    }

def compute_sentiment_dummy(symbol: str) -> Dict[str, float]:
    rng = np.random.default_rng(abs(hash(symbol + "s")) % (2**32))
    pos, hype = rng.random(), rng.random()
    return {
        "positive_news": round(pos * 100, 1),
        "social_hype": round(hype * 100, 1),
        "sentiment_score": round((pos * 0.6 + hype * 0.4) * 100, 1)
    }

def compute_correlation_dummy(df: pd.DataFrame) -> float:
    """Return a dummy correlation value between emiten and IHSG."""
    # In a real app, this would fetch IHSG data and calculate correlation.
    # For now, we return a stable dummy value.
    return 0.85

def ml_recommendation(pe, sector_pe_avg, rsi, sentiment) -> Tuple[str, float]:
    if LogisticRegression is None:
        if pe < sector_pe_avg and rsi < 50: return "Buy", 0.75
        if rsi > 70: return "Sell", 0.80
        return "Hold", 0.70
    
    # Train dummy model
    rng = np.random.default_rng(42)
    X = rng.normal(size=(100, 3))
    y = (X[:, 0] < 0).astype(int) # Dummy target
    model = LogisticRegression().fit(X, y)
    
    feat = np.array([[pe - sector_pe_avg, rsi - 50, sentiment - 50]])
    prob = model.predict_proba(feat)[0]
    idx = np.argmax(prob)
    return ["Sell", "Buy"][idx] if idx < 2 else "Hold", float(prob[idx])

def optimize_strategy_with_pulp(metrics: dict) -> Optional[dict]:
    if pulp is None: return None
    candidates = []
    for r in [0.5, 1.0, 1.5, 2.0]:
        candidates.append({"risk_pct": r, "expected_profit": metrics['final_equity'] * (r/2.0), "win_rate": 55 - r*2})
    
    prob = pulp.LpProblem("Optimization", pulp.LpMaximize)
    x = [pulp.LpVariable(f"x_{i}", 0, 1, pulp.LpBinary) for i in range(len(candidates))]
    prob += pulp.lpSum(c["expected_profit"] * x[i] for i, c in enumerate(candidates))
    prob += pulp.lpSum(x) == 1
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    for i, v in enumerate(x):
        if v.value() == 1: return candidates[i]
    return None
