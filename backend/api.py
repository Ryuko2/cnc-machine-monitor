"""
CNC Machine Monitor - Enhanced FastAPI Backend with Data Storage & Reports
Run with: python api.py
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import asyncio
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
from haas_machine import create_default_machines, HaasMachine

app = FastAPI(title="CNC Machine Monitor API")

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database path
DB_PATH = "machines_data.db"

# Initialize machines
machines: Dict[str, HaasMachine] = create_default_machines()

# Connected WebSocket clients
connected_clients: List[WebSocket] = []

# ============================================
# DATABASE SETUP
# ============================================

def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Machine samples table - stores time-series data
    c.execute("""
        CREATE TABLE IF NOT EXISTS machine_samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            machine_id TEXT NOT NULL,
            machine_name TEXT,
            execution TEXT,
            cycle_phase TEXT,
            spindle_speed REAL,
            spindle_load REAL,
            spindle_temp REAL,
            feed_rate REAL,
            rapid_rate REAL,
            axis_x REAL,
            axis_y REAL,
            axis_z REAL,
            servo_load_x REAL,
            servo_load_y REAL,
            servo_load_z REAL,
            temperature REAL,
            current_amps REAL,
            vibration REAL,
            part_count INTEGER,
            total_cycles INTEGER,
            production_rate INTEGER,
            alarm TEXT,
            warnings TEXT,
            oil_pressure REAL,
            oil_level REAL
        )
    """)
    
    # Daily summaries table
    c.execute("""
        CREATE TABLE IF NOT EXISTS daily_summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            machine_id TEXT NOT NULL,
            total_parts INTEGER,
            total_cycles INTEGER,
            avg_spindle_load REAL,
            max_spindle_load REAL,
            avg_spindle_temp REAL,
            max_spindle_temp REAL,
            total_runtime_minutes REAL,
            total_idle_minutes REAL,
            total_alarm_minutes REAL,
            alarm_count INTEGER,
            avg_production_rate REAL,
            UNIQUE(date, machine_id)
        )
    """)
    
    # Alarms log table
    c.execute("""
        CREATE TABLE IF NOT EXISTS alarm_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            machine_id TEXT NOT NULL,
            machine_name TEXT,
            alarm_code INTEGER,
            alarm_message TEXT,
            duration_seconds REAL
        )
    """)
    
    # Create indexes for faster queries
    c.execute("CREATE INDEX IF NOT EXISTS idx_samples_timestamp ON machine_samples(timestamp)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_samples_machine ON machine_samples(machine_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_summaries_date ON daily_summaries(date)")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def save_sample(machine_id: str, data: dict):
    """Save a machine sample to the database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    warnings_json = json.dumps(data.get('warnings', []))
    
    c.execute("""
        INSERT INTO machine_samples (
            timestamp, machine_id, machine_name, execution, cycle_phase,
            spindle_speed, spindle_load, spindle_temp,
            feed_rate, rapid_rate,
            axis_x, axis_y, axis_z,
            servo_load_x, servo_load_y, servo_load_z,
            temperature, current_amps, vibration,
            part_count, total_cycles, production_rate,
            alarm, warnings, oil_pressure, oil_level
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('timestamp', datetime.utcnow().isoformat()),
        machine_id,
        data.get('name', ''),
        data.get('execution', ''),
        data.get('cyclePhase', ''),
        data.get('spindleSpeed', 0),
        data.get('spindleLoad', 0),
        data.get('spindleTemp', 0),
        data.get('feedRate', 0),
        data.get('rapidRate', 0),
        data.get('axisPositions', {}).get('X', 0),
        data.get('axisPositions', {}).get('Y', 0),
        data.get('axisPositions', {}).get('Z', 0),
        data.get('servoLoad', {}).get('X', 0),
        data.get('servoLoad', {}).get('Y', 0),
        data.get('servoLoad', {}).get('Z', 0),
        data.get('temperature', 0),
        data.get('currentAmps', 0),
        data.get('vibration', 0),
        data.get('partCount', 0),
        data.get('totalCycles', 0),
        data.get('productionRate', 0),
        data.get('alarm'),
        warnings_json,
        data.get('oilPressure', 0),
        data.get('oilLevel', 0)
    ))
    
    conn.commit()
    conn.close()


def get_historical_data(machine_id: str, hours: int = 24, limit: int = 1000):
    """Get historical data for a machine"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    since = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
    
    c.execute("""
        SELECT * FROM machine_samples 
        WHERE machine_id = ? AND timestamp > ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (machine_id, since, limit))
    
    rows = c.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_all_historical_data(hours: int = 24):
    """Get historical data for all machines"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    since = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
    
    c.execute("""
        SELECT * FROM machine_samples 
        WHERE timestamp > ?
        ORDER BY timestamp DESC
    """, (since,))
    
    rows = c.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def generate_daily_summary(date: str = None):
    """Generate daily summary for all machines"""
    if date is None:
        date = datetime.utcnow().strftime('%Y-%m-%d')
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    start_time = f"{date}T00:00:00"
    end_time = f"{date}T23:59:59"
    
    summaries = []
    
    for machine_id in machines.keys():
        c.execute("""
            SELECT 
                COUNT(*) as sample_count,
                MAX(part_count) - MIN(part_count) as parts_produced,
                MAX(total_cycles) - MIN(total_cycles) as cycles_completed,
                AVG(spindle_load) as avg_spindle_load,
                MAX(spindle_load) as max_spindle_load,
                AVG(spindle_temp) as avg_spindle_temp,
                MAX(spindle_temp) as max_spindle_temp,
                SUM(CASE WHEN execution = 'RUNNING' THEN 1 ELSE 0 END) as running_samples,
                SUM(CASE WHEN execution = 'IDLE' THEN 1 ELSE 0 END) as idle_samples,
                SUM(CASE WHEN execution = 'ALARM' THEN 1 ELSE 0 END) as alarm_samples,
                AVG(production_rate) as avg_production_rate
            FROM machine_samples
            WHERE machine_id = ? AND timestamp BETWEEN ? AND ?
        """, (machine_id, start_time, end_time))
        
        row = c.fetchone()
        
        if row and row['sample_count'] > 0:
            summary = {
                'date': date,
                'machine_id': machine_id,
                'machine_name': machines[machine_id].name,
                'total_parts': row['parts_produced'] or 0,
                'total_cycles': row['cycles_completed'] or 0,
                'avg_spindle_load': round(row['avg_spindle_load'] or 0, 2),
                'max_spindle_load': round(row['max_spindle_load'] or 0, 2),
                'avg_spindle_temp': round(row['avg_spindle_temp'] or 0, 2),
                'max_spindle_temp': round(row['max_spindle_temp'] or 0, 2),
                'runtime_minutes': round((row['running_samples'] or 0) / 60, 2),
                'idle_minutes': round((row['idle_samples'] or 0) / 60, 2),
                'alarm_minutes': round((row['alarm_samples'] or 0) / 60, 2),
                'avg_production_rate': round(row['avg_production_rate'] or 0, 2),
                'utilization_percent': round(
                    ((row['running_samples'] or 0) / max(row['sample_count'], 1)) * 100, 2
                )
            }
            summaries.append(summary)
    
    conn.close()
    return summaries


def get_chart_data(machine_id: str, metric: str, hours: int = 1):
    """Get time-series data for charting"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    since = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
    
    metric_map = {
        'spindle_speed': 'spindle_speed',
        'spindle_load': 'spindle_load',
        'spindle_temp': 'spindle_temp',
        'feed_rate': 'feed_rate',
        'temperature': 'temperature',
        'vibration': 'vibration',
        'current_amps': 'current_amps',
        'part_count': 'part_count',
    }
    
    db_column = metric_map.get(metric, 'spindle_speed')
    
    c.execute(f"""
        SELECT timestamp, {db_column} as value
        FROM machine_samples 
        WHERE machine_id = ? AND timestamp > ?
        ORDER BY timestamp ASC
    """, (machine_id, since))
    
    rows = c.fetchall()
    conn.close()
    
    return [{'timestamp': row['timestamp'], 'value': row['value']} for row in rows]


# ============================================
# API ENDPOINTS
# ============================================

def get_all_machine_data() -> Dict:
    """Get current state of all machines"""
    return {machine_id: machine.to_dict() for machine_id, machine in machines.items()}


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web dashboard"""
    return FileResponse('static/index.html')


@app.get("/api/machines")
async def get_machines():
    """Get all machine data (REST endpoint)"""
    return get_all_machine_data()


@app.get("/api/machines/{machine_id}")
async def get_machine(machine_id: str):
    """Get single machine data"""
    if machine_id in machines:
        return machines[machine_id].to_dict()
    return {"error": "Machine not found"}


@app.get("/api/machines/{machine_id}/history")
async def get_machine_history(
    machine_id: str, 
    hours: int = Query(default=24, ge=1, le=168)
):
    """Get historical data for a machine"""
    return get_historical_data(machine_id, hours)


@app.get("/api/history")
async def get_all_history(hours: int = Query(default=24, ge=1, le=168)):
    """Get historical data for all machines"""
    return get_all_historical_data(hours)


@app.get("/api/machines/{machine_id}/chart/{metric}")
async def get_machine_chart(
    machine_id: str,
    metric: str,
    hours: int = Query(default=1, ge=1, le=24)
):
    """Get chart data for a specific metric"""
    return get_chart_data(machine_id, metric, hours)


@app.get("/api/reports/daily")
async def get_daily_report(date: str = None):
    """Get daily summary report"""
    return generate_daily_summary(date)


@app.get("/api/reports/summary")
async def get_summary_stats():
    """Get overall summary statistics"""
    machine_data = get_all_machine_data()
    
    total_parts = sum(m.get('partCount', 0) for m in machine_data.values())
    running_count = sum(1 for m in machine_data.values() if m.get('execution') == 'RUNNING')
    alarm_count = sum(1 for m in machine_data.values() if m.get('alarm'))
    avg_load = sum(m.get('spindleLoad', 0) for m in machine_data.values()) / len(machine_data)
    
    return {
        'total_machines': len(machine_data),
        'running_machines': running_count,
        'idle_machines': len(machine_data) - running_count - alarm_count,
        'alarm_machines': alarm_count,
        'total_parts_today': total_parts,
        'average_spindle_load': round(avg_load, 2),
        'timestamp': datetime.utcnow().isoformat()
    }


@app.post("/api/machines/{machine_id}/power")
async def toggle_power(machine_id: str):
    """Toggle machine power"""
    if machine_id in machines:
        machines[machine_id].set_power(not machines[machine_id].power)
        return {"success": True, "power": machines[machine_id].power}
    return {"error": "Machine not found"}


@app.post("/api/machines/{machine_id}/clear-alarm")
async def clear_alarm(machine_id: str):
    """Clear machine alarm"""
    if machine_id in machines:
        machines[machine_id].clear_alarm()
        return {"success": True}
    return {"error": "Machine not found"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    connected_clients.append(websocket)
    print(f"Client connected. Total clients: {len(connected_clients)}")
    
    try:
        while True:
            # Update all machines
            for machine_id, machine in machines.items():
                machine.update(1.0)
                # Save to database every update
                save_sample(machine_id, machine.to_dict())
            
            # Send data to client
            data = get_all_machine_data()
            await websocket.send_json(data)
            
            # Wait 1 second
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print(f"Client disconnected. Total clients: {len(connected_clients)}")


# Background task to update machines (for REST polling)
async def update_machines_task():
    """Background task that updates machine state every second"""
    sample_counter = 0
    while True:
        for machine_id, machine in machines.items():
            machine.update(1.0)
            # Save sample every 5 seconds to reduce DB writes
            if sample_counter % 5 == 0:
                save_sample(machine_id, machine.to_dict())
        sample_counter += 1
        await asyncio.sleep(1)


@app.on_event("startup")
async def startup_event():
    """Start background update task and initialize DB"""
    # Initialize database
    init_db()
    
    # Create static directory if not exists
    Path("static").mkdir(exist_ok=True)
    
    # Start background task
    asyncio.create_task(update_machines_task())
    
    print("=" * 60)
    print("CNC Machine Monitor API Started!")
    print("=" * 60)
    print(f"Machines loaded: {len(machines)}")
    for mid, m in machines.items():
        print(f"  - {m.name} ({m.model})")
    print("=" * 60)
    print("Endpoints:")
    print("  Dashboard:  http://localhost:5000/")
    print("  REST API:   http://localhost:5000/api/machines")
    print("  WebSocket:  ws://localhost:5000/ws")
    print("  Reports:    http://localhost:5000/api/reports/daily")
    print("=" * 60)


# Create static directory and copy frontend
   from pathlib import Path
   import shutil
   
   static_dir = Path("static")
   static_dir.mkdir(exist_ok=True)
   
   frontend_html = Path(__file__).parent.parent / "frontend" / "index.html"
   if frontend_html.exists():
       shutil.copy2(frontend_html, static_dir / "index.html")
   
   # Mount static files
   if static_dir.exists():
       app.mount("/static", StaticFiles(directory="static"), name="static")
