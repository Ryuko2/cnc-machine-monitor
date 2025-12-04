# Deployment Guide

This guide covers deploying the CNC Machine Monitor to various platforms and environments.

## Table of Contents

- [Local Network Deployment](#local-network-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Docker Deployment](#docker-deployment)
- [Production Considerations](#production-considerations)

## Local Network Deployment

### Windows Server

1. **Install Prerequisites**
   ```bash
   # Install Python 3.10+
   # Install Git
   ```

2. **Clone and Setup**
   ```bash
   git clone https://github.com/yourusername/cnc-machine-monitor.git
   cd cnc-machine-monitor
   pip install -r requirements.txt
   ```

3. **Configure Firewall**
   ```bash
   # Allow port 5000 through Windows Firewall
   netsh advfirewall firewall add rule name="CNC Monitor" dir=in action=allow protocol=TCP localport=5000
   ```

4. **Run as Service**
   - Use NSSM (Non-Sucking Service Manager):
   ```bash
   nssm install CNCMonitor "C:\Python310\python.exe" "C:\path\to\cnc-machine-monitor\backend\api.py"
   nssm start CNCMonitor
   ```

### Linux Server

1. **Install Prerequisites**
   ```bash
   sudo apt update
   sudo apt install python3.10 python3-pip git
   ```

2. **Clone and Setup**
   ```bash
   git clone https://github.com/yourusername/cnc-machine-monitor.git
   cd cnc-machine-monitor
   pip3 install -r requirements.txt
   ```

3. **Create Systemd Service**
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
   User=www-data
   WorkingDirectory=/opt/cnc-machine-monitor/backend
   ExecStart=/usr/bin/python3 /opt/cnc-machine-monitor/backend/api.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

4. **Enable and Start**
   ```bash
   sudo systemctl enable cnc-monitor
   sudo systemctl start cnc-monitor
   sudo systemctl status cnc-monitor
   ```

## Cloud Deployment

### AWS EC2

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance Type: t2.micro (free tier) or t2.small
   - Security Group: Allow TCP port 5000

2. **Connect and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python
   sudo apt install python3.10 python3-pip git -y
   
   # Clone repository
   git clone https://github.com/yourusername/cnc-machine-monitor.git
   cd cnc-machine-monitor
   
   # Install dependencies
   pip3 install -r requirements.txt
   
   # Setup systemd service (see Linux Server section)
   ```

3. **Configure Security Group**
   - Add inbound rule: TCP port 5000 from your IP
   - Or use Nginx reverse proxy (see below)

### Google Cloud Platform

1. **Create VM Instance**
   ```bash
   gcloud compute instances create cnc-monitor \
     --image-family=ubuntu-2204-lts \
     --image-project=ubuntu-os-cloud \
     --machine-type=e2-micro \
     --tags=http-server
   ```

2. **Setup Firewall**
   ```bash
   gcloud compute firewall-rules create allow-cnc-monitor \
     --allow=tcp:5000 \
     --target-tags=http-server
   ```

3. **Connect and Deploy**
   ```bash
   gcloud compute ssh cnc-monitor
   # Follow standard Linux setup
   ```

### Heroku

1. **Create `Procfile`**
   ```
   web: cd backend && uvicorn api:app --host=0.0.0.0 --port=$PORT
   ```

2. **Create `runtime.txt`**
   ```
   python-3.10.12
   ```

3. **Deploy**
   ```bash
   heroku create your-cnc-monitor
   git push heroku main
   ```

### DigitalOcean

1. **Create Droplet**
   - Choose Ubuntu 22.04
   - Select droplet size
   - Add SSH key

2. **Setup**
   ```bash
   ssh root@your-droplet-ip
   # Follow standard Linux setup
   ```

## Docker Deployment

### Create Dockerfile

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Create static directory and copy frontend
RUN mkdir -p backend/static && \
    cp frontend/index.html backend/static/

WORKDIR /app/backend

EXPOSE 5000

CMD ["python", "api.py"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  cnc-monitor:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/backend/data
    environment:
      - DB_PATH=/app/backend/data/machines_data.db
    restart: unless-stopped
```

### Build and Run

```bash
# Build image
docker build -t cnc-monitor .

# Run container
docker run -d -p 5000:5000 --name cnc-monitor cnc-monitor

# Or use docker-compose
docker-compose up -d
```

### Docker Hub

```bash
# Tag and push
docker tag cnc-monitor yourusername/cnc-monitor:latest
docker push yourusername/cnc-monitor:latest
```

## Production Considerations

### Reverse Proxy with Nginx

1. **Install Nginx**
   ```bash
   sudo apt install nginx
   ```

2. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/cnc-monitor
   ```

   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:5000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Enable Site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/cnc-monitor /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

### Database Backup

Create backup script `backup.sh`:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/cnc-monitor"
DB_PATH="/opt/cnc-machine-monitor/backend/machines_data.db"

mkdir -p $BACKUP_DIR
sqlite3 $DB_PATH ".backup $BACKUP_DIR/machines_data_$DATE.db"

# Keep only last 30 days
find $BACKUP_DIR -name "machines_data_*.db" -mtime +30 -delete
```

Add to crontab:
```bash
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

### Monitoring

#### Application Logs

```bash
# View logs
sudo journalctl -u cnc-monitor -f

# Or if using Docker
docker logs -f cnc-monitor
```

#### Health Check Endpoint

Add to `api.py`:
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
```

#### Uptime Monitoring

Use services like:
- UptimeRobot (free)
- Pingdom
- StatusCake

### Performance Tuning

1. **Use Gunicorn** (instead of uvicorn directly)
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app --bind 0.0.0.0:5000
   ```

2. **Database Optimization**
   - Regular VACUUM
   - Index optimization
   - Consider PostgreSQL for larger deployments

3. **Caching**
   - Add Redis for caching
   - Cache dashboard data
   - Reduce database queries

### Security

1. **Change Default Settings**
   - Modify default machine names
   - Change API endpoints if needed

2. **Enable Authentication**
   - Add API key authentication
   - Implement user login

3. **Firewall Rules**
   ```bash
   # Allow only specific IPs
   sudo ufw allow from YOUR_IP to any port 5000
   ```

4. **Rate Limiting**
   - Implement rate limiting on API endpoints
   - Protect against DDoS

5. **Regular Updates**
   ```bash
   # Update dependencies
   pip install -r requirements.txt --upgrade
   
   # Update system
   sudo apt update && sudo apt upgrade
   ```

### Scaling

For high-traffic deployments:

1. **Load Balancing**
   - Use Nginx or HAProxy
   - Multiple backend instances

2. **Database**
   - Move to PostgreSQL
   - Use connection pooling
   - Read replicas

3. **Caching**
   - Redis for session data
   - CDN for static files

4. **Message Queue**
   - Use RabbitMQ or Redis for WebSocket scaling

## Maintenance

### Update Application

```bash
cd cnc-machine-monitor
git pull
pip install -r requirements.txt --upgrade
sudo systemctl restart cnc-monitor
```

### Database Maintenance

```bash
# Backup
sqlite3 machines_data.db ".backup machines_data_backup.db"

# Vacuum (optimize)
sqlite3 machines_data.db "VACUUM;"

# Check integrity
sqlite3 machines_data.db "PRAGMA integrity_check;"
```

### Log Rotation

Create `/etc/logrotate.d/cnc-monitor`:
```
/var/log/cnc-monitor/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload cnc-monitor > /dev/null
    endscript
}
```

## Support

For deployment issues:
- Check logs: `sudo journalctl -u cnc-monitor -n 100`
- Verify firewall: `sudo ufw status`
- Test connectivity: `curl http://localhost:5000/api/machines`

---

For questions, open an issue on GitHub!
