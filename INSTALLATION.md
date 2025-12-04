# Installation Guide

This guide will walk you through installing and setting up the CNC Machine Monitor on various platforms.

## Table of Contents
- [System Requirements](#system-requirements)
- [Windows Installation](#windows-installation)
- [Mac Installation](#mac-installation)
- [Linux Installation](#linux-installation)
- [Docker Installation](#docker-installation-optional)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **Processor**: Dual-core CPU
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 500MB free space
- **Python**: Version 3.8 or higher
- **Network**: WiFi or Ethernet for remote access

### Supported Operating Systems
- Windows 10/11
- macOS 10.14 (Mojave) or later
- Linux (Ubuntu 18.04+, Debian 10+, CentOS 7+)

### Supported Browsers
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Windows Installation

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"

Verify installation:
```cmd
python --version
```

### Step 2: Download the Project

**Option A: Using Git**
```cmd
git clone https://github.com/yourusername/cnc-machine-monitor.git
cd cnc-machine-monitor
```

**Option B: Download ZIP**
1. Go to the GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Open Command Prompt in the extracted folder

### Step 3: Run the Application

Simply double-click `start.bat` or run:
```cmd
start.bat
```

The dashboard will open automatically at `http://localhost:5000`

## Mac Installation

### Step 1: Install Python

**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

**Option B: Download from python.org**
Download and install from [python.org](https://www.python.org/downloads/)

Verify installation:
```bash
python3 --version
```

### Step 2: Download the Project

```bash
git clone https://github.com/yourusername/cnc-machine-monitor.git
cd cnc-machine-monitor
```

### Step 3: Run the Application

```bash
chmod +x start.sh
./start.sh
```

Open your browser to `http://localhost:5000`

## Linux Installation

### Step 1: Install Python

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**CentOS/RHEL:**
```bash
sudo yum install python3 python3-pip
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip
```

Verify installation:
```bash
python3 --version
```

### Step 2: Download the Project

```bash
git clone https://github.com/yourusername/cnc-machine-monitor.git
cd cnc-machine-monitor
```

### Step 3: Run the Application

```bash
chmod +x start.sh
./start.sh
```

Open your browser to `http://localhost:5000`

## Manual Installation (All Platforms)

If the startup scripts don't work, follow these manual steps:

### 1. Install Dependencies

```bash
# Navigate to project directory
cd cnc-machine-monitor

# Install Python packages
pip install -r requirements.txt
```

### 2. Start the Server

```bash
# Navigate to backend directory
cd backend

# Run the API server
python api.py
```

### 3. Access the Dashboard

Open your browser to: `http://localhost:5000`

## Docker Installation (Optional)

If you prefer using Docker:

### Step 1: Install Docker

Download and install Docker Desktop:
- [Windows/Mac](https://www.docker.com/products/docker-desktop)
- [Linux](https://docs.docker.com/engine/install/)

### Step 2: Create Dockerfile

Create a file named `Dockerfile` in the project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/

WORKDIR /app/backend

EXPOSE 5000

CMD ["python", "api.py"]
```

### Step 3: Build and Run

```bash
# Build the Docker image
docker build -t cnc-monitor .

# Run the container
docker run -p 5000:5000 cnc-monitor
```

Access at `http://localhost:5000`

## Network Access Setup

### Finding Your Computer's IP Address

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" under your active network adapter

**Mac/Linux:**
```bash
ifconfig | grep inet
# or
ip addr show
```
Look for an address like `192.168.x.x` or `10.0.x.x`

### Firewall Configuration

**Windows Firewall:**
1. Open Windows Defender Firewall
2. Click "Advanced settings"
3. Click "Inbound Rules" → "New Rule"
4. Select "Port" → Next
5. Select "TCP" and enter port `5000`
6. Allow the connection
7. Name it "CNC Monitor"

**Mac Firewall:**
```bash
# Usually not needed, but if you have strict firewall:
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add python3
```

**Linux (UFW):**
```bash
sudo ufw allow 5000/tcp
```

## Troubleshooting

### Python Not Found

**Windows:**
- Reinstall Python and check "Add Python to PATH"
- Or add manually: System Properties → Environment Variables → PATH

**Mac/Linux:**
- Use `python3` instead of `python`
- Install using your package manager

### Port Already in Use

If port 5000 is taken:

1. Edit `backend/api.py`
2. Change the last line:
```python
uvicorn.run(app, host="0.0.0.0", port=5001)  # Use 5001 instead
```

### Permission Denied (Linux/Mac)

```bash
chmod +x start.sh
```

### Dependencies Won't Install

Try using a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Can't Access from Mobile

1. Ensure your phone is on the same WiFi network
2. Check firewall settings (see above)
3. Try accessing by IP instead of hostname
4. Disable any VPN on your phone temporarily

### Database Errors

If you see database errors:

```bash
# Delete the old database
rm backend/machines_data.db

# Restart the application
```

### WebSocket Connection Failed

1. Check if the server is running
2. Refresh the browser page
3. Check browser console for errors (F12)
4. Try a different browser

## Updating the Application

To update to the latest version:

```bash
cd cnc-machine-monitor
git pull origin main
pip install -r requirements.txt --upgrade
```

## Uninstallation

To remove the application:

1. Stop the server (Ctrl+C)
2. Delete the project folder
3. (Optional) Uninstall Python packages:
```bash
pip uninstall fastapi uvicorn websockets
```

## Getting Help

If you encounter issues not covered here:

1. Check the [main README](README.md)
2. Search [existing issues](https://github.com/yourusername/cnc-machine-monitor/issues)
3. Create a [new issue](https://github.com/yourusername/cnc-machine-monitor/issues/new) with:
   - Your operating system
   - Python version
   - Error messages
   - Steps you've tried

## Next Steps

After successful installation:

1. Read the [User Guide](docs/USER_GUIDE.md) (if available)
2. Customize machine configurations in `backend/haas_machine.py`
3. Explore the API documentation at `http://localhost:5000/docs`
4. Configure mobile access for shop floor monitoring

---

**Need help?** Open an issue on GitHub!
