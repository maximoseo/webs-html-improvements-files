# SKILL: Apprise
**Source:** https://github.com/caronc/apprise
**Domain:** code
**Trigger:** When sending notifications to multiple services (Slack, Discord, Telegram, email, SMS, etc.) from code or CLI

## Summary
A Python notification library and CLI that supports 100+ notification services with a unified URL-based syntax. One library to send to Telegram, Discord, Slack, AWS SNS, Gotify, and almost any other notification service.

## Key Patterns
- Unified URL syntax: `service://params` for all notification services
- Supports attachments and images where services allow
- Asynchronous sending for fast multi-service delivery
- CLI tool ships with library: `apprise -b "message" service://...`
- Configuration files (YAML/TEXT) for reusable notification setups
- Plugin/hook system for custom notification services

## Usage
Install: `pip install apprise`. Use URL builder at appriseit.com for constructing service URLs. Chain multiple service URLs to notify several platforms at once.

## Code/Template
```python
import apprise
a = apprise.Apprise()
a.add("slack://tokenA/tokenB/tokenC/#channel")
a.add("discord://webhook_id/webhook_token")
a.notify(body="Deploy complete!", title="CI/CD")

# CLI usage:
# apprise -b "Hello World" discord://webhook_id/token
# apprise -b "Alert!" slack://token/#channel tgram://bottoken/chatid
```
