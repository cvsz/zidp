# AGENTS.md — ZIdentity Repository Agent Contract

## Mission

This repository implements **ZeaZ Identity & Account Security Platform (`zidentity`)**, the central identity/security plane for the ZeaZ ecosystem. The primary user surface is `account.zeaz.dev`.

Agents must treat security, correctness, privacy, and operational safety as first-class requirements. Read `zeaz.md` when present in the repository hierarchy, then `docs/AI_MASTER_PRODUCTION_PROMPT.md`, then this file before making substantial changes.

## Operating rules

- Inspect the exact current branch/head and relevant files before editing.
- Preserve existing correct behavior unless the requested change requires otherwise.
- Prefer small, complete, reviewable changes.
- No production-path placeholders, TODO implementations, fake security controls, hard-coded credentials, or undocumented bypasses.
- Never weaken CI, security scanning, authorization, validation, cryptography, branch/release controls, or tests merely to make a check pass.
- Never commit credentials, tokens, private keys, recovery secrets, production secrets, or sensitive personal data.
- Use approved secret-management systems for real secrets.
- Treat browser input, API input, OAuth clients, dependencies, pull requests, generated artifacts, and external service responses as untrusted.
- Validate and authorize on the server side.
- Fail closed for authentication, authorization, recovery, and other security-sensitive decisions.
- Do not invent cryptographic protocols. Use vetted standards and maintained libraries.
- Do not log credentials, tokens, recovery keys, session cookies, or unnecessary personal data.
- Keep tenant/application boundaries explicit in domain and persistence layers.
- Every security-sensitive mutation must have an auditable event.
- Recovery must not become an authentication bypass.
- Support access must not become unrestricted impersonation or a hidden administrator path.

## Product architecture

The intended bounded contexts are:

- Identity
- Authentication
- Authorization
- Device Trust
- Risk Engine
- Recovery
- Notification
- Audit
- OAuth/OIDC federation
- Administration

Preferred infrastructure direction is PostgreSQL for durable state, Redis only where justified for ephemeral state/coordination, Vault/KMS-compatible secret management, Docker/Kubernetes-compatible deployment, Terraform for infrastructure, and OpenTelemetry-compatible observability. Existing repository choices take precedence when they are secure and maintainable.

A mature standards-compliant identity provider such as Keycloak may be evaluated instead of implementing protocol primitives from scratch. Such a decision requires an ADR and must preserve ZeaZ-specific security policy, UX, audit, and integration boundaries.

## Security requirements

ZIdentity targets:

- WebAuthn / passkeys / FIDO2
- TOTP MFA and hardware security keys
- Trusted-device lifecycle
- Risk-based and step-up authentication
- Secure sessions and global revocation
- Recovery keys and recovery contacts
- Security delays for high-risk changes
- OAuth 2.1 and OpenID Connect
- RBAC/ABAC and scoped authorization
- Service accounts and machine authentication
- Immutable audit/security events
- Security notifications
- Data minimization and privacy controls

Sensitive operations such as credential changes, MFA removal, recovery changes, privilege changes, and account deletion require recent authentication and may require phishing-resistant step-up authentication and/or a security delay.

## Change-safety gate

For non-trivial changes:

1. Inspect current implementation and trust boundaries.
2. Identify authentication/authorization impact.
3. Identify data migration and compatibility impact.
4. Identify operational and deployment impact.
5. Define rollback before changing stateful behavior.
6. Implement the smallest complete change.
7. Add or update tests, especially security regression tests.
8. Run relevant formatting, lint, unit, integration, security, and build checks.
9. Review the final diff for secrets and security regressions.
10. Update documentation and ADRs when behavior or architecture changes.

## Verification

At minimum, touched Markdown/YAML/configuration must be syntactically valid. Workflows must use least-privilege permissions. Secrets and sensitive data must not enter source control. Authentication and authorization behavior must have automated coverage. Documentation must describe actual implementation rather than aspirational functionality.

## Pull requests and releases

PRs should state scope, tests, security impact, compatibility/migration impact, documentation impact, deployment impact, and rollback. Releases require evidence from passing required checks and release validation. Never claim a deployment, audit, migration, or production readiness state without exact evidence.

## Documentation ownership

- `.github/`: GitHub automation and repository governance.
- `docs/`: architecture, security, development, operations, release, recovery, API, and ADR documentation.
- Root Markdown: repository policy, lifecycle, security, and project-level guidance.
- `docs/AI_MASTER_PRODUCTION_PROMPT.md`: canonical AI execution contract for the complete ZIdentity target architecture.

## No scope drift

Do not turn ZIdentity into a general application framework or unrelated ZeaZ business service. Integrations with zPay, zWallet, zBiz, zTTato, zVeo, ZTrader, and other applications belong at explicit identity/API trust boundaries.
