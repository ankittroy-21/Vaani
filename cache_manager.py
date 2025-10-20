# cache_manager.py - Simple yet powerful caching system for Vaani

import json
import time
from functools import wraps
import hashlib
import os

class CacheManager:
    """
    A simple caching system with TTL (Time To Live) support.
    Caches data in memory with automatic expiration.
    """
    
    def __init__(self):
        self.memory_cache = {}
        self.cache_ttl = {
            'weather': 1800,      # 30 minutes
            'news': 3600,         # 1 hour
            'prices': 14400,      # 4 hours
            'static': 86400       # 24 hours (schemes, crop data)
        }
        self.stats = {
            'hits': 0,
            'misses': 0,
            'total_queries': 0
        }
    
    def cache_key(self, func_name, *args, **kwargs):
        """Generate unique cache key from function name and arguments"""
        # Create a string representation of the arguments
        key_data = f"{func_name}:{str(args)}:{str(kwargs)}"
        # Hash it to create a consistent key
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key):
        """Retrieve data from cache if valid"""
        self.stats['total_queries'] += 1
        
        if key in self.memory_cache:
            data, timestamp, ttl = self.memory_cache[key]
            # Check if cache is still valid
            if time.time() - timestamp < ttl:
                self.stats['hits'] += 1
                print(f"✓ Cache HIT for key: {key[:8]}... (Age: {int(time.time() - timestamp)}s)")
                return data
            else:
                # Cache expired, remove it
                print(f"✗ Cache EXPIRED for key: {key[:8]}...")
                del self.memory_cache[key]
        
        self.stats['misses'] += 1
        print(f"✗ Cache MISS for key: {key[:8]}...")
        return None
    
    def set(self, key, data, category='static'):
        """Store data in cache with TTL"""
        ttl = self.cache_ttl.get(category, 3600)
        self.memory_cache[key] = (data, time.time(), ttl)
        print(f"✓ Cached data for key: {key[:8]}... (TTL: {ttl}s)")
    
    def clear(self, category=None):
        """Clear cache - all or specific category"""
        if category:
            # Clear only entries of specific category (more complex, skip for now)
            pass
        else:
            self.memory_cache.clear()
            print("✓ Cache cleared completely")
    
    def get_stats(self):
        """Get cache statistics"""
        if self.stats['total_queries'] > 0:
            hit_rate = (self.stats['hits'] / self.stats['total_queries']) * 100
        else:
            hit_rate = 0
        
        return {
            'total_queries': self.stats['total_queries'],
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'hit_rate': f"{hit_rate:.1f}%",
            'cache_size': len(self.memory_cache)
        }
    
    def cached_call(self, category='static'):
        """
        Decorator for caching function results.
        
        Usage:
        @cache.cached_call('weather')
        def get_weather(city):
            # ... fetch weather
            return data
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                key = self.cache_key(func.__name__, *args, **kwargs)
                
                # Try to get from cache
                cached = self.get(key)
                if cached is not None:
                    return cached
                
                # If not in cache, call the function
                print(f"→ Executing {func.__name__}...")
                result = func(*args, **kwargs)
                
                # Store result in cache
                if result is not None:  # Don't cache None/errors
                    self.set(key, result, category)
                
                return result
            return wrapper
        return decorator
    
    def print_stats(self):
        """Print cache statistics in a nice format"""
        stats = self.get_stats()
        print("\n" + "="*50)
        print("📊 CACHE STATISTICS")
        print("="*50)
        print(f"Total Queries: {stats['total_queries']}")
        print(f"Cache Hits:    {stats['hits']}")
        print(f"Cache Misses:  {stats['misses']}")
        print(f"Hit Rate:      {stats['hit_rate']}")
        print(f"Cache Size:    {stats['cache_size']} items")
        print("="*50 + "\n")

# Global cache instance (singleton pattern)
cache = CacheManager()

# For testing purposes
if __name__ == "__main__":
    print("Testing Cache Manager...")
    
    # Test basic cache operations
    cache.set("test_key", {"data": "test value"}, "weather")
    result = cache.get("test_key")
    print(f"Retrieved: {result}")
    
    # Test decorator
    @cache.cached_call('weather')
    def test_function(city):
        print(f"  [Simulating API call for {city}]")
        time.sleep(1)  # Simulate slow API
        return f"Weather data for {city}"
    
    # First call - should be slow
    print("\nFirst call (should be slow):")
    start = time.time()
    result1 = test_function("Lucknow")
    print(f"  Result: {result1}")
    print(f"  Time: {time.time() - start:.2f}s")
    
    # Second call - should be instant
    print("\nSecond call (should be instant from cache):")
    start = time.time()
    result2 = test_function("Lucknow")
    print(f"  Result: {result2}")
    print(f"  Time: {time.time() - start:.2f}s")
    
    # Print statistics
    cache.print_stats()
