# 🌟 Gemini API Integration Guide for Vaani

## Overview
Vaani now includes **General Knowledge Service** powered by Google's Gemini AI! This feature enables Vaani to answer curious questions that children might ask their parents, making it a friendly educational companion.

## 🎯 What Can It Do?

### Types of Questions Answered
- **Science & Nature**: "आसमान नीला क्यों होता है?", "बारिश कैसे होती है?"
- **Animals & Birds**: "शेर क्यों दहाड़ता है?", "चिड़िया कैसे उड़ती है?"
- **Space & Planets**: "चाँद पर क्या होता है?", "तारे क्यों चमकते हैं?"
- **Body & Health**: "हमें भूख क्यों लगती है?", "हम क्यों सोते हैं?"
- **Technology**: "कंप्यूटर कैसे काम करता है?", "मोबाइल में आवाज कैसे आती है?"
- **General Curiosity**: Any "क्यों", "कैसे", "क्या", "कौन", "कहाँ", "कब" questions

### Example Conversations

**Child**: "पापा, बताओ आसमान नीला क्यों होता है?"
**Vaani**: "बेटा, आसमान नीला इसलिए दिखता है क्योंकि सूरज की रोशनी जब हवा से टकराती है, तो नीला रंग सबसे ज्यादा फैलता है। जैसे पानी में रंग मिलाने पर फैल जाता है, वैसे ही नीला रंग पूरे आसमान में फैल जाता है!"

**Child**: "मम्मी, बारिश कैसे होती है?"
**Vaani**: "बेटा, जब धूप से पानी भाप बनकर ऊपर जाता है और बादल बनता है। फिर जब बादल बहुत भारी हो जाता है, तो वह पानी की बूंदों के रूप में नीचे गिरता है। यही बारिश है!"

## 🚀 Setup Instructions

### Step 1: Get Gemini API Key

1. Visit: [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Copy the generated API key

### Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install the `google-generativeai` package along with other dependencies.

### Step 3: Add API Key to Vaani

#### Method 1: Automatic Setup (First Run)
When you run Vaani for the first time, it will ask for all API keys including Gemini:

```powershell
python main.py
```

You'll see:
```
--- API Key Setup ---
...
--------------------------------------------------
 Gemini API Key (Optional - for general knowledge questions)
 Get it from: https://makersuite.google.com/app/apikey
 Enter your Gemini API Key (or press Enter to skip):
--------------------------------------------------
```

#### Method 2: Manual Setup
Create or edit the `.env` file in your project folder:

```env
WEATHER_API_KEY="your_weather_key"
GNEWS_API_KEY="your_news_key"
AGMARKNET_API_KEY="your_agmarknet_key"
GEMINI_API_KEY="your_gemini_key_here"
```

### Step 4: Test the Integration

Run the test script to verify everything is working:

```powershell
python general_knowledge_service.py
```

You should see:
```
✅ Gemini API is configured!

Testing with sample questions:

Q: आसमान नीला क्यों होता है?
A: [Gemini's child-friendly answer in Hindi]
...
```

## 📝 How It Works

### Architecture

```
User Voice Command
       ↓
Speech Recognition (listen_command)
       ↓
Command Processing (main.py)
       ↓
Is it a General Knowledge Question?
  ├── Yes → general_knowledge_service.py
  │         ↓
  │    Gemini API (gemini-pro model)
  │         ↓
  │    Child-friendly Hindi Response
  │         ↓
  └── No → Other Services (Weather, News, etc.)
       ↓
Text-to-Speech (bolo)
       ↓
Voice Output to User
```

### Question Detection Logic

The system identifies general knowledge questions by checking for:

1. **Question Words**: क्यों, कैसे, क्या, कौन, कहाँ, कब, etc.
2. **Curiosity Topics**: आसमान, चाँद, बारिश, जानवर, etc.
3. **Question Markers**: ?, ।, "बताओ", "समझाओ", etc.
4. **Parental Address**: "पापा बताओ", "मम्मी बताओ", etc.

### Response Customization

The Gemini prompt is designed to:
- Use simple, easy Hindi (suitable for children aged 5-12)
- Keep answers concise (3-5 sentences)
- Use everyday examples for explanation
- Maintain a positive and encouraging tone
- Include fun facts when possible

## 🎨 Customization

### Modify Response Style

Edit `general_knowledge_service.py` to change the prompt:

```python
prompt = f"""
तुम एक प्यार करने वाले माता-पिता की तरह जवाब दो।
...
[Customize this section]
"""
```

### Add More Question Triggers

Edit `Config.py` to add more trigger words:

```python
general_knowledge_triggers = [
    # Add your custom triggers here
    "मुझे सिखाओ",
    "ये कैसे होता है",
    # ... more triggers
]
```

### Add More Topics

```python
child_curiosity_topics = [
    # Add topics that children ask about
    "robot", "volcano", "ocean",
    # ... more topics
]
```

## 🔧 Troubleshooting

### Issue: "Gemini API is not configured"
**Solution**: Make sure `GEMINI_API_KEY` is properly set in your `.env` file.

### Issue: "Error in Gemini API call"
**Possible causes**:
1. Invalid API key - Get a new one from Google AI Studio
2. API quota exceeded - Check your usage at [Google AI Studio](https://makersuite.google.com/)
3. Network connectivity issues - Check your internet connection

### Issue: Responses are in English instead of Hindi
**Solution**: The prompt is designed for Hindi, but if you get English responses:
1. Make sure your question is in Hindi
2. Check if the Gemini model supports Hindi (gemini-pro does)
3. Modify the prompt to be more explicit about Hindi output

### Issue: Answers are too complex for children
**Solution**: Edit the prompt in `general_knowledge_service.py` to request simpler language:
```python
prompt = f"""
बहुत ही सरल शब्दों में समझाओ, जैसे 5 साल के बच्चे को समझाओगे।
...
"""
```

## 📊 Usage Statistics

### API Limits
- **Free Tier**: 60 requests per minute
- **Paid Tier**: Higher limits available

Check your usage at: [Google AI Studio Console](https://makersuite.google.com/)

### Best Practices
1. Use the free tier for development and testing
2. Monitor your API usage regularly
3. Implement caching for frequently asked questions (future enhancement)
4. Consider rate limiting for production use

## 🌐 Integration Flow in main.py

```python
# Priority 11: General Knowledge Questions (before unrecognized)
elif (any(trigger in command_lower for trigger in Config.general_knowledge_triggers) or 
      any(topic in command_lower for topic in Config.child_curiosity_topics) or
      '?' in command or '।' in command):
    # Try to handle as general knowledge question
    if not handle_general_knowledge_query(command, bolo):
        # If not handled, fall through to unrecognized
        print("मैं यह समझ नहीं पाई, कृपया फिर से कहें।")
        bolo("मैं यह समझ नहीं पाई, कृपया फिर से कहें।")
        log_unprocessed_query_remote(original_command)
```

## 🎓 Educational Benefits

### For Children
- Encourages curiosity and learning
- Gets answers in their native language (Hindi)
- Builds confidence to ask questions
- Makes learning fun and interactive

### For Parents
- Helps answer difficult questions
- Provides scientifically accurate information
- Saves time researching answers
- Supports children's education

## 🔐 Security & Privacy

### API Key Security
- Never share your API key publicly
- Keep `.env` file in `.gitignore`
- Regenerate key if compromised

### Data Privacy
- Questions are sent to Google's Gemini API
- Google's privacy policy applies
- No personal data is required
- Conversation history is not stored by Vaani

## 📚 Example Questions List

### Science
- आसमान नीला क्यों होता है?
- बारिश कैसे होती है?
- इंद्रधनुश कैसे बनता है?
- बिजली क्यों कड़कती है?
- धरती गोल क्यों है?

### Nature
- पेड़ कैसे बढ़ते हैं?
- फूल रंगीन क्यों होते हैं?
- पत्ते हरे क्यों होते हैं?
- समुद्र में नमक कैसे आया?

### Animals
- शेर जंगल का राजा क्यों है?
- चिड़िया कैसे उड़ती है?
- मछली पानी में कैसे रहती है?
- हाथी इतना बड़ा क्यों होता है?

### Space
- चाँद क्यों चमकता है?
- तारे क्यों टिमटिमाते हैं?
- सूरज गर्म क्यों है?
- अंतरिक्ष में क्या होता है?

### Body
- हमें भूख क्यों लगती है?
- हम क्यों सोते हैं?
- खून लाल क्यों होता है?
- हम कैसे बोलते हैं?

### Technology
- कंप्यूटर कैसे काम करता है?
- मोबाइल में आवाज कैसे आती है?
- बिजली कैसे बनती है?
- टीवी में तस्वीर कैसे आती है?

## 🚀 Future Enhancements

### Planned Features
1. **Response Caching**: Store common questions to reduce API calls
2. **Age-Appropriate Responses**: Adjust complexity based on age
3. **Follow-up Questions**: Handle "और क्यों?", "फिर क्या?"
4. **Visual Explanations**: Generate diagrams for complex topics
5. **Quiz Mode**: Test knowledge with fun questions
6. **Multilingual Support**: English, other Indian languages

### Contributing
Want to improve the General Knowledge feature?
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📞 Support

### Getting Help
- Check the troubleshooting section above
- Review the code comments in `general_knowledge_service.py`
- Test with the provided test script
- Check Google's Gemini API documentation

### Useful Links
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google AI Studio](https://makersuite.google.com/)
- [Python SDK Documentation](https://github.com/google/generative-ai-python)

## 📄 License

This integration uses Google's Gemini API which has its own terms of service. Please review:
- [Google's Terms of Service](https://policies.google.com/terms)
- [Gemini API Terms](https://ai.google.dev/terms)

---

**Made with ❤️ for curious children and supportive parents!**

Happy Learning! 🎓✨
