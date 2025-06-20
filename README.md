# Pi Server Project

Full-stack web application for practicing development-to-deployment workflow using GitHub. Develop on local machine, deploy to Raspberry Pi server.

## Tech Stack

- **Frontend**: Vite + React
- **Backend**: Python + Flask
- **Database**: PostgreSQL
- **Deployment**: Raspberry Pi

## Project Structure

```
piServerProject/
├── frontend/          # Vite + React application
├── backend/           # Python + Flask API
├── database/          # PostgreSQL schemas and migrations
├── docs/              # Documentation
├── README.md          # This file
└── PROJECTLOG.md      # Development log and updates
```

## Setup Instructions

### Prerequisites

- Node.js (v18+ **Required for Vite**)
- Python (v3.9+)
- PostgreSQL
- Git

### Raspberry Pi Setup

**Node.js Version Issue**: Vite requires Node.js v18+ with modern crypto support. Raspberry Pi often has older versions.

**Recommended: Use NVM (Node Version Manager)**:
```bash
# Install NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Reload shell or restart terminal
source ~/.bashrc

# Install and use Node.js v18
nvm install 18
nvm use 18
nvm alias default 18

# Verify version
node --version  # Should show v18+
```

**Alternative: Manual NodeSource Install**:
```bash
# Remove old Node.js completely
sudo apt remove --purge nodejs npm
sudo apt autoremove

# Install Node.js v18+ using NodeSource
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify version
node --version  # Should show v18+
```

**If still getting v16**: The system package manager may be overriding. Use NVM method above.

### Raspberry Pi Firewall Configuration

**Check if ports are blocked**:
```bash
# Check firewall status
sudo ufw status

# Check if ports are listening
sudo netstat -tlnp | grep :5000
sudo netstat -tlnp | grep :5173
```

**Open required ports**:
```bash
# Allow development ports
sudo ufw allow 5000/tcp
sudo ufw allow 5173/tcp

# Optional: Allow SSH if needed
sudo ufw allow ssh

# Enable firewall (if not already enabled)
sudo ufw enable

# Verify rules
sudo ufw status verbose
```

**Alternative: Disable firewall for development**:
```bash
sudo ufw disable
```

### Troubleshooting Network Access

**Step 1: Verify services are listening**:
```bash
# Check if services bind to all interfaces (should show 0.0.0.0)
sudo netstat -tlnp | grep :5000
sudo netstat -tlnp | grep :5173

# Alternative check
sudo ss -tlnp | grep :5173
```

**Step 2: Test local connectivity**:
```bash
# Test from Pi itself
curl http://localhost:5173
curl http://192.168.1.165:5173

# Check Pi's IP address
ip addr show
hostname -I
```

**Step 3: Firewall troubleshooting**:
```bash
# Check firewall status
sudo ufw status

# Temporarily disable for testing
sudo ufw disable

# Try accessing from another device now
```

**Step 4: Router/Network issues**:
- Some routers block inter-device communication
- Try accessing from Pi's browser first: `http://localhost:5173`
- Check if other devices can ping the Pi: `ping 192.168.1.165`

### Chrome Access Issues

**Chrome blocks local network access by default. Solutions**:

1. **Use a different browser**:
   - Firefox, Safari, or Edge work better for local development

2. **Chrome flags** (temporary fix):
   - Go to `chrome://flags/#block-insecure-private-network-requests`
   - Set to "Disabled"
   - Restart Chrome

3. **Add Chrome launch flag**:
   ```bash
   # Launch Chrome with flag
   google-chrome --disable-web-security --user-data-dir="/tmp/chrome_dev"
   ```

4. **Use HTTPS** (advanced):
   - Set up SSL certificates for local development
   - Access via `https://192.168.1.165:5173`

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd piServerProject
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Database Setup**
   ```bash
   # Install PostgreSQL
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   
   # Start PostgreSQL service
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   
   # Create database and user
   sudo -u postgres psql
   CREATE DATABASE pi_server_db;
   CREATE USER pi_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE pi_server_db TO pi_user;
   \q
   
   # Test connection
   psql -h localhost -U pi_user -d pi_server_db
   ```

5. **Environment Variables**
   ```bash
   # Create backend/.env file
   cd backend
   cp .env.example .env
   
   # Edit .env with your values:
   DATABASE_URL=postgresql://pi_user:your_password@localhost:5432/pi_server_db
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   FLASK_ENV=development
   ```

### Running the Application

1. **Start Backend**
   ```bash
   cd backend
   python app.py
   # Available at: http://0.0.0.0:5000 (all network interfaces)
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   npm run dev
   # Available at: http://0.0.0.0:5173 (all network interfaces)
   ```

3. **Access from other devices**
   ```
   Frontend: http://[PI_IP_ADDRESS]:5173
   Backend:  http://[PI_IP_ADDRESS]:5000
   ```

### Deployment to Raspberry Pi

1. **Push changes to GitHub**
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

2. **On Raspberry Pi**
   ```bash
   git pull origin main
   # Follow setup instructions above
   # Configure systemd services for production
   ```

## Current Status

🚧 **In Development**: Authentication system implementation

## Features

- [ ] User Authentication (Registration, Login, Logout)
- [ ] User Management
- [ ] Database Integration
- [ ] API Endpoints
- [ ] Frontend Components
- [ ] Deployment Scripts

## Development Workflow

1. Develop locally
2. Test functionality
3. Commit changes
4. Push to GitHub
5. Deploy to Raspberry Pi
6. Verify deployment

See [PROJECTLOG.md](./PROJECTLOG.md) for detailed development updates and documentation.
