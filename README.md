# ZIDP — ZeaZ Identity Provider

**ZeaZ Identity Provider (ZIDP)** is the central identity, authentication, authorization, device-trust, recovery, federation, and account-security plane for the ZeaZ ecosystem.

- Repository: cvsz/zidp
- User portal target: account.zeaz.dev
- Protocol target: OAuth 2.1 + OpenID Connect
- Authentication target: Passkeys/WebAuthn, FIDO2/security keys, MFA, and controlled password fallback
- Deployment target: self-hosted, cloud-native, cost-efficient ZeaZ infrastructure

> **Security note:** ZIDP uses standards-based identity capabilities. It does not copy proprietary Apple implementation, protocols, source code, UI, or branding.

## Product scope

ZIDP is intended to provide:
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

## Current executable baseline

The repository now contains a **local-development-only** Keycloak 26.8.1 runtime backed by PostgreSQL 17.11. It imports one development realm and one public browser client with an exact loopback callback and PKCE S256. CI starts this stack with ephemeral credentials and smoke-tests OIDC discovery, JWKS, redirect rejection, and disabled implicit/password grants.

This is not a production identity service. It does not yet implement ZeaZ tenant membership, RBAC/ABAC policy, risk and recovery policy, security audit integration, production client provisioning, or the account portal. No customer application is migrated to this issuer. The local HTTP endpoint must not be exposed through a tunnel, public DNS, or production traffic.

See docs/adr/0001-keycloak-dev-protocol-engine.md and docs/development.md before using the local runtime.

## ZeaZ ecosystem role

```text
                         account.zeaz.dev
                               |
                         ZIDP / OIDC
                               |
          +--------------------+--------------------+
          |                    |                    |
        zPay                zWallet              zTTato
        zBiz                  zVeo               ZTrader
          |                    |                    |
          +--------------------+--------------------+
                               |
                    Central Security Plane
```

Applications must receive only the identity claims/scopes they require. Recovery secrets, authentication credentials, and unrelated application data remain outside application trust boundaries.

## Security model

Security-sensitive operations require recent authentication and may require phishing-resistant step-up authentication, trusted-device confirmation, security delay, or additional policy checks. Account recovery is a separate state machine and must never become an authentication bypass.

The canonical AI implementation contract is docs/AI_MASTER_PRODUCTION_PROMPT.md; repository behavior is governed by AGENTS.md.

Relevant standards include WebAuthn/FIDO2, OAuth 2.1, OpenID Connect, OWASP ASVS/API Security, and NIST digital-identity guidance. Exact conformance must be verified against deployed components and tests.

## Repository structure

```text
.github/
docs/
  adr/
  AI_MASTER_PRODUCTION_PROMPT.md
  architecture.md
  development.md
  release.md
infra/
  dev/
    docker-compose.yml
    keycloak/
scripts/
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

Production readiness is **not established**. The local runtime is only an executable protocol-development foundation. A production claim requires implementation of ZeaZ identity and tenant policy, security review, passing exact-head tests, secure deployment, rollback, backup/restore, observability, and operational evidence.

See:
- docs/AI_MASTER_PRODUCTION_PROMPT.md
- docs/architecture.md
- docs/development.md
- IMPLEMENTATION-CHECKLIST.md
- SECURITY.md
- ROADMAP.md
