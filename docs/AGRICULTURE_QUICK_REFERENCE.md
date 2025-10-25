# Agriculture Module - Quick Reference

## 🚀 Quick Start

```python
from vaani.services.agriculture.agri_command_processor import process_agriculture_command

# Simple usage
process_agriculture_command(
    command="आलू का भाव बताओ",
    bolo_func=bolo,
    entities={'crop': 'आलू', 'market': 'लखनऊ'},
    context=context
)
```

## 📝 Query Examples

### Price Queries
```
"आलू का भाव क्या है?"
"लखनऊ मंडी में टमाटर की कीमत?"
"गेहूं का दाम बताओ"
"दिल्ली में प्याज का रेट?"
```

### Scheme Queries
```
"किसान सम्मान निधि के बारे में बताओ"
"सभी योजनाएं बताओ"
"गेहूं के लिए सब्सिडी है क्या?"
"कृषि लोन की जानकारी दो"
"फसल बीमा योजना बताओ"
```

### Advisory Queries
```
"गेहूं की खेती कैसे करें?"
"धान में बुवाई के बारे में बताओ"
"टमाटर की पूरी जानकारी दो"
"आलू में रोग प्रबंधन कैसे करें?"
```

## 🔧 Configuration

### Environment Variables
```bash
AGMARKNET_API_KEY=your_api_key_here
```

### Logging Configuration
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 📊 Supported Data

### Commodities (30+)
आलू, प्याज, टमाटर, गेहूं, धान, चावल, मक्का, बैंगन, भिंडी, गाजर, मूली, पालक, मिर्च, अदरक, हल्दी, चना, मटर, अरहर, मूंग, सोयाबीन, मूंगफली, कपास, गन्ना, केला, आम, संतरा...

### Markets (20+)
लखनऊ, दिल्ली, मुंबई, कानपुर, बंगलौर, चेन्नई, कोलकाता, हैदराबाद, अहमदाबाद, पुणे...

### Schemes (12+)
- PM-KISAN (किसान सम्मान निधि)
- PM-KUSUM (कुसुम योजना)
- Ayushman Bharat (आयुष्मान भारत)
- PM Fasal Bima (फसल बीमा)
- Krishi Sinchai (कृषि सिंचाई)
- And more...

## 🛠️ Utility Functions

### Clear Price Cache
```python
from vaani.services.agriculture.agri_price_service import clear_price_cache
clear_price_cache()
```

### Load Crop Data
```python
from vaani.services.agriculture.agri_advisory_service import load_crop_data
crop_data = load_crop_data("गेहूं")
```

### Load Scheme Data
```python
from vaani.services.agriculture.agri_scheme_service import load_json_data
scheme = load_json_data('scheme_data', 'pm_kisan.json')
```

## 📂 File Structure

```
data/
├── crop_data/              # Crop information JSONs
│   ├── गेहूं.json
│   ├── धान.json
│   └── ...
├── scheme_data/            # Government schemes
│   ├── pm_kisan.json
│   ├── pm_kusum.json
│   └── ...
├── subsidy_data/           # Crop subsidies
│   ├── gehu_subsidies.json
│   └── ...
└── offline_cache/          # Cached data
    └── price_cache.json
```

## 🐛 Troubleshooting

### Issue: "Module not found"
```bash
# Solution
$env:PYTHONPATH = "C:\path\to\Vaani-2"
```

### Issue: "API key missing"
```bash
# Solution: Add to .env
AGMARKNET_API_KEY=your_key
```

### Issue: "Data file not found"
```
# System automatically uses fallback data
# Check: logs/agriculture.log
```

## 📈 Performance Tips

1. **Enable Caching**: Prices cached for 6 hours automatically
2. **Use Logging**: Set level to INFO for production, DEBUG for development
3. **Preload Data**: Load frequently used crop data at startup
4. **Monitor Logs**: Check logs/agriculture.log regularly

## ✅ Testing

```bash
# Run full test suite
python tests/test_agriculture.py

# Quick test
python -c "from vaani.services.agriculture.agri_price_service import get_fallback_price; print(get_fallback_price('आलू', 'लखनऊ', 'UP'))"
```

## 🔗 Links

- Full Documentation: `vaani/services/agriculture/README.md`
- Refinement Summary: `docs/AGRICULTURE_REFINEMENT_SUMMARY.md`
- Test Suite: `tests/test_agriculture.py`

## 📞 Support

For issues, check:
1. Logs: `logs/agriculture.log`
2. Console error messages
3. Data file formats in `data/` directory

---

**Quick Reference v2.0** | Updated: October 25, 2025
