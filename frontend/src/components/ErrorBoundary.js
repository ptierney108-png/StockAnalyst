import React, { Component } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { 
      hasError: false, 
      error: null, 
      errorInfo: null 
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
    
    // Log error to monitoring service
    console.error('StockWise Error:', error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ 
      hasError: false, 
      error: null, 
      errorInfo: null 
    });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[400px] flex items-center justify-center bg-gray-50 rounded-lg border border-gray-200">
          <div className="text-center p-8 max-w-md">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <AlertTriangle className="w-8 h-8 text-red-600" />
            </div>
            
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Something went wrong
            </h3>
            
            <p className="text-gray-600 mb-6">
              {this.props.fallbackMessage || 
               "We encountered an error while loading this section. This might be due to network issues or temporary service disruption."}
            </p>
            
            <div className="space-y-3">
              <button
                onClick={this.handleRetry}
                className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Try Again
              </button>
              
              {this.props.showDetails && this.state.error && (
                <details className="text-left bg-gray-100 p-4 rounded-lg text-sm">
                  <summary className="cursor-pointer font-medium text-gray-700 mb-2">
                    Error Details
                  </summary>
                  <div className="text-gray-600 font-mono text-xs">
                    <div className="mb-2">
                      <strong>Error:</strong> {this.state.error.toString()}
                    </div>
                    <div>
                      <strong>Component Stack:</strong>
                      <pre className="mt-1 whitespace-pre-wrap">
                        {this.state.errorInfo?.componentStack}
                      </pre>
                    </div>
                  </div>
                </details>
              )}
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

// Specialized error boundaries for different app sections
export const StockAnalysisErrorBoundary = ({ children }) => (
  <ErrorBoundary 
    fallbackMessage="Unable to load stock analysis data. This could be due to API rate limits or network connectivity issues."
    showDetails={process.env.NODE_ENV === 'development'}
  >
    {children}
  </ErrorBoundary>
);

export const StockScreenerErrorBoundary = ({ children }) => (
  <ErrorBoundary 
    fallbackMessage="Unable to load stock screening results. Please try adjusting your filter criteria or refreshing the page."
    showDetails={process.env.NODE_ENV === 'development'}
  >
    {children}
  </ErrorBoundary>
);

export const ChartErrorBoundary = ({ children }) => (
  <ErrorBoundary 
    fallbackMessage="Chart data could not be rendered. This might be due to invalid data or chart configuration issues."
    showDetails={process.env.NODE_ENV === 'development'}
  >
    {children}
  </ErrorBoundary>
);

export default ErrorBoundary;