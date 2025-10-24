# Migration Guide for Vaani Project Reorganization

This document guides you through updating imports and other references after the project reorganization.

## Import Updates

After migrating files to the new structure, you'll need to update imports in all Python files. Here's a quick reference:

### Old Import â†’ New Import

- `import Config` â†’ `import vaani.core.config as Config`
- `from Config import X` â†’ `from vaani.core.config import X`
- `import Voice_tool` â†’ `import vaani.core.voice_tool as Voice_tool`
- `from Voice_tool import X` â†’ `from vaani.core.voice_tool import X`
- `import Time` â†’ `import vaani.services.time.time_service as Time`
- `from Time import X` â†’ `from vaani.services.time.time_service import X`
- `import Weather` â†’ `import vaani.services.weather.weather_service as Weather`
- `from Weather import X` â†’ `from vaani.services.weather.weather_service import X`
- `import News` â†’ `import vaani.services.news.news_service as News`
- `from News import X` â†’ `from vaani.services.news.news_service import X`
- `import Wikipedia` â†’ `import vaani.services.knowledge.wikipedia_service as Wikipedia`
- `from Wikipedia import X` â†’ `from vaani.services.knowledge.wikipedia_service import X`

### Updating Main Module

The `main.py` file will need the most extensive updates. Here's a template for the imports section:

```python
import time
import os
import random
from datetime import datetime
import logging

# Core imports
from vaani.core.voice_tool import bolo_stream as bolo, listen_command
from vaani.core import api_key_manager, config as Config
from vaani.core.offline_mode import OfflineMode
from vaani.core.language_manager import get_language_manager, handle_language_command

# Service imports
from vaani.services.time.time_service import current_time, get_date_of_day_in_week, get_day_summary
from vaani.services.weather.weather_service import get_weather
from vaani.services.news.news_service import get_news, process_news_selection
from vaani.services.knowledge.wikipedia_service import search_wikipedia
from vaani.services.knowledge.general_knowledge_service import handle_general_knowledge_query
from vaani.services.agriculture.agri_command_processor import process_agriculture_command
from vaani.services.finance.financial_literacy_service import handle_financial_query
from vaani.services.finance.expense_tracker_service import process_expense_command
from vaani.services.finance.simple_calculator_service import handle_calculation_query
from vaani.services.social.social_scheme_service import handle_social_schemes_query
from vaani.services.social.emergency_assistance_service import handle_emergency_query

# Optional imports
try:
    from vaani.services.communication.sms_integration import SMSIntegration
    SMS_INTEGRATION_ENABLED = True
except ImportError:
    SMS_INTEGRATION_ENABLED = False
```

## Path Updates

You'll also need to update paths to data files. Some common patterns:

- Replace `"crop_data/..."` with `"data/crop_data/..."`
- Replace `"scheme_data/..."` with `"data/scheme_data/..."`
- Replace `"loan_data/..."` with `"data/loan_data/..."`
- Replace `"subsidy_data/..."` with `"data/subsidy_data/..."`

## Testing Your Migration

After updating all imports, test the application to ensure everything works:

1. Run the main application:
   ```
   python -m vaani.core.main
   ```

2. Check that all services are functioning properly
   - Test voice input/output
   - Test weather service
   - Test news service
   - Test other key services

3. Run tests:
   ```
   python -m unittest discover tests
   ```

## Troubleshooting Common Issues

- **ImportError**: Check that the import path matches the new file location
- **ModuleNotFoundError**: Make sure all `__init__.py` files are created
- **FileNotFoundError**: Update data file paths to use the new structure
- **AttributeError**: Check for any renamed modules or functions

## Reverting if Necessary

The reorganization script creates copies of files rather than moving them, so if issues arise, you can continue using the original files while fixing problems in the new structure.
