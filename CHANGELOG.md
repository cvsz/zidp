# Changelog

All notable changes to ZIDP should be documented here. The format follows Keep a Changelog and releases should use Semantic Versioning unless an ADR specifies otherwise.

## [Unreleased]

### Added
- Local-only Keycloak 26.8.1 and PostgreSQL 17.11 development runtime with an isolated OIDC realm
- OIDC smoke tests for issuer discovery, JWKS, PKCE S256, exact redirect rejection, and disabled implicit/password grants
- ADR documenting the protocol-engine boundary and deferred production adoption
- CI integration job that starts the local IdP with ephemeral credentials and removes its database volume after testing
- CODEOWNERS policy assigning all repository paths to the independent policedbc reviewer

### Changed
- Replaced placeholder Makefile targets with real local development lifecycle commands
- Moved Docker image dependency monitoring to the local runtime directory

### Security
- Bound the local IdP port to loopback and isolated its Docker network
- Disabled implicit flow, Resource Owner Password Credentials, and service accounts in the sample public client
- Masked ephemeral CI administrator/database passwords before exporting them to subsequent steps
- Kept tenant authorization, production credentials, and production issuer configuration out of the development realm

### Existing product definition
- ZIDP product definition as the central ZeaZ Identity Provider and account-security plane
- Canonical AI production master prompt covering authentication, recovery, OAuth/OIDC, authorization, device trust, risk, audit, privacy, operations, testing, and release gates
- Production architecture covering identity, authentication, authorization, device trust, risk, recovery, notifications, and audit bounded contexts
- Production implementation checklist and phased delivery roadmap

### Changed
- Renamed product/repository references from ZIdentity/cvsz/zidentity to ZIDP/cvsz/zidp
- Set canonical user portal to account.zeaz.dev
- Updated repository governance and architecture documentation to use ZIDP terminology

### Security
- Defined passkey/WebAuthn and FIDO2 as preferred phishing-resistant authentication targets
- Defined step-up authentication for sensitive account operations
- Defined recovery as a separate state machine that must not become an authentication bypass
- Defined secure device/session lifecycle, audit, risk, and high-risk protection requirements
- Defined least-privilege OAuth/OIDC and application trust boundaries
