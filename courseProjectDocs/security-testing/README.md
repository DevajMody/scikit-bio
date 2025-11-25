# Security Testing

Security vulnerability scanning for scikit-bio using Bandit.

## Prerequisites

```bash
pip install bandit
```

## Running Security Scans

```bash
# Scan entire project
bandit -r skbio/ -f json -o security_results.json

# Scan specific module (as done in this report)
bandit -r skbio/util/ -f json -o bandit_results.json

# Human-readable output
bandit -r skbio/util/ -ll

# Show only high severity
bandit -r skbio/util/ -ll --severity-level high
```

## Expected Output

```
Run started:2025-11-08 23:04:21.123456

Test results:
>> Issue: [B324:hashlib] Use of weak MD5 hash for security.
   Severity: High   Confidence: High
   Location: skbio/util/_misc.py:176

>> Issue: [B607:start_process_with_partial_path] Starting a process with partial path
   Severity: Low   Confidence: High
   Location: skbio/util/_gpu.py:24

Code scanned:
    Total lines of code: 2203
    Total lines skipped: 0

Run metrics:
    Total issues (by severity):
        High: 1
        Low: 9
```

## Interpreting Results

- **High Severity:** Requires attention, potential security risk
- **Medium Severity:** Should be reviewed
- **Low Severity:** Informational, may be false positives
