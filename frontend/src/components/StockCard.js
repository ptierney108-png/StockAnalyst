import React from 'react';
import { Link } from 'react-router-dom';
import { TrendingUp, TrendingDown } from 'lucide-react';

const StockCard = ({ stock }) => {
  const isPositive = stock.change >= 0;
  const changePercent = stock.change_percent?.replace('%', '') || '0';
  
  return (
    <Link
      to={`/analysis?symbol=${stock.symbol}`}
      className="block bg-white rounded-lg shadow hover:shadow-md transition-shadow duration-200 p-6"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <h3 className="text-lg font-bold text-gray-900">{stock.symbol}</h3>
            {isPositive ? (
              <TrendingUp className="h-4 w-4 text-green-500" />
            ) : (
              <TrendingDown className="h-4 w-4 text-red-500" />
            )}
          </div>
          <p className="text-sm text-gray-600 mb-3">{stock.name}</p>
          
          <div className="flex items-center justify-between">
            <div>
              <p className="text-2xl font-bold text-gray-900">
                ${stock.price?.toFixed(2) || '0.00'}
              </p>
            </div>
            
            <div className="text-right">
              <div className={`flex items-center space-x-1 ${
                isPositive ? 'text-green-600' : 'text-red-600'
              }`}>
                <span className="font-medium">
                  {isPositive ? '+' : ''}${stock.change?.toFixed(2) || '0.00'}
                </span>
              </div>
              <div className={`text-sm ${
                isPositive ? 'text-green-600' : 'text-red-600'
              }`}>
                {isPositive ? '+' : ''}{changePercent}%
              </div>
            </div>
          </div>
          
          {stock.volume && (
            <div className="mt-3 pt-3 border-t border-gray-100">
              <div className="flex justify-between text-sm text-gray-500">
                <span>Volume</span>
                <span>{stock.volume?.toLocaleString()}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </Link>
  );
};

export default StockCard;