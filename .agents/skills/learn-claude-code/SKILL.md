# SKILL: Learn Claude Code - Harness Engineering for Real Agents
**Source:** https://github.com/shareAI-lab/learn-claude-code
**Domain:** code
**Trigger:** When understanding the theory behind AI agent harness engineering, distinguishing real agents from prompt-plumbing pipelines, or teaching agent architecture fundamentals

## Summary
Deep theoretical and practical guide to harness engineering for AI agents. Distinguishes between "training agents" (model) and "harness engineering" (environment/infrastructure). Teaches how to build the vehicle that lets trained models operate effectively.

## Key Patterns
- Agent = Model (trained neural network) + Harness (environment/infrastructure)
- Agency comes from model training, not code orchestration
- Harness is the vehicle; model is the driver
- Critique of prompt-plumbing "agents" as Rube Goldberg machines
- Historical evidence: DQN, OpenAI Five, AlphaStar, LLM agents all prove agency is trained

## Usage
Read the conceptual framework to inform how you design Claude Code harnesses. Focus on giving Claude the right environment (tools, context, scope) rather than building complex orchestration logic.

## Code/Template
Key insight: "You cannot engineer your way to agency. Agency is learned, not programmed."
When building harnesses: minimize orchestration logic, maximize tool quality and context clarity.
