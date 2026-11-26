# CORS Origin Validation Hardening

## Overview

This contribution improves the validation of `CORS_ORIGINS` in the API configuration to ensure that only valid, exact HTTP(S) origins are accepted.

The change strengthens an existing validation mechanism and adds automated test coverage for malformed and unsafe origin values.

## Problem

The previous implementation checked whether an origin started with `http://` or `https://` and rejected wildcard characters.

However, this basic check could still accept malformed or unintended values, including origins containing paths, invalid ports, credentials, query strings, or fragments.

## Implementation

The validation logic in `apps/api/src/app/core/config.py` was improved using Python's standard-library `urllib.parse.urlsplit`.

The updated validation:

- Allows only HTTP and HTTPS schemes.
- Requires a valid hostname and network location.
- Rejects wildcard origins.
- Rejects leading, trailing, and embedded whitespace.
- Rejects URL credentials.
- Rejects paths other than an optional trailing slash.
- Rejects query strings and fragments, including empty delimiters.
- Rejects malformed, empty, and out-of-range ports.
- Normalizes an optional trailing slash.

## Automated Tests

Additional parameterized test cases were added to `apps/api/tests/core/test_config.py`.

The tests cover:

- Wildcard origins.
- Missing or invalid URL schemes and hostnames.
- URL paths.
- Invalid ports.
- Embedded whitespace.
- Credentials.
- Query strings and fragments.
- Empty query and fragment delimiters.

Existing tests for default configuration and supported origin formats were retained.

## Verification

The following project checks were executed:

| Check | Result |
|---|---|
| Ruff lint | Passed |
| Ruff formatting | Passed |
| Frontend Biome checks | Passed |
| Frontend TypeScript typecheck | Passed |
| API test suite | 22 passed |
| Python dependency security audit | No known vulnerabilities found |
| Frontend dependency audit | 1 moderate vulnerability reported |
| Production build | Passed |

The frontend audit finding is recorded separately from the CORS implementation; this contribution does not include frontend dependency changes.

## Files Changed

| File | Purpose |
|---|---|
| `apps/api/src/app/core/config.py` | Improved CORS origin validation |
| `apps/api/tests/core/test_config.py` | Added validation test coverage |

## Summary

This change makes CORS origin configuration validation stricter and more predictable while preserving support for valid HTTP(S) origins. It also improves regression protection through automated tests.
