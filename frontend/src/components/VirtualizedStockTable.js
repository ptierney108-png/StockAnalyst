import React, { memo, useMemo } from 'react';
import { FixedSizeList } from 'react-window';
import { Target, TrendingUp, TrendingDown } from 'lucide-react';

const VirtualizedStockTable = memo(({ 
  stocks, 
  sortBy, 
  sortDirection, 
  onSort, 
  detectPPOHook,
  onExport 
}) => {
  // Memoize sorted stocks to prevent unnecessary sorting
  const sortedStocks = useMemo(() => {
    if (!sortBy) return stocks;
    
    return [...stocks].sort((a, b) => {
      let aValue = a[sortBy];
      let bValue = b[sortBy];
      
      // Handle string comparisons
      if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }
      
      // Handle numeric comparisons
      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return sortDirection === 'asc' ? aValue - bValue : bValue - aValue;
      }
      
      // Handle string comparisons
      if (sortDirection === 'asc') {
        return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
      } else {
        return aValue > bValue ? -1 : aValue < bValue ? 1 : 0;
      }
    });
  }, [stocks, sortBy, sortDirection]);

  // Table header component
  const TableHeader = memo(() => (
    <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Target className="h-5 w-5 text-green-600" />
          <h2 className="text-xl font-bold text-gray-900">
            Screening Results ({stocks.length} stocks found)
          </h2>
        </div>
        <button 
          onClick={onExport}
          className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 font-medium transition-colors"
        >
          <span>Export Results</span>
        </button>
      </div>
      
      {/* Table Headers */}
      <div className="grid grid-cols-12 gap-2 text-xs font-medium text-gray-500 uppercase tracking-wider">
        <div 
          className="cursor-pointer hover:text-gray-700 flex items-center"
          onClick={() => onSort('symbol')}
        >
          Symbol {sortBy === 'symbol' && (sortDirection === 'asc' ? '↑' : '↓')}
        </div>
        <div className="col-span-2">Company</div>
        <div 
          className="cursor-pointer hover:text-gray-700 text-right"
          onClick={() => onSort('price')}
        >
          Price {sortBy === 'price' && (sortDirection === 'asc' ? '↑' : '↓')}
        </div>
        <div>Volume Today</div>
        <div>Volume Avg 3M</div>
        <div 
          className="cursor-pointer hover:text-gray-700 text-right"
          onClick={() => onSort('return1d')}
        >
          1D Return {sortBy === 'return1d' && (sortDirection === 'asc' ? '↑' : '↓')}
        </div>
        <div>DMI/ADX</div>
        <div>PPO (3 Days)</div>
        <div 
          className="cursor-pointer hover:text-gray-700 text-right"
          onClick={() => onSort('ppoSlope')}
        >
          PPO Slope {sortBy === 'ppoSlope' && (sortDirection === 'asc' ? '↑' : '↓')}
        </div>
        <div>Options</div>
        <div>Earnings</div>
        <div>Sector</div>
      </div>
    </div>
  ));

  // Individual stock row component (memoized for performance)
  const StockRow = memo(({ index, style }) => {
    const stock = sortedStocks[index];
    const hook = detectPPOHook(stock.ppoValues);
    
    return (
      <div style={style} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
        <div className="grid grid-cols-12 gap-2 px-6 py-3 text-sm">
          {/* Symbol */}
          <div className="font-bold text-blue-600">{stock.symbol}</div>
          
          {/* Company */}
          <div className="col-span-2 text-gray-900 truncate">{stock.name}</div>
          
          {/* Price */}
          <div className="text-right font-semibold text-gray-900">
            ${stock.price.toFixed(2)}
          </div>
          
          {/* Volume Today */}
          <div className="text-gray-600">
            {(stock.volume / 1000000).toFixed(1)}M
          </div>
          
          {/* Volume Avg 3M */}
          <div className="text-gray-600">
            {(stock.volume3m / 1000000).toFixed(1)}M
          </div>
          
          {/* 1D Return */}
          <div className={`text-right font-medium ${
            stock.return1d >= 0 ? 'text-green-600' : 'text-red-600'
          }`}>
            {stock.return1d >= 0 ? '+' : ''}{stock.return1d.toFixed(2)}%
          </div>
          
          {/* DMI/ADX */}
          <div className="text-center">
            <div className="text-xs text-gray-500">DMI: {stock.dmi.toFixed(1)}</div>
            <div className="text-xs text-gray-500">ADX: {stock.adx?.toFixed(1) || 'N/A'}</div>
          </div>
          
          {/* PPO (3 Days) */}
          <div className="text-center">
            <div className="space-y-1">
              {stock.ppoValues?.map((ppo, idx) => {
                const dayLabels = ['Today', 'Yesterday', '2 Days Ago'];
                return (
                  <div key={idx} className={`text-xs px-1 py-0.5 rounded font-medium ${
                    ppo >= 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    <div className="text-xs text-gray-500">{dayLabels[idx]}({idx})</div>
                    {ppo >= 0 ? '+' : ''}{ppo.toFixed(3)}
                  </div>
                );
              }) || 'N/A'}
            </div>
          </div>
          
          {/* PPO Slope */}
          <div className="text-right">
            <div className="space-y-1">
              <span className={`inline-flex items-center px-2 py-1 rounded text-xs font-semibold ${
                stock.ppoSlope >= 0 
                  ? 'bg-blue-100 text-blue-800' 
                  : 'bg-orange-100 text-orange-800'
              }`}>
                {hook === 'positive' && <span className="mr-1">⭐</span>}
                {hook === 'negative' && <span className="mr-1">⚠️</span>}
                {stock.ppoSlope >= 0 ? '+' : ''}{stock.ppoSlope.toFixed(2)}%
              </span>
              {hook && (
                <div className={`text-xs font-medium ${
                  hook === 'positive' ? 'text-green-700' : 'text-red-700'
                }`}>
                  {hook === 'positive' ? '+ Hook' : '- Hook'}
                </div>
              )}
            </div>
          </div>
          
          {/* Options */}
          <div className="text-center">
            <div className="space-y-1">
              {stock.optionable ? (
                <>
                  <div className="text-xs">
                    <span className="text-green-600 font-medium">C: {stock.callBid?.toFixed(2)}-{stock.callAsk?.toFixed(2)}</span>
                  </div>
                  <div className="text-xs">
                    <span className="text-red-600 font-medium">P: {stock.putBid?.toFixed(2)}-{stock.putAsk?.toFixed(2)}</span>
                  </div>
                  <div className="text-xs text-gray-500 font-medium">
                    Exp: {stock.optionsExpiration || 'N/A'}
                  </div>
                </>
              ) : (
                <span className="text-gray-400 text-xs">N/A</span>
              )}
            </div>
          </div>
          
          {/* Earnings */}
          <div className="text-center text-xs">
            <div className="text-gray-600">
              Last: {stock.lastEarnings?.toLocaleDateString() || 'N/A'}
            </div>
            <div className={`font-medium ${
              stock.daysToEarnings <= 7 ? 'text-orange-600' : 'text-gray-600'
            }`}>
              Next: {stock.nextEarnings?.toLocaleDateString() || 'N/A'}
            </div>
          </div>
          
          {/* Sector */}
          <div className="text-xs text-gray-600 truncate">
            {stock.sector}
          </div>
        </div>
      </div>
    );
  });

  // Calculate row height based on content
  const ROW_HEIGHT = 120; // Adjusted for multi-line content
  const HEADER_HEIGHT = 120;
  const MAX_HEIGHT = 600; // Maximum table height

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
      <TableHeader />
      
      {/* Virtualized List */}
      <div style={{ height: Math.min(MAX_HEIGHT, sortedStocks.length * ROW_HEIGHT + HEADER_HEIGHT) }}>
        <FixedSizeList
          height={Math.min(MAX_HEIGHT, sortedStocks.length * ROW_HEIGHT)}
          itemCount={sortedStocks.length}
          itemSize={ROW_HEIGHT}
          width="100%"
          itemData={sortedStocks}
        >
          {StockRow}
        </FixedSizeList>
      </div>
      
      {/* Footer with performance info */}
      <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 text-sm text-gray-600">
        <div className="flex justify-between items-center">
          <span>Displaying {sortedStocks.length} results with virtualization</span>
          <span>Scroll performance optimized for large datasets</span>
        </div>
      </div>
    </div>
  );
});

VirtualizedStockTable.displayName = 'VirtualizedStockTable';

export default VirtualizedStockTable;