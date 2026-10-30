# ADR 0001: Use Keycloak as the local OIDC protocol engine

- Status: Accepted for local development only; production adoption is deferred
- Date: 2026-10-31
- Owners: ZIDP maintainers; independent security review required before production adoption

## Context

The current ZIDP repository defines a central identity product but contains no executable identity service, database schema, or protocol integration tests. Implementing OAuth/OIDC, token issuance, signing-key rotation, session security, and WebAuthn ceremonies from scratch would create avoidable protocol and cryptographic risk.

The repository's canonical production prompt explicitly requires evaluating mature standards-compliant identity components before implementing protocol primitives.

## Decision

Use upstream Keycloak 26.8.1 as the protocol engine for an isolated local development runtime, backed by PostgreSQL 17.11.

The initial development realm:

- is reachable only through a loopback-bound host port;
- uses a Docker network with external connectivity disabled;
- imports no users, tenant memberships, production clients, or credentials;
- defines one public browser client with one exact loopback callback;
- enables Authorization Code flow with PKCE S256;
- disables implicit flow, Resource Owner Password Credentials, and service accounts;
- requires local administrator and database passwords from an ignored .env file;
- is never exposed as account.zeaz.dev and is not a production issuer.

Keycloak owns standards-based protocol execution. ZeaZ-specific identity lifecycle, tenant membership, RBAC/ABAC policy, risk and step-up decisions, recovery policy, security notifications, application integration, and audit governance remain explicit ZIDP responsibilities. No downstream application is authorized to trust caller-supplied tenant or role claims.

## Alternatives considered

1. Build OAuth/OIDC primitives in a new service. Rejected for the initial protocol core because it increases cryptographic, protocol-conformance, and long-term maintenance risk.
2. Adopt another self-hosted IdP. Deferred pending a documented feature/security/operability comparison.
3. Use a hosted identity SaaS. Not selected for the initial foundation because it adds recurring cost and an external control-plane dependency.

## Consequences

Positive:
- Provides an executable local OIDC discovery, JWKS, and authorization endpoint for integration work.
- Uses a mature standards-oriented implementation rather than custom token/protocol code.
- Gives CI a real PostgreSQL-backed protocol smoke test.

Negative / constraints:
- Introduces an upstream Keycloak runtime dependency and upgrade obligations.
- The local development realm is not a tenant authorization model.
- The local HTTP endpoint and bootstrap administrator are unsuitable for staging or production.
- This decision does not establish WebAuthn, MFA, recovery, audit, HA, DR, or production compliance.

Before any staging/production adoption, require a separate deployment/security ADR covering digest-pinned images, TLS/hostname, secret-manager integration, admin-network isolation, realm/client provisioning, tenant and role claim policy, phishing-resistant authentication policy, audit export, rate limiting, backup/restore, key rotation, SLOs, HA/DR, incident response, upgrade/rollback, load tests, independent review, and operator approval.

## Validation

scripts/test-idp-dev.py checks:

- exact OIDC issuer and required discovery endpoints;
- JWKS availability and signing-key metadata;
- PKCE S256 support;
- valid Authorization Code request reaches the login ceremony;
- unregistered redirect URI is rejected;
- implicit and password grants are rejected.

This smoke test does not authenticate a user, exchange an authorization code, prove tenant isolation, or establish production readiness.

## Rollback

Stop the local stack with make dev-down. Local data is isolated in the zidp_dev_postgres Docker volume. make dev-reset deletes that local development volume and all local Keycloak state; it is intentionally destructive and must never be used against a production database.
