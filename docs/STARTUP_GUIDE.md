# Enhanced Budget Pro - Daily Startup Guide

**Version:** 1.0.0  
**Last Updated:** December 14, 2025

---

## 🚀 Automated Startup (Recommended)

### Quick Start

```bash
./start_enhanced_budget_pro.sh
```

This single command handles everything:
1. ✅ Checks Git status and offers to pull latest changes
2. ✅ Verifies Python environment
3. ✅ Activates/creates virtual environment
4. ✅ Installs/updates dependencies
5. ✅ Clears Python cache
6. ✅ Kills existing Streamlit processes
7. ✅ Checks port availability
8. ✅ Displays project status
9. ✅ Prompts for launch mode

---

## 📋 Launch Options

When you run the startup script, you'll see:

```
================================================
   Launch Options
================================================
1) Start Streamlit UI (Recommended)
2) Start Flask Web App
3) Run Tests
4) Exit (manual start)

Select option (1-4):
```

### Option 1: Streamlit UI (Recommended)
- **Best for:** Interactive dashboard, data visualization, producer insights
- **URL:** http://localhost:8501
- **Features:** Full UI with AI Producer Mode

### Option 2: Flask Web App
- **Best for:** Web-based file upload, batch processing
- **URL:** http://localhost:5000
- **Features:** Upload scripts, download reports

### Option 3: Run Tests
- **Best for:** Validating installation, checking for issues
- **Output:** Full test suite results
- **Auto-prompt:** Optionally starts Streamlit after tests

### Option 4: Manual Start
- **Best for:** Advanced users, debugging
- **Output:** Shows manual commands
- **Usage:** Run commands yourself

---

## �� Manual Startup (Advanced)

If you prefer manual control:

### Step 1: Activate Virtual Environment
```bash
# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Clear Cache (Optional)
```bash
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
```

### Step 4: Start Application
```bash
# Streamlit UI
streamlit run ui_app.py

# Flask Web App
python web_app.py

# CLI
python -m src.cli analyze --input samples/test_script.fdx --out ./output
```

---

## 🐳 Docker Startup (DevContainer)

If running in a DevContainer:

### Automatic Activation
The startup script works in DevContainers automatically.

### Manual DevContainer Start
```bash
# Already in container with Python and dependencies
./start_enhanced_budget_pro.sh
```

---

## 🔄 Daily Workflow

### Morning Routine
```bash
cd /path/to/EnhancedBudgetPro
./start_enhanced_budget_pro.sh
```

**The script handles:**
- Git updates
- Dependency refreshes
- Cache clearing
- Process cleanup
- Port management

### During Development
Keep Streamlit running, it will auto-reload on file changes.

### End of Day
Just close the terminal or press `Ctrl+C` to stop.

---

## 🛠️ Troubleshooting

### Issue: "Permission denied"
```bash
chmod +x start_enhanced_budget_pro.sh
```

### Issue: "Port 8501 already in use"
The script automatically handles this, but manually:
```bash
lsof -ti:8501 | xargs kill -9
```

### Issue: "Virtual environment not activating"
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Streamlit not found"
```bash
pip install --upgrade streamlit
```

### Issue: "Git pull fails"
```bash
git stash
git pull origin main
git stash pop
```

---

## ⚙️ Systemd Service (Linux)

For automatic startup on Linux boot:

### Create Service File
```bash
sudo nano /etc/systemd/system/enhanced-budget-pro.service
```

### Service Configuration
```ini
[Unit]
Description=Enhanced Budget Pro Streamlit Service
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/EnhancedBudgetPro
Environment="PATH=/path/to/EnhancedBudgetPro/.venv/bin"
ExecStart=/path/to/EnhancedBudgetPro/.venv/bin/streamlit run ui_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable and Start
```bash
sudo systemctl enable enhanced-budget-pro
sudo systemctl start enhanced-budget-pro
sudo systemctl status enhanced-budget-pro
```

---

## 🪟 Windows Task Scheduler

For automatic startup on Windows:

### Create Batch File
```batch
@echo off
cd C:\path\to\EnhancedBudgetPro
call .venv\Scripts\activate
streamlit run ui_app.py
```

### Schedule Task
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: At log on
4. Action: Start a program
5. Program: `C:\path\to\EnhancedBudgetPro\start.bat`

---

## 🍎 macOS LaunchAgent

For automatic startup on macOS:

### Create Plist File
```bash
nano ~/Library/LaunchAgents/com.enhancedbudgetpro.plist
```

### LaunchAgent Configuration
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.enhancedbudgetpro</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/EnhancedBudgetPro/start_enhanced_budget_pro.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
```

### Load LaunchAgent
```bash
launchctl load ~/Library/LaunchAgents/com.enhancedbudgetpro.plist
```

---

## 📊 Health Checks

### Check Running Status
```bash
# Check if Streamlit is running
pgrep -f streamlit

# Check port usage
lsof -i :8501

# Check logs (if running as service)
journalctl -u enhanced-budget-pro -f
```

### Verify Installation
```bash
cd /path/to/EnhancedBudgetPro
python -c "import streamlit; print(streamlit.__version__)"
python -c "import pandas; print(pandas.__version__)"
```

---

## 🔐 Security Notes

### Production Deployment
- Change default ports
- Enable authentication
- Use HTTPS/TLS
- Restrict network access
- Set up firewall rules

### Development
- Keep on localhost
- Don't expose to internet
- Use virtual environment
- Keep dependencies updated

---

## 📝 Customization

### Modify Startup Script

Edit `start_enhanced_budget_pro.sh`:

```bash
# Change default port
streamlit run ui_app.py --server.port=8080

# Change browser behavior
streamlit run ui_app.py --server.headless=true

# Enable wider layout
streamlit run ui_app.py --theme.base="dark"
```

### Environment Variables

Create `.env` file:
```bash
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=false
STREAMLIT_THEME_BASE=light
```

---

## 🎯 Best Practices

### Daily Routine
1. Run `./start_enhanced_budget_pro.sh`
2. Select Streamlit UI option
3. Let auto-reload handle file changes
4. Close terminal when done

### Weekly Maintenance
1. Pull latest changes from Git
2. Update dependencies: `pip install --upgrade -r requirements.txt`
3. Run tests: `pytest tests/ -v`
4. Clear old output files

### Monthly Review
1. Check for security updates
2. Review logs for errors
3. Backup important data
4. Update documentation

---

## 🆘 Support

### Common Commands
```bash
# Full restart
./start_enhanced_budget_pro.sh

# Manual start
source .venv/bin/activate && streamlit run ui_app.py

# Test installation
python test_phase_12_0.py

# View logs
tail -f ~/.streamlit/logs/*.log
```

### Getting Help
- Check documentation in `docs/`
- Review `PROJECT_OVERVIEW.md`
- Check GitHub issues
- Contact: @hneal055

---

**Startup Guide Version:** 1.0.0  
**Compatible With:** Enhanced Budget Pro v12.0.0+

*"One command to rule them all."* 🚀
