# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 0.1.x   | ✅        |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Report vulnerabilities by emailing: **n7for8572@gmail.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Affected versions
- Potential impact

### Response Timeline

| Action | Time |
| ------ | ---- |
| Initial acknowledgement | ≤ 48 hours |
| Triage and severity assessment | ≤ 5 days |
| Fix or mitigation | ≤ 30 days (critical: ≤ 7 days) |
| Public disclosure | After fix is released |

### Scope

In scope:
- Validation bypass via crafted `HttpRequest`
- Middleware security issues
- Dependency vulnerabilities

Out of scope:
- Vulnerabilities in Django or Pydantic themselves (report upstream)
- Issues in your own application code
