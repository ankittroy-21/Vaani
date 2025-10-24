# 🔧 FFmpeg Installation Guide - Windows

## Quick Fix

FFmpeg is required for the professional voice enhancement feature. Here are multiple ways to install it:

---

## ✅ Option 1: Using Chocolatey (Easiest - Recommended)

### Step 1: Install Chocolatey (if not already installed)

Run PowerShell **as Administrator** and execute:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### Step 2: Install FFmpeg

```powershell
choco install ffmpeg -y
```

### Step 3: Verify Installation

```powershell
# Close and reopen PowerShell, then:
ffmpeg -version
```

If you see version information, you're all set! ✅

---

## ✅ Option 2: Manual Installation (Windows)

### Step 1: Download FFmpeg

1. Go to: https://www.gyan.dev/ffmpeg/builds/
2. Download: **ffmpeg-release-essentials.zip**
3. Extract to: `C:\ffmpeg`

### Step 2: Add to PATH

**PowerShell (as Administrator):**
```powershell
$env:Path += ";C:\ffmpeg\bin"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [System.EnvironmentVariableTarget]::Machine)
```

**Or manually:**
1. Right-click "This PC" → Properties
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "System variables", find "Path"
5. Click "Edit" → "New"
6. Add: `C:\ffmpeg\bin`
7. Click OK on all dialogs

### Step 3: Verify

```powershell
# Close and reopen PowerShell
ffmpeg -version
```

---

## ✅ Option 3: Using Scoop (Alternative Package Manager)

### Step 1: Install Scoop

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

### Step 2: Install FFmpeg

```powershell
scoop install ffmpeg
```

### Step 3: Verify

```powershell
ffmpeg -version
```

---

## ✅ Option 4: Use Vaani Without Voice Enhancement

If you don't want to install FFmpeg, Vaani will **automatically fall back** to the original voice:

```python
# The system will detect FFmpeg is not available and use original voice
# No action needed - it works automatically!
```

**Status**: ✅ Vaani still works, just without the professional voice enhancement

---

## 🧪 After Installation - Test Voice

Once FFmpeg is installed:

```powershell
# Test the professional voice
python test_voice.py

# Or run Vaani
python main.py
```

You should now hear the **professional female news anchor voice**! 🎤

---

## 🐛 Troubleshooting

### Issue: "FFmpeg not found" after installation

**Solution 1: Restart PowerShell**
```powershell
# Close PowerShell completely and open a new window
ffmpeg -version
```

**Solution 2: Check PATH manually**
```powershell
$env:Path -split ';' | Select-String "ffmpeg"
```

Should show: `C:\ffmpeg\bin` or similar

**Solution 3: Add to PATH again**
```powershell
# Run as Administrator
$env:Path += ";C:\ffmpeg\bin"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [System.EnvironmentVariableTarget]::Machine)
```

### Issue: "Access Denied" when adding to PATH

**Solution**: Run PowerShell **as Administrator**
- Right-click PowerShell
- Select "Run as administrator"
- Try the PATH command again

### Issue: Still not working

**Solution**: Use Vaani without voice enhancement
- Vaani automatically falls back to original voice
- All features still work perfectly
- Just without the pitch modification

---

## 📊 What You Get With/Without FFmpeg

| Feature | With FFmpeg | Without FFmpeg |
|---------|-------------|----------------|
| Voice Assistant | ✅ Works | ✅ Works |
| All Features | ✅ Works | ✅ Works |
| Audio Playback | ✅ Fast | ✅ Fast |
| Voice Type | 👩 Female News Anchor | 🤖 Original gTTS |
| Performance | ⚡ Fast | ⚡ Fast |

**Bottom Line**: Vaani works great either way! FFmpeg just adds the professional voice enhancement. 🎤

---

## 🎯 Quick Decision Guide

### Install FFmpeg if you want:
- ✅ Professional female news anchor voice
- ✅ Palki Sharma inspired delivery
- ✅ Enhanced audio quality

### Skip FFmpeg if:
- ⏩ You want quick setup (5 minutes vs 30 seconds)
- ⏩ You're okay with the original gTTS voice
- ⏩ You have installation/permission issues

**Both options work perfectly!** 🎉

---

## 💡 Pro Tip

After installing FFmpeg, run:
```powershell
python test_voice.py
```

This will:
1. Check if FFmpeg is properly installed ✅
2. Play sample with professional voice 🎤
3. Compare with original voice 🔊
4. Show you the difference! 🌟

---

## 📞 Quick Commands Summary

```powershell
# Option 1: Chocolatey (easiest)
choco install ffmpeg -y

# Option 2: Scoop (alternative)
scoop install ffmpeg

# Verify
ffmpeg -version

# Test
python test_voice.py

# Run Vaani
python main.py
```

---

## ✅ Installation Status Check

Run this to check your status:

```powershell
python -c "from Voice_tool import FFMPEG_AVAILABLE, PYDUB_AVAILABLE; print(f'PyDub: {PYDUB_AVAILABLE}, FFmpeg: {FFMPEG_AVAILABLE}, Voice Enhancement: {PYDUB_AVAILABLE and FFMPEG_AVAILABLE}')"
```

**Expected Output:**
- `PyDub: True, FFmpeg: True, Voice Enhancement: True` ✅ Perfect!
- `PyDub: True, FFmpeg: False, Voice Enhancement: False` ⚠️ Need FFmpeg
- `PyDub: False, FFmpeg: False, Voice Enhancement: False` ⚠️ Need pydub + FFmpeg

---

**Last Updated**: October 20, 2025  
**Status**: Fallback mechanism ✅  
**Vaani Works**: With or without FFmpeg! 🎉
