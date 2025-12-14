# Integration Setup Guide

## Quick Start

1. Copy configuration template:
   ```
   cp integrations.json.sample integrations.json
   ```

2. Edit integrations.json and enable desired integrations

3. Test connections:
   ```
   python test_integrations.py
   ```

## Slack Integration

### Setup (10 minutes)

1. Go to https://api.slack.com/apps
2. Create New App - From scratch
3. Name: Enhanced Budget Pro
4. Enable Incoming Webhooks
5. Add New Webhook to Workspace
6. Copy webhook URL

### Configure

Edit integrations.json:
```json
{
  "slack": {
    "enabled": true,
    "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
  }
}
```

### Test

```bash
python test_integrations.py
```

You should see: Slack connection: OK

## Webhook Integration

### Setup

Create an endpoint that accepts POST requests:

```javascript
// Example Node.js server
const express = require('express');
const app = express();

app.post('/api/budget-webhook', express.json(), (req, res) => {
  console.log('Received:', req.body);
  res.status(200).send('OK');
});

app.listen(3000);
```

### Configure

```json
{
  "webhook": {
    "enabled": true,
    "url": "https://your-server.com/api/budget-webhook",
    "auth_token": "optional-secret-token"
  }
}
```

### Payload Format

```json
{
  "event": "analysis_complete",
  "timestamp": "2025-12-13T17:30:00",
  "script_info": {
    "name": "script.fdx",
    "scenes": 12,
    "characters": 8
  },
  "budget": {
    "total": 111215.00
  }
}
```

## Google Sheets Integration

### Setup (30 minutes)

1. Go to https://console.cloud.google.com/
2. Create new project
3. Enable Google Sheets API
4. Create Service Account
5. Download JSON key file
6. Create Google Sheet
7. Share with service account email
8. Install dependencies:
   ```
   pip install google-api-python-client google-auth
   ```

### Configure

```json
{
  "sheets": {
    "enabled": true,
    "spreadsheet_id": "YOUR_SPREADSHEET_ID",
    "service_account_file": "./config/service-account.json"
  }
}
```

## Usage

Integrations run automatically after CLI analysis:

```bash
python -m src.cli analyze --input script.fdx --out ./output
```

You'll see integration status in output:
```
Slack export: OK
Webhook export: OK
Sheets export: OK
```

## Troubleshooting

### Slack webhook invalid
- Verify URL starts with https://hooks.slack.com/
- Check webhook wasn't deleted in Slack

### Webhook timeout
- Verify URL is accessible
- Check firewall rules
- Test with curl

### Google Sheets permission denied
- Verify service account has Editor access
- Check spreadsheet_id is correct
- Ensure API is enabled

## Security

- Never commit integrations.json
- Add to .gitignore
- Use environment variables in production
- Rotate tokens regularly
