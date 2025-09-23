import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Navigation from './components/Navigation';
import { AnalysisSkeleton, StockCardSkeleton, TableSkeleton } from './components/LoadingSkeleton';
import './App.css';

// Lazy load all major pages for better performance
const Dashboard = lazy(() => import('./pages/Dashboard'));
const StockDetail = lazy(() => import('./pages/StockDetail'));
const Portfolio = lazy(() => import('./pages/Portfolio'));
const Watchlist = lazy(() => import('./pages/Watchlist'));
const Market = lazy(() => import('./pages/Market'));
const StockAnalysis = lazy(() => import('./components/StockAnalysis'));
const StockScreener = lazy(() => import('./pages/StockScreener'));
const PointBasedDecision = lazy(() => import('./pages/PointBasedDecision'));

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navigation />
          <main className="container mx-auto px-4 py-8">
            <Suspense fallback={
              <div className="max-w-7xl mx-auto px-6 py-8">
                <AnalysisSkeleton />
              </div>
            }>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/analysis" element={
                  <Suspense fallback={
                    <div className="max-w-7xl mx-auto px-6 py-8">
                      <AnalysisSkeleton />
                    </div>
                  }>
                    <StockAnalysis />
                  </Suspense>
                } />
                <Route path="/screener" element={
                  <Suspense fallback={
                    <div className="max-w-7xl mx-auto px-6 py-8">
                      <TableSkeleton rows={10} cols={8} />
                    </div>
                  }>
                    <StockScreener />
                  </Suspense>
                } />
                <Route path="/point-decision" element={<PointBasedDecision />} />
                <Route path="/stock/:symbol" element={<StockDetail />} />
                <Route path="/portfolio" element={<Portfolio />} />
                <Route path="/watchlist" element={<Watchlist />} />
                <Route path="/market" element={<Market />} />
              </Routes>
            </Suspense>
          </main>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;