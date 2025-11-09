# 🏗️ Vaani Project Architecture & Flow

**Voice Assistant for Illiterate Users | College Minor Project**

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Application Flow](#application-flow)
4. [Component Details](#component-details)
5. [API Integrations](#api-integrations)
6. [Data Flow](#data-flow)

---

## 🎯 Project Overview

**Vaani** is a Python-based voice assistant designed for illiterate and semi-literate users in India. It enables access to:
- 🌾 Agricultural information (crop prices, farming advice)
- 💰 Financial literacy & government schemes
- 📰 News and knowledge services
- 🚨 Emergency helplines

**Tech Stack:**
- **Language:** Python 3.8+
- **Voice Input:** SpeechRecognition (Google STT)
- **Voice Output:** gTTS (Google Text-to-Speech)
- **Audio:** pygame, pydub, ffmpeg
- **NLU:** Sentence Transformers (semantic understanding)
- **APIs:** OpenWeatherMap, NewsAPI, Agmarknet, Google Gemini

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION                         │
│                    (Voice Input via Microphone)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VAANI CORE SYSTEM                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  main.py - Main Application Loop                         │  │
│  │  - Voice input capture (listen_command)                  │  │
│  │  - Command routing (if-elif chain)                       │  │
│  │  - Response generation (bolo/bolo_stream)                │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  voice_tool.py - Voice I/O Handler                       │  │
│  │  - Speech-to-Text (Google STT)                           │  │
│  │  - Text-to-Speech (gTTS)                                 │  │
│  │  - Audio effects & streaming                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  context_manager.py - State Management                   │  │
│  │  - NewsContext, AgriculturalContext, SchemeContext       │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  language_manager.py - Multi-language Support            │  │
│  │  - Hindi, English, regional languages                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  config.py - Configuration & Trigger Phrases             │  │
│  │  - All command triggers & responses                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Weather    │  │     News     │  │    Agriculture       │  │
│  │   Service    │  │   Service    │  │      Service         │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Financial   │  │    Social    │  │    Knowledge         │  │
│  │   Literacy   │  │   Schemes    │  │  (Wikipedia/Gemini)  │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Emergency  │  │  Calculator  │  │   Expense Tracker    │  │
│  │  Assistance  │  │   Service    │  │      Service         │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL APIS & DATA                          │
│  • OpenWeatherMap API (Weather)                                 │
│  • NewsAPI (News Headlines)                                     │
│  • Agmarknet API (Crop Prices)                                  │
│  • Google Gemini AI (General Knowledge)                         │
│  • Wikipedia API (Encyclopedia)                                 │
│  • Local JSON Files (Schemes, Crops, Loans)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Application Flow

### 1️⃣ **Startup Flow**
```
main.py starts
    │
    ├─→ Load environment variables (.env file)
    │
    ├─→ Initialize language_manager (get user's language)
    │
    ├─→ Initialize offline_mode (check internet connectivity)
    │
    ├─→ Display startup message via bolo()
    │
    └─→ Enter main loop (while True)
```

### 2️⃣ **Main Loop Flow**
```
While True:
    │
    ├─→ listen_command() 
    │   ├─→ Start listening for voice input
    │   ├─→ Capture audio via microphone
    │   ├─→ Send to Google Speech Recognition API
    │   └─→ Return transcribed text (or None if error)
    │
    ├─→ Check if command received
    │   │
    │   ├─→ Normalize command (lowercase, strip whitespace)
    │   │
    │   ├─→ Check against trigger phrases (if-elif chain)
    │   │   │
    │   │   ├─→ Time/Date triggers? → call time_service
    │   │   ├─→ Weather triggers? → call weather_service  
    │   │   ├─→ News triggers? → call news_service
    │   │   ├─→ Agriculture triggers? → call agri_command_processor
    │   │   ├─→ Scheme triggers? → call social_scheme_service
    │   │   ├─→ Calculator triggers? → call calculator_service
    │   │   ├─→ Financial triggers? → call financial_literacy_service
    │   │   ├─→ Emergency triggers? → call emergency_assistance_service
    │   │   ├─→ Language change? → call handle_language_command
    │   │   ├─→ Exit triggers? → break loop
    │   │   └─→ Unknown? → call general_knowledge_service (Gemini)
    │   │
    │   └─→ Service processes & returns response
    │       │
    │       └─→ bolo() speaks response to user
    │
    └─→ sleep(1) and repeat
```

### 3️⃣ **Voice Input Flow (listen_command)**
```
listen_command() called
    │
    ├─→ Initialize recognizer
    │
    ├─→ Open microphone
    │
    ├─→ bolo("सुन रहा हूं") - "I'm listening"
    │
    ├─→ Adjust for ambient noise (1 second)
    │
    ├─→ Listen for audio (5 second timeout)
    │
    ├─→ Send audio to Google Speech Recognition
    │   ├─→ language = 'hi-IN' (Hindi)
    │   └─→ Get transcribed text
    │
    ├─→ Return command text
    │
    └─→ (On error: return None, speak error message)
```

### 4️⃣ **Voice Output Flow (bolo_stream)**
```
bolo_stream(text, lang) called
    │
    ├─→ Convert text to speech (gTTS)
    │
    ├─→ Save to temporary .mp3 file
    │
    ├─→ Apply audio effects (optional):
    │   ├─→ Speed adjustment (1.15x)
    │   ├─→ Volume normalization
    │   └─→ Save as processed .mp3
    │
    ├─→ Load audio with pygame
    │
    ├─→ Play audio
    │
    ├─→ Wait until finished
    │
    ├─→ Cleanup temp files
    │
    └─→ Return to caller
```

### 5️⃣ **Service Call Example: News Service**
```
User says: "समाचार सुनाओ" (Tell me news)
    │
    ├─→ listen_command() captures: "समाचार सुनाओ"
    │
    ├─→ main.py checks triggers: Config.news_trigger
    │   └─→ Match found! ["समाचार", "न्यूज", "news"]
    │
    ├─→ Call get_news(command, bolo, context)
    │   │
    │   ├─→ Extract category from command (or use "general")
    │   │
    │   ├─→ Call NewsAPI: fetch_news_api(category)
    │   │   ├─→ Make HTTP request to NewsAPI
    │   │   ├─→ Parse JSON response
    │   │   └─→ Return list of articles
    │   │
    │   ├─→ Store articles in NewsContext
    │   │
    │   ├─→ Read top 5 headlines via bolo()
    │   │
    │   ├─→ Ask: "विस्तार से सुनना चाहेंगे?" (Want details?)
    │   │
    │   ├─→ listen_command() for user response
    │   │
    │   └─→ If yes: call process_news_selection()
    │       ├─→ User says number (1-5)
    │       ├─→ Read full article description
    │       └─→ Return
    │
    └─→ Return to main loop
```

---

## 🧩 Component Details

### 📁 Core Components

#### `vaani/core/main.py` (Entry Point)
**Purpose:** Main application loop and command routing

**Key Functions:**
- `main()` - Entry point, infinite loop
- `log_unprocessed_query()` - Logs unknown commands

**Flow:**
1. Initialize services
2. Loop: listen → route → respond
3. Exit on "बंद करो" command

**Dependencies:**
- All service modules
- voice_tool, language_manager, context_manager

---

#### `vaani/core/voice_tool.py` (Voice I/O)
**Purpose:** Handle speech input/output

**Key Functions:**
- `listen_command()` - Capture voice input
  - Uses `speech_recognition` library
  - Google Speech-to-Text API
  - Returns transcribed text
  
- `bolo_stream(text, lang)` - Text-to-speech output
  - Uses `gTTS` library
  - Generates audio file
  - Plays via `pygame`
  
- `apply_voice_effects(input_file, output_file)` - Audio processing
  - Speed adjustment
  - Volume normalization
  - Uses `pydub` library

**Alias:** `bolo = bolo_stream` (for backward compatibility)

---

#### `vaani/core/context_manager.py` (State Management)
**Purpose:** Manage context across user interactions

**Classes:**
- `BaseContext` - Base class for all contexts
  - `state` - Current state
  - `data` - Dictionary for storing context data
  - `set(**kwargs)` - Set multiple attributes
  - `get(key, default)` - Get value from data
  
- `NewsContext` - News service context
  - Stores article list
  - Tracks selected article
  
- `AgriculturalContext` - Agriculture service context
  - Stores crop information
  - Tracks user's crop queries
  
- `SchemeContext` - Scheme service context
  - Stores scheme details
  - Tracks eligibility checks

---

#### `vaani/core/language_manager.py` (i18n)
**Purpose:** Multi-language support

**Functions:**
- `get_language_manager()` - Get language instance
- `handle_language_command(command, bolo)` - Switch language
- `get_phrase(key)` - Get translated phrase
- `get_tts_code()` - Get language code for TTS

**Supported Languages:**
- Hindi (hi)
- English (en)
- Marathi (mr)
- Bengali (bn)
- Tamil (ta)

---

#### `vaani/core/config.py` (Configuration)
**Purpose:** Central configuration and trigger phrases

**Key Contents:**
- **Trigger Phrases:** Lists for each command type
  - `news_trigger = ["समाचार", "न्यूज", "news"]`
  - `weather_trigger = ["मौसम", "weather"]`
  - `agriculture_trigger = ["खेती", "फसल", "crop"]`
  - etc. (30+ trigger lists)
  
- **Response Templates:** Pre-defined responses
  - `greeting_responses` - Greeting messages
  - `goodbye_responses` - Exit messages
  - `startup_responses` - Welcome messages
  
- **API Keys:** Environment variable names
  - `OPENWEATHER_API_KEY`
  - `NEWS_API_KEY`
  - `GEMINI_API_KEY`
  
- **Entity Mappings:** Aliases for crops, schemes, etc.
  - `CROP_ALIASES` - Crop name variations
  - `SCHEME_ALIASES` - Scheme name variations

---

### 📁 Service Components

#### `vaani/services/time/time_service.py`
**Functions:**
- `current_time()` - Current time
- `get_date_of_day_in_week(day)` - Next occurrence of day
- `get_day_summary()` - Today's date info

---

#### `vaani/services/weather/weather_service.py`
**Functions:**
- `get_weather(command, bolo)` - Fetch & speak weather
  - Calls OpenWeatherMap API
  - Extracts location from command
  - Returns temperature, humidity, condition

---

#### `vaani/services/news/news_service.py`
**Functions:**
- `get_news(command, bolo, context)` - Fetch news
  - Calls NewsAPI
  - Stores in context
  - Reads headlines
  
- `process_news_selection(command, bolo, context)` - Article details
  - Reads full description
  - Handles user selection (1-5)

---

#### `vaani/services/agriculture/agri_command_processor.py`
**Functions:**
- `process_agriculture_command(command, bolo, context)` - Route agricultural queries
  - Market prices (Agmarknet API)
  - Crop information (local JSON)
  - Farming advice
  - Subsidy information

**Data Sources:**
- `data/crop_data/*.json` - 30+ crop files
- `data/subsidy_data/*.json` - Subsidy schemes
- Agmarknet API - Real-time prices

---

#### `vaani/services/social/social_scheme_service.py`
**Functions:**
- `handle_social_schemes_query(command, bolo, context)` - Government schemes
  - PM-KISAN
  - Ayushman Bharat
  - MUDRA Loans
  - etc.

**Data Sources:**
- `data/scheme_data/*.json` - Scheme details
- `data/loan_data/*.json` - Loan information

---

#### `vaani/services/knowledge/general_knowledge_service.py`
**Functions:**
- `handle_general_knowledge_query(command, bolo)` - General questions
  - Uses Google Gemini AI
  - Generates human-like responses
  - Fallback for unknown commands

---

## 🔌 API Integrations

### 1. Google Speech-to-Text (STT)
- **Library:** `speech_recognition`
- **Usage:** Voice input capture
- **Free Tier:** Yes (via Google Cloud)

### 2. Google Text-to-Speech (TTS)
- **Library:** `gTTS`
- **Usage:** Voice output generation
- **Free Tier:** Yes

### 3. OpenWeatherMap API
- **Endpoint:** `http://api.openweathermap.org/data/2.5/weather`
- **Usage:** Weather information
- **Free Tier:** 1000 calls/day

### 4. NewsAPI
- **Endpoint:** `https://newsapi.org/v2/top-headlines`
- **Usage:** Latest news headlines
- **Free Tier:** 100 requests/day

### 5. Agmarknet API
- **Endpoint:** `https://api.data.gov.in/resource/...`
- **Usage:** Agricultural market prices
- **Free Tier:** Yes (Government API)

### 6. Google Gemini AI
- **Library:** `google-generativeai`
- **Usage:** General knowledge queries
- **Free Tier:** Yes (limited)

---

## 📊 Data Flow Diagram

```
┌─────────────┐
│    USER     │
│  (Speaks)   │
└──────┬──────┘
       │ Voice
       ▼
┌─────────────────────┐
│  Microphone Input   │
└──────┬──────────────┘
       │ Audio
       ▼
┌─────────────────────┐
│ Google STT API      │
│ (Speech Recognition)│
└──────┬──────────────┘
       │ Text (Command)
       ▼
┌─────────────────────┐
│    main.py          │
│  Command Router     │
└──────┬──────────────┘
       │
       ├─→ Time Service → Response
       ├─→ Weather API → JSON → Response
       ├─→ News API → JSON → Response
       ├─→ Agriculture Service → JSON/API → Response
       ├─→ Scheme Service → JSON → Response
       ├─→ Gemini AI → Response
       │
       ▼
┌─────────────────────┐
│  bolo_stream()      │
│  (Text-to-Speech)   │
└──────┬──────────────┘
       │ Audio File (.mp3)
       ▼
┌─────────────────────┐
│  Audio Effects      │
│  (Speed, Volume)    │
└──────┬──────────────┘
       │ Processed Audio
       ▼
┌─────────────────────┐
│  pygame Player      │
│  (Speaker Output)   │
└──────┬──────────────┘
       │ Sound
       ▼
┌─────────────┐
│    USER     │
│  (Hears)    │
└─────────────┘
```

---

## 🗂️ Directory Structure

```
Vaani-2/
├── vaani/                          # Main package
│   ├── core/                       # Core modules
│   │   ├── main.py                 # Entry point
│   │   ├── voice_tool.py           # Voice I/O
│   │   ├── context_manager.py      # State management
│   │   ├── language_manager.py     # Multi-language
│   │   ├── config.py               # Configuration
│   │   └── offline_mode.py         # Offline support
│   │
│   ├── services/                   # Service modules
│   │   ├── time/                   # Time services
│   │   ├── weather/                # Weather services
│   │   ├── news/                   # News services
│   │   ├── agriculture/            # Agricultural services
│   │   ├── social/                 # Scheme & emergency services
│   │   ├── finance/                # Financial services
│   │   └── knowledge/              # Wikipedia & Gemini
│   │
│   └── utils/                      # Utility modules
│
├── data/                           # Static data
│   ├── crop_data/                  # 30+ crop JSON files
│   ├── scheme_data/                # Government schemes
│   ├── loan_data/                  # Loan information
│   ├── subsidy_data/               # Subsidy details
│   └── offline_cache/              # Cached responses
│
├── tests/                          # Test files
│
├── logs/                           # Application logs
│
├── cache/                          # Runtime cache
│
├── .env                            # Environment variables
├── requirements.txt                # Python dependencies
├── start_vaani.ps1                 # Windows startup script
└── README.md                       # Project documentation
```

---

## 🚀 Startup Command

```bash
# Windows
python -m vaani.core.main

# Or use PowerShell script
.\start_vaani.ps1
```

---

**Last Updated:** November 7, 2025
