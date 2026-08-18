# ADR 016 — JWT (JSON Web Tokens) for Stateless Authentication

## Context

The system requires:

1. **User authentication**: Verifying identity via email/password at sign-in
2. **Stateless authorization**: No server-side session storage; each request proves identity with a token
3. **Claim-based access control**: Authorization decisions based on embedded user context (user_id, role)
4. **Decentralized validation**: Lambda functions validate tokens without calling a central auth service

Traditional session-based authentication would require a session store (DynamoDB or external cache), increasing complexity and latency. Stateless JWT tokens eliminate this requirement.

## Decision

Use **JWT (JSON Web Tokens)** for authentication and authorization:

- **Token structure**: Header (alg, typ) + Payload (sub, user_id, email, exp, iat) + Signature (RS256 with RSA key pair)
- **Signing**: RS256 (RSA SHA-256) using application-managed private/public key pair
- **Validation**: Every HTTP endpoint validates JWT signature using public key before processing
- **Token lifespan**: 24 hours (configurable)
- **Refresh mechanism**: Clients re-authenticate to obtain new token (no refresh token rotation)

### Key Management

- **Private key**: Stored in AWS Secrets Manager / environment variable `JWT_PRIVATE_KEY`
- **Public key**: Stored in AWS Secrets Manager / environment variable `JWT_PUBLIC_KEY`, used for validation
- **Rotation strategy**: Dual-key support allows gradual migration when keys rotate

## Alternatives Considered

- **OAuth 2.0 / OpenID Connect**: Full-featured provider (Auth0, Okta, Cognito); adds operational complexity and cost for simple use case.
- **API Keys**: Simple but limited; no claim-based authorization, no expiry, harder to rotate.
- **Lambda authorizers (custom)**: More complex than validating JWT in application code; adds latency.
- **Amazon Cognito**: Managed service but adds vendor lock-in, operational overhead, and cost.

## Consequences

- **Advantages**:
  - Stateless: No server-side session store required; scales horizontally
  - Standard format: Compatible with existing JWT libraries across languages
  - Claim-based access control: user_id embedded in token, no lookup needed
  - Fast validation: Signature check via public key is cryptographically fast
  - Cost-effective: No additional auth service charges
- **Disadvantages**:
  - **Token revocation complexity**: Revoking a token requires maintaining a blacklist (in Redis or DynamoDB)
  - **Key rotation overhead**: Must manage multiple active keys during rotation
  - **Token size**: JWTs are larger than session cookies, increasing request size
  - **Security considerations**: Private key exposure is critical; requires secure storage and rotation
  - **No real-time invalidation**: Once issued, token is valid until expiry (mitigated by short TTL)
- **Mitigations**:
  - Keep token TTL short (24 hours or less) to limit exposure window
  - Use strong RSA keys (minimum 2048-bit)
  - Rotate keys quarterly or on suspected compromise
  - Implement token blacklist in Redis for immediate revocation if needed
  - Transmit tokens over HTTPS only
  - Validate issuer (iss) and audience (aud) claims if using external integrations

## Implementation Notes

- **Token Creation** (signin): User email/password verified → token generated with `user_id`, `email`, `exp`, `iat`
- **Token Validation** (all HTTP endpoints):
  1. Extract token from Authorization header
  2. Decode JWT (verify signature, expiry, issuer)
  3. Extract user_id for authorization decisions
  4. Reject if signature invalid, token expired, or claims missing
- **Error Handling**: Return 401 Unauthorized if token invalid/missing; return 403 Forbidden if insufficient permissions
