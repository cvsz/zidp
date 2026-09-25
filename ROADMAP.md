# ZIdentity Roadmap

ZIdentity is the central identity and account-security plane for the ZeaZ ecosystem. Delivery is evidence-driven: an item is complete only when implementation, tests, security validation, documentation, and operational evidence exist.

## Phase 0 — Governance and architecture

- [x] Establish `cvsz/zidentity` product identity
- [x] Replace generic template README with ZIdentity scope
- [x] Establish repository agent/security contract
- [x] Add canonical AI production master prompt
- [x] Define central identity architecture
- [x] Define production implementation checklist
- [ ] Configure branch/ruleset protections
- [ ] Complete security-focused CODEOWNERS
- [ ] Create threat-model ADRs

## Phase 1 — Identity foundation

- [ ] Account and identity domain
- [ ] Tenant/application model
- [ ] PostgreSQL persistence model
- [ ] Domain validation and typed contracts
- [ ] Account lifecycle API
- [ ] Security-event model

## Phase 2 — Strong authentication

- [ ] WebAuthn/passkeys
- [ ] FIDO2/security-key support
- [ ] TOTP MFA
- [ ] Password fallback with memory-hard hashing
- [ ] Authentication abuse controls
- [ ] Authentication event audit

## Phase 3 — Device, session, and risk security

- [ ] Device lifecycle
- [ ] Trusted-device management
- [ ] Secure session architecture
- [ ] Global session revocation
- [ ] Risk engine
- [ ] Step-up authentication
- [ ] High-risk/stolen-device protection

## Phase 4 — Recovery

- [ ] Recovery-key lifecycle
- [ ] Recovery contacts
- [ ] Recovery quorum policy
- [ ] Recovery state machine
- [ ] Security delay
- [ ] Credential replacement
- [ ] Recovery notifications
- [ ] Recovery-abuse detection

## Phase 5 — Federation and authorization

- [ ] OAuth 2.1 Authorization Code + PKCE
- [ ] OpenID Connect
- [ ] Client registration/lifecycle
- [ ] Consent management
- [ ] Scope/audience enforcement
- [ ] RBAC
- [ ] ABAC/policy engine where justified
- [ ] Service accounts / M2M
- [ ] Token revocation and refresh-token controls

## Phase 6 — ZeaZ ecosystem integration

- [ ] Integrate `zPay`
- [ ] Integrate `zWallet`
- [ ] Integrate `zBiz`
- [ ] Integrate `zTTato`
- [ ] Integrate `zVeo`
- [ ] Integrate `ZTrader`
- [ ] Publish stable identity/API contracts
- [ ] Establish application-specific scopes and audiences

## Phase 7 — Operations and security assurance

- [ ] OpenTelemetry instrumentation
- [ ] Security alerting
- [ ] Backup/restore verification
- [ ] Disaster recovery
- [ ] Key and secret rotation
- [ ] Incident response runbooks
- [ ] SAST/CodeQL
- [ ] Dependency review
- [ ] Secret scanning/push protection
- [ ] Container/IaC scanning
- [ ] SBOM and artifact provenance
- [ ] Security regression suite

## Phase 8 — Production release gate

- [ ] Fresh-environment bootstrap verified
- [ ] Full automated test suite green
- [ ] Security test suite green
- [ ] Migration/rollback verified
- [ ] Backup restore verified
- [ ] Monitoring and alerting verified
- [ ] Release artifact provenance verified
- [ ] No critical/high unresolved security issue without approved exception
- [ ] Production readiness evidence published
