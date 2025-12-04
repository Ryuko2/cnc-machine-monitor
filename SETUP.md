# Setup Guide

This guide will walk you through setting up the CNC Machine Monitor on your system.

## Table of Contents

- [System Requirements](#system-requirements)
- [Quick Start](#quick-start)
- [Detailed Installation](#detailed-installation)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 100MB for application + space for database
- **Network**: Local network for mobile access (optional)

### Recommended Requirements
- **Python**: 3.10 or higher
- **RAM**: 4GB or more
- **Browser**: Latest version of Chrome, Firefox, Safari, or Edge

## Quick Start

### For Windows Users

1. **Download and Install Python**
   - Visit [python.org](https://www.python.org/downloads/)
   - Download Python 3.10 or higher
   - **IMPORTANT**: Check "Add Python to PATH" during installation

2. **Download the Project**
   ```bash
   git clone https://github.com/yourusername/cnc-machine-monitor.git
   cd cnc-machine-monitor
   ```

3. **Run the Application**
   - Double-click `start.bat`
   - Or open Command Prompt and run:
     ```bash
     start.bat
     ```

4. **Access Dashboard**
   - Open browser to `http://localhost:5000`

### For Mac/Linux Users

1. **Check Python Installation**
   ```bash
   python3 --version
   ```
   If Python is not installed, install it using your package manager.

2. **Download the Project**
   ```bash
   git clone https://github.com/yourusername/cnc-machine-monitor.git
   cd cnc-machine-monitor
   ```

3. **Run the Application**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

4. **Access Dashboard**
   - Open browser to `http://localhost:5000`

## Detailed Installation

### Step 1: Python Installation

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Check "Add Python to PATH"**
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```

#### macOS
Using Homebrew:
```bash
brew install python@3.10
```

Or download from [python.org](https://www.python.org/downloads/)

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.10 python3-pip
```

### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/cnc-machine-monitor.git
cd cnc-machine-monitor
```

If you don't have Git installed:
- **Windows**: Download from [git-scm.com](https://git-scm.com/)
- **Mac**: `brew install git`
- **Linux**: `sudo apt install git`

Alternatively, download as ZIP from GitHub and extract.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or on Mac/Linux:
```bash
pip3 install -r requirements.txt
```

### Step 4: Setup Directory Structure

```bash
mkdir -p backend/static
cp frontend/index.html backend/static/
```

### Step 5: Start the Server

#### Option A: Using Startup Scripts

**Windows:**
```bash
start.bat
```

**Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

#### Option B: Manual Start

```bash
cd backend
python api.py
```

Or on Mac/Linux:
```bash
cd backend
python3 api.py
```

### Step 6: Access the Dashboard

Open your browser to:
- **Local Access**: `http://localhost:5000`
- **Network Access**: `http://YOUR-IP:5000`

To find your IP address:
- **Windows**: Run `ipconfig` in Command Prompt
- **Mac**: Run `ifconfig | grep inet`
- **Linux**: Run `ip addr show`

## Configuration

### Change Port

Edit `backend/api.py`, line 482:
```python
uvicorn.run(app, host="0.0.0.0", port=5000)  # Change 5000 to your desired port
```

### Add/Remove Machines

Edit `backend/haas_machine.py`, find the `create_default_machines()` function:

```python
def create_default_machines() -> Dict[str, HaasMachine]:
    return {
        "machine_1": HaasMachine(
            machine_id="machine_1",
            name="Haas VF-2",
            model="VF-2",
            mtype="CNC_MILL",
        ),
        # Add more machines here...
    }
```

### Database Location

Edit `backend/api.py`, line 30:
```python
DB_PATH = "machines_data.db"  # Change to your desired path
```

### Enable Auto-Start on Boot

#### Windows
1. Press `Win + R`
2. Type `shell:startup` and press Enter
3. Create a shortcut to `start.bat` in the opened folder

#### Mac
1. Open System Preferences > Users & Groups
2. Click Login Items
3. Add the application to the list

#### Linux (systemd)
Create a service file:
```bash
sudo nano /etc/systemd/system/cnc-monitor.service
```

Add:
```ini
[Unit]
Description=CNC Machine Monitor
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/cnc-machine-monitor/backend
ExecStart=/usr/bin/python3 api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable cnc-monitor
sudo systemctl start cnc-monitor
```

## Troubleshooting

### Issue: "Python not found"

**Solution:**
- Windows: Reinstall Python and check "Add to PATH"
- Mac/Linux: Use `python3` instead of `python`

### Issue: "Module not found"

**Solution:**
```bash
pip install -r requirements.txt --break-system-packages
```

### Issue: "Port already in use"

**Solution:**
- Change port in `api.py` (line 482)
- Or stop the process using port 5000:
  - Windows: `netstat -ano | findstr :5000` then `taskkill /PID <pid> /F`
  - Mac/Linux: `lsof -ti:5000 | xargs kill`

### Issue: "Permission denied" (Linux/Mac)

**Solution:**
```bash
chmod +x start.sh
```

### Issue: Dashboard not loading

**Solution:**
1. Check that `frontend/index.html` is copied to `backend/static/`
2. Clear browser cache
3. Try a different browser
4. Check console for errors (F12)

### Issue: WebSocket connection failed

**Solution:**
1. Ensure server is running
2. Check firewall settings
3. Try using the server's IP address instead of localhost
4. Check browser console for specific error messages

### Issue: Database errors

**Solution:**
1. Delete `machines_data.db` file
2. Restart the server (it will recreate the database)

### Getting More Help

If you encounter issues not listed here:
1. Check the [GitHub Issues](https://github.com/yourusername/cnc-machine-monitor/issues)
2. Create a new issue with:
   - Your operating system
   - Python version
   - Error messages
   - Steps to reproduce

## Next Steps

- Read the [README.md](README.md) for feature documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute
- Explore the API at `http://localhost:5000/docs`

---

Need help? Open an issue on GitHub!
