# StockWise Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Vercel (Recommended - Free)
1. Create Vercel account
2. Upload this code to GitHub manually
3. Connect Vercel to your GitHub repo
4. Deploy with one click

### Option 2: Railway (Full-stack - $5/month)
1. Create Railway account
2. Upload code to GitHub manually
3. Connect Railway to GitHub repo
4. Deploy both frontend and backend

## 📁 Essential Files Structure
```
/backend/
  - server.py (FastAPI backend)
  - requirements.txt (Python dependencies)
  - .env (API keys - UPDATE THESE)

/frontend/
  - src/ (React components)
  - package.json (dependencies)
  - .env (backend URL - UPDATE THIS)
```

## 🔑 Environment Variables to Update

### Backend (.env):
```
ALPHA_VANTAGE_KEY=your_alpha_vantage_key
POLYGON_IO_API_KEY=your_polygon_key
MONGO_URL=your_mongodb_atlas_url
EMERGENT_LLM_KEY=replace_with_openai_key
```

### Frontend (.env):
```
REACT_APP_BACKEND_URL=your_deployed_backend_url
```

## 🛠 Local Development Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
python server.py

# Frontend (new terminal)
cd frontend
yarn install
yarn start
```

## 📞 Support Contacts
- Discord: https://discord.gg/VzKfwCXC4A
- Email: support@emergent.sh

## 🎯 Key Features Implemented
- Stock Screener with PPO Hook filtering
- Technical Analysis with performance optimizations
- Real-time data source indicators
- Point-based decision system
- Comprehensive results display