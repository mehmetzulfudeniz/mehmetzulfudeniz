# Support Diagnostic Toolkit

A dependency-free Python CLI for common Technical Support / Support Engineering checks.

## Checks

- DNS resolution
- TCP port connectivity
- HTTP/HTTPS availability
- TLS protocol, cipher and certificate expiry
- JSON API reachability and response validation
- Combined endpoint health check

## Usage

```bash
python diagnostic.py dns example.com
python diagnostic.py tcp example.com 443
python diagnostic.py http https://example.com
python diagnostic.py tls example.com
python diagnostic.py api https://api.github.com
python diagnostic.py all https://example.com
```

Machine-readable output is available with `--json`:

```bash
python diagnostic.py --json all https://example.com
```

## Why This Project Exists

Support engineers frequently need to isolate whether an incident is related to DNS, TCP connectivity, HTTP behavior, TLS, or an upstream API. This tool groups those first-line checks into one portable CLI without third-party dependencies.

## Roadmap

- Batch checks from YAML/JSON configuration
- HTTP header assertions
- DNS record-type queries
- Exportable incident report
- Retry/backoff policies
- Unit and integration tests
- GitHub Actions CI
