import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";

// Register service worker for performance and offline capability
if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('StockWise SW registered: ', registration);
        
        // Check for updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              console.log('StockWise SW: New content available, reload to update');
              // Could show update notification here
            }
          });
        });
      })
      .catch((error) => {
        console.log('StockWise SW registration failed: ', error);
      });
  });
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
