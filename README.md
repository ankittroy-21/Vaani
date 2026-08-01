<div align="center">

# 🤖 Vaani (वाणी)

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=00C853&center=true&vCenter=true&width=750&lines=Voice-First+Digital+Inclusion+Platform;Democratizing+Digital+Access+for+300M%2B+Indians;Natural+Hindi+%26+Regional+Language+NLU;Real-Time+Crop+Prices%2C+Weather+%26+Government+Schemes" alt="Typing SVG" />

### 🗣️ *Democratizing Digital Access Through Voice – Empowering India's Underserved Populations*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Google STT](https://img.shields.io/badge/Google-Speech_Recognition-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://cloud.google.com/speech-to-text)
[![gTTS](https://img.shields.io/badge/Google-gTTS-34A853?style=for-the-badge&logo=google&logoColor=white)](https://pypi.org/project/gTTS/)
[![Sentence Transformers](https://img.shields.io/badge/NLU-Sentence_Transformers-FF6F00?style=for-the-badge&logo=huggingface&logoColor=white)](https://www.sbert.net/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![SDG Goals](https://img.shields.io/badge/SDG-No_Poverty_%26_Decent_Work-green.svg?style=for-the-badge)](https://sdgs.un.org/goals)

---

**Bridging the Digital Divide with Zero Literacy Barriers! 🌾**

[🌐 Deploy on Render](https://render.com/deploy?repo=https://github.com/groupnumber-9/Vaani) • [📖 About](#-about-the-project) • [⚙️ How It Works](#️-how-it-works) • [🏗️ Architecture](#-system-architecture) • [🛠️ Tech Stack](#️-technology-stack) • [🚀 Setup](#-setup--deployment)

</div>

---

## 📖 About the Project

**Vaani (वाणी)** is India's first voice-first digital inclusion platform designed specifically for **300+ million functionally illiterate and semi-literate citizens**. By removing text literacy as a pre-requisite for digital services, Vaani enables anyone who can speak to seamlessly access essential government schemes, agricultural advice, market commodity prices, weather forecasts, financial services, news, and emergency assistance.

While agriculture served as our entry point, Vaani empowers all underserved populations: **farmers (146M), elderly citizens (104M), disabled persons (27M), domestic workers (50M), daily wage workers (139M), women in conservative families (80M), and migrant workers (139M)** who are otherwise excluded from India's digital revolution.

> [!NOTE]  
> **🎯 Mission:** To democratize digital access across India by ensuring that literacy is never a barrier to accessing critical information, fundamental rights, financial tools, and life-saving emergency services.

---

## 🚨 The Problem

<div align="center">

```ascii
╔══════════════════════════════════════════════════════════════╗
║        ⚠️  CHALLENGES IN RURAL & LITERACY-BARRED ACCESS     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📄  Text-heavy mobile apps & websites bar 300M+ citizens   ║
║  🌾  Farmers lack real-time market prices & crop disease info║
║  🏛️  Government welfare schemes remain unused & inaccessible  ║
║  🌦️  Unpredictable weather losses without localized alerts   ║
║  📱  Complex touch UI navigation confuses elderly & disabled  ║
║  🌐  Poor internet connectivity in remote rural pockets      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

</div>

Traditional mobile applications and digital government portals rely heavily on text literacy, complex menu navigation, and constant high-speed internet connection. This creates a severe digital divide, leaving over 695 million rural and semi-literate Indians without access to vital economic and social resources.

---

## ✅ Our Solution

**Vaani** transforms digital interaction into an intuitive, voice-first experience powered by semantic NLU and local caching:

<table>
<tr>
<td width="50%">

### 🎯 Core Capabilities
- 🗣️ **Conversational Voice Interface in Natural Hindi**
- 🌾 **Live Agmarknet Market Prices & Crop Advisories**
- 📋 **Automated Government Scheme Eligibility Checker**
- 🌦️ **Location-Aware Weather Forecasts & Warnings**

</td>
<td width="50%">

### 🚀 Key Benefits
- ⚡ **Zero Literacy Barrier (Spoken Voice In & Out)**
- 🌐 **Offline Mode for Low Connectivity Areas**
- 💰 **Built-in Expense Tracker & Calculator**
- 🚨 **One-Touch Voice Emergency Helpline Router**

</td>
</tr>
</table>

---

## ⚙️ How It Works

<div align="center">

```mermaid
sequenceDiagram
    participant User
    participant WebUI as Browser UI / Mic
    participant STT as Google Speech API
    participant Router as Main Engine (main.py)
    participant NLU as Sentence Transformer NLU
    participant Services as Service Layer
    participant TTS as gTTS & Audio Engine
    participant Cache as Offline Cache / Local Data

    User->>WebUI: Speak Query (Hindi/Regional)
    WebUI->>STT: Stream Audio Input
    STT-->>Router: Return Transcribed Text
    Router->>NLU: Semantic Intent Matching
    alt Online Mode
        Services->>APIs: Query Agmarknet / Weather / News API
        APIs-->>Services: Return Live Data
    else Offline Mode
        Services->>Cache: Query Local Cache / JSON Data
        Cache-->>Services: Return Cached Response
    end
    Services-->>Router: Formulate Spoken Response Text
    Router->>TTS: Convert Text to Speech (gTTS + Pydub)
    TTS-->>WebUI: Stream Audio Playback (.mp3)
    WebUI-->>User: Play Spoken Response & Display Card
```

</div>

### 🔄 Step-by-Step User Journey

<table>
<tr>
<td width="33%" align="center">

### 1️⃣ Speak Command
<br/>

[![Speech Recognition](https://img.shields.io/badge/Voice_Input-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://cloud.google.com/speech-to-text)

<br/>

Click microphone or speak naturally in Hindi / regional dialect

</td>
<td width="33%" align="center">

### 2️⃣ Intent Recognition
<br/>

[![Sentence Transformers](https://img.shields.io/badge/Smart_NLU-FF6F00?style=for-the-badge&logo=huggingface&logoColor=white)](https://www.sbert.net/)

<br/>

Sentence Transformers map colloquial speech to underlying actions

</td>
<td width="33%" align="center">

### 3️⃣ Live API / Cache Retrieval
<br/>

[![API Integration](https://img.shields.io/badge/Live_APIs-00C853?style=for-the-badge&logo=fastapi&logoColor=white)](https://data.gov.in)

<br/>

Fetches Agmarknet prices, OpenWeather reports, or cached JSON

</td>
</tr>
<tr>
<td width="33%" align="center">

### 4️⃣ Context Management
<br/>

[![State Engine](https://img.shields.io/badge/State_Manager-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

<br/>

Remembers conversation history for seamless multi-turn follow-ups

</td>
<td width="33%" align="center">

### 5️⃣ Voice Synthesis
<br/>

[![gTTS & Audio](https://img.shields.io/badge/Audio_Processing-34A853?style=for-the-badge&logo=google&logoColor=white)](https://pypi.org/project/gTTS/)

<br/>

Generates natural speech with volume normalization & speed tuning

</td>
<td width="33%" align="center">

### 6️⃣ Audio Response
<br/>

[![Audio Output](https://img.shields.io/badge/Voice_Output-FF9900?style=for-the-badge&logo=speaker&logoColor=white)](https://www.pygame.org/)

<br/>

Plays audio response clearly while rendering summary cards on screen

</td>
</tr>
</table>

---

## 🏗️ System Architecture

```mermaid
flowchart TB
    subgraph Client["🌐 Client & Interaction Layer"]
        WebUI["Web Interface<br/>(HTML5 / CSS3 / Web Speech API)"]
        CLI["Terminal CLI Interface<br/>(Pygame Audio / SoundDevice)"]
    end
    
    subgraph Core["⚙️ Core Processing & Voice Pipeline"]
        Router["main.py Engine Router"]
        VoiceIO["voice_tool.py<br/>(STT & gTTS Synthesis)"]
        LangMgr["language_manager.py<br/>(Multi-language Support)"]
        NLU["Sentence Transformer & RapidFuzz<br/>Semantic Intent Classifier"]
        OfflineMgr["offline_mode.py & CacheManager"]
    end
    
    subgraph Services["⚡ Domain Service Layer"]
        S_Agri["Agriculture Service<br/>(Crops, Mandi Prices, Subsidies)"]
        S_Weather["Weather Service<br/>(Live Weather & Forecasts)"]
        S_News["News Service<br/>(Category Headlines & Summaries)"]
        S_Scheme["Social Welfare Service<br/>(PM-KISAN, Loans, Pensions)"]
        S_Finance["Finance & Expense Service<br/>(Calculator, Expense Tracker)"]
        S_Emerg["Emergency Assistance<br/>(Helpline Router)"]
        S_GK["Knowledge Service<br/>(Wikipedia & Gemini AI)"]
    end
    
    subgraph Data["💾 Storage & External Integration Layer"]
        Agmarknet["🌾 Agmarknet API"]
        OpenWeather["🌦️ OpenWeatherMap API"]
        GNews["📰 GNews API"]
        Gemini["🧠 Google Gemini AI"]
        LocalData[("📦 Local JSON Data<br/>(30+ Crops, Schemes, Cache)")]
    end
    
    WebUI -->|1. Voice / Text Query| Router
    CLI -->|1. Mic Audio Input| Router
    Router --> VoiceIO
    Router --> LangMgr
    Router --> NLU
    Router --> OfflineMgr
    
    NLU -->|2. Route Intent| Services
    
    S_Agri --> Agmarknet
    S_Agri --> LocalData
    S_Weather --> OpenWeather
    S_News --> GNews
    S_News --> LocalData
    S_Scheme --> LocalData
    S_Finance --> LocalData
    S_Emerg --> LocalData
    S_GK --> Gemini
    
    Services -->|3. Structured Response| Router
    Router -->|4. Speech Output| WebUI
    Router -->|4. Play Audio| CLI
    
    style Client fill:#00d4ff,stroke:#0099cc,stroke-width:3px
    style Core fill:#ff66ff,stroke:#cc44cc,stroke-width:3px
    style Services fill:#ff6b35,stroke:#cc5529,stroke-width:3px
    style Data fill:#00ff88,stroke:#00cc66,stroke-width:3px
```

---

## 🛠️ Technology Stack

<div align="center">

### 🗣️ Speech, Audio & NLU

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SpeechRecognition](https://img.shields.io/badge/SpeechRecognition-3.10-4285F4?style=for-the-badge&logo=google&logoColor=white)
![gTTS](https://img.shields.io/badge/gTTS-2.5-34A853?style=for-the-badge&logo=google&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.5-E10098?style=for-the-badge&logo=python&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Audio_Effects-0078D7?style=for-the-badge&logo=ffmpeg&logoColor=white)
![Sentence Transformers](https://img.shields.io/badge/Sentence_Transformers-NLU-FF6F00?style=for-the-badge&logo=huggingface&logoColor=white)

**Advanced STT, gTTS voice synthesis, Pydub volume/speed enhancement, Pygame playback, and semantic intent matching**

### 🌐 Backend Server & Web Framework

![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![Flask CORS](https://img.shields.io/badge/Flask_CORS-4.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

**Flask web engine serving REST endpoints, Web Speech mic integration, and responsive cards**

### 🔌 APIs & External Integrations

![OpenWeatherMap](https://img.shields.io/badge/OpenWeatherMap-API-EB6E4B?style=for-the-badge&logo=openweathermap&logoColor=white)
![GNews](https://img.shields.io/badge/GNews-API-FF4500?style=for-the-badge&logo=google-news&logoColor=white)
![Agmarknet](https://img.shields.io/badge/Agmarknet-Government_API-00C853?style=for-the-badge&logo=data-dot-gov&logoColor=white)
![Google Gemini AI](https://img.shields.io/badge/Google_Gemini-AI_Knowledge-8E44AD?style=for-the-badge&logo=google-gemini&logoColor=white)
![Wikipedia](https://img.shields.io/badge/Wikipedia-API-000000?style=for-the-badge&logo=wikipedia&logoColor=white)

**Integrated government & commercial REST APIs for real-time weather, market rates, news, and knowledge queries**

### 📦 Storage & Deployment

![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Render](https://img.shields.io/badge/Render-Cloud_Deploy-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-Offline_Cache-000000?style=for-the-badge&logo=json&logoColor=white)

**Offline-first local JSON caching architecture deployable on Render cloud or Docker containers**

</div>

---

## 📂 Project Structure

```
Vaani/
│
├── 📁 vaani/                       # Core Package Source Code
│   ├── 📁 core/                    # System Core & Engine Modules
│   │   ├── 🚀 main.py              # Application entry point & command router loop
│   │   ├── 🔊 voice_tool.py        # SpeechRecognition (STT) & gTTS audio pipeline
│   │   ├── 🧠 context_manager.py   # State management (NewsContext, AgriContext, SchemeContext)
│   │   ├── 🌐 language_manager.py  # Multi-language translation & TTS code resolver
│   │   ├── ⚙️ config.py            # Central triggers (30+ lists), phrases & API keys
│   │   ├── 💾 offline_mode.py      # Offline connectivity checker & local fallback router
│   │   ├── ⚡ cache_manager.py      # Cache invalidation & storage controller
│   │   └── 🔒 api_key_manager.py  # Secure API key encryption & loader
│   │
│   ├── 📁 services/                # Modular Domain Service Layer
│   │   ├── 🌾 agriculture/         # Crop advisories (30+ crops) & Agmarknet market rates
│   │   ├── 🌦️ weather/             # OpenWeatherMap API wrapper & rain advisories
│   │   ├── 📰 news/                # GNews API integration & headline summarizer
│   │   ├── 📋 social/              # Government schemes (PM-KISAN, Ayushman Bharat) & emergency
│   │   ├── 💸 finance/             # Expense tracker, daily calculator & financial literacy
│   │   ├── 🧠 knowledge/           # Wikipedia API & Google Gemini AI fallback
│   │   ├── 📱 communication/       # SMS / USSD messaging integration
│   │   └── 🕒 time/                # Current date, time & history facts
│   │
│   ├── 📁 utils/                   # Shared Helper Utilities
│   └── 🌐 web.py                   # Flask server entry point & web API routes
│
├── 📁 data/                        # Static Data Models & Offline Cache
│   ├── 🌾 crop_data/               # JSON datasets for 30+ crops
│   ├── 📋 scheme_data/             # Government scheme eligibility guidelines
│   ├── 💳 loan_data/               # Microfinance & KCC loan details
│   ├── 💸 subsidy_data/            # Agricultural subsidies documentation
│   └── 💾 offline_cache/           # Cached news, weather, and market responses
│
├── 📁 docs/                        # Project Documentation
│   ├── 🏗️ PROJECT_ARCHITECTURE.md  # Detailed system architecture & flow diagrams
│   ├── 📖 USER_MANUAL.md           # End-user voice command guide
│   ├── 🐛 DEBUGGING_GUIDE.md       # Error tracking & troubleshooting procedures
│   └── 🚀 RENDER_DEPLOYMENT_GUIDE.md# Cloud deployment step-by-step instructions
│
├── 📁 tests/                       # Automated Test Suite (Unittest)
├── ⚡ start_web.ps1                 # Windows web interface launcher script
├── ⚡ start_vaani.ps1               # Windows CLI launcher script
├── 🐳 Dockerfile                   # Docker container build specification
├── ⚙️ render.yaml                  # Render cloud deployment specification
├── 📄 requirements.txt             # Python dependencies specification
├── 📄 setup.py                     # Package installation configuration
├── 📖 README.md                    # Main Project Documentation
└── 📄 LICENSE                      # MIT Open Source License
```

---

## 🗣️ Voice Commands & Service Reference

<div align="center">

| Service | Example Hindi Voice Command | Functionality | Data Source / API |
|:---:|:---|:---|:---|
| 🌾 **Crop Advisory** | `"धान की खेती के बारे में बताओ"` | Comprehensive farming guide, soil & sowing tips | Local JSON (30+ crops) |
| 💰 **Market Prices** | `"आज गेहूं का रेट क्या है"` | Real-time commodity market prices | Agmarknet API |
| 📋 **Govt Schemes** | `"PM Kisan योजना के बारे में बताओ"` | Scheme details, eligibility & application steps | Scheme JSON Datasets |
| 🌦️ **Weather Report** | `"दिल्ली का मौसम कैसा है"` | Temperature, humidity, rain forecast & advice | OpenWeatherMap API |
| 📰 **Voice News** | `"आज की ताज़ा खबरें सुनाओ"` | Top headlines with interactive details | GNews API & Cache |
| 🧮 **Calculator** | `"500 में से 200 घटाओ"` | Hands-free spoken arithmetic calculations | Internal Math Engine |
| 💸 **Expense Tracker**| `"खर्चा जोड़ो 500 रुपये बीज"` | Log expense items and query monthly spend totals | Local Storage / JSON |
| 🚨 **Emergency** | `"एम्बुलेंस नंबर बताओ"` | Immediate helpline routing (100, 102, 1091) | Emergency Directory |
| 🧠 **General Knowledge**| `"भारत की राजधानी क्या है"` | Answer curiosity questions & general facts | Google Gemini AI / Wikipedia |

</div>

---

## 🚀 Setup & Deployment Guide

### Prerequisites

* **Python 3.8+** (Python 3.10+ recommended)
* **Microphone & Speaker** connected to your device
* **FFmpeg** installed (for audio enhancement with Pydub)
* Modern web browser (Google Chrome or Microsoft Edge recommended)

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ankittroy-21/Vaani.git
cd Vaani
```

---

### 2️⃣ Install Dependencies & FFmpeg

**Install Python packages:**
```bash
pip install -r requirements.txt
```

**Install FFmpeg:**
* **Windows (PowerShell):**
  ```powershell
  .\scripts\install_ffmpeg.ps1
  ```
* **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt-get update && sudo apt-get install -y ffmpeg
  ```
* **macOS:**
  ```bash
  brew install ffmpeg
  ```

---

### 3️⃣ Configure API Keys

Create a `.env` file in the root directory:

```env
WEATHER_API_KEY=your_openweathermap_key
GNEWS_API_KEY=your_gnews_key
AGMARKNET_API_KEY=your_agmarknet_key
GEMINI_API_KEY=your_google_gemini_key
```

> **Free API Keys:**
> * OpenWeatherMap: [openweathermap.org](https://openweathermap.org/appid)
> * GNews: [gnews.io](https://gnews.io/)
> * Agmarknet: [data.gov.in](https://data.gov.in)

---

### 4️⃣ Run Vaani Locally

#### Option A: Web Interface (Recommended) 🌐

**Windows (PowerShell Quick Start):**
```powershell
.\start_web.ps1
```

**Manual Start (Any OS):**
```bash
python -m vaani.web
```
Open your browser at **`http://localhost:5000`** 🎉

#### Option B: Terminal CLI Mode 💻

```bash
python -m vaani.core.main
```

---

### 5️⃣ Deploy to Cloud (Render / Docker)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/groupnumber-9/Vaani)

**Deploy with Docker:**
```bash
docker build -t vaani-app .
docker run -p 5000:5000 vaani-app
```

---

## 🔮 Future Enhancements & Roadmap

<div align="center">

```mermaid
timeline
    title Vaani Development Roadmap
    section Phase 1 (Completed)
        Q4 2025 : Core NLU & Voice Engine
               : Agmarknet & Weather Integration
               : Web Interface & Offline Cache
    section Phase 2 (Current)
        Q1 2026 : Multi-language Support (Marathi, Bengali)
               : Render Cloud Deployment & Keep-Alive
               : Advanced Financial Expense Logging
    section Phase 3 (Upcoming)
        Q2 2026 : AI Crop Disease Detection from Photos
               : Native Android App with Offline Voice
               : SMS / USSD Integration for Feature Phones
    section Phase 4 (Future)
        Q3-Q4 2026 : IoT Sensor Integration for Soil Moisture
               : Voice Community Forum for Farmers
               : Expansion to 10+ Regional Dialects
```

</div>

### 🎯 Planned Features Checklist

- [x] Natural Hindi Voice STT & gTTS Audio Pipeline
- [x] Agmarknet Live Mandi Prices & 30+ Crop Datasets
- [x] Offline Mode Cache for Essential Schemes & News
- [ ] 📱 **Native Android Application** - Offline voice processing on low-cost smartphones
- [ ] 🤖 **AI Crop Disease Scanner** - Instant leaf diagnosis using computer vision
- [ ] 📲 **USSD & Interactive Voice Response (IVR)** - Access via basic feature phones without internet
- [ ] 🗣️ **Extended Regional Language Support** - Full support for Punjabi, Gujarati, Telugu, and Kannada

---

## 💡 Key Concepts & Use Cases

<table>
<tr>
<td width="50%">

### 🌾 For Farmers & Rural Citizens
- ✅ Speak naturally in Hindi to check crop market prices before selling
- ✅ Learn step-by-step disease control methods for 30+ crops
- ✅ Check eligibility for PM-KISAN, crop insurance, and solar pumps
- ✅ Get urgent weather advisories to plan harvesting & spraying

</td>
<td width="50%">

### 🎓 For Developers & Civic Tech Researchers
- ✅ Reference implementation of low-literacy voice interface design
- ✅ Offline-first architecture combining live APIs with local JSON cache
- ✅ Hybrid NLU combining Sentence Transformers with fuzzy matching
- ✅ Aligned with UN Sustainable Development Goals (SDG 1 & SDG 8)

</td>
</tr>
</table>

---

## 👥 Contributors

<div align="center">

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/tech4commun">
        <img src="https://github.com/tech4commun.png" width="100px;" alt="Arpit Verma"/><br />
        <sub><b>Arpit Verma</b></sub>
      </a><br />
      <a href="https://github.com/tech4commun">GitHub</a> •
      <a href="https://www.linkedin.com/in/arpit-verma-98010129a/">LinkedIn</a>
    </td>
    <td align="center">
      <a href="https://github.com/ankittroy-21">
        <img src="https://github.com/ankittroy-21.png" width="100px;" alt="Ankit Roy"/><br />
        <sub><b>Ankit Roy</b></sub>
      </a><br />
      <a href="https://github.com/ankittroy-21">GitHub</a> •
      <a href="https://www.linkedin.com/in/ankittroy-21">LinkedIn</a>
    </td>
    <td align="center">
      <a href="https://github.com/anurag-joshi-1403">
        <img src="https://github.com/anurag-joshi-1403.png" width="100px;" alt="Anurag Joshi"/><br />
        <sub><b>Anurag Joshi</b></sub>
      </a><br />
      <a href="https://github.com/anurag-joshi-1403">GitHub</a> •
      <a href="https://www.linkedin.com/in/anurag-joshi-1403">LinkedIn</a>
    </td>
  </tr>
</table>

**College Minor Project | UN SDG Aligned (No Poverty & Decent Work)**

</div>

---

## 📄 License & Support

<div align="center">

This project is open-source under the **MIT License** — see the [LICENSE](LICENSE) file for details.

### 🌟 Show Your Support

If you find **Vaani** impactful or inspiring, please consider leaving a ⭐ on GitHub!

[![GitHub stars](https://img.shields.io/github/stars/ankittroy-21/Vaani?style=social)](https://github.com/ankittroy-21/Vaani/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ankittroy-21/Vaani?style=social)](https://github.com/ankittroy-21/Vaani/network/members)
[![GitHub issues](https://img.shields.io/github/issues/ankittroy-21/Vaani?style=social)](https://github.com/ankittroy-21/Vaani/issues)

---

### 💬 Vaani: If You Can Speak, You Deserve Equal Access to Information & Opportunities!

**© 2026 Vaani Team | Built with ❤️ for Digital Inclusion**

</div>
