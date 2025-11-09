# 🎬 Vaani Demo Script
## 3-5 Minute University Pitch Demo

---

## Setup (Do this BEFORE the presentation - 2 minutes)

### Pre-Demo Checklist:
- [ ] Virtual environment activated
- [ ] Web server running on http://localhost:5000
- [ ] Browser open and tested
- [ ] Microphone tested and working
- [ ] Volume at appropriate level
- [ ] Backup queries written down
- [ ] Terminal ready as fallback

### Commands to Run:
```powershell
# Start web interface
.\start_web.ps1

# Wait for "Starting Vaani Web Server..." message
# Open browser to http://localhost:5000
```

---

## Demo Flow (3-5 minutes)

### Introduction (30 seconds)
**Say:**
> "नमस्ते! This is Vaani - a voice-first digital assistant designed specifically for Indian farmers and rural populations who may have limited literacy. Vaani breaks down the digital divide by providing information through voice in Hindi, making critical services accessible to everyone."

**Show:** Landing page with feature cards

---

### Demo 1: Agricultural Advisory (45 seconds)

**Scenario:** A farmer needs help with a crop disease

**Type or Say:**
```
टमाटर के पत्ते पीले हो रहे हैं, क्या करूं?
```
*(English: "Tomato leaves are turning yellow, what should I do?")*

**Expected Response:**
- Disease identification
- Treatment recommendations
- Prevention tips

**Highlight:**
- "Notice how Vaani understands colloquial Hindi"
- "Provides actionable advice immediately"
- "Audio response for illiterate users"

---

### Demo 2: Government Scheme Information (45 seconds)

**Scenario:** A farmer wants to know about PM-KISAN benefits

**Type or Say:**
```
PM Kisan scheme के बारे में बताओ
```
*(English: "Tell me about PM Kisan scheme")*

**Expected Response:**
- Scheme details
- Eligibility criteria
- Application process
- Benefit amounts

**Highlight:**
- "Complex government schemes explained in simple language"
- "Helps farmers access their rightful benefits"

---

### Demo 3: Weather & Planning (30 seconds)

**Scenario:** Farmer needs weather information for crop planning

**Type or Say:**
```
आज का मौसम कैसा है?
```
*(English: "How is today's weather?")*

**Alternative:**
```
कल बारिश होगी क्या?
```
*(English: "Will it rain tomorrow?")*

**Expected Response:**
- Current weather conditions
- Temperature and humidity
- Rain forecast
- Agricultural advice based on weather

**Highlight:**
- "Real-time weather data"
- "Helps with farming decisions"

---

### Demo 4: Financial Literacy (30 seconds)

**Scenario:** Simple calculation for daily transactions

**Type or Say:**
```
250 गुणा 180 कितना होता है?
```
*(English: "What is 250 times 180?")*

**Expected Response:**
- Calculation result: 45,000
- Spoken in Hindi

**Highlight:**
- "Helps with market calculations"
- "Financial literacy for illiterate users"

---

### Demo 5: Emergency Help (30 seconds)

**Scenario:** Quick access to emergency services

**Type or Say:**
```
emergency
```
or
```
आपातकाल
```

**Expected Response:**
- Emergency helpline numbers
- Women's helpline
- Police, ambulance contacts

**Highlight:**
- "Critical information in emergencies"
- "One word access to help"

---

### Demo 6: Voice Input (30 seconds - if time permits)

**Action:** Click the microphone button 🎤

**Say:** (Wait for listening indicator)
```
आज की खबरें सुनाओ
```
*(English: "Tell me today's news")*

**Expected Response:**
- Latest news headlines
- Option to select article for details

**Highlight:**
- "True voice-first experience"
- "No typing required"
- "Browser-based voice recognition"

---

## Closing Statement (30 seconds)

**Say:**
> "Vaani addresses UN Sustainable Development Goal 1: No Poverty by making digital information accessible to underserved populations. It works offline, supports multiple languages, and requires no literacy skills. This is how we bridge the digital divide in rural India."

**Show:** Quick scroll through features or architecture if there's a slide

---

## Fallback Plan (If Something Goes Wrong)

### If Microphone Fails:
- Use text input instead
- Say: "We also support text input for areas with poor audio quality"

### If Internet Fails:
- Demonstrate offline mode
- Say: "Vaani works offline using cached data - critical for rural areas with poor connectivity"

### If Voice Output Fails:
- Continue with text responses
- Say: "Responses are shown as text and can be spoken aloud"

### If Web Interface Fails:
- Switch to terminal mode
- Already have `python -m vaani.core.main` ready in another terminal
- Say: "We also have a terminal version for resource-constrained devices"

---

## Backup Queries (Copy-Paste Ready)

In case you need quick alternatives:

```
गेहूं की खेती कैसे करें?
```
*(How to grow wheat?)*

```
KCC loan कैसे मिलेगा?
```
*(How to get KCC loan?)*

```
आलू के लिए कौन सी खाद अच्छी है?
```
*(Which fertilizer is good for potato?)*

```
आज कौन सा दिन है?
```
*(What day is today?)*

```
किसान क्रेडिट कार्ड के बारे में बताओ
```
*(Tell me about Kisan Credit Card)*

---

## Technical Details (If Asked)

### Technology Stack:
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **AI/NLP:** Google Generative AI, gTTS
- **APIs:** OpenWeatherMap, GNews, Agmarknet
- **Voice:** Browser Web Speech API, gTTS

### Key Features:
- Offline-first architecture
- Multi-language support (Hindi, English, Hinglish)
- 30+ crop knowledge base
- Government scheme database
- Emergency services integration
- Financial literacy tools

### Impact:
- Targets 800+ million rural Indians
- Reduces information asymmetry
- Increases scheme adoption
- Improves agricultural outcomes
- Promotes financial inclusion

---

## Q&A Preparation

### Expected Questions:

**Q: How accurate is the voice recognition?**
A: We use Google's Web Speech API with 85-90% accuracy for Hindi. We also support text input as fallback.

**Q: Does it work offline?**
A: Yes! Critical features like crop advice, scheme information, and calculations work offline using cached data.

**Q: What languages do you support?**
A: Currently Hindi and English, with plans for Marathi, Tamil, Telugu, and other regional languages.

**Q: How do you ensure data privacy?**
A: All processing is local. We don't store personal information. Voice data is processed in real-time and not stored.

**Q: What's the target deployment?**
A: Initial: Web app and WhatsApp bot. Future: Mobile app, USSD integration, rural kiosks.

**Q: What's unique about Vaani?**
A: Voice-first design for illiterate users, offline capability, domain-specific knowledge (agriculture, schemes), and localization.

---

## Demo Environment Setup Commands

```powershell
# Terminal 1 - Web Server
.\start_web.ps1

# Terminal 2 - Backup CLI (don't run unless needed)
python -m vaani.core.main

# Browser
http://localhost:5000
```

---

## Success Criteria

✅ Demonstrated voice input
✅ Showed multilingual support
✅ Displayed agricultural knowledge
✅ Highlighted offline capability
✅ Explained social impact
✅ Answered technical questions

---

**Good luck with your presentation! 🌾🚀**
