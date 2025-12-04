# CNC Machine Monitor - Green Theme Edition

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A real-time CNC machine monitoring dashboard with WebSocket support, data logging, and historical analytics. Features a professional industrial green theme interface for monitoring multiple Haas CNC machines.

![Dashboard Preview](docs/screenshot.png)

> **Note**: This is a simulation/demonstration project. For production use with real CNC machines, you'll need to implement actual machine communication protocols (MTConnect, OPC-UA, etc.).

## 🚀 Features

- **Real-Time Monitoring**: WebSocket-based live updates for machine status
- **Multi-Machine Support**: Monitor multiple CNC machines simultaneously
- **Industrial Green Theme**: Professional, easy-to-read interface
- **Historical Data**: SQLite database for storing machine metrics
- **Production Analytics**: Daily summaries, charts, and production reports
- **Mobile Responsive**: Access from desktop, tablet, or phone
- **RESTful API**: Full REST API for integration with other systems
- **Alarm Management**: Real-time alarm tracking and history

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Screenshots](#screenshots)
- [License](#license)

## ⚡ Quick Start

### Windows

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cnc-machine-monitor.git
cd cnc-machine-monitor
```

2. Run the startup script:
```bash
start.bat
```

3. Open your browser to `http://localhost:5000`

### Mac/Linux

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cnc-machine-monitor.git
cd cnc-machine-monitor
```

2. Make the script executable and run:
```bash
chmod +x start.sh
./start.sh
```

3. Open your browser to `http://localhost:5000`

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cnc-machine-monitor.git
cd cnc-machine-monitor
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create the static directory and copy files:
```bash
mkdir -p backend/static
cp frontend/index.html backend/static/
```

4. Start the server:
```bash
cd backend
python api.py
```

## 🔧 Configuration

### Machine Configuration

Edit `backend/haas_machine.py` to configure your machines. The default configuration includes:

- **Haas VF-2**: Vertical Machining Center
- **Haas VF-4**: Large Format Mill
- **Haas HMC**: Horizontal Machining Center
- **Haas Lathe**: CNC Lathe
- **Press Brake**: Press Machine
- **Laser Cutter**: Laser Cutting System

### Network Configuration

To access from mobile devices on your local network:

1. Find your computer's IP address:
   - **Windows**: `ipconfig`
   - **Mac/Linux**: `ifconfig` or `ip addr`

2. Open browser on phone to: `http://YOUR-IP:5000`

### Database Configuration

By default, the system uses SQLite with the database file at `backend/machines_data.db`. To change this, edit the `DB_PATH` variable in `backend/api.py`.

## 📚 API Documentation

### REST Endpoints

#### Get All Machines
```http
GET /api/machines
```

#### Get Single Machine
```http
GET /api/machines/{machine_id}
```

#### Get Machine History
```http
GET /api/machines/{machine_id}/history?hours=24
```

#### Get Chart Data
```http
GET /api/machines/{machine_id}/chart/{metric}?hours=1
```
Metrics: `spindle_speed`, `spindle_load`, `spindle_temp`, `feed_rate`, `temperature`, `vibration`, `current_amps`, `part_count`

#### Get Daily Report
```http
GET /api/reports/daily?date=2024-01-01
```

#### Get Summary Statistics
```http
GET /api/reports/summary
```

#### Toggle Machine Power
```http
POST /api/machines/{machine_id}/power
```

#### Clear Machine Alarm
```http
POST /api/machines/{machine_id}/clear-alarm
```

### WebSocket Connection

Connect to `ws://localhost:5000/ws` for real-time machine updates. The server sends JSON data every second with the current state of all machines.

Example JavaScript client:
```javascript
const ws = new WebSocket('ws://localhost:5000/ws');

ws.onmessage = (event) => {
    const machines = JSON.parse(event.data);
    console.log('Machine data:', machines);
};
```

## 🛠️ Development

### Project Structure

```
cnc-machine-monitor/
├── backend/
│   ├── api.py              # FastAPI server
│   ├── haas_machine.py     # Machine simulation logic
│   └── static/             # Served frontend files
│       └── index.html
├── frontend/
│   └── index.html          # Dashboard UI
├── docs/
│   └── screenshot.png      # Documentation images
├── start.bat               # Windows startup script
├── start.sh                # Mac/Linux startup script
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

### Running in Development Mode

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run with auto-reload:
```bash
cd backend
uvicorn api:app --reload --host 0.0.0.0 --port 5000
```

### Adding New Machines

1. Open `backend/haas_machine.py`
2. Add a new machine to the `create_default_machines()` function:

```python
def create_default_machines() -> Dict[str, HaasMachine]:
    return {
        # ... existing machines ...
        "machine_6": HaasMachine(
            machine_id="machine_6",
            name="My New Machine",
            model="VF-6",
            mtype="CNC_MILL",
            specs={
                "spindlePower": 40,
                "maxRPM": 8100,
                "rapidTraverse": 1200,
                "toolCapacity": 30,
            }
        ),
    }
```

## 📸 Screenshots

### Main Dashboard
![Main Dashboard](docs/dashboard-main.png)

### Machine Details
![Machine Details](docs/machine-details.png)

### Historical Charts
![Charts](docs/charts.png)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI inspired by industrial monitoring systems
- Machine simulation based on Haas CNC specifications

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/cnc-machine-monitor](https://github.com/yourusername/cnc-machine-monitor)

---

**Note**: This is a simulation/monitoring tool. For production environments, ensure proper security measures are in place and consult with your IT department before deployment.
