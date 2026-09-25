# Changelog

All notable changes to ZIDP should be documented here. The format follows Keep a Changelog and releases should use Semantic Versioning unless an ADR specifies otherwise.

## [Unreleased]

### Added
- ZIDP product definition as the central ZeaZ Identity Provider and account-security plane
- Canonical AI production master prompt covering authentication, recovery, OAuth/OIDC, authorization, device trust, risk, audit, privacy, operations, testing, and release gates
- Production architecture covering identity, authentication, authorization, device trust, risk, recovery, notifications, and audit bounded contexts
- Production implementation checklist and phased delivery roadmap

### Changed
- Renamed product/repository references from ZIdentity/`cvsz/zidentity` to ZIDP/`cvsz/zidp`
- Set canonical user portal to `account.zeaz.dev`
- Updated repository governance and architecture documentation to use ZIDP terminology

### Security
- Defined passkey/WebAuthn and FIDO2 as preferred phishing-resistant authentication targets
- Defined step-up authentication for sensitive account operations
- Defined recovery as a separate state machine that must not become an authentication bypass
- Defined secure device/session lifecycle, audit, risk, and high-risk protection requirements
- Defined least-privilege OAuth/OIDC and application trust boundaries
