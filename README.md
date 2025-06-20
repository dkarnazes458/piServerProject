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
   # Create PostgreSQL database
   createdb pi_server_db
   # Run migrations (once implemented)
   python backend/migrate.py
   ```

5. **Environment Variables**
   ```bash
   # Backend .env file
   DATABASE_URL=postgresql://username:password@localhost:5432/pi_server_db
   SECRET_KEY=your-secret-key
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
