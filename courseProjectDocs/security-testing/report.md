# Security Testing Report

## Test Scope and Coverage

**Tool Used:** Bandit (Python security linter)

**Scope:** Scanned `skbio/util/` module (2,203 lines of code across 20 files)

**Vulnerability Types Targeted:**
- Command injection (CWE-78)
- Use of weak cryptographic hashes (CWE-327)
- Improper check for unusual conditions (CWE-703)

## Vulnerability Summary

| # | Title | Type | Severity | File | Recommended Fix |
|---|-------|------|----------|------|-----------------|
| 1 | Weak MD5 Hash | Insecure Cryptography (CWE-327) | High | `_misc.py:176` | Use `hashlib.md5(usedforsecurity=False)` or switch to SHA-256 |
| 2 | Subprocess with Partial Path | Command Injection Risk (CWE-78) | Low | `_gpu.py:24` | Use absolute path `/usr/bin/nvidia-smi` |
| 3 | Subprocess Call | Command Injection Risk (CWE-78) | Low | `_gpu.py:24` | Validate input before subprocess execution |
| 4 | Subprocess Import | Potential Misuse (CWE-78) | Low | `_gpu.py:11` | Ensure subprocess is used safely |
| 5 | Assert in Production Code | Improper Check (CWE-703) | Low | `_testing.py:184` | Replace with proper exception handling |
| 6 | Assert in Production Code | Improper Check (CWE-703) | Low | `_testing.py:192` | Replace with proper exception handling |

## Execution and Results

**Scan Summary:**
- Total issues: 10
- High severity: 1
- Low severity: 9
- Files scanned: 20
- Lines analyzed: 2,203

**Execution Command:**
```bash
bandit -r skbio/util/ -f json -o bandit_results.json
```

**Key Findings:**

1. **MD5 Hash (High):** Used for file checksumming, not security. Adding `usedforsecurity=False` would silence the warning appropriately.

2. **Subprocess Issues (Low):** The `nvidia-smi` call uses a hardcoded command with no user input, making injection unlikely. Using absolute path would improve security.

3. **Assert Statements (Low):** Located in `_testing.py` which is test utility code. Asserts are acceptable here as they're not production code paths.

**No failed scans or unexpected behavior.**

## Group Contributions

**Devaj:**
- Ran Bandit security scanner on skbio/util module
- Documented 6 vulnerabilities with severity and fixes
- Created README and report
