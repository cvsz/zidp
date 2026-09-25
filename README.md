# ZIdentity

**ZeaZ Identity & Account Security Platform** — the central identity, authentication, authorization, device-trust, recovery, and security-control plane for the ZeaZ ecosystem.

- Repository: `cvsz/zidentity`
- User portal: `account.zeaz.dev`
- Protocol target: OAuth 2.1 + OpenID Connect
- Authentication target: Passkeys/WebAuthn, FIDO2/security keys, MFA, and controlled password fallback
- Deployment target: self-hosted, cloud-native, cost-efficient ZeaZ infrastructure

> **Security note:** This project implements standards-based identity capabilities inspired by modern account-security products. It does not copy Apple proprietary implementation, protocols, source code, UI, or branding.

## Product scope

ZIdentity provides:

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
                    ZIdentity / OIDC / OAuth 2.1
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
        zPay                zWallet              zTTato
          │                    │                    │
        zBiz                  zVeo               ZTrader
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                    Central Security Plane
```

Applications receive only the identity claims/scopes they require. Recovery secrets, authentication credentials, and unrelated application data remain outside application trust boundaries.

## Security model

Security-sensitive operations use recent authentication and may require phishing-resistant step-up authentication, trusted-device confirmation, security delay, or additional policy checks. Account recovery is a separate state machine and must never become an authentication bypass.

The project follows the engineering direction in `AGENTS.md` and the canonical AI implementation contract in [`docs/AI_MASTER_PRODUCTION_PROMPT.md`](docs/AI_MASTER_PRODUCTION_PROMPT.md).

Relevant standards and guidance include WebAuthn/FIDO2, OAuth 2.1, OpenID Connect, OWASP ASVS/API Security, and NIST digital-identity guidance. Standards are implementation targets; exact conformance must be verified against the deployed components and test suite.

## Repository structure

```text
.github/                       GitHub automation and governance
docs/
  adr/                         Architecture Decision Records
  AI_MASTER_PRODUCTION_PROMPT.md
  architecture.md
  development.md
  release.md
AGENTS.md                      Agent/repository contract
SECURITY.md                    Vulnerability reporting and security policy
IMPLEMENTATION-CHECKLIST.md    Production implementation gate
ROADMAP.md                     Delivery roadmap
```

Implementation components should be added under clearly bounded domains rather than creating speculative scaffolding.

## Development principles

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

- [`docs/AI_MASTER_PRODUCTION_PROMPT.md`](docs/AI_MASTER_PRODUCTION_PROMPT.md)
- [`docs/architecture.md`](docs/architecture.md)
- [`IMPLEMENTATION-CHECKLIST.md`](IMPLEMENTATION-CHECKLIST.md)
- [`SECURITY.md`](SECURITY.md)
- [`ROADMAP.md`](ROADMAP.md)
