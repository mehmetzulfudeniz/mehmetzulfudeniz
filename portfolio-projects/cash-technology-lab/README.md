# Cash Technology Lab

> Independent portfolio project for cash-processing software, device integration, monitoring, reconciliation, and audit workflows.

[![Unofficial](https://img.shields.io/badge/status-unofficial%20engineering%20lab-blue)](#legal--scope)

This project demonstrates software-engineering skills relevant to **cash centers, cash-in-transit operations, banknote processing systems, and technical support**. It uses publicly documented Giesecke+Devrient (G+D) product capabilities only as domain references.

**It does not contain G+D source code, firmware, binaries, license files, credentials, proprietary communication protocols, or reverse-engineered interfaces.**

## Why this project exists

Modern cash operations combine hardware, software, networking, reconciliation, monitoring, traceability, and service engineering. The goal of this lab is to demonstrate those engineering concepts with original, testable code.

## Implemented modules

### 1. Banknote processing engine

`cashtech/engine.py`

- count and denomination modes
- authentication reject handling
- fitness sorting
- orientation sorting
- serial-number capture when supported by the selected simulation profile
- accepted/rejected value and quantity summaries
- output-stacker allocation
- multi-currency validation boundary

### 2. Public-spec device profiles

`cashtech/profiles.py`

Simulation profiles currently cover publicly described capabilities for:

- G+D BPS C1
- G+D BPS C2-4 evo
- G+D BPS C6
- G+D BPS M3 / M evo
- G+D BPS M5 / M evo
- G+D BPS M7 / M evo

The profiles are **not device emulators**. They are configuration objects for an original processing simulator.

### 3. Vendor-neutral device gateway

`cashtech/gateway.py`

A clean transport abstraction separates business logic from machine communication. The repository ships only a `LoopbackTransport` simulator.

A real device adapter should be added only when the developer has the vendor's authorized SDK/protocol documentation and the legal right to use it.

### 4. Fleet monitoring and KPIs

`cashtech/monitor.py`

- online/offline state
- processed/rejected totals
- reject rate
- preventive-service status
- temperature alerting
- device error aggregation

This models the type of operational visibility expected in a professional cash-center environment without cloning any vendor software.

### 5. Tamper-evident audit trail

`cashtech/audit.py`

Processing events are written to an append-only JSONL audit log chained with SHA-256 hashes. Any change to an earlier event invalidates the verification chain.

This is a portfolio implementation of a common financial-operations requirement: traceable and integrity-checked operational history.

## Quick start

Requires Python 3.11+ and no third-party dependencies.

```bash
cd portfolio-projects/cash-technology-lab
python cli.py --profile bps-c1 --count 250 --mode denomination
```

Fitness simulation:

```bash
python cli.py --profile bps-m5 --count 1000 --mode fitness
```

Serial-capture simulation:

```bash
python cli.py --profile bps-m7 --count 100 --mode serial_capture
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Architecture

```text
                    +----------------------+
                    |  Cash Center / App   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | CashDeviceGateway    |
                    | vendor-neutral API   |
                    +----------+-----------+
                               |
                    +----------+-----------+
                    |                      |
                    v                      v
          +------------------+    +------------------+
          | LoopbackTransport|    | Authorized SDK  |
          | included simulator|   | adapter (future)|
          +------------------+    +------------------+

          +------------------+    +------------------+
          | CashProcessor    |--->| Audit Log        |
          +--------+---------+    +------------------+
                   |
                   v
          +------------------+
          | Fleet KPI /      |
          | Monitoring       |
          +------------------+
```

## Public G+D domain references

G+D's public product material describes cash-center capabilities such as banknote counting/authentication, denomination and fitness sorting, serial-number reading, device connectivity, cash-center automation, track-and-trace, real-time KPIs, remote management, and secure software platforms.

See [`docs/GD_PUBLIC_PRODUCT_MAP.md`](docs/GD_PUBLIC_PRODUCT_MAP.md) for the capability map used when designing this independent lab.

## Planned engineering extensions

- REST API around processing sessions
- SQLite/PostgreSQL persistence
- operator and supervisor roles
- deposit and bag reconciliation
- shift/session closing reports
- simulated device fault codes and maintenance workflow
- metrics endpoint for observability
- Dockerized demo environment
- Android technician companion application
- authorized vendor SDK adapter interface when documentation is legally available

## Legal & scope

G+D, BPS, M evo, Compass, Eco-Remote, Eco-Protect and related product names are trademarks/product names of their respective owner. They are referenced here only to describe publicly documented domain context and interoperability learning goals.

This repository is **not affiliated with, endorsed by, or supplied by G+D**.
