import { useEffect, useCallback } from 'react';

// Performance monitoring hook and component
export const usePerformanceMonitor = (componentName) => {
  const trackRender = useCallback((phase) => {
    if (process.env.NODE_ENV === 'development') {
      const mark = `${componentName}-${phase}`;
      performance.mark(mark);
      
      if (phase === 'render-end') {
        const startMark = `${componentName}-render-start`;
        try {
          performance.measure(`${componentName}-render`, startMark, mark);
          const measure = performance.getEntriesByName(`${componentName}-render`)[0];
          if (measure.duration > 16) { // Warn if render takes more than 1 frame
            console.warn(`🐌 Slow render detected: ${componentName} took ${measure.duration.toFixed(2)}ms`);
          }
        } catch (e) {
          // Ignore measurement errors
        }
      }
    }
  }, [componentName]);

  useEffect(() => {
    trackRender('render-start');
    return () => trackRender('render-end');
  });

  return trackRender;
};

// Web Vitals monitoring
export const initWebVitalsMonitoring = () => {
  // Core Web Vitals tracking
  if (typeof window !== 'undefined' && 'PerformanceObserver' in window) {
    try {
      // Largest Contentful Paint (LCP)
      const lcpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        const lcp = lastEntry.startTime;
        
        console.log('📊 LCP (Largest Contentful Paint):', lcp.toFixed(2) + 'ms');
        
        // Track in analytics if available
        if (window.gtag) {
          window.gtag('event', 'web_vitals', {
            name: 'LCP',
            value: Math.round(lcp),
            event_category: 'Performance'
          });
        }
      });
      
      lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });

      // First Input Delay (FID)
      const fidObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry) => {
          const fid = entry.processingStart - entry.startTime;
          console.log('📊 FID (First Input Delay):', fid.toFixed(2) + 'ms');
          
          if (window.gtag) {
            window.gtag('event', 'web_vitals', {
              name: 'FID',
              value: Math.round(fid),
              event_category: 'Performance'
            });
          }
        });
      });
      
      fidObserver.observe({ entryTypes: ['first-input'] });

      // Cumulative Layout Shift (CLS)
      let clsValue = 0;
      const clsObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach((entry) => {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
          }
        });
        
        console.log('📊 CLS (Cumulative Layout Shift):', clsValue.toFixed(4));
        
        if (window.gtag) {
          window.gtag('event', 'web_vitals', {
            name: 'CLS',
            value: Math.round(clsValue * 1000),
            event_category: 'Performance'
          });
        }
      });
      
      clsObserver.observe({ entryTypes: ['layout-shift'] });

    } catch (error) {
      console.warn('Performance monitoring setup failed:', error);
    }
  }
};

// Bundle size monitoring
export const trackBundleSize = () => {
  if (typeof window !== 'undefined' && 'performance' in window) {
    window.addEventListener('load', () => {
      const navigation = performance.getEntriesByType('navigation')[0];
      if (navigation) {
        const totalSize = navigation.transferSize || 0;
        console.log('📦 Total bundle transfer size:', (totalSize / 1024).toFixed(2) + 'KB');
        
        // Track significant resources
        const resources = performance.getEntriesByType('resource');
        const jsResources = resources.filter(r => r.name.includes('.js'));
        const cssResources = resources.filter(r => r.name.includes('.css'));
        
        const jsSize = jsResources.reduce((sum, r) => sum + (r.transferSize || 0), 0);
        const cssSize = cssResources.reduce((sum, r) => sum + (r.transferSize || 0), 0);
        
        console.log('📦 JavaScript bundle size:', (jsSize / 1024).toFixed(2) + 'KB');
        console.log('📦 CSS bundle size:', (cssSize / 1024).toFixed(2) + 'KB');
      }
    });
  }
};

// Memory usage monitoring (Chrome only)
export const trackMemoryUsage = () => {
  if (typeof window !== 'undefined' && 'memory' in performance) {
    const logMemoryUsage = () => {
      const memory = performance.memory;
      console.log('🧠 Memory Usage:', {
        used: (memory.usedJSHeapSize / 1024 / 1024).toFixed(2) + 'MB',
        total: (memory.totalJSHeapSize / 1024 / 1024).toFixed(2) + 'MB',
        limit: (memory.jsHeapSizeLimit / 1024 / 1024).toFixed(2) + 'MB'
      });
    };
    
    // Log memory usage periodically
    setInterval(logMemoryUsage, 30000); // Every 30 seconds
    
    return logMemoryUsage;
  }
};

// API performance tracking
export const trackAPIPerformance = (url, startTime, endTime, success = true) => {
  const duration = endTime - startTime;
  const endpoint = new URL(url).pathname;
  
  console.log(`🌐 API ${success ? '✅' : '❌'} ${endpoint}: ${duration.toFixed(2)}ms`);
  
  // Track slow API calls
  if (duration > 3000) {
    console.warn(`🐌 Slow API detected: ${endpoint} took ${duration.toFixed(2)}ms`);
  }
  
  // Track in analytics if available
  if (window.gtag) {
    window.gtag('event', 'api_performance', {
      endpoint: endpoint,
      duration: Math.round(duration),
      success: success,
      event_category: 'Performance'
    });
  }
  
  return duration;
};

// Chart rendering performance
export const trackChartPerformance = (chartType, dataPoints, renderTime) => {
  console.log(`📊 Chart Performance - ${chartType}:`, {
    dataPoints: dataPoints,
    renderTime: renderTime.toFixed(2) + 'ms',
    pointsPerMs: (dataPoints / renderTime).toFixed(2)
  });
  
  // Warn about poor chart performance
  if (renderTime > 500) {
    console.warn(`🐌 Slow chart render: ${chartType} with ${dataPoints} points took ${renderTime.toFixed(2)}ms`);
  }
};

// Initialize all performance monitoring
export const initPerformanceMonitoring = () => {
  if (process.env.NODE_ENV === 'development') {
    console.log('🚀 StockWise Performance Monitoring Initialized');
    
    initWebVitalsMonitoring();
    trackBundleSize();
    trackMemoryUsage();
    
    // Track route changes
    let lastRoute = window.location.pathname;
    const trackRouteChange = () => {
      const currentRoute = window.location.pathname;
      if (currentRoute !== lastRoute) {
        console.log('🧭 Route change:', lastRoute, '→', currentRoute);
        lastRoute = currentRoute;
        
        // Track route performance
        performance.mark('route-change-start');
        setTimeout(() => {
          performance.mark('route-change-end');
          try {
            performance.measure('route-change', 'route-change-start', 'route-change-end');
            const measure = performance.getEntriesByName('route-change')[0];
            console.log('⏱️ Route change time:', measure.duration.toFixed(2) + 'ms');
          } catch (e) {
            // Ignore measurement errors
          }
        }, 100);
      }
    };
    
    // Listen for navigation changes
    window.addEventListener('popstate', trackRouteChange);
    
    // Override history methods to track programmatic navigation
    const originalPushState = history.pushState;
    const originalReplaceState = history.replaceState;
    
    history.pushState = function(...args) {
      originalPushState.apply(history, args);
      trackRouteChange();
    };
    
    history.replaceState = function(...args) {
      originalReplaceState.apply(history, args);
      trackRouteChange();
    };
  }
};

export default {
  usePerformanceMonitor,
  initPerformanceMonitoring,
  trackAPIPerformance,
  trackChartPerformance
};