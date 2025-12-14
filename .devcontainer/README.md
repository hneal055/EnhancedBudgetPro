# Dev Container Setup

## Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed
- [VS Code](https://code.visualstudio.com/) installed
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) installed

### First Time Setup (2 minutes)

1. **Open in Dev Container**
   - Open this project in VS Code
   - Click notification: "Reopen in Container"
   - OR: Press F1 > "Dev Containers: Reopen in Container"

2. **Wait for Build** (2-3 minutes first time)
   - Container downloads (~500MB)
   - Python 3.12 installs
   - Dependencies install automatically
   - VS Code extensions install

3. **Start Developing**
   - Everything is ready!
   - No manual setup needed

## What's Included

### Pre-installed Tools
- Python 3.12.x
- All requirements.txt packages
- pytest, black, flake8, ruff
- Git + Oh My Zsh
- VS Code extensions (Pylance, Python, Black, etc.)

### Pre-configured Ports
- **5000** - Flask web app
- **8501** - Streamlit UI

### Quick Commands (in terminal)
```bash
analyze --input samples/test_script.fdx --out ./output   # Analyze script
ui                                                       # Launch Streamlit
web                                                      # Launch Flask
tests                                                    # Run test suite
test-integrations                                        # Test integrations
format                                                   # Format code with Black
lint                                                     # Lint with flake8
```

## Development Workflow

### Running the Application

**CLI:**
```bash
python -m src.cli analyze --input samples/test_script.fdx --out ./output
```

**Streamlit UI:**
```bash
streamlit run ui_app.py
# Opens on port 8501 (auto-forwarded)
```

**Flask Web App:**
```bash
python web_app.py
# Opens on port 5000 (auto-forwarded)
```

### Testing

**Run all tests:**
```bash
pytest tests/ -v
```

**Run specific test:**
```bash
pytest tests/test_ingestion.py -v
```

**Test integrations:**
```bash
python test_integrations.py
```

### Code Quality

**Format code:**
```bash
black src/ tests/
```

**Check formatting:**
```bash
black --check src/ tests/
```

**Lint code:**
```bash
flake8 src/ tests/
```

**Run all checks:**
```bash
black --check src/ tests/ && flake8 src/ tests/ && pytest tests/
```

## Container Management

### Rebuild Container
If you update requirements.txt or devcontainer.json:
- Press F1 > "Dev Containers: Rebuild Container"

### Stop Container
- Press F1 > "Dev Containers: Reopen Folder Locally"
- Container stops automatically

### Remove Container
```bash
docker rm enhanced-budget-pro-dev
```

### View Container Logs
```bash
docker logs enhanced-budget-pro-dev
```

## Troubleshooting

### Container won't start
1. Check Docker Desktop is running
2. Restart Docker Desktop
3. Press F1 > "Dev Containers: Rebuild Container"

### Dependencies not installing
```bash
# Inside container terminal:
pip install -r requirements.txt
```

### Port already in use
```bash
# Change port in devcontainer.json
"forwardPorts": [5001, 8502]
```

### Extensions not loading
1. Press F1 > "Developer: Reload Window"
2. OR rebuild container

## VS Code Extensions Included

- **ms-python.python** - Python language support
- **ms-python.vscode-pylance** - Fast Python IntelliSense
- **ms-python.black-formatter** - Code formatting
- **ms-python.flake8** - Code linting
- **charliermarsh.ruff** - Fast Python linter
- **streetsidesoftware.code-spell-checker** - Spell checking
- **eamodio.gitlens** - Git supercharged
- **github.vscode-pull-request-github** - GitHub integration

## Settings Applied

- **Auto-format on save** with Black (100 char line length)
- **Auto-organize imports** on save
- **Pylance** for type checking and IntelliSense
- **pytest** as default test framework
- **Flake8** for linting

## Environment Variables

Set in devcontainer.json:
- PYTHONUNBUFFERED=1 - Real-time output
- PYTHONDONTWRITEBYTECODE=1 - No .pyc files
- PIP_NO_CACHE_DIR=1 - Smaller container

## Benefits

### For New Developers
- **5 minutes** to productive (vs. 30-45 min manual setup)
- No Python version conflicts
- No missing dependencies
- Consistent environment across team

### For Testing
- Isolated environment
- Reproducible test runs
- Same environment as CI/CD
- Easy integration testing

### For Team
- Everyone uses same tools
- Same code formatting
- Same linting rules
- No "works on my machine"

## Advanced Usage

### Custom Dockerfile
To add system packages, uncomment dockerfile in devcontainer.json:
```json
{
  "name": "Enhanced Budget Pro",
  "build": {
    "dockerfile": "Dockerfile"
  }
  // ...
}
```

Then edit .devcontainer/Dockerfile

### Multiple Containers
For database/Redis/etc, use docker-compose.yml:
```json
{
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace"
}
```

### Environment Variables
Add to .devcontainer/.env:
```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
DATABASE_URL=postgresql://...
```

Reference in devcontainer.json:
```json
{
  "runArgs": ["--env-file", ".devcontainer/.env"]
}
```

## CI/CD Integration

Use same container in GitHub Actions:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: mcr.microsoft.com/devcontainers/python:3.12
    steps:
      - uses: actions/checkout@v3
      - run: pip install -r requirements.txt
      - run: pytest tests/
```

## Resources

- [Dev Containers Documentation](https://code.visualstudio.com/docs/devcontainers/containers)
- [Python Dev Container](https://github.com/microsoft/vscode-dev-containers/tree/main/containers/python-3)
- [Project README](../README.md)

---

**Questions?** The container is ready to use out of the box. Just open in VS Code and click "Reopen in Container"!
