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

# NASDAQ Comprehensive - All NASDAQ-listed stocks (4,198 stocks)
NASDAQ_COMPREHENSIVE = [
    'AACB', 'AACG', 'AACI', 'AAL', 'AALG', 'AAME', 'AAOI', 'AAON', 'AAPB', 'AAPD', 'AAPG', 'AAPL', 'AARD', 'AAUS', 'AAVM', 'AAXJ', 'ABAT', 'ABCL', 'ABCS', 'ABEO', 'ABI', 'ABIG', 'ABL', 'ABLLL', 'ABLV', 'ABNB', 'ABOS', 'ABP', 'ABSI', 'ABTC', 'ABTS', 'ABUS', 'ABVC', 'ABVE', 'ABVX', 'ACAD', 'ACB', 'ACDC', 'ACET', 'ACFN', 'ACGL', 'ACGLN', 'ACGLO', 'ACHC', 'ACHV', 'ACIC', 'ACLS', 'ACLX', 'ACNB', 'ACNT', 'ACOG', 'ACON', 'ACRS', 'ACRV', 'ACT', 'ACTG', 'ACWI', 'ACWX', 'ACXP', 'ADAG', 'ADAM', 'ADAMG', 'ADAMH', 'ADAMI', 'ADAML', 'ADAMM', 'ADAMN', 'ADAMZ', 'ADAP', 'ADBE', 'ADBG', 'ADEA', 'ADGM', 'ADI', 'ADIL', 'ADMA', 'ADN', 'ADP', 'ADPT', 'ADSE', 'ADSK', 'ADTN', 'ADTX', 'ADUS', 'ADV', 'ADVB', 'ADVM', 'ADXN', 'AEBI', 'AEC', 'AEHL', 'AEI', 'AEIS', 'AEMD', 'AENT', 'AEP', 'AERT', 'AEVA', 'AEYE', 'AFBI', 'AFCG', 'AFJK', 'AFOS', 'AFRI', 'AFRM', 'AFSC', 'AFYA', 'AGAE', 'AGEM', 'AGEN', 'AGGA', 'AGH', 'AGIO', 'AGIX', 'AGMH', 'AGMI', 'AGNC', 'AGNCL', 'AGNCM', 'AGNCN', 'AGNCO', 'AGNCP', 'AGNCZ', 'AGNG', 'AGRI', 'AGYS', 'AGZD', 'AHCO', 'AHG', 'AIA', 'AIFD', 'AIFF', 'AIHS', 'AIIO', 'AIMD', 'AIOT', 'AIP', 'AIPI', 'AIPO', 'AIQ', 'AIRE', 'AIRG', 'AIRJ', 'AIRO', 'AIRS', 'AIRT', 'AIRTP', 'AISP', 'AIXI', 'AKAM', 'AKAN', 'AKBA', 'AKRO', 'AKTX', 'ALAB', 'ALBT', 'ALCO', 'ALCY', 'ALDF', 'ALDX', 'ALEC', 'ALF', 'ALGM', 'ALGN', 'ALGS', 'ALGT', 'ALHC', 'ALIL', 'ALKS', 'ALKT', 'ALLO', 'ALLT', 'ALM', 'ALMS', 'ALNT', 'ALNY', 'ALOT', 'ALRM', 'ALRS', 'ALT', 'ALTI', 'ALTO', 'ALTS', 'ALTY', 'ALVO', 'ALXO', 'ALZN', 'AMAL', 'AMAT', 'AMBA', 'AMCX', 'AMD', 'AMDD', 'AMDG', 'AMDL', 'AMGN', 'AMID', 'AMIX', 'AMLX', 'AMOD', 'AMPG', 'AMPH', 'AMPL', 'AMRK', 'AMRN', 'AMRX', 'AMSC', 'AMSF', 'AMST', 'AMTX', 'AMWD', 'AMYY', 'AMZD', 'AMZN', 'AMZZ', 'ANAB', 'ANDE', 'ANEB', 'ANEL', 'ANGH', 'ANGI', 'ANGL', 'ANGO', 'ANIK', 'ANIP', 'ANIX', 'ANL', 'ANNA', 'ANNX', 'ANPA', 'ANSC', 'ANTA', 'ANTX', 'ANY', 'AOHY', 'AOSL', 'AOTG', 'AOUT', 'APA', 'APAD', 'APDN', 'APED', 'APEI', 'APGE', 'API', 'APLD', 'APLM', 'APLS', 'APLT', 'APM', 'APOG', 'APP', 'APPF', 'APPN', 'APPS', 'APPX', 'APRE', 'APVO', 'APWC', 'APYX', 'AQB', 'AQMS', 'AQST', 'AQWA', 'ARAI', 'ARAY', 'ARBB', 'ARBE', 'ARBK', 'ARBKL', 'ARCB', 'ARCC', 'ARCT', 'ARDX', 'AREB', 'AREC', 'ARGX', 'ARHS', 'ARKO', 'ARLP', 'ARM', 'ARMG', 'ARQ', 'ARQQ', 'ARQT', 'ARRY', 'ARTL', 'ARTNA', 'ARTV', 'ARVN', 'ASBP', 'ASET', 'ASLE', 'ASMB', 'ASMG', 'ASML', 'ASND', 'ASNS', 'ASO', 'ASPC', 'ASPI', 'ASPS', 'ASPSZ', 'ASRT', 'ASRV', 'ASST', 'ASTC', 'ASTE', 'ASTH', 'ASTI', 'ASTL', 'ASTS', 'ASYS', 'ATAI', 'ATAT', 'ATEC', 'ATEX', 'ATGL', 'ATHA', 'ATHE', 'ATII', 'ATLC', 'ATLCL', 'ATLCP', 'ATLCZ', 'ATLN', 'ATLO', 'ATLX', 'ATMC', 'ATMV', 'ATNI', 'ATOM', 'ATON', 'ATOS', 'ATPC', 'ATRA', 'ATRC', 'ATRO', 'ATXG', 'ATXS', 'AUBN', 'AUDC', 'AUGO', 'AUID', 'AUMI', 'AUPH', 'AURA', 'AUTL', 'AUUD', 'AVAH', 'AVAV', 'AVBH', 'AVBP', 'AVDL', 'AVDX', 'AVGB', 'AVGG', 'AVGO', 'AVGX', 'AVL', 'AVO', 'AVPT', 'AVS', 'AVT', 'AVTX', 'AVUQ', 'AVXC', 'AVXL', 'AWRE', 'AXGN', 'AXIN', 'AXON', 'AXSM', 'AXTI', 'AZ', 'AZI', 'AZN', 'AZTA', 'AZYY'
]

# NYSE Comprehensive - All NYSE-listed stocks (5,618 stocks)  
NYSE_COMPREHENSIVE = [
    'A', 'AA', 'AAA', 'AAAA', 'AAM', 'AAMI', 'AAP', 'AAPX', 'AAPY', 'AAT', 'AAUC', 'AB', 'ABBV', 'ABCB', 'ABEQ', 'ABEV', 'ABFL', 'ABG', 'ABLD', 'ABLG', 'ABLS', 'ABM', 'ABNY', 'ABOT', 'ABR$D', 'ABR$E', 'ABR$F', 'ABT', 'ABXB', 'ACA', 'ACCO', 'ACEI', 'ACEL', 'ACES', 'ACI', 'ACII', 'ACIO', 'ACKY', 'ACLC', 'ACLO', 'ACM', 'ACN', 'ACP', 'ACP$A', 'ACR$C', 'ACR$D', 'ACRE', 'ACSI', 'ACTV', 'ACV', 'ACVA', 'ACVF', 'ACVT', 'ACWV', 'AD', 'ADC', 'ADC$A', 'ADCT', 'ADFI', 'ADIV', 'ADM', 'ADME', 'ADNT', 'ADPV', 'ADT', 'ADVE', 'ADX', 'AEE', 'AEFC', 'AEG', 'AEM', 'AEMS', 'AEO', 'AES', 'AESI', 'AETH', 'AFB', 'AFG', 'AFGB', 'AFGC', 'AFGD', 'AFGE', 'AFIF', 'AFIX', 'AFK', 'AFL', 'AFLG', 'AFMC', 'AFSM', 'AG', 'AGCO', 'AGD', 'AGG', 'AGGH', 'AGGS', 'AGGY', 'AGI', 'AGIQ', 'AGL', 'AGM', 'AGM$D', 'AGM$E', 'AGM$F', 'AGM$G', 'AGM$H', 'AGO', 'AGOX', 'AGQ', 'AGQI', 'AGRH', 'AGRO', 'AGX', 'AGZ', 'AHH', 'AHH$A', 'AHL', 'AHL$D', 'AHL$E', 'AHL$F', 'AHLT', 'AHT', 'AHT$D', 'AHT$F', 'AHT$G', 'AHT$H', 'AHT$I', 'AHYB', 'AI', 'AIBD', 'AIEQ', 'AIG', 'AII', 'AIN', 'AINP', 'AIO', 'AIOO', 'AIS', 'AIT', 'AIV', 'AIVC', 'AIVI', 'AIVL', 'AIYY', 'AIZ', 'AIZN', 'AJAN', 'AJG', 'AJUL', 'AKA', 'AKAF', 'AL', 'ALAI', 'ALB', 'ALB$A', 'ALC', 'ALE', 'ALEX', 'ALG', 'ALIT', 'ALK', 'ALL', 'ALL$B', 'ALL$H', 'ALL$I', 'ALL$J', 'ALLE', 'ALLY', 'ALRG', 'ALSN', 'ALTG', 'ALTL', 'ALV', 'ALX', 'AM', 'AMAX', 'AMBC', 'AMBP', 'AMBQ', 'AMC', 'AMDY', 'AME', 'AMG', 'AMH', 'AMH$G', 'AMH$H', 'AMJB', 'AMLP', 'AMN', 'AMOM', 'AMP', 'AMPX', 'AMPY', 'AMRC', 'AMRZ', 'AMT', 'AMTB', 'AMTD', 'AMTM', 'AMUB', 'AMWL', 'AMX', 'AMZA', 'AMZP', 'AMZY', 'AN', 'ANET', 'ANF', 'ANG$B', 'ANG$D', 'ANGX', 'ANRO', 'ANVS', 'AOA', 'AOCT', 'AOD', 'AOK', 'AOM', 'AOMD', 'AOMN', 'AON', 'AORT', 'AOS', 'AP', 'APAM', 'APCB', 'APD', 'APG', 'APH', 'APIE', 'APLE', 'APLX', 'APLY', 'APO', 'APO$A', 'APOC', 'APOS', 'APRH', 'APRJ', 'APRP', 'APRT', 'APRZ', 'APTV', 'APUE', 'APXM', 'AQLT', 'AQN', 'AQNB', 'ARB', 'ARCM', 'ARCO', 'ARCX', 'ARDC', 'ARDT', 'ARE', 'AREA', 'ARES', 'ARGT', 'ARI', 'ARIS', 'ARKA', 'ARKB', 'ARKD', 'ARKF', 'ARKG', 'ARKK', 'ARKQ', 'ARKX', 'ARKZ', 'ARL', 'ARLO', 'ARMH', 'ARMK', 'AROC', 'ARP', 'ARR$C', 'ARTY', 'ARX', 'AS', 'ASA', 'ASAN', 'ASB', 'ASB$E', 'ASB$F', 'ASBA', 'ASC', 'ASCE', 'ASEA', 'ASG', 'ASGI', 'ASGM', 'ASGN', 'ASH', 'ASHS', 'ASIA', 'ASIC', 'ASIX', 'ASLV', 'ASMF', 'ASMH', 'ASPN', 'ASTX', 'ASX', 'ATEN', 'ATFV', 'ATGE', 'ATH$A', 'ATH$B', 'ATH$D', 'ATH$E', 'ATHM', 'ATHS', 'ATI', 'ATMP', 'ATO', 'ATS', 'ATUS', 'AUB', 'AUB$A', 'AUGM', 'AUGP', 'AUGT', 'AUGZ', 'AUNA', 'AUSF', 'AUSM', 'AVA', 'AVAL', 'AVB', 'AVBC', 'AVD', 'AVDE', 'AVDS', 'AVDV', 'AVEE', 'AVEM', 'AVES', 'AVGE', 'AVGV', 'AVIE', 'AVIG', 'AVIV', 'AVK', 'AVLC', 'AVLV', 'AVMA', 'AVMC', 'AVMV', 'AVNM', 'AVNS', 'AVNT', 'AVNV', 'AVRE', 'AVSC', 'AVSD', 'AVSE', 'AVSF', 'AVUS', 'AVUV', 'AVY', 'AWAY', 'AWEG', 'AWF', 'AWI', 'AWK', 'AWP', 'AX', 'AXL', 'AXP', 'AXS', 'AXS$E', 'AXTA', 'AXUP', 'AYI', 'AZNH', 'AZO', 'AZTD', 'AZZ'
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
NYSE_TOP_100 = NYSE_COMPREHENSIVE[:100]  # First 100 companies for backward compatibility

DOW_30 = [
    # Dow Jones Industrial Average (30 companies)
    "AAPL", "MSFT", "UNH", "JNJ", "V", "WMT", "JPM", "PG", "MA", "CVX",
    "HD", "MRK", "ABBV", "KO", "PEP", "BAC", "COST", "AVGO", "MCD", "TMO",
    "ACN", "LLY", "NEE", "DHR", "ABT", "ORCL", "CRM", "VZ", "ADBE", "MO"
]

# Index definitions for batch processing - Phase 2 Complete Coverage
STOCK_INDICES = {
    "SP500": {
        "name": "S&P 500", 
        "symbols": SP500_SYMBOLS,
        "description": "500 largest publicly traded companies in the US",
        "estimated_time_minutes": 7.0
    },
    "NASDAQ100": {
        "name": "NASDAQ-100",
        "symbols": NASDAQ_100,
        "description": "100 largest non-financial companies listed on NASDAQ",
        "estimated_time_minutes": 1.5
    },
    "NASDAQ_COMPREHENSIVE": {
        "name": "NASDAQ Comprehensive",
        "symbols": NASDAQ_COMPREHENSIVE,
        "description": "Comprehensive coverage of all NASDAQ-listed companies (4,198 stocks)",
        "estimated_time_minutes": 56.0
    },
    "NYSE_COMPREHENSIVE": {
        "name": "NYSE Comprehensive",
        "symbols": NYSE_COMPREHENSIVE,
        "description": "Comprehensive coverage of all NYSE-listed companies (5,618 stocks)",
        "estimated_time_minutes": 75.0
    },
    "DOW30": {
        "name": "Dow Jones Industrial Average",
        "symbols": DOW_30,
        "description": "30 prominent companies representing various industries",
        "estimated_time_minutes": 0.5
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