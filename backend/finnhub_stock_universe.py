"""
Finnhub-based Stock Universe - Dynamic stock listing with real data
Uses Finnhub API for comprehensive, real-time stock universe
"""

import requests
import pandas as pd
from typing import List, Dict, Optional
import os
from functools import lru_cache
import time

# Finnhub configuration
FINNHUB_KEY = "d3alfb9r01qrtc0cn1v0d3alfb9r01qrtc0cn1vg"
FINNHUB_BASE = "https://finnhub.io/api/v1"

class FinnhubStockUniverse:
    """Dynamic stock universe using Finnhub API"""
    
    def __init__(self):
        self.last_fetch = {}
        self.cache_ttl = 86400  # 24 hours for symbols
        
    @lru_cache(maxsize=1)
    def get_all_us_symbols(self) -> pd.DataFrame:
        """Get all US stock symbols from Finnhub"""
        try:
            url = f"{FINNHUB_BASE}/stock/symbol?exchange=US&token={FINNHUB_KEY}"
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            
            df = pd.DataFrame(response.json())
            print(f"Retrieved {len(df)} symbols from Finnhub")
            return df
        except Exception as e:
            print(f"Error fetching symbols from Finnhub: {e}")
            return pd.DataFrame()
    
    def get_sp500_symbols(self) -> List[str]:
        """Get S&P 500 symbols from Wikipedia with fallback to static list"""
        try:
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            tables = pd.read_html(url)
            return tables[0]["Symbol"].tolist()
        except Exception as e:
            print(f"Error fetching S&P 500 symbols from Wikipedia: {e}")
            print("Using static S&P 500 fallback list")
            return SP500_SYMBOLS
    
    def get_universe_symbols(self, exchange: str = "ALL") -> List[str]:
        """
        Get stock symbols for specified universe
        
        Args:
            exchange: "NASDAQ", "NYSE", "SP500", or "ALL"
        
        Returns:
            List of stock symbols
        """
        df = self.get_all_us_symbols()
        
        if df.empty:
            return []
        
        if exchange == "SP500":
            return self.get_sp500_symbols()
        elif exchange == "NASDAQ":
            # Filter for NASDAQ symbols (typically end with Q or have specific characteristics)
            symbols = df[df["symbol"].str.isalpha()]["symbol"].tolist()
            # Simple heuristic: NASDAQ symbols often are shorter or have certain patterns
            return sorted([s for s in symbols if len(s) <= 4 or s.endswith("Q")])
        elif exchange == "NYSE":
            # Filter for NYSE symbols 
            symbols = df[df["symbol"].str.isalpha()]["symbol"].tolist()
            nasdaq_symbols = set(self.get_universe_symbols("NASDAQ"))
            return sorted([s for s in symbols if s not in nasdaq_symbols])
        else:  # ALL
            # Return all alphabetic symbols
            return sorted(df[df["symbol"].str.isalpha()]["symbol"].tolist())
    
    def get_stock_fundamentals(self, ticker: str) -> Dict:
        """Get fundamental data for a stock"""
        try:
            url = f"{FINNHUB_BASE}/stock/metric?symbol={ticker}&metric=all&token={FINNHUB_KEY}"
            data = requests.get(url, timeout=10).json()
            metrics = data.get("metric", {})
            
            return {
                "ticker": ticker,
                "forward_pe": metrics.get("peForward"),
                "peg_ratio": metrics.get("pegRatio"),
                "roe": metrics.get("roe"),
                "debt_to_equity": metrics.get("totalDebt/totalEquity"),
                "free_cashflow": metrics.get("freeCashFlow"),
                "gross_margins": metrics.get("grossMargin"),
                "operating_margins": metrics.get("operatingMargin"),
                "market_cap": metrics.get("marketCapitalization"),
                "pe_ratio": metrics.get("peInclExtraTTM"),
                "price_to_book": metrics.get("pbAnnual")
            }
        except Exception as e:
            print(f"Error fetching fundamentals for {ticker}: {e}")
            return {"ticker": ticker}
    
    def get_stock_profile(self, ticker: str) -> Dict:
        """Get company profile data"""
        try:
            url = f"{FINNHUB_BASE}/stock/profile2?symbol={ticker}&token={FINNHUB_KEY}"
            data = requests.get(url, timeout=10).json()
            
            return {
                "sector": data.get("sector"),
                "industry": data.get("finnhubIndustry"),
                "country": data.get("country"),
                "market_cap": data.get("marketCapitalization"),
                "name": data.get("name"),
                "ipo": data.get("ipo")
            }
        except Exception as e:
            print(f"Error fetching profile for {ticker}: {e}")
            return {}

# Create global instance
finnhub_universe = FinnhubStockUniverse()

# Legacy interface for compatibility with existing batch scanner
def get_stocks_by_index(index: str) -> List[str]:
    """
    Get stocks by index name (compatible with existing interface)
    
    Args:
        index: "sp500", "nasdaq", "nyse", "all", "static", "static_nasdaq100"
    
    Returns:
        List of stock symbols
    """
    # Handle static lists
    if index.lower() == "static":
        from stock_universe import NASDAQ_COMPREHENSIVE
        return NASDAQ_COMPREHENSIVE
    
    if index.lower() == "static_nasdaq100":
        from stock_universe import NASDAQ_100
        return NASDAQ_100
    
    index_map = {
        "sp500": "SP500",
        "nasdaq": "NASDAQ", 
        "nyse": "NYSE",
        "all": "ALL"
    }
    
    exchange = index_map.get(index.lower(), "ALL")
    return finnhub_universe.get_universe_symbols(exchange)

def get_index_to_finnhub_mapping(index_key):
    """Map internal index names to Finnhub function parameters"""
    mapping = {
        "SP500": "sp500",
        "NASDAQ100": "static_nasdaq100",  # Use static list for NASDAQ100 (top 100 NASDAQ companies)
        "NASDAQ_COMPREHENSIVE": "static",  # Use static list for NASDAQ_COMPREHENSIVE (4,198 curated stocks)
        "NYSE_COMPREHENSIVE": "nyse",
        "DOW30": "sp500",  # Use sp500 for DOW30 as fallback (DOW30 is subset of SP500)
        "RUSSELL2000": "static_russell2000"  # Use static Russell 2000 list
    }
    return mapping.get(index_key, "sp500")

def get_total_stock_count() -> int:
    """Get total number of unique stocks across all exchanges"""
    return len(finnhub_universe.get_universe_symbols("ALL"))

# Static fallback lists (for offline mode or API failures)
SP500_SYMBOLS = [
    'AAPL', 'ABBV', 'ABT', 'ACN', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AEE', 'AEP', 
    'AES', 'AFL', 'AIG', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL',
    'ALLE', 'AMAT', 'AMCR', 'AMD', 'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET',
    'ANSS', 'AON', 'AOS', 'APA', 'APD', 'APH', 'APTV', 'ARE', 'ATO', 'ATVI',
    'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO', 'BA', 'BAC', 'BALL', 'BAX',
    'BBWI', 'BBY', 'BDX', 'BEN', 'BF.B', 'BIIB', 'BIO', 'BK', 'BKNG', 'BKR',
    'BLK', 'BLL', 'BMY', 'BR', 'BRK.B', 'BRO', 'BSX', 'BWA', 'BXP', 'C',
    'CAG', 'CAH', 'CARR', 'CAT', 'CB', 'CBOE', 'CBRE', 'CCI', 'CCL', 'CDAY',
    'CDNS', 'CDW', 'CE', 'CEG', 'CHTR', 'CI', 'CINF', 'CL', 'CLX', 'CMA',
    'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COO', 'COP',
    'COST', 'CPB', 'CPRT', 'CPT', 'CRL', 'CRM', 'CSCO', 'CSX', 'CTAS', 'CTLT',
    'CTRA', 'CTSH', 'CTVA', 'CTXS', 'CVS', 'CVX', 'CZR', 'D', 'DAL', 'DD',
    'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISH', 'DLR', 'DLTR',
    'DOV', 'DOW', 'DPZ', 'DRE', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN', 'DXC',
    'DXCM', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR',
    'ENPH', 'EOG', 'EPAM', 'EQIX', 'EQR', 'ES', 'ESS', 'ETN', 'ETR', 'ETSY',
    'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FANG', 'FAST', 'FB',
    'FBHS', 'FCX', 'FDX', 'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FLT', 'FMC',
    'FOX', 'FOXA', 'FRC', 'FRT', 'FTNT', 'FTV', 'GDRX', 'GD', 'GE', 'GILD',
    'GIS', 'GL', 'GLW', 'GM', 'GOOGL', 'GOOG', 'GPC', 'GPN', 'GRMN', 'GS',
    'GWW', 'HAL', 'HAS', 'HBAN', 'HBI', 'HCA', 'HD', 'HES', 'HIG', 'HII',
    'HLT', 'HOLX', 'HON', 'HPE', 'HPQ', 'HRL', 'HSIC', 'HST', 'HSY', 'HUM',
    'HWM', 'IBM', 'ICE', 'IDXX', 'IEX', 'IFF', 'ILMN', 'INCY', 'INFO', 'INTC',
    'INTU', 'IP', 'IPG', 'IPGP', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW',
    'IVZ', 'J', 'JBHT', 'JCI', 'JKHY', 'JNJ', 'JNPR', 'JPM', 'JWN', 'K',
    'KDP', 'KEY', 'KEYS', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO',
    'KR', 'L', 'LDOS', 'LEG', 'LEN', 'LH', 'LHX', 'LIN', 'LKQ', 'LLY',
    'LMT', 'LNC', 'LNT', 'LOW', 'LRCX', 'LUMN', 'LUV', 'LVS', 'LW', 'LYB',
    'LYV', 'MA', 'MAA', 'MAR', 'MAS', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ',
    'MDT', 'MET', 'META', 'MGM', 'MHK', 'MKC', 'MKTX', 'MLM', 'MMC', 'MMM',
    'MNST', 'MO', 'MOH', 'MOS', 'MPC', 'MPWR', 'MRK', 'MRNA', 'MRO', 'MS',
    'MSCI', 'MSFT', 'MSI', 'MTB', 'MTCH', 'MTD', 'MU', 'NCLH', 'NDAQ', 'NDSN',
    'NEE', 'NEM', 'NFLX', 'NI', 'NKE', 'NLOK', 'NLSN', 'NOC', 'NOW', 'NRG',
    'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NVR', 'NWL', 'NWS', 'NWSA', 'NXPI',
    'O', 'ODFL', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OTIS', 'OXY', 'PAYC', 'PAYX',
    'PCAR', 'PEAK', 'PEG', 'PENN', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH',
    'PHM', 'PKG', 'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'POOL', 'PPG',
    'PPL', 'PRU', 'PSA', 'PSX', 'PTC', 'PVH', 'PWR', 'PXD', 'PYPL', 'QCOM',
    'QRVO', 'RCL', 'RE', 'REG', 'REGN', 'RF', 'RHI', 'RJF', 'RL', 'RMD',
    'ROK', 'ROL', 'ROP', 'ROST', 'RSG', 'RTX', 'SBAC', 'SBNY', 'SBUX', 'SCHW',
    'SEDG', 'SEE', 'SHW', 'SIVB', 'SJM', 'SLB', 'SNA', 'SNPS', 'SO', 'SPG',
    'SPGI', 'SRE', 'STE', 'STT', 'STX', 'STZ', 'SWK', 'SWKS', 'SYF', 'SYK',
    'SYY', 'T', 'TAP', 'TDG', 'TDY', 'TECH', 'TEL', 'TER', 'TFC', 'TFX',
    'TGT', 'TJX', 'TMO', 'TMUS', 'TPG', 'TPR', 'TRGP', 'TRMB', 'TROW', 'TRV',
    'TSCO', 'TSLA', 'TSN', 'TT', 'TTWO', 'TWTR', 'TXN', 'TXT', 'TYL', 'UA',
    'UAA', 'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNP', 'UPS', 'URI', 'USB',
    'V', 'VFC', 'VIAC', 'VLO', 'VMC', 'VNO', 'VRSK', 'VRSN', 'VRTX', 'VTR',
    'VTRS', 'VZ', 'WAB', 'WAT', 'WBA', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR',
    'WM', 'WMB', 'WMT', 'WRB', 'WRK', 'WST', 'WU', 'WY', 'WYNN', 'XEL',
    'XLNX', 'XOM', 'XRAY', 'XYL', 'YUM', 'ZBH', 'ZBRA', 'ZION', 'ZTS'
]

if __name__ == "__main__":
    # Test the implementation
    universe = FinnhubStockUniverse()
    
    print("Testing Finnhub Stock Universe...")
    
    # Test different exchanges
    for exchange in ["SP500", "NASDAQ", "NYSE", "ALL"]:
        symbols = universe.get_universe_symbols(exchange)
        print(f"{exchange}: {len(symbols)} symbols")
        print(f"Sample: {symbols[:10]}")
        print()
    
    # Test fundamentals
    fundamentals = universe.get_stock_fundamentals("AAPL")
    print(f"AAPL Fundamentals: {fundamentals}")
    
    profile = universe.get_stock_profile("AAPL")
    print(f"AAPL Profile: {profile}")