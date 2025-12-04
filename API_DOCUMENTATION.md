# API Documentation

The CNC Machine Monitor provides a RESTful API and WebSocket interface for real-time machine monitoring.

## Base URL

When running locally: `http://localhost:5000`

## Authentication

Currently, the API does not require authentication. For production deployments, consider adding authentication middleware.

## REST API Endpoints

### Dashboard

#### `GET /`
Returns the HTML dashboard interface.

**Response:** HTML page

---

### Machine Endpoints

#### `GET /api/machines`
Get a list of all monitored machines.

**Response:**
```json
{
  "mill1": {
    "id": "mill1",
    "name": "VF-2 Main Floor",
    "model": "VF-2",
    "type": "CNC_MILL",
    "power": true,
    "execution": "RUNNING",
    "position": {
      "X": 234.56,
      "Y": 123.45,
      "Z": 45.67
    },
    "spindle": {
      "rpm": 3500,
      "load": 45.2
    }
  }
}
```

#### `GET /api/machines/{machine_id}`
Get detailed information for a specific machine.

**Parameters:**
- `machine_id` (path): Machine identifier (e.g., "mill1", "lathe1")

**Response:**
```json
{
  "id": "mill1",
  "name": "VF-2 Main Floor",
  "model": "VF-2",
  "type": "CNC_MILL",
  "specs": {
    "axisLimits": {
      "X": [0, 762],
      "Y": [0, 406],
      "Z": [0, 508]
    },
    "spindlePower": 30,
    "maxRPM": 8100
  },
  "status": {
    "power": true,
    "execution": "RUNNING",
    "cyclePhase": "CUTTING",
    "alarm": null
  },
  "position": {
    "X": 234.56,
    "Y": 123.45,
    "Z": 45.67
  },
  "spindle": {
    "rpm": 3500,
    "load": 45.2,
    "power": 15.5
  },
  "feeds": {
    "current": 120,
    "programmed": 150,
    "override": 80
  }
}
```

#### `GET /api/machines/{machine_id}/samples`
Get historical sample data for a machine.

**Parameters:**
- `machine_id` (path): Machine identifier
- `hours` (query, optional): Number of hours of history (default: 24, max: 168)
- `limit` (query, optional): Maximum number of samples (default: 1000)

**Example:** `/api/machines/mill1/samples?hours=12&limit=500`

**Response:**
```json
{
  "machine_id": "mill1",
  "samples": [
    {
      "timestamp": "2024-12-04T10:30:00",
      "execution": "RUNNING",
      "position_x": 234.56,
      "position_y": 123.45,
      "position_z": 45.67,
      "spindle_rpm": 3500,
      "spindle_load": 45.2,
      "feed_rate": 120,
      "alarm_active": false
    }
  ],
  "count": 500,
  "period_hours": 12
}
```

#### `GET /api/machines/{machine_id}/analytics`
Get aggregated analytics for a machine.

**Parameters:**
- `machine_id` (path): Machine identifier
- `days` (query, optional): Number of days (default: 7, max: 90)

**Example:** `/api/machines/mill1/analytics?days=30`

**Response:**
```json
{
  "machine_id": "mill1",
  "period_days": 30,
  "analytics": [
    {
      "date": "2024-12-04",
      "uptime_hours": 18.5,
      "cycle_count": 145,
      "alarm_count": 3,
      "avg_spindle_load": 42.3,
      "max_spindle_load": 78.5,
      "total_cutting_time": 12.3
    }
  ],
  "summary": {
    "total_uptime": 555,
    "total_cycles": 4350,
    "total_alarms": 89,
    "avg_daily_uptime": 18.5,
    "uptime_percentage": 77.1
  }
}
```

---

### Statistics Endpoints

#### `GET /api/stats/summary`
Get overall statistics across all machines.

**Response:**
```json
{
  "total_machines": 5,
  "machines_running": 3,
  "machines_idle": 1,
  "machines_alarm": 1,
  "total_uptime_hours": 2450.5,
  "total_cycles_today": 234,
  "active_alarms": 1
}
```

---

## WebSocket API

### Connection

Connect to: `ws://localhost:5000/ws`

The WebSocket provides real-time updates for all machines.

### Message Format

The server sends JSON messages with the following structure:

```json
{
  "type": "update",
  "timestamp": "2024-12-04T10:30:45",
  "machines": {
    "mill1": {
      "id": "mill1",
      "name": "VF-2 Main Floor",
      "power": true,
      "execution": "RUNNING",
      "position": {
        "X": 234.56,
        "Y": 123.45,
        "Z": 45.67
      },
      "spindle": {
        "rpm": 3500,
        "load": 45.2
      }
    }
  }
}
```

### Update Frequency

- Normal updates: Every 1 second
- Position updates: When machine is moving
- Status changes: Immediate

### Example WebSocket Client (JavaScript)

```javascript
const ws = new WebSocket('ws://localhost:5000/ws');

ws.onopen = () => {
    console.log('Connected to CNC Monitor');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Machine update:', data);
    // Update UI with new data
};

ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};

ws.onclose = () => {
    console.log('Disconnected from CNC Monitor');
    // Implement reconnection logic
};
```

### Example WebSocket Client (Python)

```python
import asyncio
import websockets
import json

async def monitor_machines():
    uri = "ws://localhost:5000/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Update: {data}")

asyncio.run(monitor_machines())
```

---

## Error Responses

All endpoints return standard HTTP status codes:

- `200 OK`: Successful request
- `404 Not Found`: Machine or resource not found
- `500 Internal Server Error`: Server error

Error response format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider adding rate limiting middleware.

---

## CORS Policy

The API allows cross-origin requests from any domain (`*`). For production, configure specific allowed origins in `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: `http://localhost:5000/docs`
- **ReDoc**: `http://localhost:5000/redoc`

These interfaces allow you to test API endpoints directly in your browser.

---

## Examples

### Fetch All Machines (cURL)

```bash
curl http://localhost:5000/api/machines
```

### Fetch Specific Machine (cURL)

```bash
curl http://localhost:5000/api/machines/mill1
```

### Get 24 Hours of History (cURL)

```bash
curl "http://localhost:5000/api/machines/mill1/samples?hours=24&limit=1000"
```

### Fetch All Machines (Python)

```python
import requests

response = requests.get('http://localhost:5000/api/machines')
machines = response.json()
print(machines)
```

### Fetch All Machines (JavaScript/Fetch)

```javascript
fetch('http://localhost:5000/api/machines')
    .then(response => response.json())
    .then(machines => {
        console.log(machines);
    })
    .catch(error => console.error('Error:', error));
```

---

## Future API Enhancements

Planned features for future versions:

- Authentication and authorization
- Machine control endpoints (start/stop cycles)
- Custom alert configuration
- Export endpoints (CSV, Excel)
- Webhook notifications
- GraphQL API
- API versioning

---

## Support

For API questions or issues:
- Open an issue on [GitHub](https://github.com/yourusername/cnc-machine-monitor/issues)
- Check the [main documentation](README.md)
