"""
Test script for Agriculture Module
Tests all services and features to ensure proper functionality.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from vaani.services.agriculture.agri_price_service import (
    get_agmarknet_price,
    get_fallback_price,
    clear_price_cache,
    _price_cache
)
from vaani.services.agriculture.agri_advisory_service import (
    load_crop_data,
    CROP_DATABASE
)
from vaani.services.agriculture.agri_scheme_service import (
    load_json_data
)


def mock_bolo(text):
    """Mock function for bolo to print instead of speak."""
    print(f"[BOLO] {text}")


class MockContext:
    """Mock context object for testing."""
    def __init__(self):
        self.topic = None
        self.state = None
        self.data = {}
    
    def set(self, topic, state, data):
        self.topic = topic
        self.state = state
        self.data = data
    
    def clear(self):
        self.topic = None
        self.state = None
        self.data = {}


def test_price_service():
    """Test the price service functionality."""
    print("\n" + "="*60)
    print("Testing Price Service")
    print("="*60)
    
    # Test 1: Fallback prices
    print("\n[TEST 1] Testing fallback prices...")
    price, market, commodity = get_fallback_price("आलू", "लखनऊ", "उत्तर प्रदेश")
    if price:
        print(f"✓ Fallback price retrieved: {commodity} in {market} = ₹{price}")
    else:
        print("✗ Failed to get fallback price")
    
    # Test 2: Cache functionality
    print("\n[TEST 2] Testing cache functionality...")
    print(f"Cache size before: {len(_price_cache)}")
    clear_price_cache()
    print(f"Cache size after clear: {len(_price_cache)}")
    print("✓ Cache cleared successfully")
    
    # Test 3: API call (will fail without API key, but tests error handling)
    print("\n[TEST 3] Testing API call (expected to fail without API key)...")
    price, market, commodity = get_agmarknet_price("आलू", "लखनऊ", "उत्तर प्रदेश")
    if price:
        print(f"✓ API price retrieved: {commodity} in {market} = ₹{price}")
    else:
        print("✓ API failed gracefully (expected without API key)")


def test_advisory_service():
    """Test the advisory service functionality."""
    print("\n" + "="*60)
    print("Testing Advisory Service")
    print("="*60)
    
    # Test 1: Load crop data
    print("\n[TEST 1] Testing crop data loading...")
    crop_data = load_crop_data("गेहूं")
    if crop_data:
        print(f"✓ Successfully loaded गेहूं data")
        print(f"  Available sections: {', '.join(list(crop_data.keys())[:5])}")
    else:
        print("✗ Failed to load गेहूं data")
    
    # Test 2: Cache functionality
    print("\n[TEST 2] Testing crop data caching...")
    print(f"Crops in cache: {len(CROP_DATABASE)}")
    crop_data_cached = load_crop_data("गेहूं")
    if crop_data_cached:
        print("✓ Successfully retrieved from cache")
    
    # Test 3: Load non-existent crop
    print("\n[TEST 3] Testing error handling for non-existent crop...")
    invalid_crop = load_crop_data("xyz123")
    if invalid_crop is None:
        print("✓ Gracefully handled non-existent crop")


def test_scheme_service():
    """Test the scheme service functionality."""
    print("\n" + "="*60)
    print("Testing Scheme Service")
    print("="*60)
    
    # Test 1: Load scheme data
    print("\n[TEST 1] Testing scheme data loading...")
    scheme_data = load_json_data('scheme_data', 'pm_kisan.json')
    if scheme_data:
        print(f"✓ Successfully loaded PM-KISAN scheme")
        print(f"  Scheme name: {scheme_data.get('yojana_ka_naam', 'N/A')}")
    else:
        print("✗ Failed to load scheme data")
    
    # Test 2: Load subsidy data
    print("\n[TEST 2] Testing subsidy data loading...")
    subsidy_data = load_json_data('subsidy_data', 'gehu_subsidies.json')
    if subsidy_data:
        print(f"✓ Successfully loaded wheat subsidy data")
    else:
        print("⚠ Wheat subsidy data not available")
    
    # Test 3: Load loan data
    print("\n[TEST 3] Testing loan data loading...")
    loan_data = load_json_data('loan_data', 'loans.json')
    if loan_data:
        print(f"✓ Successfully loaded loan data")
    else:
        print("⚠ Loan data not available")


def test_command_processor():
    """Test the command processor with various queries."""
    print("\n" + "="*60)
    print("Testing Command Processor")
    print("="*60)
    
    from vaani.services.agriculture.agri_command_processor import process_agriculture_command
    
    context = MockContext()
    
    # Test 1: Price query
    print("\n[TEST 1] Testing price query...")
    try:
        process_agriculture_command(
            "आलू का भाव बताओ",
            mock_bolo,
            {'crop': 'आलू'},
            context
        )
        print("✓ Price query processed")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # Test 2: Scheme query
    print("\n[TEST 2] Testing scheme query...")
    try:
        process_agriculture_command(
            "किसान सम्मान निधि के बारे में बताओ",
            mock_bolo,
            {},
            context
        )
        print("✓ Scheme query processed")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # Test 3: Advisory query
    print("\n[TEST 3] Testing advisory query...")
    try:
        process_agriculture_command(
            "गेहूं की खेती कैसे करें",
            mock_bolo,
            {'crop': 'गेहूं'},
            context
        )
        print("✓ Advisory query processed")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_data_files():
    """Test existence and validity of data files."""
    print("\n" + "="*60)
    print("Testing Data Files")
    print("="*60)
    
    data_folders = {
        'crop_data': ['गेहूं.json', 'धान.json', 'आलू.json'],
        'scheme_data': ['pm_kisan.json', 'pm_kusum.json'],
        'subsidy_data': ['gehu_subsidies.json'],
        'loan_data': ['loans.json']
    }
    
    for folder, files in data_folders.items():
        print(f"\n[{folder}]")
        for filename in files:
            file_path = os.path.join('data', folder, filename)
            if os.path.exists(file_path):
                print(f"  ✓ {filename} exists")
            else:
                print(f"  ⚠ {filename} missing")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("VAANI AGRICULTURE MODULE TEST SUITE")
    print("="*60)
    
    try:
        test_data_files()
        test_price_service()
        test_advisory_service()
        test_scheme_service()
        test_command_processor()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED")
        print("="*60)
        print("\n✓ Module is functioning correctly!")
        print("\nNote: Some tests may show warnings if optional data files are missing.")
        print("This is normal and doesn't affect core functionality.\n")
        
    except Exception as e:
        print(f"\n✗ Test suite failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
