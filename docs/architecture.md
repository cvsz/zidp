# ZIdentity Architecture

## 1. System context

ZIdentity is the central identity and account-security plane for the ZeaZ ecosystem. The user-facing portal is `account.zeaz.dev`. ZeaZ applications authenticate and authorize through standards-based OAuth 2.1 and OpenID Connect rather than implementing independent identity stores.

```text
                         account.zeaz.dev
                               │
                    ZIdentity Identity Plane
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
        zPay                zWallet              zTTato
        zBiz                  zVeo               ZTrader
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                 Audit / Risk / Security Control
```

ZIdentity is not an Apple implementation. The architecture uses public standards and general security principles; proprietary protocols, source code, UI, and undocumented behavior are explicitly out of scope.

## 2. Bounded contexts

### Identity

Account lifecycle, identity attributes, profile, tenant/application ownership, and account state.

### Authentication

Passkeys/WebAuthn, FIDO2/security keys, password fallback, TOTP MFA, authentication ceremonies, and credential lifecycle.

### Device Trust

Device registration, trusted-device state, session association, lost/revoked devices, and security notifications.

### Risk Engine

Risk signals, policy evaluation, step-up decisions, throttling, and high-risk protection.

### Recovery

Recovery keys, recovery contacts, recovery requests, verification, security delays, and credential reset.

### Authorization

OAuth/OIDC scopes, roles, permissions, policies, consent, client lifecycle, service accounts, and privileged access.

### Audit

Append-only security events, investigation metadata, audit retention, and tamper-evidence controls.

### Notification

Security alerts and user-visible notifications for sensitive account events.

## 3. Authentication model

Passkeys/WebAuthn are the preferred phishing-resistant authentication mechanism. TOTP and hardware security keys provide additional authentication options. Password authentication, if present, is a controlled fallback and must use a memory-hard password hashing scheme and credential-abuse controls.

Authentication is separate from authorization. A valid login does not automatically authorize sensitive account changes.

## 4. Step-up authentication

Sensitive operations require recent authentication and may require stronger authentication or a security delay:

- password changes
- primary email/phone changes
- passkey/security-key changes
- MFA removal
- recovery configuration changes
- account deletion
- privilege changes
- high-privilege OAuth client creation
- sensitive data export

The policy decision is server-side and auditable.

## 5. Device trust

```text
NEW -> PENDING -> TRUSTED -> SUSPENDED -> REVOKED
                         \-> LOST
```

Device metadata is minimized. The platform supports device listing, security activity, revocation, and session invalidation without treating approximate network data as precise physical location.

## 6. Recovery

Recovery is a dedicated security domain and state machine:

```text
NORMAL
  -> RECOVERY_REQUESTED
  -> IDENTITY_VERIFICATION
  -> SECURITY_DELAY
  -> RECOVERY_APPROVED
  -> NEW_CREDENTIALS
  -> ALL_SESSIONS_REVOKED
  -> NORMAL
```

Recovery keys are generated using cryptographically secure randomness and are never stored as plaintext. Recovery contacts may use a configurable quorum policy. Recovery cannot silently bypass the platform's authentication and authorization controls.

## 7. Authorization and federation

ZIdentity acts as the identity provider and authorization server for ZeaZ applications. New browser applications use Authorization Code + PKCE. OIDC provides identity claims; OAuth scopes and audience restrictions limit API access.

Recommended administrative roles:

```text
SUPER_ADMIN
SECURITY_ADMIN
SUPPORT_ADMIN
BILLING_ADMIN
AUDITOR
READ_ONLY
```

Support access is time-limited, scope-limited, consent-aware where appropriate, and fully audited. There is no unrestricted master-password or hidden `god mode` design.

## 8. Data/storage model

Durable relational state belongs in PostgreSQL. Redis may be used for ephemeral sessions, rate limits, short-lived ceremony state, locks, and cache data when justified.

Core entities include:

```text
accounts
identities
credentials
passkeys
security_keys
devices
trusted_devices
trusted_phone_numbers
sessions
refresh_tokens
recovery_keys
recovery_contacts
recovery_requests
security_events
risk_events
notifications
oauth_clients
oauth_consents
service_accounts
roles
permissions
policies
```

Entity IDs must be opaque. Ownership and tenant boundaries must be enforced in the domain and persistence layers.

Identity data is separated from application-domain data. Clients receive only the claims/scopes required for their function.

## 9. Cryptography and secrets

Use TLS 1.3 where supported, authenticated encryption through vetted libraries, memory-hard password hashing for passwords, and WebAuthn/FIDO2 for phishing-resistant credentials.

Sensitive data encryption should use envelope encryption when justified. Key management belongs in Vault/KMS-compatible infrastructure. Secrets and private keys must never be committed to Git.

No custom cryptographic primitive is permitted.

## 10. Trust boundaries

Primary trust boundaries are:

1. Unauthenticated internet -> edge/API
2. Browser -> account portal
3. Application -> OIDC authorization server
4. Identity service -> database
5. Identity service -> secret manager
6. Admin/support -> privileged control plane
7. CI/CD -> production artifact/deployment systems
8. ZeaZ application -> identity claims/tokens

Every boundary requires explicit authentication, authorization, validation, and audit behavior appropriate to its risk.

## 11. API security

Every endpoint defines authentication, authorization, input/output schemas, rate limits, idempotency requirements where relevant, error behavior, and audit behavior. API errors use stable machine-readable codes and do not disclose internal implementation details.

Apply OWASP API Security and ASVS principles.

## 12. Observability

Use OpenTelemetry-compatible traces, metrics, and structured logs where supported.

Observe authentication outcomes, MFA, passkey events, recovery, token lifecycle, risk decisions, authorization failures, rate limiting, service failures, and database health.

Never place credentials, recovery keys, tokens, session cookies, or unnecessary personal data in telemetry.

## 13. Deployment topology

The target is containerized and compatible with Docker/Kubernetes and Terraform-managed infrastructure. Cloudflare may provide edge protection where configured. PostgreSQL remains the durable source of truth; Redis is not the source of truth for identity.

The implementation must remain viable in a cost-efficient/self-hosted ZeaZ environment.

## 14. Availability and recovery

Document and test:

- database backups
- restore verification
- key rotation
- secret rotation
- session/token invalidation during incidents
- disaster recovery
- dependency failure behavior
- degraded mode
- rollback

Security-sensitive operations fail closed when a dependency outage would otherwise create an authorization bypass.

## 15. Threat model

At minimum model account takeover, credential stuffing, phishing, WebAuthn ceremony attacks, session theft, token replay, OAuth redirect abuse, recovery abuse, support abuse, privilege escalation, database compromise, secret-manager compromise, supply-chain compromise, CI/CD compromise, denial of service, and audit tampering.

Each material threat requires prevention, detection, response, and regression coverage.

## 16. Architectural constraints

- Prefer established standards and mature components over custom protocol implementations.
- Do not create speculative microservices without a concrete boundary or scaling/security requirement.
- Do not duplicate authentication logic in downstream ZeaZ applications.
- Do not mix recovery, support impersonation, and normal authentication into one privileged path.
- Do not expose internal risk signals or security secrets to client applications.
- Do not claim security properties that have not been tested and verified.

## 17. Decision records

Material decisions belong under `docs/adr/`. At minimum, create ADRs before adopting a new identity-provider core, changing credential storage strategy, changing token architecture, introducing a new key-management boundary, or materially changing recovery policy.
