#!/usr/bin/env python3
"""
Download complete NASDAQ and NYSE stock lists from official sources
Creates comprehensive stock universe with all available stocks
"""

import requests
import csv
import io
from typing import List, Set

def download_nasdaq_stocks() -> List[str]:
    """Download complete NASDAQ stock list from official NASDAQ trader"""
    try:
        url = "https://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse the pipe-delimited file
        stocks = []
        lines = response.text.strip().split('\n')
        
        for line in lines[1:]:  # Skip header
            if line.strip() and not line.startswith('File Creation Time'):
                fields = line.split('|')
                if len(fields) >= 1:
                    symbol = fields[0].strip()
                    
                    # Filter out test symbols and ETFs for stocks only
                    if symbol and len(symbol) <= 5:  # Basic symbol validation
                        # Skip obvious test symbols
                        if not symbol.startswith('TEST') and not symbol.endswith('.TEST'):
                            stocks.append(symbol)
        
        print(f"Downloaded {len(stocks)} NASDAQ stocks")
        return stocks
        
    except Exception as e:
        print(f"Error downloading NASDAQ stocks: {e}")
        return []

def download_nyse_stocks() -> List[str]:
    """Download complete NYSE and other exchange stocks from NASDAQ trader"""
    try:
        url = "https://www.nasdaqtrader.com/dynamic/symdir/otherlisted.txt"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse the pipe-delimited file
        stocks = []
        lines = response.text.strip().split('\n')
        
        for line in lines[1:]:  # Skip header
            if line.strip() and not line.startswith('File Creation Time'):
                fields = line.split('|')
                if len(fields) >= 3:
                    symbol = fields[0].strip()  # ACT Symbol
                    exchange = fields[2].strip() if len(fields) > 2 else ""  # Exchange
                    
                    # Focus on NYSE (N) and other major exchanges
                    if symbol and len(symbol) <= 5:  # Basic validation
                        if exchange in ['N', 'P', 'Z']:  # N=NYSE, P=NYSE Arca, Z=BATS
                            # Skip obvious test symbols  
                            if not symbol.startswith('TEST') and not symbol.endswith('.TEST'):
                                stocks.append(symbol)
        
        print(f"Downloaded {len(stocks)} NYSE and other exchange stocks")
        return stocks
        
    except Exception as e:
        print(f"Error downloading NYSE stocks: {e}")
        return []

def filter_common_stocks(stocks: List[str]) -> List[str]:
    """Filter to keep only common stock symbols"""
    filtered = []
    
    for symbol in stocks:
        # Skip symbols with periods, warrants, units, etc.
        if ('.' not in symbol and 
            not symbol.endswith('W') and  # Warrants
            not symbol.endswith('U') and  # Units  
            not symbol.endswith('R') and  # Rights
            len(symbol) >= 1 and len(symbol) <= 5):
            filtered.append(symbol)
    
    return filtered

def main():
    """Download and process complete stock universe"""
    print("Downloading complete NASDAQ and NYSE stock universe...")
    
    # Download stock lists
    nasdaq_stocks = download_nasdaq_stocks()
    nyse_stocks = download_nyse_stocks()
    
    # Filter to common stocks only
    nasdaq_common = filter_common_stocks(nasdaq_stocks)
    nyse_common = filter_common_stocks(nyse_stocks)
    
    # Remove duplicates and create comprehensive lists
    all_nasdaq = list(set(nasdaq_common))
    all_nyse = list(set(nyse_common))
    
    # Sort for consistency
    all_nasdaq.sort()
    all_nyse.sort()
    
    print(f"\nFinal counts:")
    print(f"NASDAQ stocks: {len(all_nasdaq)}")
    print(f"NYSE stocks: {len(all_nyse)}")
    print(f"Total unique stocks: {len(set(all_nasdaq + all_nyse))}")
    
    # Generate Python code for stock_universe.py
    print("\n# NASDAQ_COMPREHENSIVE - All NASDAQ-listed stocks")
    print(f"NASDAQ_COMPREHENSIVE = {all_nasdaq}")
    
    print(f"\n# NYSE_COMPREHENSIVE - All NYSE-listed stocks") 
    print(f"NYSE_COMPREHENSIVE = {all_nyse}")
    
    # Show samples
    print(f"\nSample NASDAQ stocks: {all_nasdaq[:10]}")
    print(f"Sample NYSE stocks: {all_nyse[:10]}")

if __name__ == "__main__":
    main()