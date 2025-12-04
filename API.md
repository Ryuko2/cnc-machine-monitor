# API Documentation

Complete API reference for the CNC Machine Monitor.

## Base URL

```
http://localhost:5000
```

## WebSocket Endpoint

### Connect to Real-Time Updates

```
ws://localhost:5000/ws
```

**Description**: Establishes a WebSocket connection for real-time machine data updates.

**Update Frequency**: 1 second

**Response Format**:
```json
{
  "machine_1": {
    "id": "machine_1",
    "name": "Haas VF-2",
    "model": "VF-2",
    "type": "CNC_MILL",
    "power": true,
    "execution": "RUNNING",
    "cyclePhase": "CUTTING",
    "spindleSpeed": 5420,
    "spindleLoad": 67.3,
    "spindleTemp": 42.5,
    "feedRate": 150.2,
    "rapidRate": 0,
    "axisPositions": {
      "X": 381.5,
      "Y": 203.4,
      "Z": 254.1
    },
    "partCount": 145,
    "totalCycles": 892,
    "productionRate": 25,
    "alarm": null,
    "warnings": [],
    "temperature": 75.2,
    "vibration": 2.1,
    "currentAmps": 15.3
  },
  "machine_2": { ... }
}
```

**JavaScript Example**:
```javascript
const ws = new WebSocket('ws://localhost:5000/ws');

ws.onopen = () => {
    console.log('Connected to CNC Monitor');
};

ws.onmessage = (event) => {
    const machines = JSON.parse(event.data);
    updateDashboard(machines);
};

ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};

ws.onclose = () => {
    console.log('Disconnected from CNC Monitor');
};
```

## REST API Endpoints

### Dashboard

#### `GET /`

Serves the web dashboard HTML interface.

**Response**: HTML page

---

### Machines

#### `GET /api/machines`

Get current state of all machines.

**Response**:
```json
{
  "machine_1": {
    "id": "machine_1",
    "name": "Haas VF-2",
    "execution": "RUNNING",
    ...
  },
  "machine_2": { ... }
}
```

**Example**:
```bash
curl http://localhost:5000/api/machines
```

---

#### `GET /api/machines/{machine_id}`

Get current state of a specific machine.

**Parameters**:
- `machine_id` (path) - Machine identifier (e.g., "machine_1")

**Response**:
```json
{
  "id": "machine_1",
  "name": "Haas VF-2",
  "model": "VF-2",
  "type": "CNC_MILL",
  "power": true,
  "execution": "RUNNING",
  "spindleSpeed": 5420,
  "spindleLoad": 67.3,
  "partCount": 145
}
```

**Error Response**:
```json
{
  "error": "Machine not found"
}
```

**Example**:
```bash
curl http://localhost:5000/api/machines/machine_1
```

---

### Historical Data

#### `GET /api/machines/{machine_id}/history`

Get historical data for a specific machine.

**Parameters**:
- `machine_id` (path) - Machine identifier
- `hours` (query, optional) - Number of hours to retrieve (default: 24, max: 168)

**Response**:
```json
[
  {
    "id": 12345,
    "timestamp": "2024-01-15T10:30:00",
    "machine_id": "machine_1",
    "machine_name": "Haas VF-2",
    "execution": "RUNNING",
    "spindle_speed": 5420,
    "spindle_load": 67.3,
    "part_count": 145,
    ...
  },
  ...
]
```

**Example**:
```bash
curl "http://localhost:5000/api/machines/machine_1/history?hours=24"
```

---

#### `GET /api/history`

Get historical data for all machines.

**Parameters**:
- `hours` (query, optional) - Number of hours to retrieve (default: 24, max: 168)

**Response**:
```json
[
  {
    "timestamp": "2024-01-15T10:30:00",
    "machine_id": "machine_1",
    "spindle_speed": 5420,
    ...
  },
  ...
]
```

**Example**:
```bash
curl "http://localhost:5000/api/history?hours=48"
```

---

### Charts

#### `GET /api/machines/{machine_id}/chart/{metric}`

Get time-series data for charting a specific metric.

**Parameters**:
- `machine_id` (path) - Machine identifier
- `metric` (path) - Metric name
- `hours` (query, optional) - Number of hours to retrieve (default: 1, max: 24)

**Available Metrics**:
- `spindle_speed`
- `spindle_load`
- `spindle_temp`
- `feed_rate`
- `temperature`
- `vibration`
- `current_amps`
- `part_count`

**Response**:
```json
[
  {
    "timestamp": "2024-01-15T10:30:00",
    "value": 5420
  },
  {
    "timestamp": "2024-01-15T10:30:01",
    "value": 5425
  },
  ...
]
```

**Example**:
```bash
curl "http://localhost:5000/api/machines/machine_1/chart/spindle_speed?hours=1"
```

**Chart.js Example**:
```javascript
async function loadChart(machineId, metric) {
    const response = await fetch(
        `/api/machines/${machineId}/chart/${metric}?hours=1`
    );
    const data = await response.json();
    
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => new Date(d.timestamp)),
            datasets: [{
                label: metric,
                data: data.map(d => d.value)
            }]
        }
    });
}
```

---

### Reports

#### `GET /api/reports/daily`

Get daily production summary for all machines.

**Parameters**:
- `date` (query, optional) - Date in YYYY-MM-DD format (default: today)

**Response**:
```json
[
  {
    "date": "2024-01-15",
    "machine_id": "machine_1",
    "machine_name": "Haas VF-2",
    "total_parts": 245,
    "total_cycles": 1432,
    "avg_spindle_load": 65.3,
    "max_spindle_load": 89.2,
    "avg_spindle_temp": 41.7,
    "max_spindle_temp": 55.3,
    "runtime_minutes": 420.5,
    "idle_minutes": 35.2,
    "alarm_minutes": 4.3,
    "avg_production_rate": 35,
    "utilization_percent": 91.5
  },
  ...
]
```

**Example**:
```bash
curl "http://localhost:5000/api/reports/daily?date=2024-01-15"
```

---

#### `GET /api/reports/summary`

Get overall summary statistics for all machines.

**Response**:
```json
{
  "total_machines": 6,
  "running_machines": 4,
  "idle_machines": 1,
  "alarm_machines": 1,
  "total_parts_today": 1240,
  "average_spindle_load": 62.5,
  "timestamp": "2024-01-15T10:30:00"
}
```

**Example**:
```bash
curl http://localhost:5000/api/reports/summary
```

---

### Machine Control

#### `POST /api/machines/{machine_id}/power`

Toggle machine power on/off.

**Parameters**:
- `machine_id` (path) - Machine identifier

**Response**:
```json
{
  "success": true,
  "power": false
}
```

**Error Response**:
```json
{
  "error": "Machine not found"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/machines/machine_1/power
```

**JavaScript Example**:
```javascript
async function togglePower(machineId) {
    const response = await fetch(
        `/api/machines/${machineId}/power`,
        { method: 'POST' }
    );
    const result = await response.json();
    console.log(`Power is now: ${result.power ? 'ON' : 'OFF'}`);
}
```

---

#### `POST /api/machines/{machine_id}/clear-alarm`

Clear an active alarm on a machine.

**Parameters**:
- `machine_id` (path) - Machine identifier

**Response**:
```json
{
  "success": true
}
```

**Error Response**:
```json
{
  "error": "Machine not found"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/machines/machine_1/clear-alarm
```

---

## Data Models

### Machine State

```typescript
interface Machine {
  id: string;
  name: string;
  model: string;
  type: "CNC_MILL" | "LATHE" | "PRESS_BRAKE" | "LASER";
  power: boolean;
  execution: "IDLE" | "RUNNING" | "ALARM" | "STOPPED";
  cyclePhase: string;
  spindleSpeed: number;      // RPM
  spindleLoad: number;        // percentage
  spindleTemp: number;        // °F
  feedRate: number;           // ipm
  rapidRate: number;          // ipm
  axisPositions: {
    X: number;
    Y: number;
    Z: number;
  };
  servoLoad: {
    X: number;
    Y: number;
    Z: number;
  };
  partCount: number;
  totalCycles: number;
  productionRate: number;     // parts/hour
  temperature: number;        // °F
  vibration: number;
  currentAmps: number;
  oilPressure: number;        // PSI
  oilLevel: number;           // percentage
  alarm: string | null;
  alarmCode: number | null;
  warnings: Warning[];
}
```

### Warning

```typescript
interface Warning {
  type: "MAINTENANCE" | "TEMPERATURE" | "VIBRATION" | "LOAD";
  message: string;
  value: number;
  threshold: number;
}
```

### Historical Sample

```typescript
interface HistoricalSample {
  id: number;
  timestamp: string;
  machine_id: string;
  machine_name: string;
  execution: string;
  cycle_phase: string;
  spindle_speed: number;
  spindle_load: number;
  spindle_temp: number;
  feed_rate: number;
  part_count: number;
  // ... additional fields
}
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK` - Request successful
- `404 Not Found` - Machine or resource not found
- `500 Internal Server Error` - Server error

Error responses include a descriptive message:
```json
{
  "error": "Description of the error"
}
```

---

## Rate Limiting

Currently, there are no rate limits. For production deployments, consider implementing rate limiting.

---

## CORS

CORS is enabled for all origins in development mode. For production, configure specific allowed origins in `api.py`.

---

## Interactive Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: `http://localhost:5000/docs`
- **ReDoc**: `http://localhost:5000/redoc`

---

## Python Client Example

```python
import requests
import websockets
import asyncio
import json

# REST API Example
def get_machines():
    response = requests.get('http://localhost:5000/api/machines')
    return response.json()

def toggle_power(machine_id):
    response = requests.post(f'http://localhost:5000/api/machines/{machine_id}/power')
    return response.json()

# WebSocket Example
async def monitor_machines():
    uri = "ws://localhost:5000/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            machines = json.loads(message)
            print(f"Received data for {len(machines)} machines")
            # Process machine data
            await asyncio.sleep(1)

# Run WebSocket client
asyncio.run(monitor_machines())
```

---

## Support

For API questions or issues:
- Check the interactive docs at `/docs`
- Open an issue on GitHub
- Review the example implementations in the dashboard code

---

Last Updated: 2024-01-15
