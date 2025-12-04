# Frequently Asked Questions (FAQ)

Common questions and answers about the CNC Machine Monitor.

## General Questions

### What is this project?

The CNC Machine Monitor is a real-time monitoring dashboard for CNC machines. It provides:
- Live machine status updates
- Historical data tracking
- Production analytics
- Alarm management
- RESTful API access

### Is this a real CNC machine controller?

No. This is a **monitoring and data visualization tool** with a built-in machine simulator. It's designed to demonstrate what a monitoring system could look like. For production use, you would integrate it with actual CNC machines via protocols like MTConnect or OPC-UA.

### Can I use this for real machines?

The current version uses simulated machines. To connect to real machines, you would need to:
1. Replace the simulation logic in `haas_machine.py`
2. Implement actual machine communication (MTConnect, OPC-UA, Modbus, etc.)
3. Add security and authentication
4. Test thoroughly in your environment

### Is it free?

Yes! This project is open source under the MIT License. You can use it, modify it, and distribute it freely.

---

## Installation & Setup

### What are the system requirements?

- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher (3.10+ recommended)
- **RAM**: 2GB minimum, 4GB recommended
- **Disk**: 100MB + database storage

### Do I need programming knowledge?

For basic use, no. Just run the startup scripts. For customization, basic Python knowledge is helpful.

### How do I install it?

Three methods:
1. **Easy**: Double-click `start.bat` (Windows) or `./start.sh` (Mac/Linux)
2. **Manual**: `pip install -r requirements.txt` then `python backend/api.py`
3. **Docker**: `docker-compose up -d`

See [QUICKSTART.md](QUICKSTART.md) for details.

### Can I run it without internet?

Yes! The application runs entirely locally and doesn't require internet access.

---

## Usage Questions

### How do I access the dashboard?

Open your browser to `http://localhost:5000`

### Can I access it from my phone?

Yes! Find your computer's IP address and visit `http://YOUR-IP:5000` from any device on the same network.

### How often does the data update?

Real-time data updates every 1 second via WebSocket connection.

### Where is the data stored?

In a SQLite database file: `backend/machines_data.db`

### How much data can it store?

SQLite can handle millions of records, but performance may degrade with very large datasets (>1M records). Consider implementing data archiving for long-term deployments.

### Can I export the data?

Currently, data is accessible via the API. You can:
- Query historical data endpoints
- Connect to the SQLite database directly
- Use the API to export to CSV/Excel (custom implementation)

### How do I backup my data?

Simply copy the `machines_data.db` file:
```bash
cp backend/machines_data.db backup_$(date +%Y%m%d).db
```

---

## Customization

### How do I add more machines?

Edit `backend/haas_machine.py`, modify the `create_default_machines()` function:

```python
"machine_7": HaasMachine(
    machine_id="machine_7",
    name="My Machine",
    model="VF-6",
    mtype="CNC_MILL"
),
```

### Can I change the colors/theme?

Yes! Edit `frontend/index.html` and modify the CSS styles. The current theme uses green (#00ff00) and dark backgrounds.

### How do I change the port?

Edit `backend/api.py`, line 482:
```python
uvicorn.run(app, host="0.0.0.0", port=5000)  # Change port here
```

### Can I add authentication?

Authentication is not included by default. For production use, consider:
- Adding FastAPI security dependencies
- Implementing JWT tokens
- Using OAuth2
- Reverse proxy with authentication (Nginx, Apache)

### How do I connect to real machines?

You would need to:
1. Identify your machine's communication protocol (MTConnect, OPC-UA, Modbus, etc.)
2. Replace simulation logic in `haas_machine.py` with actual machine communication
3. Install necessary protocol libraries
4. Handle connection errors and retries
5. Implement machine-specific data parsing

---

## Technical Questions

### What technology stack is used?

- **Backend**: Python, FastAPI, Uvicorn
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Real-time**: WebSockets
- **API**: RESTful JSON API

### Why Python?

Python is:
- Easy to learn and modify
- Great for rapid development
- Has excellent libraries for industrial protocols
- Cross-platform compatible

### Can I use PostgreSQL instead of SQLite?

Yes! Modify `backend/api.py`:
1. Install `psycopg2` or `asyncpg`
2. Replace SQLite connection code with PostgreSQL
3. Update connection strings

### Is it production-ready?

The current version is suitable for:
- Development and testing
- Small-scale deployments
- Demonstrations
- Learning projects

For production, add:
- Authentication/authorization
- Input validation
- Error handling improvements
- Load balancing (for multiple machines)
- Database optimization
- Security hardening

### How scalable is it?

- **Machines**: Can handle dozens of machines on modest hardware
- **Data**: SQLite limits depend on disk space
- **Clients**: WebSocket can handle dozens of concurrent connections
- **For larger scale**: Consider PostgreSQL, Redis, load balancing

### Does it support HTTPS?

Not directly. Use a reverse proxy (Nginx, Apache) with SSL certificates. See [DEPLOYMENT.md](DEPLOYMENT.md).

---

## Troubleshooting

### The server won't start

Check:
1. Python is installed: `python --version`
2. Dependencies are installed: `pip install -r requirements.txt`
3. Port 5000 is not in use: `netstat -ano | findstr :5000` (Windows) or `lsof -ti:5000` (Mac/Linux)
4. You're in the correct directory

### Dashboard shows blank page

Check:
1. `backend/static/index.html` exists
2. Copy it: `cp frontend/index.html backend/static/`
3. Clear browser cache
4. Check browser console for errors (F12)

### WebSocket connection failed

Check:
1. Server is running
2. Firewall allows port 5000
3. No VPN interfering
4. Try `ws://IP:5000/ws` instead of `localhost`

### Database locked error

This can happen if:
- Multiple instances are running
- Database file has wrong permissions
- Disk is full

Solution: Stop all instances, delete database, restart.

### High CPU usage

Normal for the simulation. Each machine update requires calculations. For real machines, CPU usage will be much lower.

---

## Performance

### How many machines can it monitor?

Tested with up to 20 simulated machines on modest hardware. Real-world limits depend on:
- Machine update frequency
- Database write frequency
- Number of connected clients
- Server hardware

### Can I reduce database writes?

Yes! In `api.py`, line 443, change:
```python
if sample_counter % 5 == 0:  # Currently saves every 5 seconds
```

Increase this number to save less frequently.

### How do I optimize performance?

1. Reduce sampling frequency
2. Implement data aggregation
3. Use PostgreSQL for large datasets
4. Add Redis caching
5. Optimize database indexes
6. Use connection pooling

---

## Deployment

### Can I deploy this to the cloud?

Yes! See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- AWS EC2
- Google Cloud
- DigitalOcean
- Heroku
- Docker deployment

### Should I use Docker?

Docker is recommended for:
- Easy deployment
- Consistent environments
- Cloud platforms
- Multiple instances

### How do I secure it?

1. Add authentication
2. Use HTTPS (reverse proxy)
3. Implement rate limiting
4. Regular security updates
5. Firewall configuration
6. Database encryption

---

## Contributing

### Can I contribute?

Yes! Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

### I found a bug

Please [open an issue](https://github.com/yourusername/cnc-machine-monitor/issues) with:
- Description
- Steps to reproduce
- Your environment (OS, Python version)
- Error messages

### I have a feature request

Great! [Open an issue](https://github.com/yourusername/cnc-machine-monitor/issues) describing:
- The feature
- Use case
- Why it would be useful

---

## License

### What license is this under?

MIT License - you can use it freely for any purpose.

### Can I use it commercially?

Yes! The MIT License allows commercial use.

### Do I need to credit you?

Not required, but appreciated! Include the original license file if you redistribute.

---

## Support

### Where can I get help?

1. Check this FAQ
2. Read the [documentation](README.md)
3. Search [existing issues](https://github.com/yourusername/cnc-machine-monitor/issues)
4. Open a new issue
5. Join discussions

### Is there a community?

Check the [GitHub Discussions](https://github.com/yourusername/cnc-machine-monitor/discussions) page.

---

## Future Plans

### What's coming next?

See [CHANGELOG.md](CHANGELOG.md) for planned features:
- User authentication
- Real machine integration (MTConnect)
- Mobile app
- Advanced analytics
- Email/SMS notifications
- PDF reports

### Can I request features?

Yes! Open an issue with your feature request.

---

**Still have questions?** Open an issue on [GitHub](https://github.com/yourusername/cnc-machine-monitor/issues)!
