# test_performance.py - Performance Testing Script for Vaani

import time
import statistics
import sys
from datetime import datetime

# Import Vaani modules
from Weather import get_weather, get_general_weather, get_rain_forecast
from News import get_news
from cache_manager import cache

def mock_bolo(text, lang='hi'):
    """Mock bolo function that doesn't play audio during testing"""
    print(f"  [AUDIO OUTPUT]: {text[:100]}...")

def measure_time(func, *args, **kwargs):
    """Measure execution time of a function"""
    start = time.time()
    try:
        result = func(*args, **kwargs)
        duration = time.time() - start
        return duration, True, result
    except Exception as e:
        duration = time.time() - start
        print(f"  ✗ Error: {str(e)[:50]}...")
        return duration, False, None

def run_test(test_name, func, *args, iterations=3, **kwargs):
    """Run a test multiple times and collect statistics"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {test_name}")
    print(f"{'='*60}")
    
    times = []
    successes = 0
    
    for i in range(iterations):
        print(f"\n  Run {i+1}/{iterations}:")
        duration, success, result = measure_time(func, *args, **kwargs)
        times.append(duration)
        
        if success:
            successes += 1
            print(f"  ✓ Completed in {duration:.2f}s")
        else:
            print(f"  ✗ Failed in {duration:.2f}s")
    
    # Calculate statistics
    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)
    median_time = statistics.median(times)
    success_rate = (successes / iterations) * 100
    
    print(f"\n  📊 Results:")
    print(f"     Average:      {avg_time:.2f}s")
    print(f"     Minimum:      {min_time:.2f}s")
    print(f"     Maximum:      {max_time:.2f}s")
    print(f"     Median:       {median_time:.2f}s")
    print(f"     Success Rate: {success_rate:.0f}%")
    
    return {
        'test_name': test_name,
        'avg': avg_time,
        'min': min_time,
        'max': max_time,
        'median': median_time,
        'success_rate': success_rate
    }

def main():
    print("\n" + "="*60)
    print("🚀 VAANI PERFORMANCE TEST SUITE")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    results = []
    
    # Test 1: Weather query (no cache)
    print("\n\n🌦️  WEATHER API TESTS")
    cache.clear()  # Clear cache before test
    result = run_test(
        "Weather API - Lucknow (Cold Cache)",
        get_general_weather,
        "लखनऊ का मौसम",
        "Lucknow",
        mock_bolo,
        iterations=2
    )
    results.append(result)
    
    # Test 2: Weather query (with cache)
    result = run_test(
        "Weather API - Lucknow (Warm Cache)",
        get_general_weather,
        "लखनऊ का मौसम",
        "Lucknow",
        mock_bolo,
        iterations=3
    )
    results.append(result)
    
    # Test 3: Rain forecast
    result = run_test(
        "Rain Forecast API",
        get_rain_forecast,
        "दिल्ली में कब बारिश होगी",
        "Delhi",
        mock_bolo,
        iterations=2
    )
    results.append(result)
    
    # Test 4: News query
    print("\n\n📰 NEWS API TESTS")
    cache.clear()
    result = run_test(
        "News API - General (Cold Cache)",
        get_news,
        "समाचार",
        mock_bolo,
        iterations=2
    )
    results.append(result)
    
    # Test 5: News query with cache
    result = run_test(
        "News API - General (Warm Cache)",
        get_news,
        "समाचार",
        mock_bolo,
        iterations=3
    )
    results.append(result)
    
    # Print summary
    print("\n\n" + "="*60)
    print("📊 PERFORMANCE SUMMARY")
    print("="*60)
    print(f"\n{'Test Name':<40} {'Avg Time':<12} {'Success':<10}")
    print("-"*60)
    
    for r in results:
        print(f"{r['test_name']:<40} {r['avg']:.2f}s        {r['success_rate']:.0f}%")
    
    # Cache statistics
    print("\n")
    cache.print_stats()
    
    # Performance targets
    print("\n" + "="*60)
    print("🎯 PERFORMANCE TARGETS")
    print("="*60)
    print("  Audio Response:     < 1.0s   (Target achieved with streaming)")
    print("  API Call (Weather): < 2.0s   (Cold cache)")
    print("  API Call (News):    < 2.0s   (Cold cache)")
    print("  Cached Responses:   < 0.3s   (Warm cache)")
    print("  Overall Response:   < 3.0s   (After Day 3 optimizations)")
    print("="*60)
    
    # Calculate improvement
    cold_avg = sum(r['avg'] for r in results if 'Cold' in r['test_name']) / max(1, sum(1 for r in results if 'Cold' in r['test_name']))
    warm_avg = sum(r['avg'] for r in results if 'Warm' in r['test_name']) / max(1, sum(1 for r in results if 'Warm' in r['test_name']))
    
    if cold_avg > 0 and warm_avg > 0:
        improvement = ((cold_avg - warm_avg) / cold_avg) * 100
        print(f"\n🎉 Cache Improvement: {improvement:.0f}% faster on cached queries!")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
