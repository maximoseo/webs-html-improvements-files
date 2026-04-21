# EXAMPLES: Skill Utilization

This document provides concrete examples of how the newly ingested and merged skills are applied in practice.

## Example 1: Applying the HTML Redesign Mega Skill
**Scenario:** A user provides a basic text layout for a WordPress blog post and asks for a professional HTML template.
**Action:** The agent invokes `html-redesign-mega`.
**Output Snippet:**
```html
<article dir="rtl" style="font-family: sans-serif; color: #1F2D3D;">
  <!-- TOC Component -->
  <details style="border: 1px solid #e2e8f0; border-radius: 8px;">
    <summary style="cursor: pointer; padding: 16px;">תוכן עניינים</summary>
    <div style="padding: 16px;">
      <a href="#section-1">למה לבחור בנו?</a>
    </div>
  </details>
  <!-- Content -->
  <h2 id="section-1" style="margin-top: 4rem;">למה לבחור בנו?</h2>
  <p style="line-height: 1.8;">...</p>
  <!-- Floating Scroll Top -->
  <button id="scrollTopBtn" style="position: fixed; bottom: 76px; left: 16px; width: 44px; height: 44px;">↑</button>
</article>
```

## Example 2: Applying Talk Normal & Caveman Mode
**Scenario:** The user asks, "Can you check if my code has any bugs?"
**Before:** "Hello! I would be absolutely delighted to help you check your code for bugs. Let me take a look at the file you provided and I will get back to you with my findings..."
**After (Activated Skill):** "Checking code. Found 2 syntax errors on lines 14 and 42. Fixes applied. Tests passing."

## Example 3: Applying Spec-Driven Development (SDD)
**Scenario:** User says "Build a login page."
**Action:** The agent halts code generation and outputs a spec matrix first.
**Output:**
```markdown
# Spec: Login Page
- **Inputs:** Email, Password, CSRF Token.
- **Validation:** Email regex, password length > 8.
- **States:** Idle, Loading, Error, Success.
- **Accessibility:** ARIA labels, focus trap.
Approve this spec before I write the implementation.
```

## Example 4: Applying Spider King (Protocol Reversing)
**Scenario:** User asks to scrape a dynamically loaded JS table.
**Action:** Instead of writing a fragile Puppeteer script to click buttons, the agent inspects the Network tab, identifies the underlying GraphQL/REST API, and writes a robust `fetch` wrapper targeting the API endpoint with the correct headers.
