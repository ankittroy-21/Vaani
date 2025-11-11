# 🤖 Vaani – Voice-First Digital Inclusion for ALL 💬

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SDG Goals](https://img.shields.io/badge/SDG-8%20Goals%20Aligned-green.svg)](https://sdgs.un.org/goals)

**College Minor Project | Democratizing Digital Access Through Voice**

Vaani is India's first voice-first digital inclusion platform designed for **300+ million functionally illiterate Indians** - eliminating literacy as a barrier to digital services. While agriculture was our entry point, Vaani serves all underserved populations: **farmers (146M), elderly citizens (104M), disabled persons (27M), domestic workers (50M), daily wage workers (139M), women in conservative families (80M), and millions more** excluded from India's digital revolution.

**Core Principle:** *If you can speak, you deserve equal access to information, rights, and opportunities.*

Vaani operates entirely through voice commands in Hindi and Indian languages, making government schemes, healthcare information, financial services, legal rights, and emergency assistance accessible to **everyone** - regardless of literacy level.

---

## 📚 Documentation

This project has comprehensive documentation:

1. **[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md)** - Complete system architecture, flow diagrams, and technical details
2. **[PROJECT_PROGRESS.md](PROJECT_PROGRESS.md)** - Development phases, accomplishments, and future goals
3. **[BROADER_VISION.md](BROADER_VISION.md)** - ⭐ **Expanded vision: Beyond farmers to all illiterate populations**
4. **[USER_MANUAL.md](USER_MANUAL.md)** - End-user guide with examples
5. **[DEMO_SCRIPT.md](DEMO_SCRIPT.md)** - 5-minute demo walkthrough
6. **[DEBUGGING_GUIDE.md](DEBUGGING_GUIDE.md)** - Error tracking, debugging techniques, and useful commands

---

## 🎯 Mission & Impact

**Democratizing Digital India - Beyond Literacy**

Vaani addresses the fundamental barrier facing **695+ million Indians**: literacy should never determine access to digital services.

### **Who Benefits:**
- 🌾 **Farmers (146M)** - Agricultural advice, market prices, weather forecasts
- 👴 **Elderly Citizens (104M)** - Healthcare info, pension schemes, medicine reminders
- ♿ **Disabled Persons (27M)** - Complete voice navigation, independence, dignity
- 🏠 **Domestic Workers (50M)** - Rights information, safety helplines, skill training
- 🏗️ **Daily Wage Workers (139M)** - MGNREGA status, minimum wage info, loan schemes
- 🛒 **Street Vendors (10M)** - Business calculations, PM SVANidhi loans
- 🧕 **Women in Conservative Families (80M)** - Maternal health, empowerment, privacy
- 🚂 **Migrant Workers (139M)** - Language translation, local services, emergency help
- 👧 **Children** - Homework help, curiosity questions, learning support

### **What They Get:**
- 📱 Access to government schemes and social welfare programs
- 🌾 Agricultural information and market prices for farmers
- 💰 Financial literacy and expense tracking
- 📰 News and information in simplified language
- 🚨 Emergency assistance and helpline access
- 🌐 Offline mode for areas with limited connectivity

---

## ✨ Core Features

### 🗣️ **Advanced Voice Interface**
- Natural spoken Hindi with support for multiple Indian languages
- Colloquial language understanding
- Offline voice processing capability
- Enhanced voice quality with audio processing

### 🌾 **Comprehensive Agricultural Suite**
- Real-time market prices via Agmarknet API
- Detailed crop-specific farming advice (30+ crops)
- Information on agricultural schemes and subsidies
- Seasonal farming guidance
- Pest control and disease management tips

### 💰 **Financial Services**
- Financial literacy education
- Expense tracking and budget management
- Simple calculator for daily transactions
- Information on loans and microfinance schemes

### 📋 **Government Scheme Information**
- PM-KISAN, PM Fasal Bima Yojana
- Ayushman Bharat health insurance
- MUDRA loans and Kisan Credit Card
- Social welfare schemes (pension, housing, etc.)
- Scheme eligibility checker

### 🌦️ **Advanced Weather & Forecasting**
- Location-based weather reports
- Temperature, humidity, wind speed
- Rain prediction (today, tomorrow, next likely day)
- Agricultural weather advisories

### 📰 **Enhanced News Service**
- Latest headlines in simplified language
- Category-based news (politics, sports, business, etc.)
- Offline news caching
- Detailed article summaries
- Voice-friendly news delivery

### 🌐 **Knowledge & Utilities**
- Wikipedia search with simplified summaries
- General knowledge queries
- Current time and date information
- Historical facts about current date

### 🚨 **Emergency Services**
- Quick access to emergency helplines
- Women's helpline information
- Health emergency guidance
- Natural disaster assistance

### 🔄 **Offline Mode**
- Works without internet connection
- Cached data for essential services
- Offline news storage
- Local data processing

### 🌍 **Multi-Language Support**
- Hindi (Primary)
- Support for regional Indian languages
- Easy language switching
- Localized responses

### 🧠 **Smart NLU Engine**
- Powered by Sentence Transformer models
- Semantic intent understanding
- Context-aware responses
- Handles diverse speaking styles



---

## � Project Structure

The project follows professional Python packaging standards:

```
vaani/
├── vaani/                          # Main package
│   ├── core/                       # Core functionality
│   │   ├── main.py                # Application entry point
│   │   ├── config.py              # Configuration
│   │   ├── voice_tool.py          # Voice I/O processing
│   │   ├── language_manager.py    # Multi-language support
│   │   ├── offline_mode.py        # Offline functionality
│   │   ├── cache_manager.py       # Caching system
│   │   └── api_key_manager.py     # Secure API key handling
│   │
│   ├── services/                  # Service modules
│   │   ├── agriculture/           # Agricultural services
│   │   ├── finance/               # Financial services
│   │   ├── news/                  # News services
│   │   ├── weather/               # Weather services
│   │   ├── knowledge/             # Knowledge services
│   │   ├── social/                # Social welfare services
│   │   ├── communication/         # SMS/USSD integration
│   │   └── time/                  # Time services
│   │
│   └── data/                      # Data models
│
├── data/                          # Data files
│   ├── crop_data/                # Crop information (30+ crops)
│   ├── scheme_data/              # Government schemes
│   ├── loan_data/                # Loan information
│   ├── subsidy_data/             # Subsidy information
│   └── offline_cache/            # Offline data cache
│
├── docs/                          # Documentation
│   ├── user_guides/              # User documentation
│   ├── developer_guides/         # Developer documentation
│   └── architecture/             # Architecture docs
│
├── tests/                         # Test files
├── scripts/                       # Utility scripts
├── logs/                          # Log files
├── setup.py                       # Package installation
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

---

## � Deployment

### Deploy to Render (Free Tier)

Deploy Vaani to the cloud in minutes with automatic keep-alive!

**Quick Deploy:**
```bash
# 1. Verify project
python verify_render_deployment.py

# 2. Push to GitHub
git push origin main

# 3. Deploy on Render
# Visit https://dashboard.render.com
# Connect your GitHub repo
# Render auto-detects configuration!
```

**Features:**
- ✅ **Keep-Alive**: Auto-ping every 14 minutes (stays active 24/7)
- ✅ **Auto-Deploy**: Push to GitHub, automatic deployment
- ✅ **Free SSL**: HTTPS enabled automatically
- ✅ **Zero Config**: Works out of the box

**Documentation:**
- 📖 [Quick Start Guide](RENDER_QUICKSTART.md) - Deploy in 5 minutes
- 📚 [Full Deployment Guide](RENDER_DEPLOYMENT_GUIDE.md) - Complete documentation
- 🔧 [Verification Script](verify_render_deployment.py) - Test before deploying

**Your app will be live at:** `https://your-app-name.onrender.com`

---

## �🛠️ Built With

### Core Technologies
* **Python** 3.8+ (3.10+ recommended)
* **Package Structure:** Professional Python packaging with setuptools

### AI & NLU
* **sentence-transformers** - Semantic understanding
* **torch** - Deep learning backend
* **rapidfuzz** - Fast fuzzy string matching

### Voice Processing
* **SpeechRecognition** - Speech-to-text conversion
* **gTTS (Google Text-to-Speech)** - Text-to-speech synthesis
* **pygame** - Audio playback
* **pydub** - Audio enhancement
* **FFmpeg** - Audio format conversion

### Data & APIs
* **requests** - HTTP API communication
* **wikipedia** - Encyclopedia lookups
* **cryptography** - Secure key management
* **python-dotenv** - Environment configuration

### APIs Integrated
* **OpenWeatherMap API** - Weather forecasts
* **GNews API** - News headlines
* **Agmarknet API** - Agricultural market prices (data.gov.in)
* **Wikipedia API** - Knowledge base
      

---

## 🚀 Getting Started

### Prerequisites

* **Python 3.8+** (Python 3.10+ recommended)
* **Microphone** connected to your computer
* **Internet connection** (for initial setup and online features)
* **FFmpeg** (for enhanced voice features)
* **Operating System:** Windows, Linux, or macOS

### Quick Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/ankittroy-21/Vaani.git
cd Vaani
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Install FFmpeg
**Windows:**
```powershell
.\scripts\install_ffmpeg.ps1
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

#### 4. Set Up API Keys
Create a `.env` file in the project root:

```env
WEATHER_API_KEY=your_openweathermap_key
GNEWS_API_KEY=your_gnews_key
AGMARKNET_API_KEY=your_agmarknet_key
```

**Get Your Free API Keys:**
- **OpenWeatherMap:** [https://openweathermap.org/appid](https://openweathermap.org/appid)
- **GNews:** [https://gnews.io/](https://gnews.io/)
- **Agmarknet:** [https://data.gov.in](https://data.gov.in)

#### 5. Install the Package (Optional)
For system-wide installation:
```bash
pip install -e .
```

---

## 🎮 Running Vaani

### Option A: Web Interface (Recommended for Demo) 🌐

The web interface provides a modern, user-friendly way to interact with Vaani through your browser, with both text and voice input support.

**Windows PowerShell:**
```powershell
# Quick start with auto-setup
.\start_web.ps1
```

**Manual start:**
```powershell
# 1. Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the web server
python -m vaani.web
```

**Linux/macOS:**
```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the web server
python -m vaani.web
```

**Access the interface:**
Open your browser and navigate to: **http://localhost:5000**

**Features:**
- 🎤 Voice input via browser microphone
- ⌨️ Text input for quick queries
- 🔊 Audio playback of responses
- 📱 Mobile-friendly responsive design
- 🌐 Works offline (limited features)
- 🚀 Quick action buttons for common queries

---

### Option B: Terminal/CLI Mode

For development or terminal-based usage:

### Method 1: As a Module (Recommended)
```bash
python -m vaani.core.main
```

### Method 2: Using PowerShell Script
```powershell
.\start_vaani.ps1
```

### Method 3: After Installation
```bash
pip install -e .
vaani
```

### Method 4: Direct Execution
```bash
cd vaani/core
python main.py
```

---

## 📚 Quick Start Guide

1. **Launch Vaani:** Run the application using one of the methods above
2. **Wait for Greeting:** Vaani will greet you with "नमस्ते! मैं वाणी हूँ"
3. **Speak Commands:** Use any of the voice commands (see examples below)
4. **Listen to Response:** Vaani will provide spoken responses
5. **Exit:** Say "बंद करो" or "अलविदा" to exit

For detailed instructions, see [Quick Start Guide](docs/user_guides/QUICK_START_GUIDE.md)


# 🗣️ Voice Command Examples

## Basic Commands

### 🕒 Time & Date
* `"समय बताओ"` - Current time
* `"आज कौन सा दिन है"` - Today's day
* `"आज की तारीख बताओ"` - Today's date

### 👋 Greetings & Controls
* `"नमस्ते"` - Greet Vaani
* `"बंद करो"` / `"अलविदा"` - Exit application
* `"भाषा बदलो"` - Change language

---

## 🌾 Agriculture Commands

### 🌱 Crop Information
* `"धान की खेती के बारे में बताओ"` - Rice farming guide
* `"गेहूं कैसे उगाएं"` - Wheat cultivation
* `"टमाटर की देखभाल कैसे करें"` - Tomato care
* `"आलू में कौन सा खाद डालें"` - Potato fertilization

### 💰 Market Prices
* `"आज धान का भाव क्या है"` - Rice market price
* `"गेहूं का रेट बताओ"` - Wheat price
* `"प्याज की कीमत क्या चल रही है"` - Onion price

### 📋 Schemes & Subsidies
* `"किसान योजना के बारे में बताओ"` - Farmer schemes
* `"फसल बीमा योजना क्या है"` - Crop insurance
* `"कृषि सब्सिडी की जानकारी दो"` - Agricultural subsidies
* `"किसान क्रेडिट कार्ड कैसे बनवाएं"` - KCC information

---

## 🌦️ Weather Services

### Basic Weather
* `"दिल्ली का मौसम बताओ"` - Delhi weather
* `"लखनऊ का तापमान क्या है"` - Lucknow temperature
* `"आज बारिश होगी क्या"` - Rain prediction

### Detailed Forecasts
* `"पूरी मौसम की जानकारी दो"` - Complete weather report
* `"हवा की गति बताओ"` - Wind speed
* `"कल बारिश होगी"` - Tomorrow's rain forecast

---

## 📰 News Services

### General News
* `"आज की ताज़ा खबरें सुनाओ"` - Latest headlines
* `"खबरें बताओ"` - News headlines
* `"पहली खबर"` / `"दूसरी खबर"` - Specific article

### Category-Based News
* `"राजनीति की खबरें"` - Political news
* `"खेल समाचार"` - Sports news
* `"मनोरंजन की खबरें"` - Entertainment news
* `"व्यापार समाचार"` - Business news

---

## 💰 Financial Services

### Financial Literacy
* `"बचत कैसे करें"` - Savings tips
* `"बजट कैसे बनाएं"` - Budget planning
* `"निवेश क्या है"` - Investment basics
* `"ब्याज दर क्या होती है"` - Interest rates

### Expense Tracking
* `"खर्चा जोड़ो 500 रुपये खाना"` - Add expense
* `"कुल खर्चा बताओ"` - Total expenses
* `"आज का खर्चा"` - Today's expenses
* `"इस महीने का बजट"` - Monthly budget

### Calculator
* `"100 और 200 जोड़ो"` - Addition
* `"500 में से 200 घटाओ"` - Subtraction
* `"10 गुना 5"` - Multiplication
* `"100 बांटो 4 से"` - Division

---

## � Social Welfare & Emergency

### Government Schemes
* `"आयुष्मान भारत योजना"` - Ayushman Bharat
* `"पेंशन योजना"` - Pension schemes
* `"आवास योजना"` - Housing schemes
* `"मुद्रा लोन कैसे मिलेगा"` - MUDRA loan

### Emergency Services
* `"एम्बुलेंस नंबर बताओ"` - Ambulance helpline
* `"महिला हेल्पलाइन"` - Women's helpline
* `"आपातकालीन नंबर"` - Emergency numbers

---

## 🌐 Knowledge & Information

### Wikipedia Searches
* `"विकिपीडिया पर महात्मा गांधी खोजो"` - Search Gandhi
* `"भारत के बारे में बताओ"` - About India
* `"ताज महल की जानकारी"` - Taj Mahal info

### General Knowledge
* `"भारत की राजधानी"` - Capital of India
* `"सबसे बड़ा देश कौन सा है"` - Largest country
* `"आज का इतिहास"` - Today in history

---

## 🎯 Advanced Features

### Multi-Language Support
* Seamlessly switches between Hindi and regional languages
* Understands colloquial phrases and dialects

### Offline Mode
* Works without internet for cached data
* Stores essential information locally

### Context Awareness
* Remembers conversation context
* Follows up on previous queries

---

✨ **Pro Tip:** Speak naturally! Vaani understands colloquial Hindi and various speaking styles.

---

## 🧪 Testing

### Run All Tests
```bash
python -m unittest discover tests
```

### Run Specific Tests
```bash
# Test voice functionality
python -m unittest tests.test_voice

# Test multilanguage support
python -m unittest tests.test_multilang

# Test performance
python -m unittest tests.test_performance

# Test Gemini integration
python -m unittest tests.test_gemini_integration
```

### Verify Improvements
```bash
python tests/verify_improvements.py
```

---

## � Documentation

Comprehensive documentation is available in the `docs/` directory:

### For Users
* [Quick Start Guide](docs/user_guides/QUICK_START_GUIDE.md) - Get started quickly
* [FFmpeg Installation](docs/user_guides/FFMPEG_INSTALLATION.md) - Audio setup guide
* [Multilanguage Guide](docs/user_guides/MULTILANG_GUIDE.md) - Language features
* [News Enhancement Guide](docs/user_guides/NEWS_ENHANCEMENT_GUIDE.md) - News features
* [Voice Enhancement Guide](docs/user_guides/VOICE_ENHANCEMENT_GUIDE.md) - Voice features

### For Developers
* [Architecture](docs/architecture/ARCHITECTURE.md) - System architecture
* [Visual Summary](docs/architecture/VISUAL_SUMMARY.md) - Visual overview
* [Roadmap](docs/developer_guides/ROADMAP.md) - Future plans
* [SDG No Poverty Guide](docs/developer_guides/SDG_NO_POVERTY_GUIDE.md) - Social impact
* [Gemini Integration](docs/developer_guides/GEMINI_INTEGRATION_GUIDE.md) - AI integration
* [Verification Guide](docs/developer_guides/VERIFICATION_GUIDE.md) - Testing guide
* [Migration Guide](docs/MIGRATION_GUIDE.md) - Import migration guide

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
# API Keys
WEATHER_API_KEY=your_openweathermap_key
GNEWS_API_KEY=your_gnews_key
AGMARKNET_API_KEY=your_agmarknet_key

# Optional Settings
SMS_INTEGRATION_ENABLED=False
OFFLINE_MODE=False
LOG_LEVEL=INFO
```

### Custom Configuration
Edit `vaani/core/config.py` to customize:
- Trigger words and phrases
- Response templates
- Voice settings
- Cache durations
- API endpoints

---

## 🌟 Key Features in Detail

### Offline Mode
Vaani works even without internet:
- Cached news articles
- Offline crop information
- Local weather data
- Government scheme details
- Emergency numbers

### Enhanced Voice Quality
- Audio normalization
- Noise reduction
- Speed optimization
- Pitch adjustment
- Clear pronunciation

### Smart Caching
- Intelligent data caching
- Automatic cache updates
- Offline-first approach
- Reduced API calls
- Faster response times

### Security
- Encrypted API keys
- Secure data storage
- Privacy-focused design
- No personal data collection
- Local processing

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute
1. **Report Bugs** - Found a bug? Create an issue
2. **Suggest Features** - Have ideas? We'd love to hear them
3. **Submit Pull Requests** - Code contributions are welcome
4. **Improve Documentation** - Help make docs better
5. **Add Translations** - Support more languages

### Development Setup
```bash
# Fork the repository
git clone https://github.com/YOUR_USERNAME/Vaani.git
cd Vaani

# Create a branch
git checkout -b feature/your-feature-name

# Make your changes and test
python -m unittest discover tests

# Commit and push
git add .
git commit -m "Add your feature"
git push origin feature/your-feature-name

# Create a Pull Request
```

### Coding Standards
- Follow PEP 8 style guide
- Write clear commit messages
- Add tests for new features
- Update documentation
- Comment your code

---

## 🐛 Troubleshooting

### Common Issues

#### Microphone Not Working
```bash
# Check microphone access
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

#### FFmpeg Not Found
```bash
# Windows
.\scripts\install_ffmpeg.ps1

# Linux/Mac
which ffmpeg
```

#### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Unicode Errors (Windows)
The application automatically handles Unicode encoding. If issues persist:
- Use Windows Terminal instead of CMD
- Set console encoding to UTF-8

#### API Rate Limits
- Use offline mode for frequent queries
- Check API key quotas
- Enable caching in config

For more help, see [Verification Guide](docs/developer_guides/VERIFICATION_GUIDE.md)

---

## 📊 Project Status

### Current Version
**v1.0.0** - Production Ready

### Features Status
- ✅ Voice Recognition & Synthesis
- ✅ Agricultural Advisory System
- ✅ Weather Forecasting
- ✅ News Service with Offline Mode
- ✅ Financial Literacy Tools
- ✅ Government Scheme Information
- ✅ Emergency Services
- ✅ Multi-language Support
- ✅ Offline Mode
- ✅ Professional Package Structure
- 🚧 SMS/USSD Integration (In Development)
- 🚧 Mobile App Version (Planned)

---

## 🎯 Roadmap

### Short Term (Q1 2026)
- [ ] Mobile application (Android)
- [ ] SMS/USSD complete integration
- [ ] More regional languages
- [ ] Voice customization options
- [ ] Expanded crop database (50+ crops)

### Medium Term (Q2-Q3 2026)
- [ ] AI-powered crop disease detection
- [ ] Real-time commodity trading alerts
- [ ] Community forum integration
- [ ] Video tutorials for farmers
- [ ] IoT sensor integration

### Long Term (Q4 2026+)
- [ ] iOS application
- [ ] Blockchain-based farmer registry
- [ ] Microfinance integration
- [ ] Supply chain management
- [ ] International expansion

See [ROADMAP.md](docs/developer_guides/ROADMAP.md) for detailed plans.

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Vaani Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

### Organizations
* **UN SDG Initiative** - Inspiration for SDG Goal 1 focus
* **Government of India** - Open data APIs (Agmarknet)
* **data.gov.in** - Agricultural data access

### Technologies
* **OpenAI** - For AI research and inspiration
* **Google** - Text-to-Speech services
* **OpenWeatherMap** - Weather data
* **GNews** - News aggregation
* **Wikipedia** - Knowledge base

### Community
* All contributors who have helped improve Vaani
* Beta testers who provided valuable feedback
* The open-source community for amazing tools

---

## 👥 Team

**Vaani Development Team**

From **Babu Banarasi Das University**

[![BBDU Logo](https://bbdu.ac.in/wp-content/uploads/2018/10/bbd-logo.png)](https://bbdu.ac.in)

---

## 📞 Contact & Support

### Get Help
- **GitHub Issues:** [Report bugs or request features](https://github.com/ankittroy-21/Vaani/issues)
- **Email:** support@vaani-assistant.com
- **Documentation:** [https://github.com/ankittroy-21/Vaani/docs](https://github.com/ankittroy-21/Vaani/docs)

### Follow Updates
- **GitHub:** [@ankittroy-21](https://github.com/ankittroy-21)
- **Repository:** [Vaani](https://github.com/ankittroy-21/Vaani)

---

## 🌍 Social Impact

Vaani directly contributes to **UN SDG Goal 1: No Poverty** by:

- 📱 Bridging the digital divide for illiterate populations
- 🌾 Empowering farmers with market information
- 💰 Promoting financial literacy and inclusion
- 📋 Simplifying access to government welfare schemes
- 🏥 Providing emergency service information
- 🎓 Offering educational content through voice

**Target Impact:** Reaching 10 million illiterate users by 2027

---

## ⭐ Star History

If you find Vaani helpful, please consider giving it a star ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=ankittroy-21/Vaani&type=Date)](https://star-history.com/#ankittroy-21/Vaani&Date)

---

## 🎉 Quick Links

- [📥 Installation Guide](#-getting-started)
- [🎮 Running Vaani](#-running-vaani)
- [🗣️ Voice Commands](#️-voice-command-examples)
- [📖 Documentation](#-documentation)
- [🤝 Contributing](#-contributing)
- [🐛 Troubleshooting](#-troubleshooting)
- [📜 License](#-license)

---

<div align="center">

**Made with ❤️ for India's Illiterate Populations**

*Empowering Everyone Through Voice Technology*

**[⬆ Back to Top](#-vaani--voice-assistant-for-everyone-)**

</div>
