"""
Redis Caching Layer for Batch Stock Processing
Implements multi-level caching strategy:
- Level 1: In-memory cache (1-2 minute expiry)
- Level 2: Redis cache (5-minute expiry)  
- Level 3: MongoDB cache (background refresh)
"""

import json
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging
import os

logger = logging.getLogger(__name__)

# Try to import Redis clients, handle gracefully if not available
try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
    logger.info("Redis client available - persistence enabled")
except ImportError as e:
    REDIS_AVAILABLE = False
    redis = None
    logger = logging.getLogger(__name__)
    logger.warning(f"Redis not available ({e}), using in-memory cache only")

@dataclass
class CacheEntry:
    data: Any
    timestamp: datetime
    expiry: datetime
    source: str
    
    def to_dict(self):
        return {
            'data': self.data,
            'timestamp': self.timestamp.isoformat(),
            'expiry': self.expiry.isoformat(),
            'source': self.source
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data=data['data'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            expiry=datetime.fromisoformat(data['expiry']),
            source=data['source']
        )

class BatchCacheManager:
    """Multi-level caching manager for batch stock processing"""
    
    def __init__(self):
        self.redis_client = None
        self.memory_cache: Dict[str, CacheEntry] = {}
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'memory_hits': 0,
            'redis_hits': 0,
            'db_hits': 0
        }
        
        # Cache TTL settings (in seconds)
        self.MEMORY_TTL = 120  # 2 minutes
        self.REDIS_TTL = 300   # 5 minutes
        self.DB_TTL = 1800     # 30 minutes
        
    async def initialize(self):
        """Initialize Redis connection"""
        if not REDIS_AVAILABLE:
            logger.info("Redis not available, using in-memory cache only")
            return
            
        try:
            # Try to connect to Redis (will use default local Redis if available)
            redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
            self.redis_client = redis.from_url(
                redis_url, 
                encoding="utf-8", 
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )
            # Test connection
            await self.redis_client.ping()
            logger.info("Redis cache initialized successfully")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Using in-memory cache only.")
            self.redis_client = None
    
    def _generate_cache_key(self, symbol: str, data_type: str, timeframe: str = "default") -> str:
        """Generate standardized cache keys"""
        return f"batch_stock:{symbol}:{data_type}:{timeframe}"
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if cache entry is expired"""
        return datetime.utcnow() > entry.expiry
    
    async def get_cached_stock_data(self, symbol: str, data_type: str, timeframe: str = "default") -> Optional[Dict[str, Any]]:
        """
        Get cached stock data with multi-level cache lookup
        Returns: Cache data if found and valid, None otherwise
        """
        cache_key = self._generate_cache_key(symbol, data_type, timeframe)
        
        # Level 1: Check memory cache first
        if cache_key in self.memory_cache:
            entry = self.memory_cache[cache_key]
            if not self._is_expired(entry):
                self.cache_stats['hits'] += 1
                self.cache_stats['memory_hits'] += 1
                logger.debug(f"Memory cache hit for {cache_key}")
                return entry.data
            else:
                # Remove expired entry
                del self.memory_cache[cache_key]
        
        # Level 2: Check Redis cache
        if self.redis_client:
            try:
                redis_data = await self.redis_client.get(cache_key)
                if redis_data:
                    entry_dict = json.loads(redis_data)
                    entry = CacheEntry.from_dict(entry_dict)
                    
                    if not self._is_expired(entry):
                        self.cache_stats['hits'] += 1
                        self.cache_stats['redis_hits'] += 1
                        logger.debug(f"Redis cache hit for {cache_key}")
                        
                        # Promote to memory cache
                        self.memory_cache[cache_key] = entry
                        return entry.data
                    else:
                        # Remove expired Redis entry
                        await self.redis_client.delete(cache_key)
            except Exception as e:
                logger.warning(f"Redis cache lookup failed for {cache_key}: {e}")
        
        # Cache miss
        self.cache_stats['misses'] += 1
        logger.debug(f"Cache miss for {cache_key}")
        return None
    
    async def set_cached_stock_data(self, symbol: str, data_type: str, data: Dict[str, Any], 
                                  timeframe: str = "default", source: str = "api"):
        """
        Cache stock data in multiple levels
        """
        cache_key = self._generate_cache_key(symbol, data_type, timeframe)
        timestamp = datetime.utcnow()
        
        # Create cache entries with different expiry times
        memory_entry = CacheEntry(
            data=data,
            timestamp=timestamp,
            expiry=timestamp + timedelta(seconds=self.MEMORY_TTL),
            source=source
        )
        
        redis_entry = CacheEntry(
            data=data,
            timestamp=timestamp,
            expiry=timestamp + timedelta(seconds=self.REDIS_TTL),
            source=source
        )
        
        # Store in memory cache
        self.memory_cache[cache_key] = memory_entry
        
        # Store in Redis cache
        if self.redis_client:
            try:
                await self.redis_client.setex(
                    cache_key,
                    self.REDIS_TTL,
                    json.dumps(redis_entry.to_dict(), default=str)
                )
                logger.debug(f"Cached data in Redis for {cache_key}")
            except Exception as e:
                logger.warning(f"Redis cache storage failed for {cache_key}: {e}")
    
    async def get_batch_progress(self, batch_id: str) -> Optional[Dict[str, Any]]:
        """Get batch processing progress"""
        cache_key = f"batch_progress:{batch_id}"
        
        if self.redis_client:
            try:
                progress_data = await self.redis_client.get(cache_key)
                if progress_data:
                    return json.loads(progress_data)
            except Exception as e:
                logger.warning(f"Failed to get batch progress {batch_id}: {e}")
        
        # Fallback to memory cache
        if cache_key in self.memory_cache:
            entry = self.memory_cache[cache_key]
            if not self._is_expired(entry):
                return entry.data
        
        return None
    
    async def set_batch_progress(self, batch_id: str, progress_data: Dict[str, Any]):
        """Set batch processing progress with 30-minute expiry"""
        cache_key = f"batch_progress:{batch_id}"
        
        # Store in Redis with 30-minute expiry
        if self.redis_client:
            try:
                await self.redis_client.setex(
                    cache_key,
                    1800,  # 30 minutes
                    json.dumps(progress_data, default=str)
                )
            except Exception as e:
                logger.warning(f"Failed to set batch progress {batch_id}: {e}")
        
        # Store in memory cache as backup
        timestamp = datetime.utcnow()
        entry = CacheEntry(
            data=progress_data,
            timestamp=timestamp,
            expiry=timestamp + timedelta(seconds=1800),
            source="batch_progress"
        )
        self.memory_cache[cache_key] = entry
    
    def cleanup_memory_cache(self):
        """Clean up expired entries from memory cache"""
        expired_keys = [
            key for key, entry in self.memory_cache.items() 
            if self._is_expired(entry)
        ]
        
        for key in expired_keys:
            del self.memory_cache[key]
        
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired memory cache entries")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = (self.cache_stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'total_requests': total_requests,
            'cache_hits': self.cache_stats['hits'],
            'cache_misses': self.cache_stats['misses'],
            'hit_rate_percent': round(hit_rate, 2),
            'memory_hits': self.cache_stats['memory_hits'],
            'redis_hits': self.cache_stats['redis_hits'],
            'db_hits': self.cache_stats['db_hits'],
            'memory_cache_size': len(self.memory_cache)
        }
    
    async def clear_cache(self, pattern: str = None):
        """Clear cache entries matching pattern"""
        if pattern:
            # Clear specific pattern from memory cache
            keys_to_delete = [key for key in self.memory_cache.keys() if pattern in key]
            for key in keys_to_delete:
                del self.memory_cache[key]
            
            # Clear from Redis
            if self.redis_client:
                try:
                    keys = await self.redis_client.keys(f"*{pattern}*")
                    if keys:
                        await self.redis_client.delete(*keys)
                except Exception as e:
                    logger.warning(f"Failed to clear Redis cache pattern {pattern}: {e}")
        else:
            # Clear all cache
            self.memory_cache.clear()
            if self.redis_client:
                try:
                    await self.redis_client.flushdb()
                except Exception as e:
                    logger.warning(f"Failed to clear Redis cache: {e}")
    
    async def close(self):
        """Close Redis connections"""
        if self.redis_client:
            await self.redis_client.close()

# Global cache manager instance
cache_manager = BatchCacheManager()