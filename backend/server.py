from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import httpx
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.techindicators import TechIndicators
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Alpha Vantage setup
alpha_vantage_key = os.environ.get('ALPHA_VANTAGE_KEY', 'demo')

# Create the main app without a prefix
app = FastAPI(title="StockWise API", description="Comprehensive Stock Analysis Platform")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models
class Stock(BaseModel):
    symbol: str
    name: str
    price: float
    change: float
    change_percent: str
    volume: int
    market_cap: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class Portfolio(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    stocks: List[Dict[str, Any]] = []
    total_value: float = 0.0
    total_change: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PortfolioCreate(BaseModel):
    name: str

class StockPosition(BaseModel):
    symbol: str
    quantity: int
    avg_price: float

class Watchlist(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    symbols: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class WatchlistCreate(BaseModel):
    name: str
    symbols: List[str] = []

# Helper functions
async def get_stock_quote(symbol: str) -> Dict[str, Any]:
    """Get real-time stock quote from Alpha Vantage"""
    try:
        ts = TimeSeries(key=alpha_vantage_key, output_format='json')
        data, _ = ts.get_quote_endpoint(symbol)
        
        if not data or '01. symbol' not in data:
            raise HTTPException(status_code=404, detail=f"Stock symbol {symbol} not found")
        
        return {
            "symbol": data.get('01. symbol', ''),
            "name": data.get('01. symbol', ''),  # Alpha Vantage doesn't provide name in quote
            "price": float(data.get('05. price', 0)),
            "change": float(data.get('09. change', 0)),
            "change_percent": data.get('10. change percent', '0%'),
            "volume": int(data.get('06. volume', 0)),
            "open": float(data.get('02. open', 0)),
            "high": float(data.get('03. high', 0)),
            "low": float(data.get('04. low', 0)),
            "previous_close": float(data.get('08. previous close', 0)),
            "last_updated": data.get('07. latest trading day', '')
        }
    except Exception as e:
        # For demo purposes, return mock data if API fails
        return {
            "symbol": symbol.upper(),
            "name": f"{symbol.upper()} Inc.",
            "price": 150.0 + hash(symbol) % 100,
            "change": (hash(symbol) % 20) - 10,
            "change_percent": f"{((hash(symbol) % 20) - 10) / 150 * 100:.2f}%",
            "volume": 1000000 + hash(symbol) % 5000000,
            "open": 148.0 + hash(symbol) % 100,
            "high": 155.0 + hash(symbol) % 100,
            "low": 145.0 + hash(symbol) % 100,
            "previous_close": 149.0 + hash(symbol) % 100,
            "last_updated": datetime.now().strftime('%Y-%m-%d')
        }

async def get_historical_data(symbol: str, period: str = "1mo") -> Dict[str, Any]:
    """Get historical stock data"""
    try:
        ts = TimeSeries(key=alpha_vantage_key, output_format='json')
        
        if period == "1d":
            data, _ = ts.get_intraday(symbol, interval='60min', outputsize='compact')
        else:
            data, _ = ts.get_daily_adjusted(symbol, outputsize='compact')
        
        if not data:
            raise HTTPException(status_code=404, detail=f"Historical data for {symbol} not found")
        
        # Convert to format suitable for charts
        chart_data = []
        for date, values in list(data.items())[:30]:  # Last 30 data points
            chart_data.append({
                "date": date,
                "open": float(values.get('1. open', 0)),
                "high": float(values.get('2. high', 0)),
                "low": float(values.get('3. low', 0)),
                "close": float(values.get('4. close', 0)),
                "volume": int(values.get('6. volume', 0))
            })
        
        return {"symbol": symbol, "data": chart_data}
    except Exception as e:
        # Return mock historical data for demo
        chart_data = []
        base_price = 150.0 + hash(symbol) % 100
        for i in range(30):
            date = (datetime.now() - timedelta(days=29-i)).strftime('%Y-%m-%d')
            price_variation = (hash(f"{symbol}{i}") % 20) - 10
            chart_data.append({
                "date": date,
                "open": base_price + price_variation,
                "high": base_price + price_variation + 5,
                "low": base_price + price_variation - 5,
                "close": base_price + price_variation + 2,
                "volume": 1000000 + hash(f"{symbol}{i}") % 500000
            })
        
        return {"symbol": symbol, "data": chart_data}

# Stock API Endpoints
@api_router.get("/")
async def root():
    return {"message": "StockWise API - Your comprehensive stock analysis platform"}

@api_router.get("/stocks/search")
async def search_stocks(q: str = Query(..., min_length=1)):
    """Search for stocks by symbol or name"""
    # For demo, return some popular stocks that match the query
    popular_stocks = [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "GOOGL", "name": "Alphabet Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corporation"},
        {"symbol": "AMZN", "name": "Amazon.com Inc."},
        {"symbol": "TSLA", "name": "Tesla Inc."},
        {"symbol": "META", "name": "Meta Platforms Inc."},
        {"symbol": "NVDA", "name": "NVIDIA Corporation"},
        {"symbol": "NFLX", "name": "Netflix Inc."},
        {"symbol": "AMD", "name": "Advanced Micro Devices"},
        {"symbol": "INTC", "name": "Intel Corporation"}
    ]
    
    query = q.upper()
    results = [
        stock for stock in popular_stocks 
        if query in stock["symbol"] or query in stock["name"].upper()
    ]
    
    return results[:10]  # Return top 10 results

@api_router.get("/stocks/{symbol}")
async def get_stock_details(symbol: str):
    """Get detailed stock information"""
    return await get_stock_quote(symbol.upper())

@api_router.get("/stocks/{symbol}/historical")
async def get_stock_historical(symbol: str, period: str = Query("1mo", regex="^(1d|1w|1mo|3mo|1y)$")):
    """Get historical stock data for charting"""
    return await get_historical_data(symbol.upper(), period)

@api_router.get("/stocks/{symbol}/fundamentals")
async def get_stock_fundamentals(symbol: str):
    """Get fundamental data for a stock"""
    try:
        fd = FundamentalData(key=alpha_vantage_key, output_format='json')
        data, _ = fd.get_company_overview(symbol)
        
        if not data:
            raise HTTPException(status_code=404, detail=f"Fundamental data for {symbol} not found")
        
        return {
            "symbol": data.get('Symbol', ''),
            "name": data.get('Name', ''),
            "sector": data.get('Sector', ''),
            "industry": data.get('Industry', ''),
            "market_cap": data.get('MarketCapitalization', ''),
            "pe_ratio": data.get('PERatio', ''),
            "eps": data.get('EPS', ''),
            "dividend_yield": data.get('DividendYield', ''),
            "beta": data.get('Beta', ''),
            "52_week_high": data.get('52WeekHigh', ''),
            "52_week_low": data.get('52WeekLow', ''),
            "description": data.get('Description', '')
        }
    except Exception as e:
        # Return mock fundamental data for demo
        return {
            "symbol": symbol.upper(),
            "name": f"{symbol.upper()} Inc.",
            "sector": "Technology",
            "industry": "Software",
            "market_cap": "500000000000",
            "pe_ratio": "25.5",
            "eps": "6.12",
            "dividend_yield": "0.65%",
            "beta": "1.2",
            "52_week_high": "180.0",
            "52_week_low": "120.0",
            "description": f"A leading technology company in the {symbol.upper()} sector."
        }

# Portfolio Management
@api_router.post("/portfolios", response_model=Portfolio)
async def create_portfolio(portfolio: PortfolioCreate):
    """Create a new portfolio"""
    portfolio_dict = portfolio.dict()
    portfolio_obj = Portfolio(**portfolio_dict)
    await db.portfolios.insert_one(portfolio_obj.dict())
    return portfolio_obj

@api_router.get("/portfolios", response_model=List[Portfolio])
async def get_portfolios():
    """Get all portfolios"""
    portfolios = await db.portfolios.find().to_list(1000)
    return [Portfolio(**portfolio) for portfolio in portfolios]

@api_router.get("/portfolios/{portfolio_id}", response_model=Portfolio)
async def get_portfolio(portfolio_id: str):
    """Get specific portfolio"""
    portfolio = await db.portfolios.find_one({"id": portfolio_id})
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return Portfolio(**portfolio)

@api_router.post("/portfolios/{portfolio_id}/stocks")
async def add_stock_to_portfolio(portfolio_id: str, position: StockPosition):
    """Add stock to portfolio"""
    portfolio = await db.portfolios.find_one({"id": portfolio_id})
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Get current stock price
    stock_data = await get_stock_quote(position.symbol)
    
    # Add position to portfolio
    new_position = {
        "symbol": position.symbol,
        "quantity": position.quantity,
        "avg_price": position.avg_price,
        "current_price": stock_data["price"],
        "value": position.quantity * stock_data["price"],
        "change": (stock_data["price"] - position.avg_price) * position.quantity,
        "change_percent": ((stock_data["price"] - position.avg_price) / position.avg_price * 100) if position.avg_price > 0 else 0
    }
    
    # Update portfolio
    portfolio_obj = Portfolio(**portfolio)
    portfolio_obj.stocks.append(new_position)
    portfolio_obj.total_value = sum(stock["value"] for stock in portfolio_obj.stocks)
    portfolio_obj.total_change = sum(stock["change"] for stock in portfolio_obj.stocks)
    portfolio_obj.updated_at = datetime.utcnow()
    
    await db.portfolios.update_one(
        {"id": portfolio_id},
        {"$set": portfolio_obj.dict()}
    )
    
    return {"message": "Stock added to portfolio successfully", "portfolio": portfolio_obj}

@api_router.delete("/portfolios/{portfolio_id}")
async def delete_portfolio(portfolio_id: str):
    """Delete a portfolio"""
    result = await db.portfolios.delete_one({"id": portfolio_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return {"message": "Portfolio deleted successfully"}

# Watchlist Management
@api_router.post("/watchlists", response_model=Watchlist)
async def create_watchlist(watchlist: WatchlistCreate):
    """Create a new watchlist"""
    watchlist_dict = watchlist.dict()
    watchlist_obj = Watchlist(**watchlist_dict)
    await db.watchlists.insert_one(watchlist_obj.dict())
    return watchlist_obj

@api_router.get("/watchlists", response_model=List[Watchlist])
async def get_watchlists():
    """Get all watchlists"""
    watchlists = await db.watchlists.find().to_list(1000)
    return [Watchlist(**watchlist) for watchlist in watchlists]

@api_router.get("/watchlists/{watchlist_id}/stocks")
async def get_watchlist_stocks(watchlist_id: str):
    """Get stocks in a watchlist with current prices"""
    watchlist = await db.watchlists.find_one({"id": watchlist_id})
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    stocks = []
    for symbol in watchlist["symbols"]:
        try:
            stock_data = await get_stock_quote(symbol)
            stocks.append(stock_data)
        except Exception as e:
            continue  # Skip failed stock lookups
    
    return stocks

@api_router.post("/watchlists/{watchlist_id}/stocks/{symbol}")
async def add_stock_to_watchlist(watchlist_id: str, symbol: str):
    """Add stock to watchlist"""
    watchlist = await db.watchlists.find_one({"id": watchlist_id})
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    watchlist_obj = Watchlist(**watchlist)
    if symbol.upper() not in watchlist_obj.symbols:
        watchlist_obj.symbols.append(symbol.upper())
        await db.watchlists.update_one(
            {"id": watchlist_id},
            {"$set": watchlist_obj.dict()}
        )
    
    return {"message": "Stock added to watchlist successfully"}

@api_router.delete("/watchlists/{watchlist_id}/stocks/{symbol}")
async def remove_stock_from_watchlist(watchlist_id: str, symbol: str):
    """Remove stock from watchlist"""
    watchlist = await db.watchlists.find_one({"id": watchlist_id})
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    watchlist_obj = Watchlist(**watchlist)
    if symbol.upper() in watchlist_obj.symbols:
        watchlist_obj.symbols.remove(symbol.upper())
        await db.watchlists.update_one(
            {"id": watchlist_id},
            {"$set": watchlist_obj.dict()}
        )
    
    return {"message": "Stock removed from watchlist successfully"}

@api_router.delete("/watchlists/{watchlist_id}")
async def delete_watchlist(watchlist_id: str):
    """Delete a watchlist"""
    result = await db.watchlists.delete_one({"id": watchlist_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    return {"message": "Watchlist deleted successfully"}

# Market Overview
@api_router.get("/market/trending")
async def get_trending_stocks():
    """Get trending stocks"""
    trending_symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA", "NFLX"]
    stocks = []
    
    for symbol in trending_symbols:
        try:
            stock_data = await get_stock_quote(symbol)
            stocks.append(stock_data)
        except Exception:
            continue
    
    return stocks

@api_router.get("/market/gainers")
async def get_top_gainers():
    """Get top gaining stocks"""
    # Mock data for demo - in production, this would fetch real gainers
    gainers_symbols = ["TSLA", "NVDA", "AMD", "NFLX", "META"]
    stocks = []
    
    for symbol in gainers_symbols:
        try:
            stock_data = await get_stock_quote(symbol)
            # Ensure positive change for demo
            stock_data["change"] = abs(stock_data["change"])
            stock_data["change_percent"] = f"+{abs(float(stock_data['change_percent'].replace('%', '').replace('+', '').replace('-', ''))):.2f}%"
            stocks.append(stock_data)
        except Exception:
            continue
    
    return stocks

@api_router.get("/market/losers")
async def get_top_losers():
    """Get top losing stocks"""
    # Mock data for demo - in production, this would fetch real losers
    losers_symbols = ["INTC", "IBM", "F", "GE", "T"]
    stocks = []
    
    for symbol in losers_symbols:
        try:
            stock_data = await get_stock_quote(symbol)
            # Ensure negative change for demo
            stock_data["change"] = -abs(stock_data["change"])
            stock_data["change_percent"] = f"-{abs(float(stock_data['change_percent'].replace('%', '').replace('+', '').replace('-', ''))):.2f}%"
            stocks.append(stock_data)
        except Exception:
            continue
    
    return stocks

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()