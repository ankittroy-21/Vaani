# 🔐 Vaani Privacy Policy & Data Usage
## Commitment to User Privacy

**Last Updated:** November 2025

---

## Overview

Vaani is designed with **privacy-first** principles to protect farmers and rural users who may not be familiar with digital privacy concepts. We believe in transparency and user control over their data.

---

## Data Collection

### What We Collect

**Voice Data:**
- ❌ **NOT STORED** - Voice inputs are processed in real-time
- ❌ **NOT RECORDED** - No audio files are saved
- ✅ **PROCESSED LOCALLY** - Voice-to-text happens on your device or through Google's Speech API
- ✅ **IMMEDIATELY DISCARDED** - After conversion to text, audio data is deleted

**Text Queries:**
- ✅ Temporarily stored in memory during session
- ❌ Not saved to permanent database
- ❌ Not shared with third parties
- ✅ Used only to generate responses

**Usage Statistics:**
- ✅ Anonymous usage counts (number of queries)
- ✅ Error logs (to improve service quality)
- ❌ No personal identification
- ❌ No query content stored

### What We DON'T Collect

- ❌ Personal name or identity
- ❌ Phone numbers
- ❌ Location data (except when explicitly provided for weather queries)
- ❌ Financial information
- ❌ Aadhaar or government IDs
- ❌ Banking details
- ❌ Farm ownership details
- ❌ Photos or images
- ❌ Contacts or call logs

---

## How Your Data is Used

### Primary Uses

1. **Query Processing:**
   - To understand your question
   - To generate relevant responses
   - To provide spoken answers

2. **Service Improvement:**
   - Anonymous error logs
   - Performance monitoring
   - Feature usage statistics

3. **Offline Caching:**
   - Frequently accessed data cached locally
   - Enables offline functionality
   - All data stored on YOUR device

### Data Retention

| Data Type | Retention Period | Storage Location |
|-----------|------------------|------------------|
| Voice Input | 0 seconds (immediate) | Not stored |
| Text Query | Session only | Memory (RAM) |
| Response | Session only | Memory (RAM) |
| Cache Data | Until cleared | Your device |
| Error Logs | 30 days | Local logs folder |

---

## Third-Party Services

Vaani uses external APIs for enhanced functionality. Here's what data they receive:

### Google Speech Recognition API
- **Receives:** Voice audio (for transcription)
- **Purpose:** Convert speech to text
- **Retention:** Per Google's policy (typically not stored)
- **Privacy Policy:** https://policies.google.com/privacy

### Google Text-to-Speech (gTTS)
- **Receives:** Text to be spoken
- **Purpose:** Generate audio responses
- **Retention:** Not stored
- **Privacy Policy:** https://policies.google.com/privacy

### OpenWeatherMap API
- **Receives:** City/location name (if provided)
- **Purpose:** Weather forecasts
- **Retention:** Per their policy
- **Privacy Policy:** https://openweathermap.org/privacy-policy

### GNews API
- **Receives:** News query keywords
- **Purpose:** News headlines
- **Retention:** Logs may be kept per their policy
- **Privacy Policy:** https://gnews.io/privacy

### Agmarknet API (Data.gov.in)
- **Receives:** Commodity name, market name
- **Purpose:** Market price information
- **Retention:** Government servers
- **Privacy Policy:** https://data.gov.in/privacy-policy

### Google Generative AI (Gemini)
- **Receives:** Query text for general knowledge
- **Purpose:** Generate informative responses
- **Retention:** Per Google's policy
- **Privacy Policy:** https://policies.google.com/privacy

**Note:** These services are called ONLY when you use their specific features. Offline mode avoids all external API calls.

---

## Data Security

### Protection Measures

**Local Processing:**
- Most processing happens on your device
- No central database of user queries
- Offline mode eliminates internet exposure

**Secure Communication:**
- HTTPS used for all API calls (when online)
- Encrypted data transmission
- No unencrypted storage of sensitive data

**No User Accounts:**
- No login required
- No passwords to steal
- No account hacking risk
- Anonymous usage

**Open Source:**
- Code is publicly available
- Security audits possible
- Transparent implementation

---

## Your Data Rights

### You Have the Right To:

1. **Access:**
   - No personal data is stored, so nothing to access

2. **Deletion:**
   - Clear browser cache to remove local data
   - Close session to clear temporary data

3. **Portability:**
   - Export offline cache if needed
   - Copy data files from your device

4. **Opt-Out:**
   - Use offline mode to avoid external APIs
   - Text input to avoid speech recognition
   - Local data remains local

### How to Exercise Your Rights

**Clear Local Data:**
```
1. Close Vaani
2. Clear browser cache
3. Delete cache/ and logs/ folders
```

**Use Offline Mode:**
```
1. Disconnect internet
2. Use cached features only
3. No external API calls made
```

---

## Children's Privacy

Vaani may be used by children (under 18) for educational purposes, such as learning about agriculture or general knowledge.

**For Children:**
- ❌ No personal information collected
- ❌ No registration required
- ✅ Safe, educational content
- ✅ Parental supervision recommended

---

## Data Sharing

### We Do NOT Share:

- ❌ Your queries with advertisers
- ❌ Voice recordings with anyone
- ❌ Personal information with third parties
- ❌ Usage data with commercial entities

### Limited Sharing:

- ✅ Anonymous error reports (for debugging)
- ✅ Aggregate statistics (e.g., "100 users asked about weather")
- ✅ No personally identifiable information included

---

## Cookies & Tracking

**Cookies Used:**
- ✅ Session ID (to maintain conversation context)
- ✅ Language preference
- ❌ No advertising cookies
- ❌ No third-party tracking cookies

**Analytics:**
- ❌ No Google Analytics
- ❌ No Facebook Pixel
- ❌ No user tracking scripts

---

## Government & Legal Disclosure

**We Will Disclose Data Only If:**
- Legally required by Indian law
- Court order or subpoena
- National security requirements

**What Can Be Disclosed:**
- Error logs (if they exist)
- Anonymous usage statistics
- No personal data (because we don't collect it)

---

## Offline Mode Privacy

When using Vaani in **offline mode**:

✅ **Maximum Privacy:**
- No internet connection
- No external API calls
- All processing on your device
- No data leaves your computer

✅ **Available Features:**
- Crop advice (from local database)
- Scheme information (local data)
- Calculations
- Cached news

❌ **Not Available:**
- Live weather updates
- Current news headlines
- Wikipedia searches
- Market prices

**To Enable Offline Mode:**
Simply disconnect your internet. Vaani will automatically switch to offline mode.

---

## Data Sources & Attribution

### Information Sources:

**Agricultural Data:**
- Government of India agricultural databases
- ICAR (Indian Council of Agricultural Research)
- State agriculture departments
- Publicly available farming guides

**Scheme Information:**
- Official government scheme websites
- Ministry of Agriculture
- Ministry of Finance (MUDRA)
- Publicly available documentation

**Weather Data:**
- OpenWeatherMap API

**News:**
- GNews API (aggregated from public sources)

**Market Prices:**
- Agmarknet (Government of India)

All data sources are **publicly available** and used in compliance with their terms of service.

---

## Contact & Questions

### Privacy Concerns:

If you have questions about privacy:
- Email: [Your Contact Email]
- GitHub Issues: [Repository URL]/issues
- Review code: [Repository URL]

### Report Security Issues:

Found a security vulnerability?
- Email: [Security Contact Email]
- Responsible disclosure appreciated
- Will be addressed promptly

---

## Changes to This Policy

**Updates:**
- We may update this policy as Vaani evolves
- Material changes will be communicated
- Check this file for latest version
- Date of last update shown at top

**Notification:**
- Major changes: In-app message
- Minor changes: Documentation update
- Always transparent about data practices

---

## Compliance

### Indian Laws:

Vaani complies with:
- ✅ Information Technology Act, 2000
- ✅ IT (Reasonable Security Practices) Rules, 2011
- ✅ Digital Personal Data Protection Act, 2023 (when enacted)

### International Standards:

Inspired by:
- ✅ GDPR principles (EU)
- ✅ Privacy by design
- ✅ Data minimization
- ✅ User control

---

## Summary (Simple Version)

**In Plain Language:**

1. **Your voice is NOT recorded** - It's used once and thrown away
2. **Your questions are NOT saved** - They're forgotten after you get an answer
3. **No one is watching you** - No tracking, no spying
4. **Your data stays with you** - Offline mode = complete privacy
5. **We use some internet services** - Only when you ask for weather, news, etc.
6. **You're anonymous** - No login, no account, no identity needed

**Think of Vaani like talking to a helpful neighbor:**
- They remember the conversation while you're talking
- They forget it once you leave
- They don't tell others what you asked
- They help you without writing down your secrets

---

## Educational Use Notice

This privacy policy is part of an educational minor project for university submission. In a production deployment:

- Additional safeguards would be implemented
- Professional security audit would be conducted
- Dedicated privacy officer would be appointed
- Regular compliance reviews would be performed
- User consent mechanisms would be formalized

---

**Your privacy matters to us. Ask questions. Stay informed. Stay safe.** 🔐

---

*For technical details about data flow and architecture, see PROJECT_ARCHITECTURE.md*
