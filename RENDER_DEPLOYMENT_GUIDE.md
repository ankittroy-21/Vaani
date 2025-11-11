# 🚀 Deploying Vaani to Render

This guide will help you deploy the Vaani voice assistant to Render's free tier with automatic keep-alive functionality.

## 📋 Prerequisites

1. **GitHub Account** - Your code should be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com) (free)
3. **API Keys** - Get your API keys ready:
   - OpenWeatherMap API Key
   - GNews API Key
   - Agmarknet API Key (optional)
   - Gemini API Key (optional)

## 🎯 Features Included

- ✅ **Keep-Alive Functionality** - Automatic ping every 14 minutes to prevent spin-down
- ✅ **Production-Ready Configuration** - Optimized for Render free tier
- ✅ **Environment Variable Management** - Secure API key handling
- ✅ **Health Check Endpoint** - Automatic health monitoring
- ✅ **Auto-Deploy** - Automatically deploys when you push to GitHub

## 📝 Step-by-Step Deployment

### Step 1: Prepare Your GitHub Repository

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Verify these files exist in your repo:**
   - ✅ `render.yaml` - Render configuration
   - ✅ `requirements.txt` - Python dependencies
   - ✅ `runtime.txt` - Python version
   - ✅ `Procfile` - Start command
   - ✅ `Dockerfile` - Container configuration (optional)

### Step 2: Create a Web Service on Render

1. **Go to Render Dashboard:**
   - Visit [https://dashboard.render.com](https://dashboard.render.com)
   - Click "New +" button
   - Select "Web Service"

2. **Connect Your Repository:**
   - Click "Connect GitHub" (first time only)
   - Select your Vaani repository
   - Click "Connect"

3. **Configure Your Service:**
   
   **Basic Settings:**
   - **Name:** `vaani-web` (or your preferred name)
   - **Region:** Choose closest to your users (e.g., Oregon, Frankfurt)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   
   **Build & Deploy:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -m vaani.web`
   
   **Instance Type:**
   - Select **Free** plan

4. **Set Environment Variables:**
   
   Click "Advanced" and add these environment variables:
   
   | Key | Value | Description |
   |-----|-------|-------------|
   | `PYTHON_VERSION` | `3.10.0` | Python version |
   | `PORT` | `5000` | Port number (auto-set by Render) |
   | `WEATHER_API_KEY` | `your_key_here` | OpenWeatherMap API |
   | `GNEWS_API_KEY` | `your_key_here` | GNews API |
   | `AGMARKNET_API_KEY` | `your_key_here` | Agmarknet API (optional) |
   | `GEMINI_API_KEY` | `your_key_here` | Google Gemini API (optional) |
   | `KEEP_ALIVE_ENABLED` | `true` | Enable keep-alive (default: true) |
   | `DEBUG` | `false` | Production mode |

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (2-5 minutes)
   - Your app will be live at `https://your-app-name.onrender.com`

### Step 3: Verify Deployment

1. **Check Health Endpoint:**
   ```
   https://your-app-name.onrender.com/api/health
   ```
   Should return: `{"status": "ok", "service": "Vaani Web UI"}`

2. **Visit Your App:**
   ```
   https://your-app-name.onrender.com
   ```

3. **Check Logs:**
   - Go to Render Dashboard
   - Click on your service
   - Click "Logs" tab
   - Look for "Keep-Alive Service Starting..." message

## 🔄 Keep-Alive Feature Explained

### How It Works

The keep-alive mechanism prevents your Render free tier service from spinning down after 15 minutes of inactivity:

1. **Background Thread:** Starts automatically when deployed on Render
2. **Ping Interval:** Every 14 minutes (just under the 15-minute timeout)
3. **Self-Ping:** Sends HTTP GET request to `/api/health` endpoint
4. **Automatic:** No manual intervention needed

### Configuration

The keep-alive feature is configured in `vaani/web.py`:

```python
KEEP_ALIVE_INTERVAL = 14 * 60  # 14 minutes
KEEP_ALIVE_ENABLED = True  # Enable by default
```

### Monitoring Keep-Alive

Check your Render logs to see keep-alive messages:

```
[Keep-Alive] Pinging service at 2025-11-11 10:00:00
[Keep-Alive] ✅ Ping successful - Service is alive
```

### Disable Keep-Alive (if needed)

Set environment variable in Render:
```
KEEP_ALIVE_ENABLED=false
```

## 🌐 Using Your Deployed App

### Web Interface
Visit: `https://your-app-name.onrender.com`

### API Endpoints

**Health Check:**
```
GET https://your-app-name.onrender.com/api/health
```

**Text Query:**
```
POST https://your-app-name.onrender.com/api/query
Content-Type: application/json

{
  "query": "आज का मौसम बताओ",
  "session_id": "user123"
}
```

**Status:**
```
GET https://your-app-name.onrender.com/api/status
```

## 🔧 Advanced Configuration

### Using Blueprint (render.yaml)

If you want to use Infrastructure as Code, Render will automatically detect `render.yaml`:

```yaml
services:
  - type: web
    name: vaani-web
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python -m vaani.web
```

### Custom Domain

1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain
4. Configure DNS records as shown

### Scaling (Paid Plans)

For production with high traffic:
1. Upgrade to paid plan
2. Increase instance count
3. Add Redis for session storage
4. Enable auto-scaling

## 🐛 Troubleshooting

### Deployment Fails

**Issue:** Build fails
```
Error: Could not find a version that satisfies the requirement...
```

**Solution:** Check `requirements.txt` versions:
```bash
pip freeze > requirements.txt
```

### Keep-Alive Not Working

**Issue:** Service still spins down
```
[Keep-Alive] ❌ Ping failed: Connection refused
```

**Solutions:**
1. Check `RENDER_EXTERNAL_URL` is set (Render sets this automatically)
2. Verify `/api/health` endpoint is accessible
3. Check logs for errors
4. Ensure `KEEP_ALIVE_ENABLED=true`

### Audio Files Not Playing

**Issue:** Audio files fail to load
```
404 Not Found - Audio file not found
```

**Solutions:**
1. Check disk space (free tier has limits)
2. Enable audio cleanup: Set `max_files=20` in config
3. Use shorter text responses

### High Memory Usage

**Issue:** Service runs out of memory (512MB limit on free tier)

**Solutions:**
1. Reduce cache size
2. Limit concurrent users
3. Disable audio for long responses
4. Upgrade to paid plan

### Environment Variables Not Working

**Issue:** API keys not recognized
```
Error: WEATHER_API_KEY not found
```

**Solutions:**
1. Re-enter environment variables in Render dashboard
2. Restart the service
3. Check for typos in variable names
4. Ensure no quotes around values

## 📊 Monitoring & Logs

### View Logs

1. Go to Render Dashboard
2. Select your service
3. Click "Logs" tab
4. Use search to filter logs

### Common Log Messages

**Successful startup:**
```
🌾 Vaani Web Interface Starting...
🔄 Keep-Alive Service Starting...
🌐 Starting server on 0.0.0.0:5000
```

**Keep-alive working:**
```
[Keep-Alive] ✅ Ping successful - Service is alive
```

**Audio cleanup:**
```
[Audio Cleanup]: ✅ Deleted 5 files, freed 250.5 KB
```

## 💰 Free Tier Limitations

Render free tier includes:
- ✅ 750 hours/month (enough for 24/7 with keep-alive)
- ✅ 512 MB RAM
- ✅ Custom domains with SSL
- ✅ Auto-deploy from GitHub
- ⚠️ Spins down after 15 min inactivity (keep-alive prevents this)
- ⚠️ Limited build minutes
- ⚠️ Shared CPU

**Keep-alive ensures your service stays active within free tier limits!**

## 🚀 Optimization Tips

### Reduce Build Time
```yaml
buildCommand: pip install --no-cache-dir -r requirements.txt
```

### Reduce Memory Usage
```python
# In vaani/web.py
cleanup_old_audio_files(max_age_minutes=15, max_files=20)
```

### Speed Up Response Time
- Enable caching
- Use CDN for static files
- Optimize database queries

## 🔐 Security Best Practices

1. **Never commit API keys** to GitHub
2. **Use environment variables** for secrets
3. **Enable HTTPS** (automatic on Render)
4. **Validate user input** to prevent injection attacks
5. **Rate limit** API endpoints
6. **Keep dependencies updated**

## 📱 Mobile Access

Your deployed app works on mobile browsers:
- Responsive design
- Touch-friendly interface
- Works on all devices

## 🔄 Continuous Deployment

Every push to your main branch automatically deploys:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Render automatically deploys!
```

## 📞 Getting Help

- **Render Documentation:** [https://render.com/docs](https://render.com/docs)
- **Render Community:** [https://community.render.com](https://community.render.com)
- **Vaani Issues:** [GitHub Issues](https://github.com/groupnumber-9/Vaani/issues)

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `render.yaml` configured
- [ ] `requirements.txt` up to date
- [ ] Web service created on Render
- [ ] Environment variables set
- [ ] Deployment successful
- [ ] Health check passing
- [ ] Keep-alive logs visible
- [ ] Web interface accessible
- [ ] API endpoints working
- [ ] Audio playback functional

## 🎉 Success!

Your Vaani voice assistant is now live on Render with automatic keep-alive! 

**Next Steps:**
1. Share your URL: `https://your-app-name.onrender.com`
2. Monitor logs for any issues
3. Test all features
4. Gather user feedback
5. Iterate and improve

---

**Made with ❤️ for India's Digital Inclusion**

*Questions? Check the [main README](README.md) or [open an issue](https://github.com/groupnumber-9/Vaani/issues)*
