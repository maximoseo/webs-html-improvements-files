# WORKFLOW MAP

This map illustrates how the newly integrated skills interconnect during a standard agentic task.

```mermaid
graph TD
    A[User Request] --> B{Determine Intent}
    
    B -->|Code / Arch| C[Spec-Driven Dev Loop]
    B -->|Web / UI| D[HTML Redesign Mega Skill]
    B -->|Research| E[Academic Orchestrator]
    B -->|General Automation| F[Spider King / Custom Tooling]

    C --> C1(Plan / Draft Spec)
    C1 --> C2(User Approval)
    C2 --> C3(Implement Code)
    C3 --> G

    D --> D1(Hue Brand Extractor)
    D1 --> D2(RTL / Layout Engine)
    D2 --> D3(CTA / Conversion Engine)
    D3 --> D4(Accessibility Audit)
    D4 --> G

    E --> E1(Data Extraction)
    E1 --> E2(Figure / Plot Separation)
    E2 --> G

    F --> F1(Protocol Reversal)
    F1 --> G

    G[AntiVibe / Eval Loop] --> H{Validation Pass?}
    H -->|No| I[Self-Correction]
    I --> G
    H -->|Yes| J[Talk Normal Output]
    J --> K[Delivery to User]
```

## Key Workflow Stages:
1. **Intake:** The agent receives the prompt and immediately applies `Talk Normal` constraints to its internal monologues.
2. **Routing:** The request is categorized to trigger the correct mega-skill.
3. **Execution:** Specialized routines (e.g., RTL formatting, protocol reversal) are applied.
4. **Validation:** The `AntiVibe` evaluation loop ensures the agent hasn't hallucinated or skipped constraints (e.g., verifying exactly ONE `<h1>`).
5. **Delivery:** Concise, exact delivery of the required assets.
