# ZIdentity Production Implementation Checklist

This checklist is the release gate for `cvsz/zidentity`. A checked documentation item is not evidence that the underlying implementation exists; each implemented control requires test and deployment evidence.

## Repository and governance

- [x] Repository identity is `cvsz/zidentity`.
- [x] Product scope is documented as ZeaZ Identity & Account Security Platform.
- [x] `AGENTS.md` defines the repository/security contract.
- [x] Canonical AI production prompt exists at `docs/AI_MASTER_PRODUCTION_PROMPT.md`.
- [ ] Configure CODEOWNERS for security-sensitive paths.
- [ ] Configure protected `main` branch/ruleset with required checks and review.

## Identity foundation

- [ ] Account lifecycle implementation
- [ ] Identity/profile implementation
- [ ] Opaque identifiers
- [ ] Tenant/application isolation
- [ ] Credential lifecycle

## Authentication

- [ ] WebAuthn/passkey registration
- [ ] WebAuthn/passkey authentication
- [ ] FIDO2/security-key lifecycle
- [ ] Password fallback using Argon2id or an equivalent approved memory-hard scheme
- [ ] TOTP enrollment/verification
- [ ] MFA enrollment/recovery policy
- [ ] Credential abuse/rate limiting
- [ ] Authentication event audit

## Device and session security

- [ ] Device registration
- [ ] Trusted-device lifecycle
- [ ] Lost/revoked device handling
- [ ] Secure browser sessions
- [ ] Session rotation
- [ ] Global session revocation
- [ ] Refresh-token rotation/reuse detection where applicable

## Risk and step-up authentication

- [ ] Risk-signal model
- [ ] Versioned risk policy
- [ ] Low/medium/high/critical decisions
- [ ] Step-up authentication
- [ ] Security delay for high-risk mutations
- [ ] High-risk/stolen-device protection
- [ ] Security regression tests

## Recovery

- [ ] Cryptographically secure recovery-key generation
- [ ] No plaintext recovery-key storage
- [ ] Recovery-contact enrollment
- [ ] Recovery-contact quorum policy
- [ ] Recovery state machine
- [ ] Recovery security delay
- [ ] Credential reset and session revocation
- [ ] Recovery notifications
- [ ] Recovery abuse detection

## OAuth/OIDC

- [ ] Authorization Code + PKCE
- [ ] OIDC authentication
- [ ] Scope and audience restrictions
- [ ] Consent management
- [ ] Client registration/lifecycle
- [ ] Token revocation
- [ ] Refresh-token policy
- [ ] Service-account/M2M authentication
- [ ] Redirect URI validation
- [ ] OAuth security regression suite

## Authorization

- [ ] RBAC
- [ ] ABAC/policy evaluation where required
- [ ] Least-privilege scopes
- [ ] Privileged operation step-up
- [ ] Support/admin separation
- [ ] Time-limited support access
- [ ] Full privileged-operation audit

## Data protection

- [ ] TLS 1.3 where supported
- [ ] Vetted authenticated encryption
- [ ] Secret manager integration
- [ ] Key hierarchy documented
- [ ] Key rotation procedure
- [ ] Data minimization/retention policy
- [ ] Sensitive-field redaction in logs

## Security engineering

- [ ] Threat model completed
- [ ] Account-takeover tests
- [ ] Credential-stuffing tests
- [ ] Session/token replay tests
- [ ] OAuth abuse tests
- [ ] Recovery abuse tests
- [ ] Authorization boundary tests
- [ ] Tenant-isolation tests
- [ ] Supply-chain controls
- [ ] Secret scanning/push protection

## Observability and operations

- [ ] Structured security events
- [ ] Metrics
- [ ] Tracing
- [ ] Alerting
- [ ] Backup procedure
- [ ] Restore verification
- [ ] Disaster recovery procedure
- [ ] Incident response procedure
- [ ] Security-event retention policy

## CI/CD

- [ ] Formatting/lint
- [ ] Unit tests
- [ ] Integration tests
- [ ] E2E tests
- [ ] Security tests
- [ ] CodeQL/SAST
- [ ] Dependency review
- [ ] Container scanning
- [ ] IaC scanning
- [ ] SBOM generation
- [ ] Artifact provenance/signing where supported
- [ ] Least-privilege GitHub Actions permissions
- [ ] Fork/untrusted-PR secret isolation

## Documentation

- [x] README describes actual target product.
- [x] Architecture document updated from generic template to ZIdentity architecture.
- [x] AI production prompt is canonicalized.
- [ ] Development guide reflects actual implementation.
- [ ] Release guide reflects actual deployment/recovery process.
- [ ] Threat model is versioned.
- [ ] API contract is documented.
- [ ] Recovery runbook is documented.
- [ ] ADRs exist for material architecture decisions.

## Final production gate

- [ ] Fresh clone/bootstrap verified
- [ ] Full test suite passes
- [ ] Security suite passes
- [ ] No critical/high unresolved security defect without approved exception
- [ ] Migration plan verified
- [ ] Deployment verified
- [ ] Rollback verified
- [ ] Backup restore verified
- [ ] Monitoring/alerting verified
- [ ] Release artifacts traceable to source
- [ ] Production readiness evidence recorded
