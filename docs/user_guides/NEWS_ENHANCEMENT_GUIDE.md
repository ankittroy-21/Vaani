# News Service Enhancement Guide

## Introduction
This document explains the enhanced news service functionality designed specifically for illiterate users as part of supporting SDG Goal 1 (No Poverty). The enhancements focus on making news consumption more accessible and user-friendly for people with limited or no literacy skills.

## Features

### 1. Offline Support
- News caching system to make news available even without an internet connection
- Automatic expiry of cached news (configurable duration)
- Graceful fallback to cached news when connection issues occur

### 2. Simplified Language
- Complex words are automatically replaced with simpler alternatives
- Headlines are presented in numbered format for easier reference
- Dates are simplified to relative time (e.g., "2 hours ago", "yesterday") for easier comprehension

### 3. Enhanced Voice Interaction
- Multiple ways to reference news items:
  - By number ("पहली खबर", "एक", "1")
  - By saying part of the headline
  - By simple gestures (multiple repetitions of the same command)
- Better handling of user confusion through repetition detection and automatic assistance

### 4. Robustness
- Error handling with user-friendly messages
- API key validation before making requests
- Fallback mechanisms for various failure scenarios
- Logging for troubleshooting

## Usage Examples

### Basic News Retrieval
User can ask for news in natural language:
- "आज की खबर सुनाओ" (Tell me today's news)
- "किसान आंदोलन की खबर बताओ" (Tell me news about farmer protests)
- "खेती के बारे में समाचार" (News about farming)

### News Selection
After headlines are read, users can select news in various ways:
- "पहली खबर" (First news)
- "दो" (Two)
- "3" (Three)
- Or by repeating key phrases from the headline they're interested in

### Exit News Mode
- "बंद करो" (Close it)
- "कोई नहीं" (None)
- "समाप्त" (End)
- Or any phrase from the configured exit triggers

## Behind the Scenes

### Caching System
News is cached in JSON format with the following structure:
```json
{
  "hash_key": {
    "query": "original query",
    "articles": [...],
    "timestamp": 1234567890
  }
}
```

### Enhanced Number Recognition
The system recognizes numbers in multiple formats:
- Hindi words ("एक", "दो", "तीन")
- Hindi position words ("पहली", "दूसरी", "तीसरी")
- Numerals ("1", "2", "3")
- With context ("खबर नंबर 2", "दूसरी खबर")

### Language Simplification
Complex terms are automatically replaced with simpler alternatives to make news more accessible to illiterate users.

## Configuration
All news-related configuration is available in `news_config.py`:
- News trigger phrases
- Words to filter out of queries
- News summary responses
- Exit trigger phrases

## Next Steps for Future Enhancement
1. Add image descriptions for news with images (for future visual interface)
2. Implement voice tone analysis to detect user frustration
3. Add category-based news filtering for easier navigation
4. Create personalized news recommendations based on usage patterns
