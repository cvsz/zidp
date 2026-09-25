# ZIDP — ZeaZ Identity Provider

**ZeaZ Identity Provider (ZIDP)** is the central identity, authentication, authorization, device-trust, recovery, federation, and account-security plane for the ZeaZ ecosystem.

- Repository: `cvsz/zidp`
- User portal: `https://account.zeaz.dev`
- Protocol target: OAuth 2.1 + OpenID Connect
- Authentication target: Passkeys/WebAuthn, FIDO2/security keys, MFA, and controlled password fallback
- Deployment target: self-hosted, cloud-native, cost-efficient ZeaZ infrastructure

> **Security note:** ZIDP implements standards-based identity capabilities inspired by modern account-security products. It does not copy Apple proprietary implementation, protocols, source code, UI, or branding.

## Product scope

ZIDP provides:
- Account and identity lifecycle
- Passkeys / WebAuthn / FIDO2
- TOTP MFA and security keys
- Trusted-device lifecycle
- Risk-based and step-up authentication
- Session lifecycle and global revocation
- Recovery keys and recovery contacts
- Security-delay/high-risk protection
- OAuth 2.1 / OpenID Connect / SSO
- RBAC / ABAC and scoped authorization
- Service accounts and machine-to-machine authentication
- OAuth consent and client lifecycle management
- Immutable security/audit events
- Security notifications
- Privacy/data minimization controls
- Secure support/admin access
- Operational observability, backup, recovery, and incident-response controls

## ZeaZ ecosystem role

```text
                         account.zeaz.dev
                               │
                         ZIDP / OIDC
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
        zPay                zWallet              zTTato
        zBiz                  zVeo               ZTrader
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                    Central Security Plane
```

Applications receive only the identity claims/scopes they require. Recovery secrets, authentication credentials, and unrelated application data remain outside application trust boundaries.

## Security model

Security-sensitive operations use recent authentication and may require phishing-resistant step-up authentication, trusted-device confirmation, security delay, or additional policy checks. Account recovery is a separate state machine and must never become an authentication bypass.

The canonical AI implementation contract is `docs/AI_MASTER_PRODUCTION_PROMPT.md`; repository behavior is governed by `AGENTS.md`.

Relevant standards and guidance include WebAuthn/FIDO2, OAuth 2.1, OpenID Connect, OWASP ASVS/API Security, and NIST digital-identity guidance. Exact conformance must be verified against deployed components and tests.

## Repository structure

```text
.github/
docs/
  adr/
  AI_MASTER_PRODUCTION_PROMPT.md
  architecture.md
  development.md
  release.md
AGENTS.md
SECURITY.md
IMPLEMENTATION-CHECKLIST.md
ROADMAP.md
```

## Engineering principles

- Secure by default
- Least privilege
- Fail closed for security-sensitive decisions
- Standards before custom protocols
- Small, reviewable changes
- Strong typing and explicit contracts
- Defense in depth
- Data minimization
- Reproducible builds
- Observable production behavior
- No secrets in source control
- No security bypasses to make CI green

## Production readiness

A production-ready claim requires evidence from implementation, tests, security checks, deployment validation, and rollback readiness. Documentation or badges alone are not evidence of readiness.

See:
- [AI Master Production Prompt](docs/AI_MASTER_PRODUCTION_PROMPT.md)
- [Architecture](docs/architecture.md)
- [Implementation Checklist](IMPLEMENTATION-CHECKLIST.md)
- [Security Policy](SECURITY.md)
- [Roadmap](ROADMAP.md)
