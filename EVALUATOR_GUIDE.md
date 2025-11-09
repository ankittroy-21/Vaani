# 🚀 Vaani - Quick Start for Evaluators
## 5-Minute Setup & Demo Guide

**Project:** Voice Assistant for Indian Farmers  
**Type:** University Minor Project  
**Setup Time:** 5 minutes  
**Demo Time:** 3 minutes

---

## ⚡ Fastest Way to Run (3 steps)

### Windows (PowerShell):

```powershell
# Step 1: Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Start web interface
python -m vaani.web
```

**Then open:** http://localhost:5000 in your browser

---

### Linux/macOS:

```bash
# Step 1: Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Start web interface
python -m vaani.web
```

**Then open:** http://localhost:5000 in your browser

---

## 🎯 Quick Demo Queries

Once the web interface is open, try these:

### 1. Simple Greeting
**Type:** `नमस्ते`  
**Expected:** Welcome message in Hindi

### 2. Agricultural Advice
**Type:** `टमाटर के पत्ते पीले हो रहे हैं`  
**Expected:** Disease diagnosis and treatment advice

### 3. Government Scheme
**Type:** `PM Kisan के बारे में बताओ`  
**Expected:** Scheme details, eligibility, benefits

### 4. Weather Query
**Type:** `आज का मौसम कैसा है?`  
**Expected:** Current weather information

### 5. Simple Calculation
**Type:** `250 गुणा 180`  
**Expected:** 45000

### 6. Emergency
**Type:** `emergency`  
**Expected:** Emergency helpline numbers

---

## 🎤 Testing Voice Input

1. **Click the orange microphone button** (🎤)
2. **Allow microphone permission** when prompted
3. **Wait for "Listening..." message**
4. **Speak clearly:** "आज का मौसम कैसा है?"
5. **See transcription and response**
6. **Click "Play Audio"** to hear the response

---

## 📁 Project Structure (Quick Overview)

```
Vaani-2/
├── vaani/
│   ├── web.py              ← Flask web server
│   ├── core/
│   │   └── main.py         ← CLI version
│   └── services/           ← All backend services
├── web/
│   ├── templates/          ← HTML files
│   └── static/             ← CSS, JS
├── data/
│   ├── crop_data/          ← 30+ crop JSON files
│   ├── scheme_data/        ← Government schemes
│   └── offline_cache/      ← Offline data
├── start_web.ps1           ← Quick launcher
└── requirements.txt        ← Dependencies
```

---

## 🔍 Key Features to Evaluate

### 1. User Interface ⭐⭐⭐⭐⭐
- Clean, intuitive design
- Mobile-responsive
- Accessibility (voice + text)
- Feature cards for easy discovery

### 2. Voice Input/Output ⭐⭐⭐⭐
- Browser-based voice recognition
- Text-to-speech responses
- Hindi + English support
- Fallback to text input

### 3. Agricultural Knowledge ⭐⭐⭐⭐⭐
- 30+ crops documented
- Pest/disease management
- Planting guidance
- Local JSON database

### 4. Government Schemes ⭐⭐⭐⭐
- 10+ schemes covered
- Eligibility information
- Application process
- Benefit calculator

### 5. Offline Capability ⭐⭐⭐⭐
- Works without internet
- Local caching
- 70% features available
- Automatic fallback

### 6. Multi-language ⭐⭐⭐⭐
- Hindi (primary)
- English
- Hinglish (mixed)
- Easy language switching

---

## 📊 Technical Evaluation Points

### Architecture (20 points)
- ✅ Clean MVC separation
- ✅ Modular service design
- ✅ RESTful API structure
- ✅ Caching system
- ✅ Offline-first approach

### Code Quality (20 points)
- ✅ Python best practices
- ✅ Proper error handling
- ✅ Documentation (docstrings)
- ✅ Configuration management
- ✅ Security (no hardcoded keys)

### Functionality (30 points)
- ✅ Core features working
- ✅ Voice I/O functional
- ✅ Multiple services integrated
- ✅ Offline mode operational
- ✅ Error handling graceful

### Innovation (15 points)
- ✅ Voice-first design
- ✅ Illiterate-friendly
- ✅ Domain-specific (agriculture)
- ✅ Social impact focus
- ✅ Offline capability

### Documentation (15 points)
- ✅ README comprehensive
- ✅ User manual included
- ✅ API documentation
- ✅ Demo script provided
- ✅ Architecture docs

---

## 🎬 Alternative: Watch Demo Video

If you prefer to see it in action first:
1. Check `demo_video_link.txt` in submission
2. Watch 3-5 minute recorded demo
3. Then try live version

---

## 🐛 Troubleshooting

### Port Already in Use
```powershell
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or use different port
$env:FLASK_RUN_PORT=5001
python -m vaani.web
```

### Missing Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Voice Not Working
- Use text input instead
- Check browser permissions
- Try Chrome/Edge (best support)

### API Keys Warning
- Not required for demo
- Most features work without keys
- See `.env.example` if needed

---

## 📝 Evaluation Checklist

### Functionality Test (5 min)
- [ ] Web interface loads
- [ ] Text input works
- [ ] Voice input works (if mic available)
- [ ] Audio output works
- [ ] Agriculture query successful
- [ ] Scheme query successful
- [ ] Calculator works
- [ ] Offline mode detected

### Code Review (10 min)
- [ ] Check `vaani/web.py` structure
- [ ] Review `web/templates/index.html`
- [ ] Look at `vaani/core/main.py`
- [ ] Examine service modules
- [ ] Check data files structure

### Documentation Review (5 min)
- [ ] README clarity
- [ ] USER_MANUAL completeness
- [ ] DEMO_SCRIPT usefulness
- [ ] Architecture docs
- [ ] Code comments

### Innovation & Impact (5 min)
- [ ] Problem statement clarity
- [ ] Solution appropriateness
- [ ] Target user focus
- [ ] Social impact potential
- [ ] SDG alignment

---

## 🌟 Standout Features

What makes this project special:

1. **Voice-First Design**
   - Built for illiterate users
   - Natural language processing
   - No typing required

2. **Offline-First Architecture**
   - Works in low-connectivity areas
   - Local data caching
   - Automatic fallback

3. **Domain-Specific Knowledge**
   - 30+ crops documented
   - Government schemes database
   - Agricultural focus

4. **Complete Solution**
   - Web interface + CLI
   - Documentation
   - Demo materials
   - Deployment ready

5. **Social Impact**
   - Addresses real problem
   - Target: 146M+ farmers
   - SDG Goal 1 alignment
   - Accessibility focus

---

## 📧 Contact & Support

**Project Repository:** https://github.com/ankittroy-21/Vaani

**Documentation:**
- Technical: `PROJECT_ARCHITECTURE.md`
- User Guide: `USER_MANUAL.md`
- Demo: `DEMO_SCRIPT.md`
- Submission: `SUBMISSION_CHECKLIST.md`

**For Questions:**
See documentation or contact project team

---

## ⏱️ Time-Saving Tips

### For Quick Evaluation (10 minutes):
1. Run web interface (3 min)
2. Try 3 demo queries (3 min)
3. Review README (2 min)
4. Check code structure (2 min)

### For Thorough Evaluation (30 minutes):
1. Setup and run (5 min)
2. Test all features (10 min)
3. Review code quality (10 min)
4. Read documentation (5 min)

### For Presentation Attendance (7 minutes):
1. Watch live demo (3 min)
2. See slide deck (3 min)
3. Q&A (1 min)

---

## 🎯 Expected Outcomes

After testing Vaani, you should see:

✅ **A working voice assistant**
✅ **Clean, professional UI**
✅ **Accurate responses to agricultural queries**
✅ **Government scheme information**
✅ **Voice input and output functioning**
✅ **Offline capability demonstrated**
✅ **Comprehensive documentation**
✅ **Well-structured codebase**
✅ **Social impact focus**
✅ **Professional presentation materials**

---

## 🏆 Evaluation Summary Template

```
Project: Vaani - Voice Assistant for Farmers
Student: [Name]
Date: [Date]

SCORES:
- Architecture: ___/20
- Code Quality: ___/20  
- Functionality: ___/30
- Innovation: ___/15
- Documentation: ___/15
Total: ___/100

COMMENTS:
[Strengths]
[Areas for Improvement]
[Overall Impression]

GRADE: ___
```

---

## 🚀 Ready to Evaluate!

**Start here:**
```powershell
.\start_web.ps1
```

**Then open:** http://localhost:5000

**Try query:** "नमस्ते"

**That's it!** You're now experiencing Vaani.

---

**Thank you for evaluating this project! 🙏**

*Bridging the digital divide, one voice at a time.* 🌾
