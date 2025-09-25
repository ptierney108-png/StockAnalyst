"""
Stock Universe Data - Static Lists for Batch Processing
Contains comprehensive stock symbol lists for major indices
"""

# S&P 500 Companies (as of 2024) - ~500 stocks
SP500_SYMBOLS = [
    # Technology
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "AVGO", "ORCL",
    "CRM", "ACN", "ADBE", "NOW", "INTC", "IBM", "TXN", "QCOM", "AMAT", "LRCX",
    "AMD", "KLAC", "ADI", "MCHP", "CDNS", "SNPS", "ANSS", "FTNT", "NXPI", "MRVL",
    "ADSK", "ROP", "PAYX", "CTSH", "FISV", "INTU", "ADP", "MSI", "APH", "TEL",
    "IT", "JKHY", "AKAM", "WDC", "STX", "NTAP", "ZBRA", "EPAM", "GLW", "HPQ",
    
    # Healthcare & Pharmaceuticals
    "JNJ", "UNH", "PFE", "ABBV", "LLY", "TMO", "ABT", "DHR", "BMY", "MRK", 
    "AMGN", "GILD", "MDT", "CI", "CVS", "ANTM", "HUM", "CNC", "MOH", "ELV",
    "ISRG", "SYK", "BSX", "EW", "HOLX", "BAX", "BDX", "RMD", "DXCM", "ZBH",
    "ALGN", "IDXX", "IQV", "A", "MRNA", "REGN", "VRTX", "BIIB", "ILMN", "INCY",
    "AMGN", "ZTS", "WST", "WAT", "PKI", "TECH", "CRL", "LH", "DGX", "SOLV",
    
    # Financial Services
    "JPM", "BAC", "WFC", "GS", "MS", "C", "BLK", "AXP", "SCHW", "USB",
    "PNC", "TFC", "COF", "BK", "STT", "NTRS", "CFG", "HBAN", "RF", "KEY",
    "FITB", "ZION", "PBCT", "CMA", "MTB", "SIVB", "SBNY", "WAL", "EWBC", "PACW",
    "BRK.A", "BRK.B", "V", "MA", "PYPL", "FIS", "FDX", "WU", "DFS", "SYF",
    "TROW", "BEN", "IVZ", "AMG", "NTRS", "STT", "BLK", "PFG", "PRU", "MET",
    
    # Consumer Discretionary
    "AMZN", "TSLA", "HD", "MCD", "NKE", "LOW", "SBUX", "TJX", "BKNG", "ORLY",
    "YUM", "CMG", "ROSS", "AZO", "ULTA", "BBY", "DG", "DLTR", "COST", "WMT",
    "TGT", "KSS", "M", "JWN", "NCLH", "RCL", "CCL", "MAR", "HLT", "MGM",
    "WYNN", "LVS", "PENN", "DIS", "NFLX", "WBD", "PARA", "FOX", "FOXA", "LYV",
    "ETSY", "EBAY", "CHWY", "W", "WAYFAIR", "PRTS", "SEAT", "PLAY", "SIX", "FUN",
    
    # Consumer Staples  
    "PG", "KO", "PEP", "WMT", "COST", "CL", "KMB", "GIS", "K", "CPB",
    "CAG", "SJM", "HRL", "TSN", "MDLZ", "MNST", "KDP", "STZ", "BF.B", "TAP",
    "CLX", "CHD", "WBA", "CVS", "KR", "SYY", "USFD", "UNFI", "PFGC", "SMPL",
    "EL", "COTY", "REV", "IFF", "FMC", "EMN", "ALB", "CE", "CF", "MOS",
    
    # Energy
    "XOM", "CVX", "COP", "EOG", "SLB", "PSX", "VLO", "MPC", "PXD", "KMI",
    "OKE", "WMB", "EPD", "ET", "MPLX", "BKR", "HAL", "FANG", "DVN", "MRO",
    "APA", "EQT", "CNX", "AR", "SM", "RRC", "GPOR", "MTDR", "NOV", "FTI",
    "HP", "RIG", "VAL", "TRGP", "ENB", "TRP", "PPL", "D", "SO", "NEE",
    
    # Industrials
    "BA", "CAT", "UNP", "UPS", "FDX", "LMT", "RTX", "HON", "GE", "MMM",
    "DE", "EMR", "ETN", "PH", "CMI", "ITW", "ROK", "DOV", "XYL", "IEX",
    "PCAR", "CSX", "NSC", "KSU", "JBHT", "CHRW", "EXPD", "LSTR", "GWW", "WSO",
    "FAST", "POOL", "WERN", "ODFL", "SAIA", "ARCB", "MATX", "HUBG", "MRTN", "AIT",
    "AAL", "UAL", "DAL", "LUV", "ALK", "JBLU", "SAVE", "HA", "MESA", "SKYW",
    
    # Materials
    "LIN", "APD", "SHW", "FCX", "NUE", "STLD", "X", "CLF", "RS", "VMC",
    "MLM", "NEM", "GOLD", "AEM", "KGC", "AU", "CDE", "HL", "PAAS", "EGO",
    "AA", "CENX", "KALU", "ARNC", "UEC", "CCJ", "UUUU", "SMR", "LEU", "LTBR",
    "DD", "DOW", "LYB", "OLN", "WLK", "EMN", "CE", "CF", "MOS", "IFF",
    
    # Real Estate
    "AMT", "PLD", "CCI", "EQIX", "PSA", "EXR", "AVB", "EQR", "WELL", "O",
    "VICI", "SPG", "HST", "RHP", "PK", "SLG", "BXP", "KRC", "OFC", "PGRE",
    "AIV", "UDR", "CPT", "MAA", "ESS", "ELS", "UMH", "SUI", "CSR", "AHH",
    
    # Utilities
    "NEE", "DUK", "SO", "D", "AEP", "EXC", "XEL", "WEC", "ES", "AWK",
    "PPL", "PCG", "EIX", "SRE", "PEG", "ED", "ETR", "FE", "AEE", "CMS",
    "DTE", "NI", "LNT", "WTRG", "PNW", "IDA", "MDU", "NWE", "OGS", "SWX",
    
    # Communication Services  
    "GOOGL", "GOOG", "META", "NFLX", "DIS", "CMCSA", "VZ", "T", "TMUS", "CHTR",
    "DISH", "SIRI", "LUMN", "FYBR", "CABO", "ATUS", "WOW", "COGN", "GOGO", "VSAT",
    "LBRDA", "LBRDK", "BATRK", "BATRA", "FWONA", "FWONK", "LGF.A", "LGF.B", "MGNI", "SCNI"
]

# Future expansion - other indices (for Phase 2+)
NASDAQ_TOP_100 = [
    # Will be populated in Phase 2 - NASDAQ-100 companies
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "AVGO", "COST"
    # ... (additional NASDAQ stocks)
]

NYSE_TOP_100 = [
    # Will be populated in Phase 2 - Top NYSE companies not in S&P 500
    "BRK.A", "BRK.B", "JPM", "JNJ", "V", "UNH", "XOM", "MA", "PG", "HD"
    # ... (additional NYSE stocks)  
]

DOW_30 = [
    # Dow Jones Industrial Average (30 companies)
    "AAPL", "MSFT", "UNH", "JNJ", "V", "WMT", "JPM", "PG", "MA", "CVX",
    "HD", "MRK", "ABBV", "KO", "PEP", "BAC", "COST", "AVGO", "MCD", "TMO",
    "ACN", "LLY", "NEE", "DHR", "ABT", "ORCL", "CRM", "VZ", "ADBE", "MO"
]

# Index definitions for batch processing
STOCK_INDICES = {
    "SP500": {
        "name": "S&P 500", 
        "symbols": SP500_SYMBOLS,
        "description": "500 largest publicly traded companies in the US"
    },
    "NASDAQ100": {
        "name": "NASDAQ-100",
        "symbols": NASDAQ_TOP_100,
        "description": "100 largest non-financial companies listed on NASDAQ"
    },
    "NYSE100": {
        "name": "NYSE Top 100", 
        "symbols": NYSE_TOP_100,
        "description": "100 largest companies listed on NYSE"
    },
    "DOW30": {
        "name": "Dow Jones Industrial Average",
        "symbols": DOW_30,
        "description": "30 prominent companies representing various industries"
    }
}

def get_stock_universe(index_name: str = "SP500"):
    """Get stock symbols for a specific index"""
    return STOCK_INDICES.get(index_name, {}).get("symbols", [])

def get_all_indices():
    """Get information about all available indices"""
    return STOCK_INDICES

def get_total_stocks_count(indices: list = None):
    """Get total count of unique stocks across specified indices"""
    if indices is None:
        indices = ["SP500"]
    
    all_symbols = set()
    for index in indices:
        symbols = get_stock_universe(index)
        all_symbols.update(symbols)
    
    return len(all_symbols)