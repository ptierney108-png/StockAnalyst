import React from 'react';

// Reusable skeleton components for better loading states
export const StockCardSkeleton = () => (
  <div className="animate-pulse bg-white p-6 rounded-lg border border-gray-200">
    <div className="flex justify-between items-start mb-4">
      <div>
        <div className="h-6 bg-gray-200 rounded w-20 mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-32"></div>
      </div>
      <div className="h-8 bg-gray-200 rounded w-16"></div>
    </div>
    <div className="space-y-3">
      <div className="h-4 bg-gray-200 rounded w-full"></div>
      <div className="h-4 bg-gray-200 rounded w-3/4"></div>
      <div className="h-4 bg-gray-200 rounded w-1/2"></div>
    </div>
  </div>
);

export const ChartSkeleton = () => (
  <div className="animate-pulse bg-white p-6 rounded-lg border border-gray-200">
    <div className="h-6 bg-gray-200 rounded w-48 mb-6"></div>
    <div className="space-y-2">
      {[...Array(8)].map((_, i) => (
        <div key={i} className="flex items-end space-x-1">
          {[...Array(12)].map((_, j) => (
            <div
              key={j}
              className="bg-gray-200 rounded-t"
              style={{
                height: `${Math.random() * 100 + 20}px`,
                width: '20px'
              }}
            ></div>
          ))}
        </div>
      ))}
    </div>
  </div>
);

export const TableSkeleton = ({ rows = 5, cols = 6 }) => (
  <div className="animate-pulse bg-white rounded-lg border border-gray-200 overflow-hidden">
    {/* Header */}
    <div className="bg-gray-50 px-6 py-4 border-b">
      <div className="grid grid-cols-6 gap-4">
        {[...Array(cols)].map((_, i) => (
          <div key={i} className="h-4 bg-gray-200 rounded"></div>
        ))}
      </div>
    </div>
    
    {/* Rows */}
    {[...Array(rows)].map((_, i) => (
      <div key={i} className="px-6 py-4 border-b border-gray-100">
        <div className="grid grid-cols-6 gap-4">
          {[...Array(cols)].map((_, j) => (
            <div key={j} className="h-4 bg-gray-200 rounded"></div>
          ))}
        </div>
      </div>
    ))}
  </div>
);

export const AnalysisSkeleton = () => (
  <div className="animate-pulse space-y-6">
    {/* Header section */}
    <div className="bg-white p-6 rounded-lg border border-gray-200">
      <div className="flex items-center justify-between mb-4">
        <div className="h-8 bg-gray-200 rounded w-40"></div>
        <div className="h-6 bg-gray-200 rounded w-24"></div>
      </div>
      <div className="grid grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="text-center">
            <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
            <div className="h-6 bg-gray-200 rounded w-3/4 mx-auto"></div>
          </div>
        ))}
      </div>
    </div>
    
    {/* Chart section */}
    <ChartSkeleton />
    
    {/* Indicators section */}
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {[...Array(4)].map((_, i) => (
        <div key={i} className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="h-6 bg-gray-200 rounded w-32 mb-4"></div>
          <div className="space-y-2">
            <div className="h-4 bg-gray-200 rounded w-full"></div>
            <div className="h-4 bg-gray-200 rounded w-2/3"></div>
          </div>
        </div>
      ))}
    </div>
  </div>
);

export default {
  StockCardSkeleton,
  ChartSkeleton,
  TableSkeleton,
  AnalysisSkeleton
};