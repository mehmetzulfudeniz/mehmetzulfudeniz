#!/usr/bin/env python3
"""Support Diagnostic Toolkit.

A small, dependency-free CLI for common support-engineering checks:
DNS resolution, TCP connectivity, HTTP availability, TLS certificate metadata,
and JSON API health.
"""

from __future__ import annotations

import argparse
import json
import socket
import ssl
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse


@dataclass
class DiagnosticResult:
    check: str
    target: str
    ok: bool
    latency_ms: float | None = None
    details: dict[str, Any] | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _elapsed_ms(start: float) -> float:
    return round((time.perf_counter() - start) * 1000, 2)


def resolve_dns(host: str) -> DiagnosticResult:
    start = time.perf_counter()
    try:
        rows = socket.getaddrinfo(host, None)
        addresses = sorted({row[4][0] for row in rows})
        return DiagnosticResult(
            check="dns",
            target=host,
            ok=True,
            latency_ms=_elapsed_ms(start),
            details={"addresses": addresses},
        )
    except socket.gaierror as exc:
        return DiagnosticResult(
            check="dns",
            target=host,
            ok=False,
            latency_ms=_elapsed_ms(start),
            error=str(exc),
        )


def check_tcp(host: str, port: int, timeout: float = 3.0) -> DiagnosticResult:
    target = f"{host}:{port}"
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return DiagnosticResult(
                check="tcp",
                target=target,
                ok=True,
                latency_ms=_elapsed_ms(start),
                details={"port": port},
            )
    except OSError as exc:
        return DiagnosticResult(
            check="tcp",
            target=target,
            ok=False,
            latency_ms=_elapsed_ms(start),
            error=str(exc),
        )


def check_http(url: str, timeout: float = 5.0) -> DiagnosticResult:
    start = time.perf_counter()
    request = urllib.request.Request(
        url,
        method="GET",
        headers={"User-Agent": "SupportDiagnosticToolkit/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.getcode()
            return DiagnosticResult(
                check="http",
                target=url,
                ok=200 <= status < 400,
                latency_ms=_elapsed_ms(start),
                details={
                    "status": status,
                    "content_type": response.headers.get("Content-Type"),
                    "server": response.headers.get("Server"),
                },
            )
    except urllib.error.HTTPError as exc:
        return DiagnosticResult(
            check="http",
            target=url,
            ok=False,
            latency_ms=_elapsed_ms(start),
            details={"status": exc.code},
            error=str(exc),
        )
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return DiagnosticResult(
            check="http",
            target=url,
            ok=False,
            latency_ms=_elapsed_ms(start),
            error=str(exc),
        )


def check_tls(host: str, port: int = 443, timeout: float = 5.0) -> DiagnosticResult:
    target = f"{host}:{port}"
    start = time.perf_counter()
    context = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=timeout) as raw_socket:
            with context.wrap_socket(raw_socket, server_hostname=host) as tls_socket:
                certificate = tls_socket.getpeercert()
                expires_raw = certificate.get("notAfter")
                expires_at = None
                days_remaining = None
                if expires_raw:
                    expires_at = datetime.strptime(
                        expires_raw, "%b %d %H:%M:%S %Y %Z"
                    ).replace(tzinfo=timezone.utc)
                    days_remaining = (expires_at - datetime.now(timezone.utc)).days

                return DiagnosticResult(
                    check="tls",
                    target=target,
                    ok=True,
                    latency_ms=_elapsed_ms(start),
                    details={
                        "protocol": tls_socket.version(),
                        "cipher": tls_socket.cipher()[0] if tls_socket.cipher() else None,
                        "expires_at": expires_at.isoformat() if expires_at else None,
                        "days_remaining": days_remaining,
                    },
                )
    except (ssl.SSLError, OSError, ValueError) as exc:
        return DiagnosticResult(
            check="tls",
            target=target,
            ok=False,
            latency_ms=_elapsed_ms(start),
            error=str(exc),
        )


def check_json_api(url: str, timeout: float = 5.0) -> DiagnosticResult:
    start = time.perf_counter()
    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Accept": "application/json",
            "User-Agent": "SupportDiagnosticToolkit/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.getcode()
            raw = response.read(1024 * 1024)
            payload = json.loads(raw.decode(response.headers.get_content_charset() or "utf-8"))
            return DiagnosticResult(
                check="api",
                target=url,
                ok=200 <= status < 400,
                latency_ms=_elapsed_ms(start),
                details={
                    "status": status,
                    "json_type": type(payload).__name__,
                    "sample_keys": list(payload.keys())[:10] if isinstance(payload, dict) else None,
                },
            )
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, OSError) as exc:
        return DiagnosticResult(
            check="api",
            target=url,
            ok=False,
            latency_ms=_elapsed_ms(start),
            error=str(exc),
        )


def normalize_host(value: str) -> str:
    if "://" in value:
        parsed = urlparse(value)
        if not parsed.hostname:
            raise ValueError(f"Could not extract host from {value!r}")
        return parsed.hostname
    return value.strip()


def print_result(result: DiagnosticResult, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        return

    icon = "PASS" if result.ok else "FAIL"
    latency = f" ({result.latency_ms} ms)" if result.latency_ms is not None else ""
    print(f"[{icon}] {result.check.upper()} {result.target}{latency}")
    if result.details:
        for key, value in result.details.items():
            print(f"  - {key}: {value}")
    if result.error:
        print(f"  - error: {result.error}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Support-engineering network diagnostic CLI")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    dns_parser = subparsers.add_parser("dns", help="Resolve a hostname")
    dns_parser.add_argument("host")

    tcp_parser = subparsers.add_parser("tcp", help="Test TCP connectivity")
    tcp_parser.add_argument("host")
    tcp_parser.add_argument("port", type=int)

    http_parser = subparsers.add_parser("http", help="Check an HTTP/HTTPS endpoint")
    http_parser.add_argument("url")

    tls_parser = subparsers.add_parser("tls", help="Inspect TLS connectivity and certificate expiry")
    tls_parser.add_argument("host")
    tls_parser.add_argument("--port", type=int, default=443)

    api_parser = subparsers.add_parser("api", help="Check a JSON API endpoint")
    api_parser.add_argument("url")

    all_parser = subparsers.add_parser("all", help="Run DNS, TCP, HTTP and TLS checks for a URL")
    all_parser.add_argument("url")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    results: list[DiagnosticResult] = []

    if args.command == "dns":
        results.append(resolve_dns(normalize_host(args.host)))
    elif args.command == "tcp":
        results.append(check_tcp(normalize_host(args.host), args.port))
    elif args.command == "http":
        results.append(check_http(args.url))
    elif args.command == "tls":
        results.append(check_tls(normalize_host(args.host), args.port))
    elif args.command == "api":
        results.append(check_json_api(args.url))
    elif args.command == "all":
        parsed = urlparse(args.url if "://" in args.url else f"https://{args.url}")
        host = parsed.hostname
        if not host:
            raise SystemExit("Invalid URL")
        scheme = parsed.scheme or "https"
        port = parsed.port or (443 if scheme == "https" else 80)
        normalized_url = args.url if "://" in args.url else f"https://{args.url}"
        results.extend([
            resolve_dns(host),
            check_tcp(host, port),
            check_http(normalized_url),
        ])
        if scheme == "https":
            results.append(check_tls(host, port))

    if args.json and len(results) > 1:
        print(json.dumps([item.to_dict() for item in results], indent=2, ensure_ascii=False))
    else:
        for result in results:
            print_result(result, args.json)

    return 0 if all(result.ok for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
