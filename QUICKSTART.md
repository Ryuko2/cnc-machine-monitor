# Quick Start Guide

Get the CNC Machine Monitor up and running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8 or higher installed
- ✅ pip (comes with Python)
- ✅ Git installed (optional, can download ZIP instead)

### Check Python Installation

```bash
python --version
# or on Mac/Linux:
python3 --version
```

You should see something like: `Python 3.10.x`

If not installed, download from [python.org](https://www.python.org/downloads/)

---

## Installation (Choose One Method)

### Method 1: Automated Setup (Recommended)

#### Windows
1. Download the project (or `git clone`)
2. Double-click `start.bat`
3. Open browser to `http://localhost:5000`

✅ **Done!**

#### Mac/Linux
1. Download the project (or `git clone`)
2. Open Terminal in project folder
3. Run:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```
4. Open browser to `http://localhost:5000`

✅ **Done!**

---

### Method 2: Manual Setup

1. **Download the Project**
   ```bash
   git clone https://github.com/yourusername/cnc-machine-monitor.git
   cd cnc-machine-monitor
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Frontend**
   ```bash
   mkdir -p backend/static
   cp frontend/index.html backend/static/
   ```

4. **Start Server**
   ```bash
   cd backend
   python api.py
   ```

5. **Open Dashboard**
   - Go to `http://localhost:5000` in your browser

✅ **Done!**

---

### Method 3: Docker (Advanced)

```bash
# Build and run
docker-compose up -d

# Access dashboard
# Open http://localhost:5000
```

✅ **Done!**

---

## First Steps

### 1. View the Dashboard

Open `http://localhost:5000` - you should see:
- 6 simulated CNC machines
- Real-time status updates
- Green industrial theme

### 2. Explore Features

- **Machine Cards**: Show current status, spindle info, and alarms
- **Real-Time Updates**: Data updates every second
- **Machine Control**: Click machine names for details

### 3. Test the API

```bash
# Get all machines
curl http://localhost:5000/api/machines

# Get specific machine
curl http://localhost:5000/api/machines/machine_1

# Get daily report
curl http://localhost:5000/api/reports/daily
```

### 4. Access from Phone

1. Find your computer's IP:
   - **Windows**: Open Command Prompt, type `ipconfig`
   - **Mac**: Open Terminal, type `ifconfig | grep inet`
   - **Linux**: Open Terminal, type `ip addr show`

2. Look for your local IP (usually `192.168.x.x`)

3. On your phone's browser, go to: `http://YOUR-IP:5000`

---

## What's Running?

When you start the server, you get:

- **Backend API**: FastAPI server on port 5000
- **WebSocket**: Real-time data stream
- **Database**: SQLite database (auto-created)
- **6 Simulated Machines**: CNC mills, lathe, press brake, laser

---

## Stop the Server

- **Press `Ctrl+C`** in the terminal where it's running

---

## Troubleshooting

### Problem: "Python not found"
**Solution**: Install Python from python.org and ensure "Add to PATH" is checked

### Problem: "Port 5000 already in use"
**Solution**: 
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <pid> /F

# Mac/Linux
lsof -ti:5000 | xargs kill
```

### Problem: "Module not found"
**Solution**:
```bash
pip install -r requirements.txt --upgrade
```

### Problem: Dashboard not loading
**Solution**:
1. Check that `backend/static/index.html` exists
2. Copy it: `cp frontend/index.html backend/static/`
3. Restart server

### Problem: Permission denied (Mac/Linux)
**Solution**:
```bash
chmod +x start.sh
```

---

## Next Steps

1. **Read Full Documentation**: Check [README.md](README.md)
2. **Explore API**: Visit `http://localhost:5000/docs`
3. **Customize Machines**: Edit `backend/haas_machine.py`
4. **Deploy**: See [DEPLOYMENT.md](DEPLOYMENT.md)
5. **Contribute**: Read [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Common Commands

```bash
# Start server
python backend/api.py

# Start with auto-reload (development)
cd backend
uvicorn api:app --reload --host 0.0.0.0 --port 5000

# View logs (if running as service)
sudo journalctl -u cnc-monitor -f

# Backup database
cp backend/machines_data.db backup_$(date +%Y%m%d).db
```

---

## Quick Configuration

### Change Port

Edit `backend/api.py`, line 482:
```python
uvicorn.run(app, host="0.0.0.0", port=5000)  # Change 5000
```

### Add Machine

Edit `backend/haas_machine.py`, add to `create_default_machines()`:
```python
"machine_7": HaasMachine(
    machine_id="machine_7",
    name="New Machine",
    model="VF-6",
    mtype="CNC_MILL"
),
```

---

## Getting Help

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/yourusername/cnc-machine-monitor/issues)
- 💬 [Discussions](https://github.com/yourusername/cnc-machine-monitor/discussions)
- 📧 Email: your-email@example.com

---

## System Requirements Summary

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Windows 10, macOS 10.14, Ubuntu 20.04 | Latest stable |
| Python | 3.8 | 3.10+ |
| RAM | 2GB | 4GB |
| Disk | 100MB | 500MB |
| Browser | Modern browser | Latest Chrome/Firefox |

---

**Ready to monitor your CNC machines? Start the server and visit http://localhost:5000!** 🚀
