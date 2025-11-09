# 📖 Vaani User Manual
## Complete Guide to Using the Voice Assistant

---

## Table of Contents
1. [Getting Started](#getting-started)
2. [Web Interface Guide](#web-interface-guide)
3. [Voice Commands](#voice-commands)
4. [Features Guide](#features-guide)
5. [Tips and Tricks](#tips-and-tricks)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### What is Vaani?
Vaani (वाणी - meaning "voice" in Hindi) is a voice-first digital assistant designed for Indian farmers and rural populations. It helps you get information about farming, government schemes, weather, news, and more - all through simple voice or text commands in Hindi or English.

### Who Can Use Vaani?
- 🌾 Farmers needing agricultural advice
- 👴 Elderly users with limited literacy
- 📱 Anyone in rural areas seeking information
- 🎓 Students learning about agriculture
- 🏛️ Users wanting to know about government schemes

### What You Need
- 💻 A computer or smartphone with internet browser
- 🌐 Internet connection (some features work offline)
- 🎤 Microphone (optional, for voice input)
- 🔊 Speakers or headphones (to hear responses)

---

## Web Interface Guide

### Opening Vaani Web Interface

**On Windows:**
1. Open PowerShell in the Vaani folder
2. Run: `.\start_web.ps1`
3. Wait for "Starting Vaani Web Server..." message
4. Open browser and go to: `http://localhost:5000`

**On Linux/Mac:**
1. Open Terminal in the Vaani folder
2. Run: `python -m vaani.web`
3. Open browser and go to: `http://localhost:5000`

### Understanding the Interface

```
┌─────────────────────────────────────────┐
│  🌾 Vaani - किसान सहायक                │  ← Header
│  🌐 Online    🗣️ हिंदी                 │  ← Status
├─────────────────────────────────────────┤
│                                         │
│  [Conversation appears here]            │  ← Chat Area
│                                         │
│                                         │
├─────────────────────────────────────────┤
│  [🌤️ मौसम] [💰 योजनाएं] [🌾 फसल]    │  ← Quick Actions
├─────────────────────────────────────────┤
│  🎤  [Type your question here...]  ➤   │  ← Input Area
└─────────────────────────────────────────┘
```

### Using the Interface

#### Method 1: Text Input (Typing)
1. Click in the text box at the bottom
2. Type your question in Hindi or English
3. Press Enter or click the ➤ button
4. Wait for Vaani's response
5. Click 🔊 Play Audio to hear the response

#### Method 2: Voice Input (Speaking)
1. Click the 🎤 microphone button
2. Wait for "Listening..." indicator
3. Speak your question clearly
4. The text will appear automatically
5. Vaani will respond with text and audio

#### Method 3: Quick Actions
1. Click any quick action button (e.g., 🌤️ मौसम)
2. Vaani will process the query automatically
3. See the response in the chat area

---

## Voice Commands

### Basic Commands

#### Greetings
```
Hindi:
- नमस्ते
- हेलो वाणी
- सुप्रभात

English:
- Hello
- Hi Vaani
- Good morning
```

#### Getting Help
```
Hindi:
- मदद चाहिए
- आप क्या कर सकते हो?
- आपकी सुविधाएं क्या हैं?

English:
- Help
- What can you do?
- Show features
```

#### Exiting
```
Hindi:
- बंद करो
- अलविदा
- धन्यवाद

English:
- Goodbye
- Exit
- Thank you
```

---

## Features Guide

### 🌾 Agricultural Advisory

#### Crop Information
**Ask about specific crops:**
```
Hindi:
- टमाटर की खेती कैसे करें?
- गेहूं के लिए कौन सी मिट्टी अच्छी है?
- धान की बुवाई कब करें?

English:
- How to grow tomatoes?
- Which soil is good for wheat?
- When to sow paddy?
```

**Example Response:**
```
टमाटर की खेती के लिए:
1. मिट्टी: बलुई दोमट मिट्टी सबसे उपयुक्त
2. बुवाई का समय: जुलाई-अगस्त
3. तापमान: 20-25°C
4. सिंचाई: नियमित, हर 7-10 दिन
```

#### Disease Management
**Ask about plant diseases:**
```
Hindi:
- टमाटर के पत्ते पीले हो रहे हैं
- गेहूं में सफेद धब्बे दिख रहे हैं
- आलू की फसल में कीड़े लग गए

English:
- Tomato leaves turning yellow
- White spots on wheat
- Potato crop has pests
```

**Example Response:**
```
टमाटर के पत्ते पीले होने के कारण:
1. पोषक तत्वों की कमी (नाइट्रोजन)
2. पानी की अधिकता या कमी
3. पत्ती मोड़क वायरस

उपाय:
- नाइट्रोजन युक्त खाद डालें
- ड्रिप सिंचाई अपनाएं
- रोग प्रतिरोधी किस्में लगाएं
```

#### Fertilizer Recommendations
```
Hindi:
- आलू के लिए कौन सी खाद डालें?
- गेहूं में यूरिया कब डालें?
- जैविक खाद के बारे में बताओ

English:
- Which fertilizer for potato?
- When to apply urea in wheat?
- Tell me about organic fertilizer
```

### 💰 Government Schemes

#### PM-KISAN Scheme
```
Hindi:
- PM Kisan के बारे में बताओ
- किसान सम्मान निधि योजना क्या है?
- PM Kisan में कैसे आवेदन करें?

English:
- Tell me about PM Kisan
- What is PM Kisan scheme?
- How to apply for PM Kisan?
```

**Example Response:**
```
PM-KISAN (प्रधानमंत्री किसान सम्मान निधि):

लाभ: ₹6000 प्रति वर्ष (3 किश्तों में)
पात्रता:
- 2 हेक्टेयर तक जमीन वाले किसान
- भारतीय नागरिक
- खेती योग्य भूमि

आवेदन:
1. pmkisan.gov.in पर जाएं
2. "Farmer Corner" में क्लिक करें
3. आधार नंबर दर्ज करें
4. बैंक विवरण जोड़ें
```

#### Other Schemes
```
- PM Fasal Bima Yojana (फसल बीमा)
- Kisan Credit Card (किसान क्रेडिट कार्ड)
- Ayushman Bharat (आयुष्मान भारत)
- PM KUSUM (सोलर पंप योजना)
```

### 🌤️ Weather Information

#### Current Weather
```
Hindi:
- आज का मौसम कैसा है?
- दिल्ली में मौसम कैसा है?
- अभी तापमान कितना है?

English:
- How is the weather today?
- Weather in Delhi?
- What's the temperature?
```

#### Rain Forecast
```
Hindi:
- कल बारिश होगी क्या?
- इस हफ्ते बारिश होगी?
- कब बारिश आएगी?

English:
- Will it rain tomorrow?
- Rain forecast for this week?
- When will it rain?
```

**Example Response:**
```
दिल्ली का मौसम:
🌡️ तापमान: 28°C
💧 नमी: 65%
🌬️ हवा: 15 km/h
🌤️ स्थिति: आंशिक बादल

बारिश की संभावना: कल शाम 60%
सलाह: छिड़काव कार्य टालें
```

### 📰 News Service

#### Latest News
```
Hindi:
- आज की खबरें सुनाओ
- ताजा समाचार बताओ
- खेती की खबरें

English:
- Tell me today's news
- Latest headlines
- Agricultural news
```

**How it works:**
1. Vaani shows top 5 headlines
2. Say a number (1-5) to hear full article
3. Example: "पहली खबर सुनाओ" or "Number 1"

#### News Categories
```
- Sports news (खेल समाचार)
- Business news (व्यापार समाचार)
- Political news (राजनीति समाचार)
```

### 💸 Financial Services

#### Simple Calculator
```
Hindi:
- 250 गुणा 180
- 5000 में से 1500 घटाओ
- 100 जोड़ 50

English:
- Multiply 250 by 180
- Subtract 1500 from 5000
- Add 100 and 50
```

**Supported Operations:**
- Addition (जोड़, add, plus)
- Subtraction (घटाना, subtract, minus)
- Multiplication (गुणा, multiply, times)
- Division (भाग, divide)

#### Expense Tracking
```
Hindi:
- खर्च जोड़ो 500 रुपये बीज के लिए
- आज का खर्च बताओ
- इस महीने का कुल खर्च

English:
- Add expense 500 for seeds
- Show today's expenses
- Total expenses this month
```

#### Loan Information
```
Hindi:
- किसान क्रेडिट कार्ड के बारे में बताओ
- KCC loan कैसे मिलेगा?
- मुद्रा लोन क्या है?

English:
- Tell me about Kisan Credit Card
- How to get KCC loan?
- What is Mudra loan?
```

### 🚨 Emergency Services

#### Quick Emergency Access
```
Hindi:
- आपातकाल
- इमरजेंसी
- मदद चाहिए

English:
- Emergency
- Help needed
- Urgent
```

**Response includes:**
- Police: 100
- Ambulance: 102
- Fire: 101
- Women Helpline: 1091
- Farmer Helpline: 1800-180-1551

### 🕒 Time & Date

```
Hindi:
- समय बताओ
- आज कौन सा दिन है?
- आज की तारीख

English:
- What time is it?
- What day is today?
- Today's date
```

### 🌍 General Knowledge

```
Hindi:
- भारत की राजधानी क्या है?
- सूर्य क्या है?
- गाय के बारे में बताओ

English:
- What is the capital of India?
- Tell me about the Sun
- Information about cows
```

---

## Tips and Tricks

### 💡 Best Practices

1. **Speak Clearly**
   - Speak at normal pace
   - Avoid background noise
   - Use simple sentences

2. **Use Natural Language**
   - No need for formal language
   - Colloquial Hindi works fine
   - Mix Hindi and English if comfortable

3. **Be Specific**
   - Good: "टमाटर के पत्ते पीले हो रहे हैं"
   - Better: "मेरे टमाटर के पौधे के पत्ते पीले हो रहे हैं और मुड़ रहे हैं"

4. **Use Keywords**
   - Include crop name: "गेहूं", "धान", "आलू"
   - Include action: "खेती", "बुवाई", "बीमारी"
   - Include scheme name: "PM Kisan", "KCC"

### 🎯 Quick Actions for Common Tasks

**Morning Routine:**
```
1. "आज का मौसम कैसा है?"
2. "आज की खबरें सुनाओ"
3. "आज कोई योजना की नई जानकारी?"
```

**Farm Planning:**
```
1. "कल बारिश होगी क्या?"
2. "[फसल का नाम] के लिए आज कौन सा काम करें?"
3. "बाजार में [फसल] का भाव क्या है?"
```

**Financial Management:**
```
1. "खर्च जोड़ो [राशि] [कारण]"
2. "इस महीने का कुल खर्च"
3. "पिछले हफ्ते का हिसाब"
```

### 📱 Offline Mode

**What works offline:**
✅ Crop information (30+ crops)
✅ Government schemes (10+ schemes)
✅ Loan information
✅ Emergency numbers
✅ Calculator
✅ Cached news (last fetched)

**What needs internet:**
❌ Live weather forecast
❌ Latest news
❌ Wikipedia search
❌ Market prices (real-time)

**Tip:** Use Vaani online once a day to cache latest information, then use offline throughout the day.

---

## Troubleshooting

### Common Issues

#### 1. Microphone Not Working

**Problem:** Voice button doesn't respond or doesn't hear me

**Solutions:**
- Check if microphone is connected
- Allow microphone permission in browser
  - Chrome: Click 🔒 in address bar → Site settings → Allow microphone
  - Firefox: Click 🔒 → Allow microphone
- Try refreshing the page
- Use text input as fallback

#### 2. Audio Not Playing

**Problem:** Can't hear Vaani's responses

**Solutions:**
- Check system volume
- Check browser audio settings
- Click the 🔊 Play Audio button manually
- Check if headphones/speakers are connected

#### 3. Server Not Starting

**Problem:** `start_web.ps1` shows errors

**Solutions:**
```powershell
# Reinstall dependencies
pip install -r requirements.txt

# Try manual start
python -m vaani.web

# Check Python version (need 3.8+)
python --version
```

#### 4. Slow Responses

**Problem:** Vaani takes too long to respond

**Solutions:**
- Check internet connection
- First query might be slow (loading models)
- Use offline mode for basic queries
- Close other browser tabs

#### 5. Hindi Not Working

**Problem:** Hindi text appears as boxes or garbled

**Solutions:**
- Install Hindi language pack on Windows:
  - Settings → Time & Language → Language → Add Hindi
- Use Chrome or Firefox (better Hindi support)
- Update browser to latest version

#### 6. Wrong Information

**Problem:** Vaani gives incorrect or outdated information

**Solutions:**
- Provide feedback (note the query)
- Rephrase your question
- Try being more specific
- Check government websites for latest scheme details

---

## Keyboard Shortcuts

- **Enter** - Send message (when typing)
- **Ctrl + /** - Focus on input box
- **Esc** - Stop audio playback

---

## Language Support

### Supported Languages
- 🇮🇳 Hindi (हिंदी) - Primary
- 🇬🇧 English
- 🔀 Hinglish (Hindi + English mix)

### Switching Languages
```
"English में बदलो" - Switch to English
"Hindi में बदलो" - Switch to Hindi
```

### Language Examples

**Hindi:**
```
"टमाटर की खेती कैसे करें?"
"मौसम कैसा है?"
"PM Kisan के बारे में बताओ"
```

**English:**
```
"How to grow tomatoes?"
"What's the weather like?"
"Tell me about PM Kisan"
```

**Hinglish:**
```
"Tomato ki खेती कैसे करें?"
"Weather कैसा है?"
"PM Kisan scheme के बारे में बताओ"
```

---

## Safety and Privacy

### Your Data is Safe
- ✅ No personal data stored
- ✅ Voice processed in real-time
- ✅ No tracking or profiling
- ✅ Local data storage only
- ✅ Secure API connections

### What We Store Locally
- Expense records (if you use expense tracker)
- Cached responses (for offline mode)
- Language preference
- No voice recordings

---

## Getting Help

### Need More Help?

📧 **Email:** [your-email@example.com]  
🐛 **Report Issues:** [GitHub Issues Link]  
📚 **Documentation:** See README.md  
💬 **Community:** [Discord/Forum Link if any]

### Feedback

We want to improve! Please share:
- Features you'd like to see
- Issues you encountered
- Success stories
- Suggestions for improvement

---

## Credits

**Developed by:** [Your Team Name]  
**University:** [Your University]  
**Project Guide:** [Guide Name]  
**Year:** 2025

**Built with:**
- Python, Flask
- Google APIs
- OpenWeatherMap
- GNews

**Aligned with:** UN Sustainable Development Goal 1 (No Poverty)

---

## Version Information

**Current Version:** 1.0.0  
**Last Updated:** November 2025  
**Supported Crops:** 30+  
**Supported Schemes:** 10+  
**Languages:** 3 (Hindi, English, Hinglish)

---

**धन्यवाद! Thank you for using Vaani! 🌾**
