# Enhanced Budget Pro - Integration Quick Start

## What You Just Got

**3 Production-Ready Integrations:**
- Slack - Get budget notifications in your team channel
- Webhook - Send analysis data to any HTTP endpoint
- Google Sheets - Export budgets for spreadsheet collaboration

## 5-Minute Slack Setup

1. **Create Slack App** (2 min)
   - Go to: https://api.slack.com/apps
   - Click "Create New App" > "From scratch"
   - Name: "Budget Pro"
   - Select your workspace
   - Click "Incoming Webhooks" in sidebar
   - Toggle ON
   - Click "Add New Webhook to Workspace"
   - Select channel (e.g., #production)
   - Click "Allow"
   - Copy the webhook URL (starts with https://hooks.slack.com/)

2. **Configure** (1 min)
   ```bash
   cp integrations.json.sample integrations.json
   ```
   
   Edit integrations.json:
   ```json
   {
     "slack": {
       "enabled": true,
       "webhook_url": "PASTE_YOUR_WEBHOOK_URL_HERE"
     }
   }
   ```

3. **Test** (30 sec)
   ```bash
   python test_integrations.py
   ```
   
   You should see:
   ```
   [OK] slack: PASS
   [OK] slack: SUCCESS
   ```

4. **Use It** (30 sec)
   ```bash
   python -m src.cli analyze --input samples/test_script.fdx --out ./output
   ```
   
   Check your Slack channel - you'll see:
   ```
   Budget Analysis Complete: test_script.fdx
   Total Budget: ,215.00
   Scenes: 12
   Characters: 8
   Status: Ready for review
   ```

## What Happens Automatically

Every time you run CLI analysis:
1. Script is analyzed
2. Budget is calculated
3. Exports are generated
4. **Integrations are triggered**
5. Team gets notified

No extra commands needed!

## Webhook Integration (10 minutes)

Send full analysis JSON to your own server:

```json
{
  "webhook": {
    "enabled": true,
    "url": "https://your-server.com/api/budget-webhook",
    "auth_token": "optional-secret-token"
  }
}
```

Payload you'll receive:
```json
{
  "event": "analysis_complete",
  "script_info": {"name": "...", "scenes": 12, "characters": 8},
  "budget": {"total": 111215.00},
  "output_path": "./output"
}
```

## Google Sheets (30 minutes)

Requires Google Cloud setup:
1. Create Google Cloud project
2. Enable Sheets API
3. Create service account
4. Download JSON key
5. Share spreadsheet with service account email

See docs/INTEGRATION_SETUP.md for full guide.

## Architecture

```
src/IntegrationEngine/
├── base_adapter.py           # Abstract adapter interface
├── integration_manager.py     # Orchestration
└── adapters/
    ├── slack_adapter.py      # Slack notifications
    ├── webhook_adapter.py    # Generic HTTP
    └── sheets_adapter.py     # Google Sheets
```

**Design:** Adapter pattern with JSON config

## Troubleshooting

**Test fails with connection error:**
- Verify webhook URL is correct
- Check internet connection
- For Slack: webhook must start with https://hooks.slack.com/

**No notifications sent:**
- Check integrations.json exists (not .sample)
- Verify enabled: true
- Run: python test_integrations.py

**Import error:**
- Install: pip install requests
- For Sheets: pip install google-api-python-client google-auth

## Next Steps

1. Set up Slack (5 min) - Immediate team notifications
2. Set up Webhook (optional) - Custom integrations
3. Set up Sheets (optional) - Collaborative budgeting

**Ready to go?**
```bash
cp integrations.json.sample integrations.json
# Add your Slack webhook
python test_integrations.py
python -m src.cli analyze --input samples/test_script.fdx --out ./output
```

Your team gets notified. Done. :rocket:
