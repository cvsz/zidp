# Development

## Prerequisites

- Docker Engine with Docker Compose v2
- Python 3.10 or newer (standard library only for the smoke test)
- OpenSSL for generating local-only passwords

## Start the isolated local identity runtime

1. Run make setup to create .env from .env.example.
2. Generate two independent random values with openssl rand -hex 32.
3. Set the generated values as ZIDP_ADMIN_PASSWORD and ZIDP_DB_PASSWORD in the ignored .env file. Do not commit .env.
4. Run make config to validate Compose interpolation.
5. Run make dev-up to start PostgreSQL and Keycloak.
6. Run make dev-test to verify the local OIDC contract.
7. Open the local Keycloak administration console at http://127.0.0.1:8080/admin/ only when required; use the administrator credentials from the local .env.

The development issuer is http://127.0.0.1:8080/realms/zeaz-dev. Its discovery document is http://127.0.0.1:8080/realms/zeaz-dev/.well-known/openid-configuration.

The imported zeaz-web-local public client accepts only http://127.0.0.1:3000/oidc/callback, uses Authorization Code + PKCE S256, and has implicit flow, password grant, and service accounts disabled.

## Runtime boundary

This is a local development fixture, not a staging or production deployment. The HTTP port is bound to loopback and the Docker network is internal. The realm contains no users, production clients, tenant memberships, or production credentials. Do not expose this endpoint through a tunnel, reverse proxy, public DNS, or production application.

The smoke test verifies protocol discovery, JWKS, redirect rejection, and disabled grant types. It does not authenticate a real user, exchange a code, validate tenant isolation, implement ZeaZ RBAC/ABAC, or prove WebAuthn/MFA/recovery behavior.

## Lifecycle

- make dev-down stops containers while preserving the local PostgreSQL volume.
- make dev-reset deletes the local development volume and all local Keycloak state. This is destructive and must not be used outside this isolated development stack.

## Quality expectations

- Keep changes small and reviewable.
- Add regression tests for behavior changes and security boundaries.
- Prefer deterministic and reproducible tooling.
- Do not commit secrets or local credentials.
- Do not weaken security or CI gates to obtain a passing build.

## Documentation

Update architecture, development, release, and ADR documentation when behavior or operational assumptions change.
