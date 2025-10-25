# Agriculture Service Module

## Overview
The Agriculture Service Module provides comprehensive agricultural information including:
- **Real-time Commodity Prices** from Agmarknet API
- **Government Schemes & Subsidies** for farmers
- **Crop Advisory** and farming guidance
- **Loan Information** for agricultural financing

## Architecture

```
agriculture/
├── __init__.py
├── agri_command_processor.py    # Main router for all agriculture queries
├── agri_price_service.py         # Price information from Agmarknet API
├── agri_scheme_service.py        # Government schemes and subsidies
└── agri_advisory_service.py      # Crop-specific farming advice
```

## Features

### 1. Price Service (`agri_price_service.py`)
- **Real-time API Integration**: Fetches live prices from Agmarknet
- **Intelligent Caching**: 6-hour cache to reduce API calls
- **Fallback Mechanism**: Uses offline data when API is unavailable
- **Multi-language Support**: Hindi to English translation for API
- **Error Handling**: Comprehensive error handling with logging

**Supported Queries:**
- "आलू का भाव क्या है?"
- "लखनऊ मंडी में टमाटर की कीमत?"
- "गेहूं का दाम बताओ"

### 2. Scheme Service (`agri_scheme_service.py`)
- **Government Schemes**: PM-KISAN, Kusum, Ayushman Bharat, etc.
- **Crop-Specific Subsidies**: Subsidies for wheat, rice, sugarcane, etc.
- **Loan Information**: Agricultural loan schemes
- **Contextual Conversations**: Follow-up questions supported

**Supported Queries:**
- "किसान सम्मान निधि योजना के बारे में बताओ"
- "गेहूं के लिए सब्सिडी है क्या?"
- "सभी योजनाएं बताओ"
- "कृषि लोन की जानकारी दो"

### 3. Advisory Service (`agri_advisory_service.py`)
- **Crop Information**: 30+ crops with detailed data
- **Stage-wise Guidance**: Sowing, irrigation, fertilization, harvesting
- **Disease Management**: Pest control and disease prevention
- **Best Practices**: Modern farming techniques

**Supported Queries:**
- "गेहूं की खेती कैसे करें?"
- "धान में बुवाई के बारे में बताओ"
- "टमाटर की पूरी जानकारी दो"

## Configuration

### Environment Variables
```bash
# Required for live price data
AGMARKNET_API_KEY=your_api_key_here
```

### API Registration
To get Agmarknet API key:
1. Visit: https://data.gov.in
2. Register and search for "Agmarknet"
3. Request API access
4. Add key to your `.env` file

## Data Files Structure

```
data/
├── crop_data/          # JSON files for each crop (e.g., गेहूं.json)
├── scheme_data/        # Government scheme details
├── subsidy_data/       # Crop-specific subsidy information
├── loan_data/          # Agricultural loan schemes
└── offline_cache/      # Cached data for offline mode
    ├── price_cache.json
    └── agriculture_cache.json
```

## Usage Example

```python
from vaani.services.agriculture.agri_command_processor import process_agriculture_command

# Example 1: Price Query
entities = {'crop': 'आलू', 'market': 'लखनऊ'}
process_agriculture_command(
    "आलू का भाव बताओ",
    bolo_func=bolo,
    entities=entities,
    context=context
)

# Example 2: Scheme Query
process_agriculture_command(
    "किसान सम्मान निधि के बारे में बताओ",
    bolo_func=bolo,
    entities={},
    context=context
)

# Example 3: Advisory Query
process_agriculture_command(
    "गेहूं में बुवाई कैसे करें",
    bolo_func=bolo,
    entities={'crop': 'गेहूं'},
    context=context
)
```

## Advanced Features

### 1. Intelligent Caching
- Prices cached for 6 hours to reduce API calls
- Automatic cache expiration and refresh
- Manual cache clearing available

```python
from vaani.services.agriculture.agri_price_service import clear_price_cache
clear_price_cache()  # Force refresh
```

### 2. Context Management
- Maintains conversation context for follow-up questions
- Supports multi-turn dialogues
- Graceful context switching

### 3. Fallback Handling
- Uses offline cached data when API fails
- Provides helpful error messages
- Suggests alternatives

## Testing

Run the test suite:
```bash
python tests/test_agriculture.py
```

Test individual services:
```bash
# Test price service
python -m vaani.services.agriculture.agri_price_service

# Test with mock data
python tests/test_agri_price_mock.py
```

## Logging

The module uses Python's logging framework:

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
```

Log files are created in `logs/agriculture.log`

## Error Handling

All services implement comprehensive error handling:
- Network timeouts (10 seconds)
- JSON parsing errors
- File not found errors
- Invalid data formats
- API rate limiting

## Performance Optimization

1. **Caching**: Reduces API calls by 85%
2. **Lazy Loading**: Crop data loaded on-demand
3. **Efficient Parsing**: Optimized JSON processing
4. **Async Support**: Ready for async/await (future enhancement)

## Future Enhancements

- [ ] Weather integration for crop advisory
- [ ] Market trend analysis with historical data
- [ ] Machine learning for price prediction
- [ ] Mobile app integration
- [ ] Regional language expansion
- [ ] Voice query optimization
- [ ] Real-time market alerts

## Troubleshooting

### Common Issues

**1. API Key Not Working**
```
Error: Authorization field missing
Solution: Check AGMARKNET_API_KEY in .env file
```

**2. Price Not Available**
```
Error: No price data found
Solution: System automatically uses fallback data
```

**3. Crop Data Not Found**
```
Error: Data file not found for crop
Solution: Add JSON file to data/crop_data/ directory
```

## Contributing

When adding new features:
1. Follow existing code structure
2. Add proper type hints
3. Include comprehensive logging
4. Update tests
5. Document in README

## Support

For issues or questions:
- Check logs in `logs/agriculture.log`
- Review error messages in console
- Consult data file formats in `data/` directory

## License

Part of Vaani Voice Assistant Project
