#!/usr/bin/env python3
"""Smoke-test the isolated local ZIDP Keycloak development realm."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = os.environ.get("ZIDP_BASE_URL", "http://127.0.0.1:8080").rstrip("/")
REALM = os.environ.get("ZIDP_REALM", "zeaz-dev")
CLIENT_ID = "zeaz-web-local"
CALLBACK = "http://127.0.0.1:3000/oidc/callback"
ISSUER = f"{BASE_URL}/realms/{REALM}"


def request(url: str, data: bytes | None = None) -> tuple[int | None, bytes, str]:
    headers = {"Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = Request(url, data=data, headers=headers)
    try:
        with urlopen(req, timeout=5) as response:
            return response.status, response.read(), response.geturl()
    except HTTPError as error:
        return error.code, error.read(), error.geturl()
    except URLError as error:
        return None, b"", str(error.reason)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def authorization_status(
    authorization_endpoint: str, *, redirect_uri: str, response_type: str = "code"
) -> int | None:
    verifier = secrets.token_urlsafe(48)
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode("ascii")).digest()
    ).decode("ascii").rstrip("=")
    query = urlencode(
        {
            "client_id": CLIENT_ID,
            "response_type": response_type,
            "redirect_uri": redirect_uri,
            "scope": "openid",
            "state": secrets.token_urlsafe(24),
            "nonce": secrets.token_urlsafe(24),
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        }
    )
    status, _, _ = request(f"{authorization_endpoint}?{query}")
    return status


def main() -> int:
    discovery_url = f"{ISSUER}/.well-known/openid-configuration"
    deadline = time.monotonic() + 180
    discovery_status: int | None = None
    discovery_body = b""
    discovery_target = discovery_url

    while time.monotonic() < deadline:
        discovery_status, discovery_body, discovery_target = request(discovery_url)
        if discovery_status == 200:
            break
        time.sleep(2)

    if discovery_status != 200:
        response_detail = discovery_body.decode("utf-8", errors="replace").strip()[:512]
        raise AssertionError(
            "OIDC discovery did not become available "
            f"(status={discovery_status}, target={discovery_target}, "
            f"response={response_detail!r})"
        )
    discovery = json.loads(discovery_body)
    require(discovery.get("issuer") == ISSUER, "OIDC issuer does not match the pinned local issuer")

    required_endpoints = (
        "authorization_endpoint",
        "token_endpoint",
        "userinfo_endpoint",
        "jwks_uri",
        "revocation_endpoint",
        "end_session_endpoint",
    )
    for endpoint in required_endpoints:
        require(bool(discovery.get(endpoint)), f"OIDC discovery is missing {endpoint}")

    require(
        "S256" in discovery.get("code_challenge_methods_supported", []),
        "OIDC discovery does not advertise PKCE S256",
    )

    jwks_status, jwks_body, _ = request(discovery["jwks_uri"])
    require(jwks_status == 200, "JWKS endpoint is unavailable")
    jwks = json.loads(jwks_body)
    keys = jwks.get("keys", [])
    require(bool(keys), "JWKS contains no signing keys")
    require(all(key.get("kid") and key.get("kty") for key in keys), "JWKS contains an incomplete key")

    valid_status = authorization_status(
        discovery["authorization_endpoint"], redirect_uri=CALLBACK
    )
    require(valid_status == 200, f"valid Authorization Code + PKCE request returned {valid_status}")

    invalid_redirect_status = authorization_status(
        discovery["authorization_endpoint"],
        redirect_uri="http://attacker.invalid/oidc/callback",
    )
    require(
        invalid_redirect_status is not None and invalid_redirect_status >= 400,
        f"unregistered redirect URI was not rejected (status={invalid_redirect_status})",
    )

    implicit_status = authorization_status(
        discovery["authorization_endpoint"],
        redirect_uri=CALLBACK,
        response_type="token",
    )
    require(
        implicit_status is not None and implicit_status >= 400,
        f"implicit response type was not rejected (status={implicit_status})",
    )

    password_request = urlencode(
        {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "username": "synthetic-user-that-does-not-exist",
            "password": "synthetic-not-a-secret",
        }
    ).encode("ascii")
    password_status, _, _ = request(discovery["token_endpoint"], data=password_request)
    require(
        password_status is not None and password_status >= 400,
        f"Resource Owner Password Credentials grant was not rejected (status={password_status})",
    )

    print("PASS: OIDC discovery and exact issuer")
    print("PASS: JWKS endpoint and signing key metadata")
    print("PASS: Authorization Code + PKCE S256 reaches the login ceremony")
    print("PASS: unregistered redirect URI rejected")
    print("PASS: implicit flow rejected")
    print("PASS: password grant rejected")
    print("SCOPE: local development protocol smoke test only; no user authentication or tenant policy tested")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
