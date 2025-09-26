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
    'AACB', 'AACG', 'AACI', 'AAL', 'AALG', 'AAME', 'AAOI', 'AAON', 'AAPB', 'AAPD', 'AAPG', 'AAPL', 'AARD', 'AAUS', 'AAVM', 'AAXJ', 'ABAT', 'ABCL', 'ABCS', 'ABEO', 'ABI', 'ABIG', 'ABL', 'ABLLL', 'ABLV', 'ABNB', 'ABOS', 'ABP', 'ABSI', 'ABTC', 'ABTS', 'ABUS', 'ABVC', 'ABVE', 'ABVX', 'ACAD', 'ACB', 'ACDC', 'ACET', 'ACFN', 'ACGL', 'ACGLN', 'ACGLO', 'ACHC', 'ACHV', 'ACIC', 'ACLS', 'ACLX', 'ACNB', 'ACNT', 'ACOG', 'ACON', 'ACRS', 'ACRV', 'ACT', 'ACTG', 'ACWI', 'ACWX', 'ACXP', 'ADAG', 'ADAM', 'ADAMG', 'ADAMH', 'ADAMI', 'ADAML', 'ADAMM', 'ADAMN', 'ADAMZ', 'ADAP', 'ADBE', 'ADBG', 'ADEA', 'ADGM', 'ADI', 'ADIL', 'ADMA', 'ADN', 'ADP', 'ADPT', 'ADSE', 'ADSK', 'ADTN', 'ADTX', 'ADUS', 'ADV', 'ADVB', 'ADVM', 'ADXN', 'AEBI', 'AEC', 'AEHL', 'AEI', 'AEIS', 'AEMD', 'AENT', 'AEP', 'AERT', 'AEVA', 'AEYE', 'AFBI', 'AFCG', 'AFJK', 'AFOS', 'AFRI', 'AFRM', 'AFSC', 'AFYA', 'AGAE', 'AGEM', 'AGEN', 'AGGA', 'AGH', 'AGIO', 'AGIX', 'AGMH', 'AGMI', 'AGNC', 'AGNCL', 'AGNCM', 'AGNCN', 'AGNCO', 'AGNCP', 'AGNCZ', 'AGNG', 'AGRI', 'AGYS', 'AGZD', 'AHCO', 'AHG', 'AIA', 'AIFD', 'AIFF', 'AIHS', 'AIIO', 'AIMD', 'AIOT', 'AIP', 'AIPI', 'AIPO', 'AIQ', 'AIRE', 'AIRG', 'AIRJ', 'AIRO', 'AIRS', 'AIRT', 'AIRTP', 'AISP', 'AIXI', 'AKAM', 'AKAN', 'AKBA', 'AKRO', 'AKTX', 'ALAB', 'ALBT', 'ALCO', 'ALCY', 'ALDF', 'ALDX', 'ALEC', 'ALF', 'ALGM', 'ALGN', 'ALGS', 'ALGT', 'ALHC', 'ALIL', 'ALKS', 'ALKT', 'ALLO', 'ALLT', 'ALM', 'ALMS', 'ALNT', 'ALNY', 'ALOT', 'ALRM', 'ALRS', 'ALT', 'ALTI', 'ALTO', 'ALTS', 'ALTY', 'ALVO', 'ALXO', 'ALZN', 'AMAL', 'AMAT', 'AMBA', 'AMCX', 'AMD', 'AMDD', 'AMDG', 'AMDL', 'AMGN', 'AMID', 'AMIX', 'AMLX', 'AMOD', 'AMPG', 'AMPH', 'AMPL', 'AMRK', 'AMRN', 'AMRX', 'AMSC', 'AMSF', 'AMST', 'AMTX', 'AMWD', 'AMYY', 'AMZD', 'AMZN', 'AMZZ', 'ANAB', 'ANDE', 'ANEB', 'ANEL', 'ANGH', 'ANGI', 'ANGL', 'ANGO', 'ANIK', 'ANIP', 'ANIX', 'ANL', 'ANNA', 'ANNX', 'ANPA', 'ANSC', 'ANTA', 'ANTX', 'ANY', 'AOHY', 'AOSL', 'AOTG', 'AOUT', 'APA', 'APAD', 'APDN', 'APED', 'APEI', 'APGE', 'API', 'APLD', 'APLM', 'APLS', 'APLT', 'APM', 'APOG', 'APP', 'APPF', 'APPN', 'APPS', 'APPX', 'APRE', 'APVO', 'APWC', 'APYX', 'AQB', 'AQMS', 'AQST', 'AQWA', 'ARAI', 'ARAY', 'ARBB', 'ARBE', 'ARBK', 'ARBKL', 'ARCB', 'ARCC', 'ARCT', 'ARDX', 'AREB', 'AREC', 'ARGX', 'ARHS', 'ARKO', 'ARLP', 'ARM', 'ARMG', 'ARQ', 'ARQQ', 'ARQT', 'ARRY', 'ARTL', 'ARTNA', 'ARTV', 'ARVN', 'ASBP', 'ASET', 'ASLE', 'ASMB', 'ASMG', 'ASML', 'ASND', 'ASNS', 'ASO', 'ASPC', 'ASPI', 'ASPS', 'ASPSZ', 'ASRT', 'ASRV', 'ASST', 'ASTC', 'ASTE', 'ASTH', 'ASTI', 'ASTL', 'ASTS', 'ASYS', 'ATAI', 'ATAT', 'ATEC', 'ATEX', 'ATGL', 'ATHA', 'ATHE', 'ATII', 'ATLC', 'ATLCL', 'ATLCP', 'ATLCZ', 'ATLN', 'ATLO', 'ATLX', 'ATMC', 'ATMV', 'ATNI', 'ATOM', 'ATON', 'ATOS', 'ATPC', 'ATRA', 'ATRC', 'ATRO', 'ATXG', 'ATXS', 'AUBN', 'AUDC', 'AUGO', 'AUID', 'AUMI', 'AUPH', 'AURA', 'AUTL', 'AUUD', 'AVAH', 'AVAV', 'AVBH', 'AVBP', 'AVDL', 'AVDX', 'AVGB', 'AVGG', 'AVGO', 'AVGX', 'AVL', 'AVO', 'AVPT', 'AVS', 'AVT', 'AVTX', 'AVUQ', 'AVXC', 'AVXL', 'AWRE', 'AXGN', 'AXIN', 'AXON', 'AXSM', 'AXTI', 'AZ', 'AZI', 'AZN', 'AZTA', 'AZYY', 'BABX', 'BACC', 'BACQ', 'BAFE', 'BAFN', 'BAIG', 'BAND', 'BANF', 'BANFP', 'BANL', 'BANX', 'BAOS', 'BASG', 'BASV', 'BATRA', 'BATRK', 'BAYA', 'BBB', 'BBCP', 'BBGI', 'BBH', 'BBIO', 'BBLG', 'BBNX', 'BBOT', 'BBSI', 'BCAB', 'BCAL', 'BCAX', 'BCBP', 'BCDA', 'BCG', 'BCIC', 'BCLO', 'BCML', 'BCPC', 'BCRX', 'BCTX', 'BCTXZ', 'BCYC', 'BDGS', 'BDMD', 'BDRX', 'BDSX', 'BDTX', 'BDVL', 'BDYN', 'BEAG', 'BEAM', 'BEAT', 'BEEM', 'BEEP', 'BEEX', 'BEEZ', 'BELFA', 'BELFB', 'BELT', 'BENF', 'BFC', 'BFIN', 'BFRG', 'BFRI', 'BFST', 'BGC', 'BGFV', 'BGL', 'BGLC', 'BGM', 'BGMS', 'BGRN', 'BGRO', 'BHAT', 'BHF', 'BHFAL', 'BHFAM', 'BHFAN', 'BHFAO', 'BHFAP', 'BHRB', 'BHST', 'BIAF', 'BIB', 'BIIB', 'BILI', 'BINI', 'BIOA', 'BIOX', 'BIRD', 'BIS', 'BITF', 'BITS', 'BIVI', 'BIYA', 'BJDX', 'BJK', 'BJRI', 'BKCH', 'BKHA', 'BKNG', 'BKYI', 'BL', 'BLBD', 'BLBX', 'BLCN', 'BLDP', 'BLFS', 'BLFY', 'BLIN', 'BLIV', 'BLKB', 'BLMN', 'BLMZ', 'BLNE', 'BLNK', 'BLRX', 'BLTE', 'BLZE', 'BMAX', 'BMBL', 'BMDL', 'BMEA', 'BMGL', 'BMHL', 'BMRA', 'BMRC', 'BMRN', 'BNAI', 'BNC', 'BND', 'BNDX', 'BNGO', 'BNRG', 'BNTC', 'BNTX', 'BNZI', 'BODI', 'BOED', 'BOEG', 'BOF', 'BOKF', 'BOLD', 'BOLT', 'BON', 'BOOM', 'BOSC', 'BOTJ', 'BOTT', 'BOTZ', 'BOWN', 'BOXL', 'BPOP', 'BPOPM', 'BPRN', 'BPYPM', 'BPYPN', 'BPYPO', 'BPYPP', 'BRAG', 'BRBI', 'BRCB', 'BREA', 'BRFH', 'BRHY', 'BRID', 'BRKD', 'BRKRP', 'BRLS', 'BRLT', 'BRNS', 'BRNY', 'BRTX', 'BRY', 'BRZE', 'BSAA', 'BSBK', 'BSCP', 'BSCQ', 'BSCS', 'BSCT', 'BSCV', 'BSCX', 'BSCY', 'BSCZ', 'BSET', 'BSJP', 'BSJQ', 'BSJS', 'BSJT', 'BSJV', 'BSJX', 'BSLK', 'BSMP', 'BSMQ', 'BSMS', 'BSMT', 'BSMV', 'BSMY', 'BSMZ', 'BSSX', 'BSVN', 'BSVO', 'BSY', 'BTAI', 'BTBD', 'BTBT', 'BTCS', 'BTCT', 'BTF', 'BTFX', 'BTGD', 'BTM', 'BTMD', 'BTOC', 'BTOG', 'BTSG', 'BUFC', 'BUFI', 'BUFM', 'BUG', 'BULD', 'BULG', 'BULL', 'BULX', 'BUSE', 'BUSEP', 'BVFL', 'BVS', 'BWAY', 'BWB', 'BWBBP', 'BWEN', 'BWFG', 'BWIN', 'BWMN', 'BYFC', 'BYND', 'BYRN', 'BYSI', 'BZ', 'BZAI', 'BZFD', 'BZUN', 'CA', 'CAAS', 'CABA', 'CAC', 'CACC', 'CADL', 'CAEP', 'CAFG', 'CAI', 'CAKE', 'CALC', 'CALI', 'CALM', 'CAMP', 'CAMT', 'CAN', 'CANC', 'CANQ', 'CAPN', 'CAPS', 'CAPT', 'CARE', 'CARG', 'CARL', 'CARM', 'CART', 'CARV', 'CARY', 'CARZ', 'CASH', 'CASI', 'CASS', 'CASY', 'CATH', 'CATY', 'CBAT', 'CBFV', 'CBIO', 'CBLL', 'CBNK', 'CBRL', 'CBSH', 'CBUS', 'CCAP', 'CCB', 'CCBG', 'CCCC', 'CCCS', 'CCCX', 'CCD', 'CCEC', 'CCEP', 'CCFE', 'CCG', 'CCII', 'CCIX', 'CCLD', 'CCLDO', 'CCNE', 'CCNEP', 'CCOI', 'CCRN', 'CCSB', 'CCSI', 'CCSO', 'CCTG', 'CDC', 'CDIG', 'CDIO', 'CDL', 'CDLX', 'CDNA', 'CDNS', 'CDRO', 'CDT', 'CDTG', 'CDTX', 'CDXS', 'CDZI', 'CDZIP', 'CECO', 'CEFA', 'CEG', 'CELC', 'CELH', 'CELZ', 'CENN', 'CENT', 'CENTA', 'CENX', 'CEP', 'CEPF', 'CEPI', 'CEPO', 'CEPT', 'CERO', 'CERS', 'CERT', 'CETX', 'CETY', 'CEVA', 'CFA', 'CFBK', 'CFFI', 'CFFN', 'CFLT', 'CFO', 'CFSB', 'CG', 'CGABL', 'CGBD', 'CGBDL', 'CGC', 'CGCT', 'CGEM', 'CGEN', 'CGNT', 'CGNX', 'CGO', 'CGON', 'CGTL', 'CGTX', 'CHA', 'CHAC', 'CHCI', 'CHCO', 'CHDN', 'CHEF', 'CHEK', 'CHGX', 'CHI', 'CHKP', 'CHMG', 'CHPG', 'CHPS', 'CHRD', 'CHRI', 'CHRS', 'CHSCL', 'CHSCM', 'CHSCN', 'CHSCO', 'CHSCP', 'CHSN', 'CHY', 'CHYM', 'CIGI', 'CIGL', 'CIIT', 'CIL', 'CINF', 'CING', 'CISO', 'CISS', 'CIVB', 'CJET', 'CJMB', 'CLBK', 'CLBT', 'CLDX', 'CLFD', 'CLGN', 'CLIK', 'CLLS', 'CLMB', 'CLMT', 'CLNE', 'CLNN', 'CLOA', 'CLOD', 'CLOV', 'CLPS', 'CLPT', 'CLRB', 'CLRO', 'CLSD', 'CLSK', 'CLSM', 'CLST', 'CLWT', 'CLYM', 'CMBM', 'CMCO', 'CMCSA', 'CMCT', 'CME', 'CMMB', 'CMND', 'CMPS', 'CMPX', 'CMRC', 'CMTL', 'CNCK', 'CNDT', 'CNET', 'CNEY', 'CNFRZ', 'CNOB', 'CNOBP', 'CNSP', 'CNTA', 'CNTB', 'CNTX', 'CNTY', 'CNVS', 'CNXC', 'CNXN', 'COCH', 'COCO', 'COCP', 'CODA', 'CODX', 'COEP', 'COFS', 'COGT', 'COIG', 'COIN', 'COKE', 'COLA', 'COLB', 'COLL', 'COLM', 'COMM', 'COMT', 'CONI', 'CONL', 'COO', 'COOP', 'COOT', 'COPJ', 'COPP', 'CORO', 'CORT', 'CORZ', 'CORZZ', 'COSM', 'COST', 'COTG', 'COWG', 'COWS', 'COYA', 'COYY', 'CPAG', 'CPB', 'CPBI', 'CPHC', 'CPHY', 'CPIX', 'CPLS', 'CPOP', 'CPRT', 'CPRX', 'CPSH', 'CPSS', 'CPZ', 'CRAI', 'CRAQ', 'CRBP', 'CRCG', 'CRCT', 'CRDF', 'CRDL', 'CRDO', 'CRE', 'CREG', 'CRESY', 'CREV', 'CREX', 'CRGO', 'CRIS', 'CRMD', 'CRMG', 'CRML', 'CRMT', 'CRNC', 'CRNT', 'CRNX', 'CRON', 'CROX', 'CRSP', 'CRTO', 'CRUS', 'CRVL', 'CRVO', 'CRVS', 'CRWD', 'CRWG', 'CRWL', 'CRWS', 'CRWV', 'CSAI', 'CSB', 'CSCL', 'CSCO', 'CSCS', 'CSGP', 'CSGS', 'CSIQ', 'CSPI', 'CSQ', 'CSTE', 'CSTL', 'CSWC', 'CSWCZ', 'CSX', 'CTAS', 'CTBI', 'CTEC', 'CTKB', 'CTLP', 'CTMX', 'CTNM', 'CTNT', 'CTRM', 'CTRN', 'CTSH', 'CTSO', 'CUB', 'CUE', 'CURI', 'CURX', 'CV', 'CVAC', 'CVBF', 'CVCO', 'CVGI', 'CVKD', 'CVLT', 'CVNX', 'CVRX', 'CVV', 'CWBC', 'CWCO', 'CWD', 'CWST', 'CXAI', 'CXDO', 'CXSE', 'CYCN', 'CYN', 'CYRX', 'CYTK', 'CZFS', 'CZNC', 'CZWI', 'DAAQ', 'DADS', 'DAIC', 'DAIO', 'DAK', 'DAKT', 'DALI', 'DAPP', 'DARE', 'DASH', 'DAVE', 'DAWN', 'DAX', 'DBGI', 'DBVT', 'DBX', 'DCBO', 'DCGO', 'DCOM', 'DCOMG', 'DCOMP', 'DCTH', 'DDI', 'DDIV', 'DDOG', 'DECO', 'DEFT', 'DEMZ', 'DENN', 'DERM', 'DEVS', 'DFDV', 'DFGP', 'DFGX', 'DFLI', 'DFSC', 'DGCB', 'DGICA', 'DGICB', 'DGII', 'DGLO', 'DGLY', 'DGNX', 'DGRE', 'DGRS', 'DGXX', 'DH', 'DHAI', 'DHC', 'DHCNI', 'DHCNL', 'DHIL', 'DIBS', 'DIOD', 'DIVD', 'DJCO', 'DJT', 'DKI', 'DKNG', 'DKNX', 'DLHC', 'DLLL', 'DLO', 'DLPN', 'DLTH', 'DLXY', 'DMAA', 'DMAC', 'DMAT', 'DMLP', 'DMRC', 'DMXF', 'DNLI', 'DNTH', 'DNUT', 'DOGZ', 'DOMH', 'DOMO', 'DOOO', 'DORM', 'DOX', 'DPRO', 'DPZ', 'DRCT', 'DRDB', 'DRIO', 'DRIV', 'DRMA', 'DRS', 'DRTS', 'DRUG', 'DRVN', 'DSGN', 'DSGX', 'DSP', 'DSWL', 'DSY', 'DTCK', 'DTI', 'DTIL', 'DTSQ', 'DTSS', 'DTST', 'DUKH', 'DUKX', 'DUO', 'DUOL', 'DUOT', 'DVAL', 'DVAX', 'DVIN', 'DVLT', 'DVOL', 'DVQQ', 'DVRE', 'DVSP', 'DVUT', 'DVXB', 'DVXC', 'DVXE', 'DVXF', 'DVXK', 'DVXP', 'DVXV', 'DVXY', 'DVY', 'DWAS', 'DWSH', 'DWSN', 'DWTX', 'DWUS', 'DXCM', 'DXLG', 'DXPE', 'DXST', 'DYAI', 'DYCQ', 'DYFI', 'DYN', 'DYNB', 'DYTA', 'EA', 'EBAY', 'EBC', 'EBI', 'EBIZ', 'EBMT', 'EBON', 'ECBK', 'ECDA', 'ECPG', 'ECX', 'EDAP', 'EDBL', 'EDHL', 'EDIT', 'EDRY', 'EDSA', 'EDTK', 'EDUC', 'EEFT', 'EEIQ', 'EEMA', 'EFAS', 'EFOI', 'EFRA', 'EFSC', 'EFSCP', 'EFSI', 'EFTY', 'EGAN', 'EGBN', 'EGGQ', 'EGHA', 'EGHT', 'EH', 'EHGO', 'EHLD', 'EHLS', 'EHTH', 'EJH', 'EKG', 'EKSO', 'ELAB', 'ELBM', 'ELDN', 'ELFY', 'ELIL', 'ELIS', 'ELOG', 'ELSE', 'ELTK', 'ELTX', 'ELUT', 'ELVA', 'ELVN', 'ELWS', 'EM', 'EMB', 'EMBC', 'EMCB', 'EMEQ', 'EMIF', 'EML', 'EMPD', 'EMPG', 'EMXC', 'EMXF', 'ENGN', 'ENGS', 'ENLT', 'ENLV', 'ENPH', 'ENSC', 'ENSG', 'ENTA', 'ENTG', 'ENTO', 'ENTX', 'ENVB', 'ENVX', 'ENZL', 'EOLS', 'EOSE', 'EPIX', 'EPRX', 'EPSM', 'EPSN', 'EPWK', 'EQ', 'EQIX', 'ERAS', 'ERET', 'ERIC', 'ERIE', 'ERII', 'ERNA', 'ERNZ', 'ESCA', 'ESEA', 'ESGD', 'ESGE', 'ESGL', 'ESHA', 'ESLA', 'ESLT', 'ESMV', 'ESN', 'ESOA', 'ESPO', 'ESQ', 'ESTA', 'ETEC', 'ETHA', 'ETHI', 'ETHM', 'ETHZ', 'ETNB', 'ETON', 'ETRL', 'ETS', 'ETSY', 'EUDA', 'EUFN', 'EURK', 'EVAX', 'EVCM', 'EVGN', 'EVGO', 'EVLV', 'EVMT', 'EVO', 'EVOK', 'EVRG', 'EVSD', 'EVTV', 'EVYM', 'EWBC', 'EWCZ', 'EWJV', 'EWTX', 'EWZS', 'EXAS', 'EXC', 'EXE', 'EXEEL', 'EXEEZ', 'EXEL', 'EXFY', 'EXLS', 'EXOZ', 'EXPE', 'EXPI', 'EXPO', 'EXUS', 'EYE', 'EYEG', 'EYPT', 'EZGO', 'FA', 'FAB', 'FACT', 'FAD', 'FALN', 'FAMI', 'FANG', 'FARM', 'FAST', 'FAT', 'FATBB', 'FATBP', 'FATE', 'FATN', 'FBGL', 'FBIO', 'FBIOP', 'FBIZ', 'FBL', 'FBLA', 'FBLG', 'FBNC', 'FBOT', 'FBRX', 'FBYD', 'FCA', 'FCAL', 'FCAP', 'FCBC', 'FCCO', 'FCEF', 'FCEL', 'FCFS', 'FCHL', 'FCNCA', 'FCNCO', 'FCNCP', 'FCTE', 'FCUV', 'FCVT', 'FDBC', 'FDCF', 'FDFF', 'FDIF', 'FDIG', 'FDIV', 'FDMT', 'FDNI', 'FDSB', 'FDT', 'FDTS', 'FDTX', 'FDUS', 'FEAM', 'FEAT', 'FEBO', 'FEIM', 'FELE', 'FEM', 'FEMB', 'FEMS', 'FEMY', 'FENC', 'FEP', 'FEPI', 'FERA', 'FEUZ', 'FEX', 'FFAI', 'FFBC', 'FFIC', 'FFIN', 'FFIV', 'FFUT', 'FGBI', 'FGBIP', 'FGEN', 'FGI', 'FGL', 'FGM', 'FGMC', 'FGNX', 'FGNXP', 'FGSI', 'FHB', 'FHTX', 'FIBK', 'FICS', 'FID', 'FIEE', 'FIGX', 'FINX', 'FIP', 'FISI', 'FITB', 'FITBI', 'FITBO', 'FITBP', 'FIVE', 'FIVN', 'FIVY', 'FIXD', 'FIZZ', 'FJP', 'FKWL', 'FLD', 'FLDB', 'FLEX', 'FLGC', 'FLGT', 'FLL', 'FLN', 'FLNC', 'FLNT', 'FLUX', 'FLWS', 'FLX', 'FLXS', 'FLY', 'FLYE', 'FMAO', 'FMB', 'FMBH', 'FMED', 'FMET', 'FMFC', 'FMHI', 'FMNB', 'FMST', 'FMTM', 'FMUB', 'FMUN', 'FNK', 'FNKO', 'FNLC', 'FNWB', 'FNWD', 'FNX', 'FNY', 'FOFO', 'FOLD', 'FORA', 'FORD', 'FORL', 'FORM', 'FORTY', 'FOSL', 'FOSLL', 'FOX', 'FOXA', 'FOXF', 'FOXX', 'FPA', 'FPAY', 'FPXE', 'FPXI', 'FRAF', 'FRBA', 'FRD', 'FRDD', 'FRGT', 'FRHC', 'FRME', 'FRMEP', 'FROG', 'FRPH', 'FRPT', 'FRSH', 'FRST', 'FRSX', 'FSBC', 'FSCS', 'FSEA', 'FSFG', 'FSGS', 'FSHP', 'FSUN', 'FSV', 'FSZ', 'FTA', 'FTAG', 'FTAI', 'FTAIM', 'FTAIN', 'FTC', 'FTCI', 'FTCS', 'FTDS', 'FTEK', 'FTEL', 'FTFT', 'FTGC', 'FTGS', 'FTHI', 'FTHM', 'FTLF', 'FTNT', 'FTQI', 'FTRE', 'FTRI', 'FTRK', 'FTSL', 'FTSM', 'FTXG', 'FTXH', 'FTXL', 'FTXN', 'FTXO', 'FULC', 'FULT', 'FULTP', 'FUNC', 'FUND', 'FUSB', 'FV', 'FVC', 'FVCB', 'FVN', 'FWONA', 'FWONK', 'FWRD', 'FWRG', 'FXNC', 'FYC', 'FYT', 'FYX', 'GABC', 'GAIA', 'GAIN', 'GAINI', 'GAINL', 'GAINN', 'GAINZ', 'GALT', 'GAMB', 'GAME', 'GANX', 'GASS', 'GAUZ', 'GBDC', 'GBFH', 'GBIO', 'GBUG', 'GCBC', 'GCL', 'GCMG', 'GCT', 'GCTK', 'GDC', 'GDEN', 'GDEV', 'GDFN', 'GDHG', 'GDRX', 'GDS', 'GDTC', 'GDYN', 'GECC', 'GECCG', 'GECCH', 'GECCI', 'GECCO', 'GECCZ', 'GEG', 'GEGGL', 'GEHC', 'GELS', 'GEME', 'GEMI', 'GEN', 'GENK', 'GEOS', 'GERN', 'GEVO', 'GFAI', 'GFGF', 'GFS', 'GGAL', 'GGLL', 'GGLS', 'GH', 'GHRS', 'GIBO', 'GIFI', 'GIFT', 'GIG', 'GIGM', 'GIII', 'GILD', 'GILT', 'GIND', 'GINX', 'GITS', 'GKAT', 'GLAD', 'GLADZ', 'GLBE', 'GLBS', 'GLBZ', 'GLDD', 'GLDI', 'GLDY', 'GLE', 'GLGG', 'GLIBA', 'GLIBK', 'GLMD', 'GLNG', 'GLPG', 'GLPI', 'GLRE', 'GLSI', 'GLTO', 'GLUE', 'GLXG', 'GLXY', 'GMAB', 'GMGI', 'GMHS', 'GMM', 'GNFT', 'GNLN', 'GNLX', 'GNMA', 'GNOM', 'GNPX', 'GNSS', 'GNTA', 'GNTX', 'GO', 'GOCO', 'GOGO', 'GOOD', 'GOODN', 'GOODO', 'GOOG', 'GOOGL', 'GORV', 'GOSS', 'GOVI', 'GOVX', 'GP', 'GPAT', 'GPIQ', 'GPIX', 'GPRE', 'GPRF', 'GPRO', 'GQQQ', 'GRAB', 'GRAL', 'GRAN', 'GRCE', 'GREE', 'GREEL', 'GRFS', 'GRI', 'GRID', 'GRIN', 'GRNQ', 'GRPN', 'GRVY', 'GRWG', 'GSAT', 'GSBC', 'GSHD', 'GSIB', 'GSIT', 'GSM', 'GSRT', 'GSUN', 'GT', 'GTBP', 'GTEC', 'GTEN', 'GTERA', 'GTI', 'GTIM', 'GTLB', 'GTM', 'GTX', 'GURE', 'GUTS', 'GV', 'GVH', 'GWAV', 'GWRS', 'GXAI', 'GYRE', 'GYRO', 'HAFC', 'HAIN', 'HALO', 'HAO', 'HAS', 'HBAN', 'HBANL', 'HBANM', 'HBANP', 'HBCP', 'HBDC', 'HBIO', 'HBNB', 'HBNC', 'HBT', 'HCAI', 'HCAT', 'HCHL', 'HCKT', 'HCM', 'HCMA', 'HCSG', 'HCTI', 'HCWB', 'HDL', 'HDSN', 'HEAL', 'HECO', 'HEJD', 'HELE', 'HEPS', 'HEQQ', 'HERD', 'HERO', 'HERZ', 'HFBL', 'HFFG', 'HFSP', 'HFWA', 'HGBL', 'HHS', 'HIDE', 'HIFS', 'HIHO', 'HIMX', 'HIMY', 'HIMZ', 'HIND', 'HISF', 'HIT', 'HITI', 'HIVE', 'HKIT', 'HKPD', 'HLAL', 'HLIT', 'HLMN', 'HLNE', 'HLP', 'HNDL', 'HNNA', 'HNNAZ', 'HNRG', 'HNST', 'HOFT', 'HOLO', 'HOLX', 'HON', 'HOND', 'HONE', 'HOOD', 'HOOG', 'HOOI', 'HOOX', 'HOPE', 'HOTH', 'HOVNP', 'HOWL', 'HPAI', 'HPK', 'HQGO', 'HQI', 'HQY', 'HRMY', 'HROWL', 'HROWM', 'HRTS', 'HRTX', 'HRZN', 'HSAI', 'HSCS', 'HSDT', 'HSIC', 'HSII', 'HSPO', 'HSPT', 'HST', 'HSTM', 'HTBK', 'HTCO', 'HTFL', 'HTHT', 'HTLD', 'HTLM', 'HTO', 'HTOO', 'HTZ', 'HUBC', 'HUBCZ', 'HUBG', 'HUDI', 'HUIZ', 'HUMA', 'HURA', 'HURC', 'HURN', 'HUT', 'HVII', 'HWAY', 'HWBK', 'HWC', 'HWCPZ', 'HWH', 'HWKN', 'HWSM', 'HXHX', 'HYBI', 'HYFM', 'HYFT', 'HYLS', 'HYMC', 'HYMCL', 'HYP', 'HYPD', 'HYXF', 'HYZD', 'IAC', 'IART', 'IAS', 'IBAC', 'IBAT', 'IBB', 'IBBQ', 'IBCP', 'IBEX', 'IBG', 'IBGA', 'IBGB', 'IBGK', 'IBGL', 'IBIO', 'IBIT', 'IBOC', 'IBOT', 'IBRX', 'IBTF', 'IBTG', 'IBTH', 'IBTI', 'IBTJ', 'IBTK', 'IBTL', 'IBTM', 'IBTO', 'IBTP', 'IBTQ', 'ICCC', 'ICCM', 'ICFI', 'ICG', 'ICLN', 'ICMB', 'ICON', 'ICOP', 'ICUI', 'IDAI', 'IDCC', 'IDEF', 'IDN', 'IDXX', 'IDYA', 'IEF', 'IEI', 'IEP', 'IESC', 'IEUS', 'IFBD', 'IFGL', 'IFLO', 'IFRX', 'IFV', 'IGF', 'IGIB', 'IGIC', 'IGOV', 'IGSB', 'IHRT', 'IHYF', 'III', 'IIIV', 'IINN', 'IJT', 'IKT', 'ILAG', 'ILIT', 'ILMN', 'ILPT', 'IMA', 'IMAB', 'IMCC', 'IMCV', 'IMDX', 'IMG', 'IMKTA', 'IMMP', 'IMMX', 'IMNM', 'IMNN', 'IMOM', 'IMOS', 'IMPP', 'IMPPP', 'IMRN', 'IMRX', 'IMTE', 'IMTX', 'IMUX', 'IMVT', 'IMXI', 'INAB', 'INAC', 'INBK', 'INBKZ', 'INBS', 'INBX', 'INCY', 'INDB', 'INDH', 'INDI', 'INDP', 'INDV', 'INDY', 'INEO', 'INGN', 'INHD', 'INKT', 'INLF', 'INM', 'INMB', 'INMD', 'INNV', 'INO', 'INOD', 'INRO', 'INSE', 'INSG', 'INSM', 'INTA', 'INTC', 'INTG', 'INTJ', 'INTS', 'INTZ', 'INV', 'INVA', 'INVE', 'INVZ', 'IOBT', 'IONL', 'IONS', 'IONX', 'IONZ', 'IOSP', 'IOVA', 'IPCX', 'IPDN', 'IPGP', 'IPHA', 'IPM', 'IPOD', 'IPSC', 'IPST', 'IPX', 'IQ', 'IQQQ', 'IQST', 'IRBT', 'IRD', 'IRDM', 'IREN', 'IRIX', 'IRMD', 'IROH', 'IRON', 'IROQ', 'IRTC', 'IRWD', 'ISBA', 'ISHG', 'ISHP', 'ISPC', 'ISPO', 'ISRG', 'ISRL', 'ISSC', 'ISTB', 'ITIC', 'ITRI', 'ITRM', 'ITRN', 'IUS', 'IUSB', 'IUSG', 'IUSV', 'IVA', 'IVAL', 'IVDA', 'IVF', 'IVP', 'IVVD', 'IXHL', 'IXUS', 'IZEA', 'IZM', 'JACK', 'JAGX', 'JAKK', 'JAMF', 'JANX', 'JAPN', 'JAZZ', 'JBDI', 'JBHT', 'JBIO', 'JBSS', 'JCAP', 'JCSE', 'JCTC', 'JD', 'JDOC', 'JDZG', 'JEM', 'JEPQ', 'JFB', 'JFIN', 'JG', 'JGLO', 'JHAI', 'JIVE', 'JJSF', 'JKHY', 'JL', 'JLHL', 'JMID', 'JMSB', 'JOUT', 'JOYY', 'JPEF', 'JPX', 'JPY', 'JRSH', 'JSM', 'JSMD', 'JSML', 'JTAI', 'JTEK', 'JUNS', 'JVA', 'JWEL', 'JXG', 'JYD', 'JYNT', 'JZ', 'JZXN', 'KALA', 'KALV', 'KARO', 'KAT', 'KAVL', 'KBAB', 'KBSX', 'KBWB', 'KBWD', 'KBWP', 'KBWY', 'KC', 'KCHV', 'KDK', 'KDP', 'KE', 'KEAT', 'KELYA', 'KELYB', 'KFFB', 'KFII', 'KG', 'KGEI', 'KHC', 'KIDS', 'KIDZ', 'KINS', 'KITT', 'KLAC', 'KLIC', 'KLRS', 'KLTO', 'KLXE', 'KMB', 'KMDA', 'KMLI', 'KMRK', 'KMTS', 'KNDI', 'KNGZ', 'KNSA', 'KOD', 'KOID', 'KOPN', 'KOSS', 'KOYN', 'KPDD', 'KPLT', 'KPRX', 'KPTI', 'KQQQ', 'KRMA', 'KRMD', 'KRNT', 'KRNY', 'KROP', 'KROS', 'KRRO', 'KRT', 'KRUS', 'KRYS', 'KSCP', 'KSPI', 'KTCC', 'KTOS', 'KTTA', 'KURA', 'KVAC', 'KVHI', 'KWM', 'KXIN', 'KYIV', 'KYTX', 'KZIA', 'LAB', 'LAES', 'LAKE', 'LAND', 'LANDM', 'LANDO', 'LANDP', 'LARK', 'LASE', 'LAYS', 'LBGJ', 'LBRDA', 'LBRDK', 'LBRDP', 'LBRX', 'LBTYA', 'LBTYB', 'LBTYK', 'LCCC', 'LCDL', 'LCDS', 'LCFY', 'LCID', 'LCNB', 'LCUT', 'LDEM', 'LDRX', 'LDSF', 'LDWY', 'LE', 'LECO', 'LEDS', 'LEE', 'LEGH', 'LEGN', 'LENZ', 'LESL', 'LEXI', 'LEXX', 'LFMD', 'LFMDP', 'LFSC', 'LFST', 'LFUS', 'LFVN', 'LFWD', 'LGCB', 'LGCF', 'LGCL', 'LGHL', 'LGIH', 'LGN', 'LGND', 'LGO', 'LGRO', 'LGVN', 'LHAI', 'LI', 'LICN', 'LIEN', 'LIF', 'LILA', 'LILAK', 'LIMN', 'LIN', 'LINC', 'LIND', 'LINE', 'LINK', 'LIQT', 'LITE', 'LITM', 'LITP', 'LITS', 'LIVE', 'LIVN', 'LIXT', 'LKFN', 'LKQ', 'LLYVA', 'LLYVK', 'LLYZ', 'LMAT', 'LMB', 'LMBS', 'LMFA', 'LMTL', 'LMTS', 'LNKB', 'LNKS', 'LNT', 'LNTH', 'LNZA', 'LOAN', 'LOBO', 'LOCO', 'LOGI', 'LOGO', 'LOKV', 'LOOP', 'LOPE', 'LOT', 'LOVE', 'LPAA', 'LPBB', 'LPCN', 'LPLA', 'LPRO', 'LPSN', 'LPTH', 'LPTX', 'LQDA', 'LQDT', 'LRCX', 'LRE', 'LRGE', 'LRHC', 'LRND', 'LSAK', 'LSBK', 'LSCC', 'LSE', 'LSH', 'LSTA', 'LTRN', 'LTRX', 'LUCD', 'LUCY', 'LUNG', 'LVHD', 'LVO', 'LVRO', 'LVTX', 'LWAC', 'LWAY', 'LWLG', 'LX', 'LXEH', 'LXEO', 'LXRX', 'LYEL', 'LYFT', 'LYRA', 'LYTS', 'LZ', 'LZMH', 'MAAS', 'MACI', 'MAGH', 'MAMA', 'MAMK', 'MAMO', 'MANH', 'MAPS', 'MARA', 'MARPS', 'MASI', 'MASK', 'MASS', 'MAT', 'MATH', 'MAXI', 'MAXN', 'MAYA', 'MAYS', 'MAZE', 'MB', 'MBAV', 'MBB', 'MBBC', 'MBCN', 'MBIN', 'MBINL', 'MBINM', 'MBINN', 'MBIO', 'MBLY', 'MBNKO', 'MBOT', 'MBRX', 'MBS', 'MBWM', 'MBX', 'MCBS', 'MCDS', 'MCFT', 'MCGA', 'MCHB', 'MCHI', 'MCHP', 'MCHPP', 'MCHS', 'MCHX', 'MCRB', 'MCRI', 'MCSE', 'MDAI', 'MDB', 'MDBH', 'MDCX', 'MDGL', 'MDIA', 'MDIV', 'MDLZ', 'MDWD', 'MDXG', 'MDXH', 'MEDP', 'MEDX', 'MEGL', 'MELI', 'MEMS', 'MENS', 'MEOH', 'MERC', 'MESA', 'MESO', 'META', 'METC', 'METCB', 'METCI', 'METCZ', 'METD', 'METL', 'MFH', 'MFI', 'MFIC', 'MFICL', 'MFIN', 'MFLX', 'MGEE', 'MGIC', 'MGIH', 'MGNI', 'MGNX', 'MGPI', 'MGRC', 'MGRM', 'MGRT', 'MGRX', 'MGTX', 'MGX', 'MHUA', 'MIDD', 'MIGI', 'MILN', 'MIMI', 'MIND', 'MIRA', 'MIRM', 'MIST', 'MITK', 'MJID', 'MKAM', 'MKSI', 'MKTX', 'MLAB', 'MLAC', 'MLCI', 'MLCO', 'MLEC', 'MLGO', 'MLKN', 'MLTX', 'MLYS', 'MMLP', 'MMSI', 'MMYT', 'MNDO', 'MNDY', 'MNKD', 'MNMD', 'MNOV', 'MNRO', 'MNSB', 'MNSBP', 'MNST', 'MNTK', 'MNTS', 'MNY', 'MOB', 'MOBX', 'MODD', 'MODL', 'MOFG', 'MOGO', 'MOLN', 'MOMO', 'MOOD', 'MORN', 'MOVE', 'MPAA', 'MPB', 'MQ', 'MQQQ', 'MRAL', 'MRAM', 'MRBK', 'MRCC', 'MRCY', 'MREO', 'MRM', 'MRNA', 'MRNO', 'MRSN', 'MRTN', 'MRUS', 'MRVI', 'MRVL', 'MRX', 'MSAI', 'MSBI', 'MSBIP', 'MSDD', 'MSEX', 'MSFD', 'MSFL', 'MSFT', 'MSGM', 'MSGY', 'MSPRZ', 'MSS', 'MST', 'MSTP', 'MSTX', 'MTC', 'MTCH', 'MTEK', 'MTEN', 'MTEX', 'MTLS', 'MTRX', 'MTSI', 'MTVA', 'MTYY', 'MUD', 'MULL', 'MULT', 'MURA', 'MVBF', 'MVIS', 'MVLL', 'MVST', 'MWYN', 'MXCT', 'MXL', 'MYCF', 'MYCG', 'MYCH', 'MYCI', 'MYCJ', 'MYCK', 'MYCL', 'MYCM', 'MYCN', 'MYCO', 'MYGN', 'MYMF', 'MYMG', 'MYMH', 'MYMI', 'MYMJ', 'MYMK', 'MYNZ', 'MYPS', 'MYRG', 'MYSE', 'MYSZ', 'MZTI', 'NA', 'NAAS', 'NAGE', 'NAII', 'NAKA', 'NAMI', 'NAMM', 'NAMS', 'NAOV', 'NATH', 'NATO', 'NAUT', 'NAVI', 'NB', 'NBBK', 'NBIS', 'NBIX', 'NBN', 'NBTB', 'NBTX', 'NCI', 'NCIQ', 'NCMI', 'NCNA', 'NCNO', 'NCPB', 'NCPL', 'NCRA', 'NCSM', 'NCT', 'NCTY', 'NDAA', 'NDAQ', 'NDLS', 'NDRA', 'NDSN', 'NECB', 'NEGG', 'NEO', 'NEOG', 'NEON', 'NEOV', 'NEPH', 'NERD', 'NERV', 'NETD', 'NEUP', 'NEWT', 'NEWTG', 'NEWTH', 'NEWTI', 'NEWTP', 'NEWTZ', 'NEWZ', 'NEXM', 'NEXN', 'NEXT', 'NFBK', 'NFE', 'NFLX', 'NFTY', 'NFXL', 'NFXS', 'NGNE', 'NHIC', 'NHPAP', 'NHPBP', 'NHTC', 'NICE', 'NIKL', 'NIPG', 'NISN', 'NITO', 'NIVF', 'NIXT', 'NIXX', 'NKSH', 'NKTX', 'NLSP', 'NMFC', 'NMFCZ', 'NMIH', 'NMP', 'NMRA', 'NMRK', 'NMTC', 'NN', 'NNDM', 'NNE', 'NNNN', 'NNOX', 'NODK', 'NOEM', 'NOTV', 'NOVT', 'NOWL', 'NPAC', 'NPCE', 'NPFI', 'NRC', 'NRDS', 'NRES', 'NRIM', 'NRIX', 'NRSN', 'NRXP', 'NSI', 'NSIT', 'NSSC', 'NSTS', 'NSYS', 'NTAP', 'NTCL', 'NTCT', 'NTES', 'NTHI', 'NTIC', 'NTLA', 'NTNX', 'NTRA', 'NTRB', 'NTRP', 'NTRS', 'NTRSO', 'NTSK', 'NTWK', 'NTWO', 'NUAI', 'NUKK', 'NUSB', 'NUTX', 'NUVL', 'NUWE', 'NVA', 'NVAX', 'NVCT', 'NVD', 'NVDA', 'NVDD', 'NVDG', 'NVDL', 'NVDS', 'NVEC', 'NVFY', 'NVMI', 'NVNI', 'NVNO', 'NVTS', 'NVVE', 'NVX', 'NVYY', 'NWBI', 'NWE', 'NWFL', 'NWGL', 'NWL', 'NWPX', 'NWS', 'NWSA', 'NWTG', 'NXGL', 'NXL', 'NXPI', 'NXPL', 'NXST', 'NXT', 'NXTC', 'NXTG', 'NXTT', 'NXXT', 'NYAX', 'NYXH', 'NZAC', 'NZUS', 'OABI', 'OACC', 'OBA', 'OBIL', 'OBIO', 'OBLG', 'OBT', 'OCC', 'OCCI', 'OCCIM', 'OCCIN', 'OCCIO', 'OCFC', 'OCG', 'OCGN', 'OCS', 'OCSL', 'OCUL', 'ODD', 'ODDS', 'ODFL', 'ODP', 'ODVWZ', 'ODYS', 'OESX', 'OFAL', 'OFIX', 'OFLX', 'OFS', 'OFSSH', 'OFSSO', 'OGI', 'OKLL', 'OKTA', 'OKYO', 'OLB', 'OLED', 'OLLI', 'OLMA', 'OLPX', 'OM', 'OMAB', 'OMCC', 'OMCL', 'OMDA', 'OMEX', 'OMH', 'OMSE', 'ON', 'ONB', 'ONBPO', 'ONBPP', 'ONC', 'ONCH', 'ONCO', 'ONCY', 'ONDS', 'ONEG', 'ONEQ', 'ONFO', 'ONMD', 'OOQB', 'OOSB', 'OP', 'OPAL', 'OPBK', 'OPCH', 'OPEN', 'OPI', 'OPINL', 'OPK', 'OPPJ', 'OPRA', 'OPRT', 'OPRX', 'OPT', 'OPTX', 'OPTZ', 'OPXS', 'ORBS', 'ORCX', 'ORGN', 'ORGO', 'ORIC', 'ORIQ', 'ORIS', 'ORKA', 'ORKT', 'ORLY', 'ORMP', 'ORRF', 'OS', 'OSBC', 'OSCX', 'OSIS', 'OSPN', 'OSRH', 'OSS', 'OST', 'OTEX', 'OTGL', 'OTLK', 'OTLY', 'OUST', 'OUSTZ', 'OVBC', 'OVID', 'OVLY', 'OXLC', 'OXLCG', 'OXLCI', 'OXLCL', 'OXLCN', 'OXLCO', 'OXLCP', 'OXLCZ', 'OXSQ', 'OXSQG', 'OXSQH', 'OYSE', 'OZEM', 'OZK', 'OZKAP', 'PAA', 'PABD', 'PACB', 'PACH', 'PAGP', 'PAHC', 'PAL', 'PALD', 'PALI', 'PAMT', 'PANG', 'PANL', 'PASG', 'PATK', 'PATN', 'PAVM', 'PAVS', 'PAX', 'PAYO', 'PAYS', 'PAYX', 'PBBK', 'PBFS', 'PBHC', 'PBM', 'PBPB', 'PBQQ', 'PBYI', 'PC', 'PCAP', 'PCB', 'PCH', 'PCLA', 'PCMM', 'PCRX', 'PCSA', 'PCSC', 'PCT', 'PCTY', 'PCVX', 'PCYO', 'PDBA', 'PDBC', 'PDD', 'PDDL', 'PDEX', 'PDFS', 'PDLB', 'PDP', 'PDSB', 'PDYN', 'PEBK', 'PEBO', 'PECO', 'PEGA', 'PELI', 'PENG', 'PENN', 'PEP', 'PEPG', 'PEPS', 'PERI', 'PESI', 'PETS', 'PETZ', 'PEY', 'PEZ', 'PFAI', 'PFBC', 'PFF', 'PFG', 'PFI', 'PFIS', 'PFM', 'PFSA', 'PFX', 'PFXNZ', 'PGAC', 'PGC', 'PGEN', 'PGJ', 'PGNY', 'PGY', 'PHAT', 'PHH', 'PHIO', 'PHLT', 'PHO', 'PHOE', 'PHUN', 'PHVS', 'PI', 'PID', 'PIE', 'PIII', 'PINC', 'PIO', 'PIZ', 'PKBK', 'PKOH', 'PLAB', 'PLAY', 'PLBC', 'PLBL', 'PLBY', 'PLCE', 'PLMK', 'PLPC', 'PLRX', 'PLRZ', 'PLSE', 'PLT', 'PLTD', 'PLTG', 'PLTK', 'PLTS', 'PLTZ', 'PLUG', 'PLUS', 'PLUT', 'PLXS', 'PLYY', 'PMAX', 'PMBS', 'PMCB', 'PMEC', 'PMN', 'PMTS', 'PMVP', 'PN', 'PNBK', 'PNFP', 'PNFPP', 'PNQI', 'PNRG', 'PNTG', 'POAI', 'POCI', 'PODC', 'PODD', 'POET', 'POLA', 'POLE', 'PONY', 'POOL', 'POWI', 'POWL', 'POWWP', 'PPBT', 'PPC', 'PPCB', 'PPH', 'PPI', 'PPIH', 'PPSI', 'PPTA', 'PQAP', 'PQJA', 'PQJL', 'PQOC', 'PRAA', 'PRAX', 'PRCH', 'PRCT', 'PRDO', 'PRE', 'PRFX', 'PRFZ', 'PRGS', 'PRLD', 'PRME', 'PRN', 'PROF', 'PROK', 'PROP', 'PROV', 'PRPH', 'PRPL', 'PRPO', 'PRSO', 'PRTA', 'PRTC', 'PRTH', 'PRTS', 'PRVA', 'PRZO', 'PSC', 'PSCC', 'PSCD', 'PSCE', 'PSCF', 'PSCH', 'PSCI', 'PSCM', 'PSCT', 'PSEC', 'PSET', 'PSHG', 'PSIG', 'PSIX', 'PSKY', 'PSL', 'PSMT', 'PSNL', 'PSNY', 'PSTV', 'PSWD', 'PT', 'PTC', 'PTCT', 'PTEN', 'PTF', 'PTGX', 'PTH', 'PTHL', 'PTIX', 'PTLE', 'PTLO', 'PTNM', 'PTNQ', 'PTON', 'PTRN', 'PUBM', 'PUI', 'PULM', 'PVBC', 'PVLA', 'PWM', 'PWP', 'PWRD', 'PXI', 'PXS', 'PY', 'PYPD', 'PYPG', 'PYPL', 'PYXS', 'PYZ', 'PZZA', 'QABA', 'QALT', 'QAT', 'QB', 'QBIG', 'QBUF', 'QCLN', 'QCLS', 'QCMD', 'QCML', 'QCOM', 'QCRH', 'QDEL', 'QDTY', 'QETA', 'QFIN', 'QGRD', 'QH', 'QHDG', 'QIPT', 'QLDY', 'QLGN', 'QLYS', 'QMCO', 'QMID', 'QMMM', 'QMOM', 'QNCX', 'QNRX', 'QNST', 'QNTM', 'QNXT', 'QOWZ', 'QPUX', 'QQA', 'QQDN', 'QQHG', 'QQJG', 'QQLV', 'QQMG', 'QQQ', 'QQQA', 'QQQE', 'QQQG', 'QQQH', 'QQQI', 'QQQJ', 'QQQM', 'QQQP', 'QQQS', 'QQQT', 'QQQX', 'QQQY', 'QQUP', 'QQWZ', 'QQXL', 'QQXT', 'QRHC', 'QRMI', 'QRVO', 'QSEA', 'QSG', 'QSI', 'QSIX', 'QSML', 'QTEC', 'QTOP', 'QTRX', 'QTTB', 'QTUM', 'QUBT', 'QUIK', 'QURE', 'QVAL', 'QVCGA', 'QVCGP', 'QXQ', 'QYLD', 'QYLG', 'RAA', 'RAAQ', 'RADX', 'RAIL', 'RAIN', 'RAND', 'RANG', 'RANI', 'RAPP', 'RAPT', 'RARE', 'RAUS', 'RAVE', 'RAY', 'RAYA', 'RBB', 'RBBN', 'RBCAA', 'RBIL', 'RBKB', 'RBNE', 'RCAT', 'RCEL', 'RCGE', 'RCKT', 'RCKY', 'RCMT', 'RCON', 'RCT', 'RDAC', 'RDAG', 'RDCM', 'RDGT', 'RDHL', 'RDI', 'RDIB', 'RDNT', 'RDTL', 'RDTY', 'RDVT', 'RDVY', 'RDZN', 'REAI', 'REAL', 'REAX', 'REBN', 'RECT', 'REE', 'REFI', 'REG', 'REGCO', 'REGCP', 'REGN', 'REIT', 'RELI', 'RELL', 'RELY', 'REMG', 'RENB', 'RENT', 'REPL', 'RETO', 'REVB', 'REYN', 'RFAI', 'RFDI', 'RFEM', 'RFIL', 'RGC', 'RGCO', 'RGEN', 'RGLD', 'RGLO', 'RGNX', 'RGP', 'RGS', 'RGTI', 'RGTX', 'RIBB', 'RICK', 'RIGL', 'RILY', 'RILYG', 'RILYK', 'RILYL', 'RILYN', 'RILYP', 'RILYT', 'RILYZ', 'RIME', 'RING', 'RINT', 'RIOT', 'RIVN', 'RKDA', 'RKLB', 'RKLX', 'RLAY', 'RLMD', 'RLYB', 'RMBI', 'RMBS', 'RMCF', 'RMCO', 'RMNI', 'RMSG', 'RMTI', 'RNA', 'RNAC', 'RNAZ', 'RNEM', 'RNIN', 'RNRG', 'RNTX', 'RNXT', 'ROAD', 'ROBT', 'ROCK', 'ROE', 'ROIV', 'ROMA', 'ROOT', 'ROP', 'ROST', 'RPAY', 'RPD', 'RPID', 'RPRX', 'RPTX', 'RRBI', 'RRGB', 'RSSS', 'RTAC', 'RTH', 'RTXG', 'RUBI', 'RUM', 'RUN', 'RUNN', 'RUSC', 'RUSHA', 'RUSHB', 'RVMD', 'RVNL', 'RVPH', 'RVSB', 'RVSN', 'RVYL', 'RWAY', 'RWAYL', 'RWAYZ', 'RXRX', 'RXST', 'RXT', 'RYAAY', 'RYET', 'RYM', 'RYOJ', 'RYTM', 'RZLT', 'RZLV', 'SABS', 'SAFT', 'SAFX', 'SAGT', 'SAIA', 'SAIC', 'SAIH', 'SAIL', 'SAMG', 'SANA', 'SANG', 'SANM', 'SARK', 'SATL', 'SATS', 'SAVA', 'SBAC', 'SBC', 'SBCF', 'SBET', 'SBFG', 'SBFM', 'SBGI', 'SBLK', 'SBLX', 'SBRA', 'SBUX', 'SCAG', 'SCDS', 'SCHL', 'SCKT', 'SCLX', 'SCNI', 'SCNX', 'SCPH', 'SCSC', 'SCVL', 'SCWO', 'SCYX', 'SCZ', 'SDA', 'SDG', 'SDHI', 'SDM', 'SDOT', 'SDSI', 'SDST', 'SDTY', 'SDVY', 'SEAT', 'SEDG', 'SEED', 'SEEM', 'SEGG', 'SEIC', 'SEIE', 'SEIS', 'SELF', 'SELX', 'SENEA', 'SENEB', 'SEPN', 'SERA', 'SERV', 'SETM', 'SEVN', 'SEZL', 'SFBC', 'SFD', 'SFHG', 'SFIX', 'SFLO', 'SFM', 'SFNC', 'SFST', 'SFWL', 'SGA', 'SGBX', 'SGC', 'SGD', 'SGHT', 'SGLY', 'SGML', 'SGMO', 'SGMT', 'SGRP', 'SGRY', 'SHBI', 'SHC', 'SHEN', 'SHFS', 'SHIM', 'SHIP', 'SHLS', 'SHMD', 'SHOO', 'SHOP', 'SHOT', 'SHPD', 'SHPH', 'SHRY', 'SHV', 'SHY', 'SIBN', 'SIEB', 'SIFY', 'SIGA', 'SIGI', 'SIGIP', 'SILC', 'SILO', 'SIMA', 'SIMO', 'SINT', 'SION', 'SIRI', 'SISI', 'SITM', 'SIXG', 'SJ', 'SJCP', 'SJLD', 'SKBL', 'SKIN', 'SKK', 'SKRE', 'SKWD', 'SKYE', 'SKYQ', 'SKYT', 'SKYX', 'SKYY', 'SLAB', 'SLDB', 'SLDE', 'SLDP', 'SLE', 'SLGL', 'SLM', 'SLMBP', 'SLN', 'SLNG', 'SLNH', 'SLNHP', 'SLNO', 'SLP', 'SLQD', 'SLRC', 'SLRX', 'SLS', 'SLSN', 'SLVO', 'SLXN', 'SMBC', 'SMCC', 'SMCF', 'SMCI', 'SMCL', 'SMCO', 'SMCX', 'SMCZ', 'SMH', 'SMHX', 'SMID', 'SMMT', 'SMOM', 'SMPL', 'SMRI', 'SMSI', 'SMST', 'SMTC', 'SMTI', 'SMTK', 'SMX', 'SMXT', 'SNAL', 'SNCY', 'SND', 'SNDK', 'SNDL', 'SNDX', 'SNES', 'SNEX', 'SNFCA', 'SNGX', 'SNOA', 'SNPS', 'SNSE', 'SNT', 'SNTG', 'SNTI', 'SNWV', 'SNY', 'SOCA', 'SOCL', 'SOFI', 'SOFX', 'SOGP', 'SOHO', 'SOHOB', 'SOHON', 'SOHOO', 'SOLT', 'SOLZ', 'SOND', 'SONM', 'SONN', 'SONO', 'SOPA', 'SOPH', 'SORA', 'SOTK', 'SOUN', 'SOUX', 'SOWG', 'SOXQ', 'SOXX', 'SPAI', 'SPAM', 'SPAQ', 'SPBC', 'SPC', 'SPCB', 'SPCX', 'SPCY', 'SPEG', 'SPFI', 'SPHL', 'SPKL', 'SPNS', 'SPOK', 'SPPL', 'SPRB', 'SPRC', 'SPRO', 'SPRX', 'SPRY', 'SPSC', 'SPT', 'SPWH', 'SPXD', 'SPYQ', 'SQFT', 'SQFTP', 'SQLV', 'SQQQ', 'SRAD', 'SRBK', 'SRCE', 'SRDX', 'SRET', 'SRPT', 'SRRK', 'SRTA', 'SRTS', 'SRZN', 'SSBI', 'SSII', 'SSKN', 'SSM', 'SSNC', 'SSP', 'SSRM', 'SSSS', 'SSSSL', 'SSTI', 'SSYS', 'STAA', 'STAI', 'STAK', 'STBA', 'STEC', 'STEP', 'STEX', 'STFS', 'STHO', 'STI', 'STIM', 'STKE', 'STKH', 'STKL', 'STKS', 'STLD', 'STNC', 'STNE', 'STOK', 'STRA', 'STRC', 'STRD', 'STRF', 'STRK', 'STRL', 'STRO', 'STRRP', 'STRS', 'STRT', 'STRZ', 'STSS', 'STTK', 'STX', 'SUGP', 'SUIG', 'SUNE', 'SUNS', 'SUPN', 'SUPP', 'SUPX', 'SURG', 'SUSB', 'SUSC', 'SUSL', 'SUUN', 'SVA', 'SVC', 'SVCC', 'SVCO', 'SVII', 'SVRA', 'SVRE', 'SWAG', 'SWBI', 'SWIM', 'SWIN', 'SWKH', 'SWKHL', 'SWKS', 'SWP', 'SWVL', 'SXTC', 'SXTP', 'SY', 'SYBT', 'SYBX', 'SYM', 'SYNA', 'SYRE', 'SYTA', 'SYZ', 'SZZL', 'TACH', 'TACO', 'TACT', 'TAIT', 'TALK', 'TANH', 'TAOP', 'TAOX', 'TARA', 'TARK', 'TARS', 'TASK', 'TATT', 'TAVI', 'TAX', 'TAXE', 'TAXI', 'TAXS', 'TAXT', 'TAYD', 'TBBK', 'TBCH', 'TBH', 'TBHC', 'TBIL', 'TBLA', 'TBLD', 'TBMC', 'TBPH', 'TBRG', 'TC', 'TCBI', 'TCBIO', 'TCBK', 'TCBS', 'TCBX', 'TCHI', 'TCMD', 'TCOM', 'TCPC', 'TCRT', 'TCRX', 'TCX', 'TDAC', 'TDI', 'TDIC', 'TDIV', 'TDSB', 'TDSC', 'TDTH', 'TDUP', 'TEAD', 'TEAM', 'TECH', 'TECTP', 'TECX', 'TEKX', 'TEKY', 'TELA', 'TELO', 'TEM', 'TENB', 'TENX', 'TERN', 'TEXN', 'TFNS', 'TFSL', 'TGHL', 'TGL', 'TGTX', 'TH', 'THCH', 'THFF', 'THH', 'THMZ', 'THRM', 'THRY', 'THTX', 'TIGO', 'TIL', 'TILE', 'TIPT', 'TIRX', 'TITN', 'TIVC', 'TKLF', 'TKNO', 'TLF', 'TLIH', 'TLN', 'TLPH', 'TLRY', 'TLS', 'TLSA', 'TLSI', 'TLT', 'TLX', 'TMB', 'TMC', 'TMCI', 'TMDX', 'TMED', 'TMET', 'TMUS', 'TMUSI', 'TMUSL', 'TMUSZ', 'TNDM', 'TNGX', 'TNMG', 'TNON', 'TNXP', 'TNYA', 'TOI', 'TOMZ', 'TONX', 'TOP', 'TORO', 'TOWN', 'TOYO', 'TPCS', 'TPG', 'TPGXL', 'TPLS', 'TPST', 'TQQQ', 'TQQY', 'TRDA', 'TREE', 'TRI', 'TRIB', 'TRIN', 'TRINI', 'TRINZ', 'TRIP', 'TRMB', 'TRMD', 'TRMK', 'TRML', 'TRNS', 'TRON', 'TROO', 'TRS', 'TRSG', 'TRST', 'TRUD', 'TRUE', 'TRUG', 'TRUP', 'TRUT', 'TRVG', 'TRVI', 'TSAT', 'TSBK', 'TSCO', 'TSDD', 'TSEL', 'TSEM', 'TSHA', 'TSL', 'TSLA', 'TSLG', 'TSLL', 'TSLQ', 'TSLS', 'TSMG', 'TSMX', 'TSMZ', 'TSPY', 'TSSI', 'TSYY', 'TTAN', 'TTD', 'TTEC', 'TTEK', 'TTEQ', 'TTGT', 'TTMI', 'TTNP', 'TTSH', 'TTWO', 'TUG', 'TUGN', 'TURB', 'TURF', 'TUSK', 'TVA', 'TVAI', 'TVGN', 'TVRD', 'TVTX', 'TWFG', 'TWG', 'TWIN', 'TWNP', 'TWST', 'TXG', 'TXMD', 'TXN', 'TXRH', 'TXSS', 'TXUE', 'TXUG', 'TYGO', 'TYRA', 'TZOO', 'TZUP', 'UAE', 'UAL', 'UBCP', 'UBFO', 'UBND', 'UBRL', 'UBSI', 'UBXG', 'UCL', 'UCRD', 'UCTT', 'UCYB', 'UDMY', 'UEIC', 'UEVM', 'UFCS', 'UFG', 'UFIV', 'UFO', 'UFPI', 'UFPT', 'UG', 'UGRO', 'UHG', 'UITB', 'UIVM', 'UK', 'ULBI', 'ULCC', 'ULH', 'ULTA', 'ULVM', 'ULY', 'UMBF', 'UMBFO', 'UMMA', 'UNB', 'UNCY', 'UNHG', 'UNIT', 'UNIY', 'UNTY', 'UOKA', 'UONE', 'UONEK', 'UPB', 'UPBD', 'UPC', 'UPLD', 'UPST', 'UPWK', 'UPXI', 'URBN', 'URGN', 'URNJ', 'UROY', 'USAF', 'USCB', 'USCL', 'USDX', 'USEA', 'USEG', 'USFI', 'USGO', 'USIG', 'USIN', 'USIO', 'USLM', 'USMC', 'USOI', 'USOY', 'USRD', 'USSH', 'USTB', 'USVM', 'USVN', 'USXF', 'UTEN', 'UTHY', 'UTMD', 'UTRE', 'UTSI', 'UTWO', 'UTWY', 'UVSP', 'UXIN', 'UYLD', 'UYSC', 'VABK', 'VACH', 'VALN', 'VANI', 'VBIL', 'VBIX', 'VBNK', 'VBTX', 'VC', 'VCEL', 'VCIC', 'VCIG', 'VCIT', 'VCLT', 'VCRB', 'VCSH', 'VCYT', 'VECO', 'VEEA', 'VEEE', 'VELO', 'VEON', 'VERA', 'VERI', 'VERO', 'VERX', 'VFF', 'VFLO', 'VFS', 'VGAS', 'VGIT', 'VGLT', 'VGSH', 'VGUS', 'VHC', 'VIASP', 'VIAV', 'VIGI', 'VINP', 'VIOT', 'VIRC', 'VITL', 'VIVK', 'VIVS', 'VIXI', 'VKTX', 'VLGEA', 'VLY', 'VLYPN', 'VLYPO', 'VLYPP', 'VMBS', 'VMD', 'VMEO', 'VNDA', 'VNET', 'VNME', 'VNOM', 'VNQI', 'VOD', 'VOLT', 'VONE', 'VONG', 'VONV', 'VOTE', 'VPLS', 'VRA', 'VRAX', 'VRCA', 'VRDN', 'VREX', 'VRIG', 'VRM', 'VRME', 'VRNA', 'VRNS', 'VRNT', 'VRRM', 'VRSK', 'VRSN', 'VRTL', 'VRTX', 'VS', 'VSA', 'VSAT', 'VSDA', 'VSEC', 'VSEE', 'VSME', 'VSMV', 'VSTA', 'VSTD', 'VSTL', 'VSTM', 'VTC', 'VTGN', 'VTIP', 'VTRS', 'VTSI', 'VTVT', 'VTWG', 'VTWO', 'VTWV', 'VTYX', 'VUZI', 'VVOS', 'VWAV', 'VWOB', 'VXUS', 'VYMI', 'VYNE', 'WABC', 'WABF', 'WAFD', 'WAFDP', 'WAI', 'WALD', 'WASH', 'WATT', 'WAVE', 'WAY', 'WB', 'WBD', 'WBTN', 'WBUY', 'WCLD', 'WCT', 'WDAF', 'WDAY', 'WDC', 'WDFC', 'WDGF', 'WEEI', 'WEN', 'WENN', 'WERN', 'WEST', 'WETH', 'WETO', 'WEYS', 'WFCF', 'WFF', 'WFRD', 'WGMI', 'WGRX', 'WGS', 'WHF', 'WHFCL', 'WHLRD', 'WHLRL', 'WHLRP', 'WHWK', 'WILC', 'WIMI', 'WINA', 'WING', 'WISE', 'WIX', 'WKEY', 'WKHS', 'WKSP', 'WLAC', 'WLDN', 'WLDS', 'WLFC', 'WMG', 'WNEB', 'WOK', 'WOOD', 'WOOF', 'WORX', 'WPRT', 'WRAP', 'WRD', 'WRLD', 'WRND', 'WSBC', 'WSBCP', 'WSBF', 'WSBK', 'WSC', 'WSFS', 'WSML', 'WTBA', 'WTBN', 'WTF', 'WTFC', 'WTFCN', 'WTG', 'WTIP', 'WTMY', 'WTO', 'WULF', 'WVE', 'WVVI', 'WVVIP', 'WWD', 'WXM', 'WYFI', 'WYHG', 'WYNN', 'XAIX', 'XBIL', 'XBIO', 'XBIT', 'XBP', 'XBTY', 'XCH', 'XCNY', 'XEL', 'XELB', 'XENE', 'XERS', 'XFIX', 'XGN', 'XHG', 'XHLD', 'XLO', 'XMAG', 'XNET', 'XOMA', 'XOMAO', 'XOMAP', 'XOMX', 'XOMZ', 'XOS', 'XP', 'XPEL', 'XPON', 'XRAY', 'XRPI', 'XRPT', 'XRTX', 'XRX', 'XT', 'XTIA', 'XTKG', 'XTLB', 'XWEL', 'XXII', 'XYZG', 'YAAS', 'YB', 'YDES', 'YDKG', 'YGMZ', 'YHC', 'YHGJ', 'YHNA', 'YI', 'YIBO', 'YJ', 'YLDE', 'YMAT', 'YMT', 'YNOT', 'YOKE', 'YOUL', 'YQ', 'YQQQ', 'YSPY', 'YSXT', 'YTRA', 'YXT', 'YYAI', 'YYGH', 'Z', 'ZAP', 'ZAZZT', 'ZBAI', 'ZBAO', 'ZBIO', 'ZBRA', 'ZBZZT', 'ZCMD', 'ZCZZT', 'ZD', 'ZDAI', 'ZENA', 'ZENV', 'ZEO', 'ZEUS', 'ZFZZT', 'ZG', 'ZGM', 'ZIMV', 'ZION', 'ZIONP', 'ZIPP', 'ZJK', 'ZJYL', 'ZJZZT', 'ZKIN', 'ZLAB', 'ZM', 'ZNB', 'ZNTL', 'ZOOZ', 'ZS', 'ZSPC', 'ZTEK', 'ZTEN', 'ZTOP', 'ZTRE', 'ZTWO', 'ZUMZ', 'ZURA', 'ZVRA', 'ZVZZT', 'ZWZZT', 'ZXZZT', 'ZYBT', 'ZYME', 'ZYN', 'ZYXI'
]

# NYSE Comprehensive - All NYSE-listed stocks (5,618 stocks)
NYSE_COMPREHENSIVE = [
    'A', 'AA', 'AAA', 'AAAA', 'AAM', 'AAMI', 'AAP', 'AAPX', 'AAPY', 'AAT',
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
    "NASDAQ_COMPOSITE": {
        "name": "NASDAQ Composite",
        "symbols": NASDAQ_COMPOSITE,
        "description": "Comprehensive coverage of major NASDAQ-listed companies",
        "estimated_time_minutes": 42.0
    },
    "NYSE_COMPOSITE": {
        "name": "NYSE Composite",
        "symbols": NYSE_COMPOSITE,
        "description": "Comprehensive coverage of major NYSE-listed companies",
        "estimated_time_minutes": 38.0
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