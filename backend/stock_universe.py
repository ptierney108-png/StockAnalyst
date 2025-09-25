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

# NASDAQ Composite - Major NASDAQ-listed companies (comprehensive coverage)
NASDAQ_COMPOSITE = [
    # Mega Cap Technology
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "AVGO", "ORCL",
    "CRM", "ADBE", "NFLX", "AMD", "INTC", "QCOM", "TXN", "AMAT", "LRCX", "MRVL",
    "KLAC", "ADI", "MCHP", "CDNS", "SNPS", "ANSS", "FTNT", "NXPI", "ADSK", "ROP",
    "PAYX", "CTSH", "FISV", "INTU", "ADP", "MSI", "APH", "TEL", "IT", "JKHY",
    "AKAM", "WDC", "STX", "NTAP", "ZBRA", "EPAM", "GLW", "HPQ", "DOCU", "ZM",
    
    # Biotechnology & Pharmaceuticals
    "GILD", "AMGN", "REGN", "VRTX", "BIIB", "ILMN", "INCY", "MRNA", "SGEN", "ALXN",
    "BMRN", "TECH", "EXAS", "IDXX", "IQV", "MASI", "DXCM", "ALGN", "ISRG", "IOVA",
    "RARE", "UTHR", "PTCT", "FOLD", "BLUE", "EDIT", "CRSP", "NTLA", "BEAM", "ARWR",
    "RNA", "MRNA", "BNTX", "CRBU", "FATE", "FIXX", "GLYC", "IONS", "KALA", "KDMN",
    "LCTX", "LGND", "LOGI", "LYEL", "MREO", "MYGN", "NRIX", "OCUL", "PACB", "PGEN",
    
    # Consumer Discretionary & E-commerce
    "TSLA", "AMZN", "NFLX", "EBAY", "BKNG", "MAR", "SBUX", "CMG", "ORLY", "ULTA",
    "LULU", "WDAY", "ADSK", "EA", "ATVI", "TTWO", "NTES", "JD", "PDD", "BABA",
    "MELI", "SE", "GRAB", "DIDI", "UBER", "LYFT", "DASH", "ABNB", "ETSY", "W",
    "WAYFAIR", "CHWY", "ROKU", "SPOT", "ZG", "Z", "YELP", "GRPN", "MTCH", "BMBL",
    "PINS", "SNAP", "TWTR", "FB", "GOOG", "GOOGL", "META", "NFLX", "DIS", "PARA",
    
    # Communication Services & Social Media
    "META", "GOOGL", "GOOG", "NFLX", "CMCSA", "VZ", "T", "TMUS", "CHTR", "DISH",
    "SIRI", "LUMN", "FYBR", "CABO", "ATUS", "WOW", "COGN", "GOGO", "VSAT", "LBRDA",
    "LBRDK", "BATRK", "BATRA", "FWONA", "FWONK", "LGF.A", "LGF.B", "MGNI", "SCNI",
    "ROKU", "SPOT", "ZM", "DOCU", "TWLO", "OKTA", "NET", "CRWD", "ZS", "DDOG",
    
    # Financial Technology
    "PYPL", "SQ", "COIN", "HOOD", "SOFI", "LC", "AFRM", "UPST", "PAYO", "STNE",
    "NU", "OPEN", "RBLX", "U", "PATH", "BILL", "SMAR", "PCTY", "VCYT", "VEEV",
    "CRM", "WDAY", "SNOW", "PLTR", "ASML", "TEAM", "ATLR", "MDB", "DDOG", "NET",
    
    # Healthcare Technology & Services
    "ISRG", "DXCM", "ALGN", "IOVA", "RARE", "UTHR", "PTCT", "FOLD", "BLUE", "EDIT",
    "VEEV", "TDOC", "HIMS", "SDGR", "CERT", "OSCR", "PRCT", "TMDX", "VCYT", "EXAS",
    "ILMN", "PACB", "ONT", "NTRA", "NVTA", "RDNT", "SDGR", "TMDX", "VCYT", "CERT",
    
    # Emerging Growth & Innovation
    "TSLA", "PLTR", "SNOW", "CRWD", "ZS", "OKTA", "DDOG", "NET", "SMAR", "BILL",
    "PATH", "U", "RBLX", "UNITY", "AI", "SMCI", "ARM", "RIVN", "LCID", "NKLA",
    "QS", "CHPT", "BLNK", "EVB", "PLUG", "FCEL", "BE", "CLNE", "RUN", "ENPH",
    "SEDG", "NOVA", "JKS", "CSIQ", "TSM", "UMC", "ASX", "HIMX", "SIMO", "DIOD",
    
    # Additional NASDAQ Growth Companies
    "ZI", "ZUO", "ZNGA", "ZLAB", "ZEN", "ZEAL", "ZDGE", "ZCAR", "ZAGG", "YTEN",
    "YTRA", "YEXT", "YELL", "YELP", "YJ", "YORW", "YRCW", "YSAC", "YTRA", "YUMC",
    "ZUMZ", "ZUO", "ZYNE", "ZYXI", "ZSAN", "ZROZ", "ZRTX", "ZS", "ZSCL", "ZUMZ"
]

# NYSE Composite - Major NYSE-listed companies (comprehensive coverage)  
NYSE_COMPOSITE = [
    # Blue Chip Industrials
    "MMM", "AXP", "AMGN", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS",
    "DOW", "GS", "HD", "HON", "IBM", "JNJ", "JPM", "MCD", "MRK", "MSFT",
    "NKE", "PG", "CRM", "TRV", "UNH", "V", "VZ", "WBA", "WMT", "BRK.A", "BRK.B",
    
    # Financial Services Giants
    "JPM", "BAC", "WFC", "C", "GS", "MS", "AXP", "USB", "PNC", "TFC", "COF",
    "BK", "STT", "NTRS", "CFG", "HBAN", "RF", "KEY", "FITB", "ZION", "PBCT",
    "CMA", "MTB", "SIVB", "SBNY", "WAL", "EWBC", "PACW", "BLK", "TROW", "BEN",
    "IVZ", "AMG", "NTRS", "STT", "PFG", "PRU", "MET", "AIG", "ALL", "TRV",
    
    # Healthcare & Pharmaceuticals
    "JNJ", "PFE", "ABT", "BMY", "LLY", "MRK", "ABBV", "UNH", "CI", "CVS",
    "ANTM", "HUM", "CNC", "MOH", "ELV", "TMO", "DHR", "MDT", "SYK", "BSX",
    "EW", "HOLX", "BAX", "BDX", "RMD", "ZBH", "WST", "WAT", "PKI", "LH", "DGX",
    
    # Energy & Utilities
    "XOM", "CVX", "COP", "EOG", "SLB", "PSX", "VLO", "MPC", "PXD", "KMI",
    "OKE", "WMB", "EPD", "ET", "MPLX", "BKR", "HAL", "FANG", "DVN", "MRO",
    "NEE", "DUK", "SO", "D", "AEP", "EXC", "XEL", "WEC", "ES", "AWK",
    
    # Consumer Staples & Retail
    "WMT", "PG", "KO", "PEP", "COST", "TGT", "HD", "LOW", "MCD", "SBUX",
    "NKE", "TJX", "CL", "KMB", "GIS", "K", "CPB", "CAG", "SJM", "HRL",
    "TSN", "MDLZ", "MNST", "KDP", "STZ", "BF.B", "TAP", "CLX", "CHD", "WBA",
    
    # Technology & Communications (NYSE-listed)
    "IBM", "VZ", "T", "CRM", "ORCL", "ACN", "V", "MA", "PYPL", "DIS",
    "CMCSA", "CHTR", "TMUS", "DISH", "SIRI", "LUMN", "FIS", "FDX", "UPS", "WU",
    
    # Industrial Manufacturing
    "GE", "BA", "CAT", "HON", "MMM", "UTX", "LMT", "RTX", "DE", "EMR",
    "ETN", "PH", "CMI", "ITW", "ROK", "DOV", "XYL", "IEX", "PCAR", "CSX",
    
    # Materials & Chemicals
    "LIN", "APD", "SHW", "FCX", "NUE", "STLD", "X", "CLF", "RS", "VMC",
    "MLM", "NEM", "GOLD", "AEM", "KGC", "AU", "CDE", "HL", "PAAS", "EGO",
    "DD", "DOW", "LYB", "OLN", "WLK", "EMN", "CE", "CF", "MOS", "IFF",
    
    # Real Estate Investment Trusts
    "AMT", "PLD", "CCI", "EQIX", "PSA", "EXR", "AVB", "EQR", "WELL", "O",
    "VICI", "SPG", "HST", "RHP", "PK", "SLG", "BXP", "KRC", "OFC", "PGRE",
    
    # Additional NYSE Companies
    "F", "GM", "FORD", "TM", "HMC", "NSANY", "SNE", "TYO", "RACE", "FCAU",
    "DAL", "UAL", "AAL", "LUV", "ALK", "JBLU", "SAVE", "HA", "MESA", "SKYW",
    "CCL", "RCL", "NCLH", "CUK", "ONEW", "SIX", "FUN", "PLYA", "RHP", "HST"
]

# NASDAQ-100 - Top 100 non-financial companies on NASDAQ
NASDAQ_100 = [
    # Top Technology Companies
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "AVGO", "ORCL",
    "CRM", "ACN", "ADBE", "NOW", "INTC", "IBM", "TXN", "QCOM", "AMAT", "LRCX",
    "AMD", "KLAC", "ADI", "MCHP", "CDNS", "SNPS", "ANSS", "FTNT", "NXPI", "MRVL",
    "ADSK", "ROP", "PAYX", "CTSH", "FISV", "INTU", "ADP", "MSI", "APH", "TEL",
    
    # Top Biotechnology Companies
    "AMGN", "GILD", "REGN", "VRTX", "BIIB", "ILMN", "INCY", "MRNA", "SGEN", "BMRN",
    
    # Top Consumer Companies
    "COST", "SBUX", "MAR", "ORLY", "ULTA", "LULU", "WDAY", "EA", "ATVI", "NTES",
    
    # Top Communication Companies
    "NFLX", "CMCSA", "CHTR", "DISH", "SIRI", "LUMN", "ROKU", "SPOT", "ZM", "DOCU",
    
    # Top Healthcare Companies
    "ISRG", "DXCM", "ALGN", "VEEV", "TDOC", "IDXX", "IQV", "MASI", "TECH", "EXAS",
    
    # Top Emerging Growth Companies
    "TSLA", "PLTR", "SNOW", "CRWD", "ZS", "OKTA", "DDOG", "NET", "SMAR", "BILL"
]

# Legacy lists for backward compatibility
NASDAQ_TOP_100 = NASDAQ_100  # Alias for backward compatibility
NYSE_TOP_100 = NYSE_COMPOSITE[:100]  # First 100 companies for backward compatibility

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
        "symbols": NASDAQ_100,
        "description": "100 largest non-financial companies listed on NASDAQ"
    },
    "NASDAQ_COMPOSITE": {
        "name": "NASDAQ Composite",
        "symbols": NASDAQ_COMPOSITE,
        "description": "Comprehensive list of major NASDAQ-listed companies"
    },
    "NYSE100": {
        "name": "NYSE Top 100", 
        "symbols": NYSE_TOP_100,
        "description": "100 largest companies listed on NYSE"
    },
    "NYSE_COMPOSITE": {
        "name": "NYSE Composite",
        "symbols": NYSE_COMPOSITE,
        "description": "Comprehensive list of major NYSE-listed companies"
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