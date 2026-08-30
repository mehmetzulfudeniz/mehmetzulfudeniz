# Cash Center Operations API

Independent .NET 8 REST API for cash-center workflow modeling.

This portfolio project demonstrates software concepts that appear in modern cash-management environments: device telemetry, operator processing sessions, deposit receiving, reconciliation, and operational KPIs.

It is **not G+D software**, does not contain G+D source code or binaries, and does not implement any proprietary G+D protocol. Publicly documented G+D cash-management capabilities are used only as domain context.

## Features

- service health endpoint
- device health/telemetry registration
- operator processing sessions
- accumulated accepted/rejected note counts
- deposit receiving
- expected-versus-counted reconciliation
- variance detection
- fleet and cash-operation KPIs
- OpenAPI endpoint in Development mode

## Run

```bash
dotnet restore
dotnet run
```

Health check:

```http
GET /health
```

Register/update a simulated cash-processing device:

```http
PUT /api/devices/CASH-01
Content-Type: application/json

{
  "profile": "BPS C1 simulation",
  "online": true,
  "temperatureC": 39.2,
  "processedTotal": 125000,
  "rejectTotal": 870,
  "serviceDue": false,
  "lastError": null
}
```

Open a processing session:

```http
POST /api/sessions
Content-Type: application/json

{
  "operatorId": "operator-01",
  "deviceId": "CASH-01",
  "currency": "TRY"
}
```

Receive a deposit:

```http
POST /api/deposits
Content-Type: application/json

{
  "customerReference": "DEP-2026-0001",
  "currency": "TRY",
  "expectedAmount": 250000
}
```

Reconcile it:

```http
POST /api/deposits/{depositId}/reconcile
Content-Type: application/json

{
  "countedAmount": 249950
}
```

Operational KPI snapshot:

```http
GET /api/kpis
```

## Domain design

The API intentionally keeps machine communication outside the workflow service. A production architecture would use an authorized hardware adapter or vendor SDK to publish normalized device events into this service.

```text
Authorized device SDK / adapter
            |
            v
    normalized telemetry
            |
            v
+----------------------------+
| Cash Center Operations API |
| sessions / deposits / KPI  |
+----------------------------+
            |
            v
 audit / persistence / BI
```

## Planned extensions

- PostgreSQL persistence
- role-based operator/supervisor authorization
- immutable audit events
- bag/cassette/container tracking
- denomination breakdown per deposit
- shift closing
- exception approval workflow
- WebSocket/SSE device monitoring
- metrics endpoint and dashboards
- integration tests

## Legal / trademark notice

G+D and related product names belong to their respective owner. This project is independent, unofficial, and intended to demonstrate software engineering for cash-technology environments.
