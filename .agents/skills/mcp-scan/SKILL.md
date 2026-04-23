# SKILL: MCP-Scan - Security Scanner for MCP Servers
**Source:** https://github.com/rodolfboctor/mcp-scan
**Domain:** code
**Trigger:** When auditing MCP server configurations for security vulnerabilities, detecting prompt injection, leaked secrets, or supply-chain risks in AI tool setups

## Summary
Open-source security scanner that audits every MCP server configuration on your system, detecting data exfiltration, credential relay, prompt injection, typosquatting, and supply-chain vulnerabilities. Supports 16+ AI tool clients with zero network requests during scanning.

## Key Patterns
- 17+ security scanners: secrets, supply chain, prompt injection, data flow
- Data Flow Analysis to trace where data goes after MCP processing
- SARIF output for GitHub Security tab integration
- Custom security policies via .mcp-scan-policy.yml
- Compliance mapping: SOC 2, GDPR, HIPAA, PCI-DSS, NIST 800-53

## Usage
```bash
npx mcp-scan@latest              # Full security scan
npx mcp-scan@latest --json       # JSON output for CI/CD
npx mcp-scan@latest privacy      # Privacy assessment
npx mcp-scan@latest compliance   # Compliance report
npx mcp-scan@latest --ci --severity-threshold HIGH  # CI mode
```

## Code/Template
```yaml
# .mcp-scan-policy.yml
rules:
  - name: no-external-endpoints
    match:
      network_egress:
        not_in_domain: "*.mycompany.com"
    severity: HIGH
```
