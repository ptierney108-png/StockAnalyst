"""
In-Process Batch Queue System for Stock Processing
Handles batch scanning jobs with progress tracking and rate limiting
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass, asdict, field
import logging
import time
import json

logger = logging.getLogger(__name__)

class BatchStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class BatchJob:
    id: str
    symbols: List[str]
    filters: Dict[str, Any]
    status: BatchStatus
    created_at: datetime
    indices: List[str] = field(default_factory=list)  # Add indices field for persistence
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: Dict[str, Any] = None
    results: List[Dict[str, Any]] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.progress is None:
            self.progress = {
                'processed': 0,
                'total': len(self.symbols),
                'percentage': 0.0,
                'current_symbol': None,
                'estimated_completion': None,
                'api_calls_made': 0,
                'errors': []
            }
        if self.results is None:
            self.results = []
    
    def to_dict(self):
        return {
            'id': self.id,
            'symbols_count': len(self.symbols),
            'filters': self.filters,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'progress': self.progress,
            'results_count': len(self.results) if self.results else 0,
            'error': self.error
        }

class RateLimiter:
    """Rate limiter for API calls - 75 calls per minute"""
    
    def __init__(self, calls_per_minute: int = 75):
        self.calls_per_minute = calls_per_minute
        self.calls_per_second = calls_per_minute / 60.0
        self.call_times: List[float] = []
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        """Acquire permission to make an API call"""
        while True:
            async with self.lock:
                now = time.time()
                
                # Remove calls older than 1 minute
                cutoff_time = now - 60
                self.call_times = [t for t in self.call_times if t > cutoff_time]
                
                # Check if we can make another call
                if len(self.call_times) >= self.calls_per_minute:
                    # Calculate how long to wait
                    oldest_call = min(self.call_times)
                    wait_time = 60 - (now - oldest_call) + 0.1  # Add small buffer
                    logger.info(f"Rate limit hit, waiting {wait_time:.2f} seconds")
                    # Release lock before sleeping to avoid deadlock
                else:
                    # Record this call and exit the loop
                    self.call_times.append(now)
                    
                    # Add small delay to spread calls evenly
                    if len(self.call_times) > 1:
                        await asyncio.sleep(1.0 / self.calls_per_second)
                    
                    return  # Exit successfully
            
            # Sleep outside the lock to avoid deadlock
            await asyncio.sleep(wait_time)

class BatchProcessor:
    """In-process batch processing system for stock scanning with Redis persistence"""
    
    def __init__(self):
        self.jobs: Dict[str, BatchJob] = {}
        self.active_jobs: Dict[str, asyncio.Task] = {}
        self.rate_limiter = RateLimiter(calls_per_minute=75)
        self.max_concurrent_jobs = 3  # Allow up to 3 concurrent batch jobs for better user experience
        
        # Redis client for job persistence
        self.redis_client = None
        self._initialize_redis()
        
        # Statistics
        self.stats = {
            'total_jobs': 0,
            'completed_jobs': 0,
            'failed_jobs': 0,
            'total_stocks_processed': 0,
            'total_api_calls': 0,
            'average_processing_time': 0.0
        }
    
    def _initialize_redis(self):
        """Initialize Redis client for job persistence"""
        try:
            import redis
            self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
            # Test connection
            self.redis_client.ping()
            logger.info("✅ Redis connected - batch job persistence enabled")
        except Exception as e:
            logger.warning(f"⚠️ Redis not available ({e}) - using memory-only mode")
            self.redis_client = None
    
    async def _save_job_state(self, job_id: str, job: BatchJob):
        """Save job state to Redis for persistence"""
        if not self.redis_client:
            return
        
        try:
            job_data = {
                'job_id': job_id,
                'status': job.status,
                'symbols': job.symbols,
                'filters': job.filters,
                'indices': job.indices,
                'processed_count': job.processed_count,
                'total_count': job.total_count,
                'results': job.results,
                'errors': job.errors,
                'start_time': job.start_time.isoformat() if job.start_time else None,
                'last_updated': datetime.utcnow().isoformat()
            }
            
            # Save with 6 hour expiry
            self.redis_client.setex(f"batch_job:{job_id}", 21600, json.dumps(job_data))
            logger.debug(f"💾 Saved job state for {job_id}")
        except Exception as e:
            logger.error(f"❌ Failed to save job state for {job_id}: {e}")
    
    async def _restore_jobs_from_redis(self):
        """Restore active jobs from Redis on startup"""
        if not self.redis_client:
            return
        
        try:
            # Find all batch job keys
            job_keys = self.redis_client.keys("batch_job:*")
            restored_count = 0
            
            for key in job_keys:
                try:
                    job_data = json.loads(self.redis_client.get(key))
                    job_id = job_data['job_id']
                    
                    # Only restore jobs that were running
                    if job_data['status'] == 'running':
                        # Recreate BatchJob object
                        job = BatchJob(
                            symbols=job_data['symbols'],
                            filters=job_data['filters'],
                            indices=job_data['indices']
                        )
                        job.status = 'running'
                        job.processed_count = job_data['processed_count']
                        job.total_count = job_data['total_count']
                        job.results = job_data['results']
                        job.errors = job_data['errors']
                        job.start_time = datetime.fromisoformat(job_data['start_time']) if job_data['start_time'] else None
                        
                        self.jobs[job_id] = job
                        
                        # Resume processing
                        task = asyncio.create_task(self._process_batch_job(job_id))
                        self.active_jobs[job_id] = task
                        restored_count += 1
                        
                        logger.info(f"🔄 Restored batch job {job_id} - {job.processed_count}/{job.total_count} completed")
                
                except Exception as e:
                    logger.error(f"❌ Failed to restore job from {key}: {e}")
            
            if restored_count > 0:
                logger.info(f"✅ Restored {restored_count} active batch jobs from Redis")
            
        except Exception as e:
            logger.error(f"❌ Failed to restore jobs from Redis: {e}")
    
    def create_batch_job(self, symbols: List[str], filters: Dict[str, Any], indices: List[str] = None) -> str:
        """Create a new batch processing job with interleaved processing support"""
        job_id = str(uuid.uuid4())
        
        # Interleave symbols from different indices for better user feedback
        if indices and len(indices) > 1:
            interleaved_symbols = self._interleave_symbols_by_index(symbols, indices)
        else:
            interleaved_symbols = symbols
        
        job = BatchJob(
            id=job_id,
            symbols=interleaved_symbols,
            filters=filters,
            status=BatchStatus.PENDING,
            created_at=datetime.utcnow()
        )
        
        # Add metadata for Phase 2 features
        job.metadata = {
            'indices': indices or ['UNKNOWN'],
            'original_order': symbols != interleaved_symbols,
            'interleaved': indices and len(indices) > 1,
            'partial_results_enabled': True
        }
        
        self.jobs[job_id] = job
        self.stats['total_jobs'] += 1
        
        logger.info(f"Created batch job {job_id} for {len(symbols)} stocks from indices: {indices}")
        return job_id
    
    def _interleave_symbols_by_index(self, symbols: List[str], indices: List[str]) -> List[str]:
        """
        Interleave symbols from different indices to provide faster user feedback
        Instead of processing all SP500 then all NASDAQ, mix them for better progress distribution
        """
        try:
            from finnhub_stock_universe import get_stocks_by_index as get_stock_universe
            USING_FINNHUB = True
            logger.info("Using Finnhub stock universe")
        except ImportError:
            from stock_universe import get_stock_universe
            USING_FINNHUB = False
            logger.info("Using static stock universe")
        
        # Group symbols by their source index
        index_groups = {}
        symbol_to_index = {}
        
        for index in indices:
            index_symbols = set(get_stock_universe(index))
            index_groups[index] = [s for s in symbols if s in index_symbols]
            for symbol in index_groups[index]:
                symbol_to_index[symbol] = index
        
        # Interleave symbols from different indices
        interleaved = []
        max_len = max(len(group) for group in index_groups.values()) if index_groups else 0
        
        for i in range(max_len):
            for index in indices:
                if i < len(index_groups.get(index, [])):
                    interleaved.append(index_groups[index][i])
        
        # Add any remaining symbols not found in specific indices
        remaining = [s for s in symbols if s not in symbol_to_index]
        interleaved.extend(remaining)
        
        logger.info(f"Interleaved {len(symbols)} symbols from {len(indices)} indices for better feedback")
        return interleaved
    
    async def start_batch_job(self, job_id: str, process_function: Callable) -> bool:
        """Start processing a batch job"""
        if job_id not in self.jobs:
            logger.error(f"Job {job_id} not found")
            return False
        
        job = self.jobs[job_id]
        
        if job.status != BatchStatus.PENDING:
            logger.warning(f"Job {job_id} is not in pending status: {job.status}")
            return False
        
        if len(self.active_jobs) >= self.max_concurrent_jobs:
            logger.warning(f"Max concurrent jobs ({self.max_concurrent_jobs}) reached")
            return False
        
        # Start the job
        job.status = BatchStatus.RUNNING
        job.started_at = datetime.utcnow()
        
        task = asyncio.create_task(self._process_batch_job(job, process_function))
        self.active_jobs[job_id] = task
        
        logger.info(f"Started batch job {job_id}")
        return True
    
    async def _process_batch_job(self, job: BatchJob, process_function: Callable):
        """Process a batch job with progress tracking and real-time partial results"""
        try:
            results = []
            start_time = time.time()
            
            total_symbols = len(job.symbols)
            processed_count = 0
            api_call_count = 0
            errors = []
            
            # Phase 2: Real-time partial results streaming
            partial_results_batch_size = 10  # Stream results every 10 processed stocks
            last_partial_update = 0
            
            logger.info(f"Processing batch job {job.id} with {total_symbols} stocks (Phase 2: Partial Results Enabled)")
            
            for i, symbol in enumerate(job.symbols):
                try:
                    # Update progress
                    job.progress['current_symbol'] = symbol
                    job.progress['processed'] = processed_count
                    job.progress['percentage'] = (processed_count / total_symbols) * 100
                    
                    # Estimate completion time with improved accuracy for long batches
                    if processed_count > 0:
                        elapsed_time = time.time() - start_time
                        avg_time_per_stock = elapsed_time / processed_count
                        remaining_stocks = total_symbols - processed_count
                        
                        # Phase 2: Better ETA calculation for long batches
                        if processed_count < 50:  # Early stage - conservative estimate
                            estimated_seconds = remaining_stocks * (avg_time_per_stock * 1.2)
                        else:  # Later stage - more accurate estimate
                            estimated_seconds = remaining_stocks * avg_time_per_stock
                        
                        job.progress['estimated_completion'] = (
                            datetime.utcnow() + timedelta(seconds=estimated_seconds)
                        ).isoformat()
                    
                    # Rate limiting
                    await self.rate_limiter.acquire()
                    
                    # Process the stock
                    stock_data = await process_function(symbol, job.filters)
                    api_call_count += 1
                    
                    if stock_data:
                        # Apply filters to determine if stock should be included
                        if self._passes_filters(stock_data, job.filters):
                            results.append(stock_data)
                            
                            # Phase 2: Real-time partial results - update job with current results
                            job.results = results.copy()  # Update partial results in real-time
                    
                    processed_count += 1
                    job.progress['api_calls_made'] = api_call_count
                    
                    # Phase 2: Stream partial results every N stocks for better user feedback
                    if (processed_count - last_partial_update) >= partial_results_batch_size:
                        job.progress['partial_results_count'] = len(results)
                        job.progress['last_partial_update'] = datetime.utcnow().isoformat()
                        last_partial_update = processed_count
                        
                        # 💾 Save job state for persistence (every 10 stocks)
                        await self._save_job_state(job.id, job)
                        
                        logger.info(f"Batch {job.id}: Partial results update - {len(results)} matches from {processed_count}/{total_symbols} processed")
                    
                    # Log progress every 50 stocks (but less frequently for very large batches)
                    progress_log_interval = min(50, max(10, total_symbols // 20))
                    if processed_count % progress_log_interval == 0:
                        # 💾 Save job state for persistence (every 50 stocks)
                        await self._save_job_state(job.id, job)
                        logger.info(f"Batch {job.id}: Processed {processed_count}/{total_symbols} stocks ({len(results)} matches)")
                
                except Exception as e:
                    error_msg = f"Error processing {symbol}: {str(e)}"
                    logger.warning(error_msg)
                    errors.append(error_msg)
                    job.progress['errors'] = errors[-20:]  # Keep last 20 errors for large batches
                    processed_count += 1
                    continue
            
            # Job completed successfully
            job.results = results
            job.status = BatchStatus.COMPLETED
            job.completed_at = datetime.utcnow()
            job.progress['processed'] = processed_count
            job.progress['percentage'] = 100.0
            job.progress['current_symbol'] = None
            job.progress['partial_results_count'] = len(results)
            
            # 💾 Final job state save on completion
            await self._save_job_state(job.id, job)
            
            # Update statistics
            processing_time = time.time() - start_time
            self.stats['completed_jobs'] += 1
            self.stats['total_stocks_processed'] += processed_count
            self.stats['total_api_calls'] += api_call_count
            self.stats['average_processing_time'] = (
                (self.stats['average_processing_time'] * (self.stats['completed_jobs'] - 1) + processing_time) 
                / self.stats['completed_jobs']
            )
            
            # Phase 2: Enhanced completion logging for large batches
            processing_minutes = processing_time / 60
            logger.info(
                f"Phase 2 Batch job {job.id} completed: {len(results)} matches from {processed_count} stocks "
                f"in {processing_minutes:.1f} minutes ({api_call_count} API calls, {len(errors)} errors)"
            )
        
        except Exception as e:
            # Job failed
            job.status = BatchStatus.FAILED
            job.error = str(e)
            job.completed_at = datetime.utcnow()
            
            # 💾 Save final job state on failure
            await self._save_job_state(job.id, job)
            
            self.stats['failed_jobs'] += 1
            logger.error(f"Batch job {job.id} failed: {e}")
        
        finally:
            # Clean up
            if job.id in self.active_jobs:
                del self.active_jobs[job.id]
    
    def _passes_filters(self, stock_data: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Check if stock data passes the specified filters"""
        try:
            symbol = stock_data.get('symbol', 'UNKNOWN')
            
            # Log filters being applied for first few stocks
            if not hasattr(self, '_filter_debug_logged'):
                logger.info(f"🔧 FILTER DEBUG - Applied filters: {json.dumps(filters, indent=2)}")
                self._filter_debug_logged = True
            
            logger.info(f"🔍 Filtering {symbol}: price={stock_data.get('price', 0)}, dmi={stock_data.get('dmi', 0)}, ppo_slope={stock_data.get('ppo_slope_percentage', 0)}, hook={stock_data.get('ppo_hook_type')}")
            
            # Price filter
            if 'price_filter' in filters and filters['price_filter']:
                price_filter = filters['price_filter']
                price = stock_data.get('price', 0)
                
                if price_filter.get('type') == 'under':
                    max_price = price_filter.get('under', float('inf'))
                    if price > max_price:
                        logger.debug(f"❌ {symbol} filtered out: Price {price} > {max_price}")
                        return False
                elif price_filter.get('type') == 'range':
                    min_price = price_filter.get('min', 0)
                    max_price = price_filter.get('max', float('inf'))
                    if not (min_price <= price <= max_price):
                        logger.debug(f"❌ {symbol} filtered out: Price {price} not in range {min_price}-{max_price}")
                        return False
            
            # DMI filter
            if 'dmi_filter' in filters and filters['dmi_filter']:
                dmi_filter = filters['dmi_filter']
                dmi = stock_data.get('dmi', 0)
                dmi_min = dmi_filter.get('min', 0)
                dmi_max = dmi_filter.get('max', 100)
                if not (dmi_min <= dmi <= dmi_max):
                    logger.debug(f"❌ {symbol} filtered out: DMI {dmi} not in range {dmi_min}-{dmi_max}")
                    return False
            
            # PPO Slope filter
            if 'ppo_slope_filter' in filters and filters['ppo_slope_filter']:
                slope_filter = filters['ppo_slope_filter']
                slope = stock_data.get('ppo_slope_percentage', 0)
                threshold = slope_filter.get('threshold', float('-inf'))
                if slope < threshold:
                    logger.debug(f"❌ {symbol} filtered out: PPO slope {slope} < {threshold}")
                    return False
            
            # PPO Hook filter
            if 'ppo_hook_filter' in filters and filters['ppo_hook_filter'] != 'all':
                hook_filter = filters['ppo_hook_filter']
                hook_type = stock_data.get('ppo_hook_type')
                
                if hook_filter == 'positive' and hook_type != 'positive':
                    logger.debug(f"❌ {symbol} filtered out: Hook type {hook_type} != positive")
                    return False
                elif hook_filter == 'negative' and hook_type != 'negative':
                    logger.debug(f"❌ {symbol} filtered out: Hook type {hook_type} != negative")
                    return False
                elif hook_filter == 'both' and hook_type not in ['positive', 'negative']:
                    logger.debug(f"❌ {symbol} filtered out: Hook type {hook_type} not in [positive, negative]")
                    return False
            
            logger.debug(f"✅ {symbol} passed all filters")
            return True
            
        except Exception as e:
            logger.warning(f"Filter evaluation error: {e}")
            return False
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a batch job"""
        if job_id not in self.jobs:
            return None
        
        return self.jobs[job_id].to_dict()
    
    def get_job_results(self, job_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get results of a completed batch job"""
        if job_id not in self.jobs:
            return None
        
        job = self.jobs[job_id]
        return job.results if job.status == BatchStatus.COMPLETED else None
    
    def get_job_partial_results(self, job_id: str) -> Optional[List[Dict[str, Any]]]:
        """Phase 2: Get partial results of a running or completed batch job"""
        if job_id not in self.jobs:
            return None
        
        job = self.jobs[job_id]
        # Return current results even if job is still running
        return job.results if hasattr(job, 'results') and job.results else []
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a running or pending job"""
        if job_id not in self.jobs:
            return False
        
        job = self.jobs[job_id]
        
        if job.status in [BatchStatus.COMPLETED, BatchStatus.FAILED, BatchStatus.CANCELLED]:
            return False
        
        # Cancel running task
        if job_id in self.active_jobs:
            task = self.active_jobs[job_id]
            task.cancel()
            del self.active_jobs[job_id]
        
        job.status = BatchStatus.CANCELLED
        job.completed_at = datetime.utcnow()
        
        logger.info(f"Cancelled batch job {job_id}")
        return True
    
    def cleanup_old_jobs(self, max_age_hours: int = 24):
        """Clean up old completed/failed jobs"""
        cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
        
        jobs_to_remove = [
            job_id for job_id, job in self.jobs.items()
            if job.completed_at and job.completed_at < cutoff_time
            and job.status in [BatchStatus.COMPLETED, BatchStatus.FAILED, BatchStatus.CANCELLED]
        ]
        
        for job_id in jobs_to_remove:
            del self.jobs[job_id]
        
        if jobs_to_remove:
            logger.info(f"Cleaned up {len(jobs_to_remove)} old batch jobs")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get batch processing statistics"""
        active_jobs_count = len(self.active_jobs)
        pending_jobs_count = len([j for j in self.jobs.values() if j.status == BatchStatus.PENDING])
        
        return {
            **self.stats,
            'active_jobs': active_jobs_count,
            'pending_jobs': pending_jobs_count,
            'total_jobs_in_memory': len(self.jobs)
        }

# Global batch processor instance
batch_processor = BatchProcessor()