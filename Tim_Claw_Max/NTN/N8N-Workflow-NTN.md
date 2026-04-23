# N8N Workflow - NTN Marketing Automation

## Overview
Capture leads from landing page → Notify → Nurture → CRM

## Trigger: Webhook (POST)
```
URL: https://ntn.app.n8n.cloud/webhook/lead
Method: POST
```

### Body (JSON)
```json
{
  "name": "ישראל ישראלי",
  "email": "test@example.com",
  "phone": "050-1234567",
  "service": "אוטומציית מיילים",
  "source": "NTN Landing Page",
  "timestamp": "2026-04-08T10:00:00Z"
}
```

---

## Workflow Nodes

### 1. Webhook (Trigger)
```
Node: Webhook
Name: Lead Capture
Path: /webhook/lead
Method: POST
```

### 2. Set / Data Transformation
```
Node: Set
Name: Clean Lead Data
Operations:
- name:="{{ $json.name }}"
- email:="{{ $json.email }}"
- phone:="{{ $json.phone }}"
- service:="{{ $json.service }}"
- source:="NTN Landing Page"
- created_at:="{{ $now() }}"
- lead_score:="50"
```

### 3. Filter
```
Node: IF
Name: Has Email?
Condition:
{{ $json.email }} CONTAINS "@"
```

### 4a. Email Notification (If Email Exists)
```
Node: Gmail / SendGrid
Name: Send Lead Alert
To: info@ntn.co.il
Subject: "ליד חדש! {{ $json.name }}"
Body:
שם: {{ $json.name }}
אימייל: {{ $json.email }}
טלפון: {{ $json.phone }}
שירות: {{ $json.service }}
מקור: {{ $json.source }}
```

### 4b. WhatsApp Notification
```
Node: WhatsApp (via API)
Name: WhatsApp Alert
To: {{ $json.phone }}
Message:
שלום {{ $json.name }},
תודה שפנית אלינו! 🎉
נציג יצור איתך קשר תוך 24 שעות.
NTN - אוטומציות שיווק
```

### 5. CRM Entry
```
Node: HubSpot / Pipedrive / Google Sheets
Name: Add to CRM
Operation: Create Contact
Fields:
- name: {{ $json.name }}
- email: {{ $json.email }}
- phone: {{ $json.phone }}
- lead_source: NTN Landing Page
- interested_service: {{ $json.service }}
- lead_score: 50
- tags: ["new-lead", "ntn"]
```

### 6. Email Sequence (Delay → Loop)
```
Node: Schedule (Delay)
Name: Wait 1 Hour
Delay: 1 hour

Node: Send Email
Name: Follow-up Email #1
To: {{ $json.email }}
Subject: "תודה על פנייתך! 👋"
Template: follow-up-1

Node: Wait 3 Days

Node: Send Email
Name: Follow-up Email #2
Subject: "הזדמנות לשיחה? 📞"
Template: follow-up-2

Node: Wait 7 Days

Node: Send Email
Name: Follow-up Email #3
Subject: "עוד לא דיברנו... 🤔"
Template: final-chance
```

### 7. Tag Lead (After Sequence)
```
Node: HubSpot / CRM
Name: Update Lead Score
Operation: Update Contact
- lead_status: "nurtured"
- lead_score: "80"
- tags: ["nurtured", "follow-up-complete"]
```

---

## Email Templates

### Template: follow-up-1
```
שלום {{name}},

תודה על פנייתך ל-NTN! 🙏

קיבלנו את הפנייה שלך בנושא {{service}}.
נציג מקצועי יצור איתך קשר תוך 24 שעות לשיחת היכרות קצרה.

בינתיים, הנה כמה מקרי הצלחה:
- עסק X: 300% עלייה בהמרות
- עסק Y: חיסכון של 20+ שעות בחודש

נשמח לעזור גם לך!

בברכה,
צוות NTN
```

### Template: follow-up-2
```
שלום {{name}},

מקווים שהכל בסדר! 

רק רצינו להזכיר שאנחנו כאן לכל שאלה.
אם עדיין מעניין אותך {{service}}, נשמח להציע שיחת ייעוץ חינם.

לקביעת שיחה: https://cal.com/ntn

או einfach ענה למייל הזה ונחזור אליך.

בברכה,
צוות NTN
```

### Template: final-chance
```
שלום {{name}},

שלחנו לך כבר 2 הודעות ולא קיבלנו תשובה.

אנחנו מבינים שאולי הזמן עדיין לא בשל.
לכן, החלטנו להציע לך:
- ייעוץ חינם בשווי 500₪
- ניתוח אוטומציה אישי לעסק שלך

ההצעה בתוקף ל-7 ימים נוספים.

לקביעת שיחה: https://cal.com/ntn

בברכה,
צוות NTN
```

---

## N8N Workflow JSON

```json
{
  "name": "NTN Lead Capture & Nurture",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "lead",
        "responseMode": "responseNode"
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1
    },
    {
      "parameters": {
        "values": {
          "string": [
            { "name": "name", "value": "={{ $json.name }}" },
            { "name": "email", "value": "={{ $json.email }}" },
            { "name": "phone", "value": "={{ $json.phone }}" },
            { "name": "service", "value": "={{ $json.service }}" },
            { "name": "source", "value": "NTN Landing Page" },
            { "name": "created_at", "value": "={{ $now() }}" },
            { "name": "lead_score", "value": "50" }
          ]
        }
      },
      "name": "Clean Data",
      "type": "n8n-nodes-base.set"
    },
    {
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": true
          },
          "conditions": [
            {
              "id": "has-email",
              "input2": "@",
              "operation": "contains",
              "leftValue": "={{ $json.email }}"
            }
          ]
        }
      },
      "name": "Check Email",
      "type": "n8n-nodes-base.filter"
    },
    {
      "parameters": {
        "to": "info@ntn.co.il",
        "subject": "ליד חדש! {{ $json.name }}",
        "body": "שם: {{ $json.name }}<br>אימייל: {{ $json.email }}<br>טלפון: {{ $json.phone }}<br>שירות: {{ $json.service }}"
      },
      "name": "Email Alert",
      "type": "n8n-nodes-base.gmail"
    },
    {
      "parameters": {
        "functionCode": "// WhatsApp notification via API\nconst phone = $json.phone;\nconst name = $json.name;\nconst message = `שלום ${name}, תודה שפנית אלינו! נציג יצור איתך קשר תוך 24 שעות. NTN`;\n\nreturn { phone, message };"
      },
      "name": "WhatsApp Notify",
      "type": "n8n-nodes-base.code"
    },
    {
      "parameters": {
        "operation": "create",
        "sheetId": "YOUR_GOOGLE_SHEET_ID",
        "range": "A1",
        "columns": "name,email,phone,service,source,created_at"
      },
      "name": "Add to Google Sheets",
      "type": "n8n-nodes-base.googleSheets"
    }
  ],
  "connections": {
    "Webhook": {
      "main": [["Clean Data"]]
    },
    "Clean Data": {
      "main": [["Check Email"]]
    },
    "Check Email": {
      "main": [["Email Alert"], ["WhatsApp Notify"]]
    },
    "Email Alert": {
      "main": [["Add to Google Sheets"]]
    }
  }
}
```

---

## Setup Instructions

### 1. Create N8N Account
- https://n8n.io/cloud
- או Self-hosted

### 2. Import Workflow
- העתק את ה-JSON
- Import ב-N8N → Workflows → Import

### 3. Configure Nodes
- **Gmail:** חבר חשבון Google
- **Google Sheets:** צור טבלת לידים
- **WhatsApp:** הגדר API (Twilio / ChatAPI)

### 4. Update Webhook URL
- שנה את ה-URL ב-Landing Page form

---

## Integration with Landing Page

ב-landing page, שנה את ה-form:

```html
<form action="https://ntn.app.n8n.cloud/webhook/lead" method="POST">
  <input type="text" name="name" required placeholder="שם מלא">
  <input type="email" name="email" required placeholder="אימייל">
  <input type="tel" name="phone" placeholder="טלפון">
  <select name="service">
    <option value="אוטומציית מיילים">אוטומציית מיילים</option>
    <option value="צ'אט בוטים">צ'אט בוטים</option>
    <option value="SMS/WhatsApp">SMS/WhatsApp</option>
    <option value="ניהול לידים">ניהול לידים</option>
  </select>
  <button type="submit">שלח</button>
</form>
```
