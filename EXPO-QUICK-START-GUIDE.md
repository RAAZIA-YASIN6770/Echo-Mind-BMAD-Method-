# 📱 Expo Quick-Start Guide: Run EchoMind on Your Phone!

**Date:** January 30, 2026  
**Status:** Ready to Launch! 🚀

---

## 🎯 What You'll Need

### On Your Laptop:
- ✅ Node.js installed (v16 or higher)
- ✅ Python 3.8+ installed
- ✅ Backend code (already in `backend/` folder)
- ✅ Frontend code (already in `frontend/` folder)

### On Your Phone:
- ✅ **Expo Go** app (free download)
  - **iOS:** [Download from App Store](https://apps.apple.com/app/expo-go/id982107779)
  - **Android:** [Download from Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)

### Network Requirement:
- ✅ **Both laptop and phone must be on the SAME Wi-Fi network**

---

## 🚀 Step-by-Step Setup

### Step 1: Install Expo CLI (One-Time Setup)

Open PowerShell on your laptop and run:

```powershell
npm install -g expo-cli
```

This installs the Expo command-line tool globally.

---

### Step 2: Set Up the Frontend Project

Navigate to the frontend directory:

```powershell
cd "c:\Users\Raazia Yasin\Documents\echobmad\frontend"
```

Initialize the Expo project (if not already done):

```powershell
# If package.json doesn't exist, initialize:
npx create-expo-app@latest . --template blank

# Install required dependencies
npm install @react-navigation/native @react-navigation/stack
npm install react-native-screens react-native-safe-area-context
npm install react-native-gesture-handler react-native-reanimated
npm install axios
```

---

### Step 3: Find Your Laptop's IP Address

You need your laptop's local IP address so your phone can connect to the backend.

**On Windows (PowerShell):**

```powershell
ipconfig
```

Look for **"Wireless LAN adapter Wi-Fi"** section and find the **IPv4 Address**.

**Example output:**
```
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.1.105
```

**Write down this IP address!** You'll need it in the next step.

**Common IP formats:**
- `192.168.1.xxx`
- `192.168.0.xxx`
- `10.0.0.xxx`

---

### Step 4: Configure the API Service

The `frontend/services/api.js` file (created in this sprint) already has a smart IP detection system.

**Option A: Automatic Detection (Recommended)**

The API service will automatically try to detect your laptop's IP. Just make sure both devices are on the same Wi-Fi.

**Option B: Manual Configuration**

If automatic detection doesn't work, edit `frontend/services/api.js`:

```javascript
// Replace this line:
const BACKEND_IP = getLocalIPAddress();

// With your actual IP:
const BACKEND_IP = '192.168.1.105'; // Use YOUR IP from Step 3
```

---

### Step 5: Start the Backend Server

Open a **NEW PowerShell window** and run:

```powershell
cd "c:\Users\Raazia Yasin\Documents\echobmad\backend"

# Start the Flask API server
python app.py
```

**You should see:**
```
🚀 Starting EchoMind AI API Server...
📡 API will be available at http://localhost:5000
 * Running on http://0.0.0.0:5000
```

**✅ Keep this window open!** The backend must stay running.

---

### Step 6: Start the Expo Development Server

Open **ANOTHER PowerShell window** and run:

```powershell
cd "c:\Users\Raazia Yasin\Documents\echobmad\frontend"

# Start Expo
npx expo start
```

**You should see:**
```
› Metro waiting on exp://192.168.1.105:8081
› Scan the QR code above with Expo Go (Android) or the Camera app (iOS)
```

**A QR code will appear in the terminal!**

**✅ Keep this window open too!**

---

### Step 7: Connect Your Phone

#### **For Android:**

1. Open **Expo Go** app on your phone
2. Tap **"Scan QR Code"**
3. Point your camera at the QR code in the PowerShell terminal
4. Wait for the app to load (15-30 seconds)

#### **For iOS:**

1. Open the **Camera** app (not Expo Go)
2. Point at the QR code
3. Tap the notification that appears
4. It will open in Expo Go automatically
5. Wait for the app to load

---

### Step 8: Test the Connection

Once the app loads on your phone:

1. You should see the **EchoMind Dashboard** 🌳
2. Tap **"Start Learning"** to open the chat
3. Type a message like: **"What is 5 + 5?"**
4. The AI should respond with a Socratic question!

**If you see the AI response, congratulations! 🎉 Everything is connected!**

---

## 🔧 Troubleshooting

### Problem 1: "Unable to connect to backend"

**Solution:**
1. Check that both devices are on the **same Wi-Fi**
2. Verify your laptop's IP address hasn't changed (run `ipconfig` again)
3. Make sure the backend server is running (check the PowerShell window)
4. Try manually setting the IP in `frontend/services/api.js`
5. Check Windows Firewall - it might be blocking port 5000

**To allow port 5000 through Windows Firewall:**
```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "EchoMind Backend" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

---

### Problem 2: "QR Code won't scan"

**Solution:**
1. Make sure you're using the correct app:
   - **Android:** Expo Go app
   - **iOS:** Camera app (not Expo Go)
2. Try typing the URL manually in Expo Go:
   - Open Expo Go
   - Tap "Enter URL manually"
   - Type: `exp://192.168.1.105:8081` (use YOUR IP)

---

### Problem 3: "App loads but shows blank screen"

**Solution:**
1. Check the Expo terminal for errors
2. Shake your phone to open the Expo menu
3. Tap "Reload"
4. Check that `App.js` exists in the frontend folder

---

### Problem 4: "Backend returns 404 errors"

**Solution:**
1. Make sure you're running `python app.py` (not `python main.py`)
2. Check that `backend/api/onboarding.py` exists
3. Verify the API endpoints in the browser:
   - Open: `http://localhost:5000/`
   - You should see API information

---

## 📱 Using the App

### First Time Setup:

1. **Onboarding Screen** (if implemented):
   - Enter name: "Zoya"
   - Enter age: 10
   - Enter grade: 5
   - Tap "Start Learning"

2. **Dashboard Screen**:
   - View your Mystery Seed 💎
   - See your Knowledge Tree 🌳
   - Tap "Start Learning" to chat

3. **Chat Screen**:
   - Ask questions
   - Get Socratic responses
   - Watch for PII protection shield 🛡️
   - Tap "💭 I need help" for Confidence Ladder

---

## 🎨 Development Tips

### Hot Reload:
- **Save any file** in the `frontend/` folder
- The app will **automatically reload** on your phone!
- No need to restart Expo

### Debugging:
- **Shake your phone** to open the Expo developer menu
- Options:
  - **Reload** - Refresh the app
  - **Debug Remote JS** - Open Chrome debugger
  - **Show Performance Monitor** - See FPS
  - **Toggle Element Inspector** - Inspect UI elements

### Console Logs:
- All `console.log()` statements appear in the Expo terminal
- Use them to debug API calls and state changes

---

## 🌐 Network Configuration Details

### How It Works:

```
Your Phone (Expo Go)
      ↓ Wi-Fi
Your Laptop (192.168.1.105)
      ↓
Expo Dev Server (Port 8081)
      ↓
React Native App
      ↓
API Service (frontend/services/api.js)
      ↓
Backend Server (Port 5000)
      ↓
Flask API
```

### Ports Used:
- **8081** - Expo development server (Metro bundler)
- **5000** - Flask backend API
- **19000** - Expo DevTools (web interface)

### Firewall Rules Needed:
```powershell
# Allow Expo (if needed)
New-NetFirewallRule -DisplayName "Expo Metro" -Direction Inbound -LocalPort 8081 -Protocol TCP -Action Allow

# Allow Backend (if needed)
New-NetFirewallRule -DisplayName "Flask Backend" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

---

## 🎯 Quick Command Reference

### Start Everything:

**Terminal 1 (Backend):**
```powershell
cd "c:\Users\Raazia Yasin\Documents\echobmad\backend"
python app.py
```

**Terminal 2 (Frontend):**
```powershell
cd "c:\Users\Raazia Yasin\Documents\echobmad\frontend"
npx expo start
```

### Stop Everything:
- Press `Ctrl+C` in both PowerShell windows

### Restart Frontend Only:
- Press `Ctrl+C` in Terminal 2
- Run `npx expo start` again

### Restart Backend Only:
- Press `Ctrl+C` in Terminal 1
- Run `python app.py` again

---

## 📊 Performance Tips

### For Faster Development:

1. **Use Tunnel Mode** (if on different networks):
   ```powershell
   npx expo start --tunnel
   ```
   - Slower but works across different networks
   - Useful for testing from anywhere

2. **Use LAN Mode** (default, fastest):
   ```powershell
   npx expo start --lan
   ```
   - Fastest option
   - Requires same Wi-Fi network

3. **Clear Cache** (if app behaves strangely):
   ```powershell
   npx expo start -c
   ```

---

## 🎉 Success Checklist

Before showing to investors, verify:

- ✅ Backend starts without errors
- ✅ Frontend loads on phone via QR code
- ✅ Dashboard shows Mystery Seed and Tree
- ✅ Chat screen opens and accepts input
- ✅ AI responds to questions
- ✅ PII shield appears when typing email/phone
- ✅ Animations work (tree shake, seed glow)
- ✅ Navigation works (Dashboard ↔ Chat)

---

## 📞 Need Help?

### Common Issues:

| Issue | Solution |
|-------|----------|
| Can't find IP address | Run `ipconfig` in PowerShell |
| QR code won't scan | Type URL manually in Expo Go |
| Backend won't start | Check if port 5000 is already in use |
| App shows blank screen | Check Expo terminal for errors |
| API calls fail | Verify IP address in `api.js` |

### Check Logs:

**Backend Logs:**
- Look at Terminal 1 (where `python app.py` is running)
- Shows all API requests and errors

**Frontend Logs:**
- Look at Terminal 2 (where `npx expo start` is running)
- Shows React Native errors and console.log outputs

---

## 🚀 You're Ready!

**Your EchoMind AI app is now running on your actual phone!**

Next steps:
1. ✅ Test the E2E scenario (see `E2E-TEST-SCENARIO.md`)
2. ✅ Apply premium polish (see `PREMIUM-POLISH-CHECKLIST.md`)
3. ✅ Show it to investors! 💰

---

*EchoMind AI - Where learning comes alive* 🌱

**Generated:** January 30, 2026  
**Sprint:** Final Assembly - Expo Quick-Start Guide
