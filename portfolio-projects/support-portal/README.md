# Support Portal

A compact **ASP.NET Core + SQLite** ticket and incident-management API designed as a portfolio project for Support Engineer / Software Developer roles.

## Features

- Health endpoint
- Create support tickets
- List and retrieve tickets
- Update ticket status
- Delete tickets
- Priority normalization
- SQLite persistence with Entity Framework Core
- Input validation and clear HTTP responses

## Tech Stack

- C#
- .NET 8
- ASP.NET Core Minimal APIs
- Entity Framework Core
- SQLite
- REST / JSON

## Run

```bash
dotnet restore
dotnet run
```

The service creates `support.db` automatically on first run.

## API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/health` | Service health |
| GET | `/api/tickets` | List tickets |
| GET | `/api/tickets/{id}` | Get a ticket |
| POST | `/api/tickets` | Create a ticket |
| PATCH | `/api/tickets/{id}/status` | Change status |
| DELETE | `/api/tickets/{id}` | Delete a ticket |

### Create Ticket

```json
{
  "title": "User cannot sign in",
  "description": "Authentication returns HTTP 401 after password reset.",
  "priority": "High",
  "requester": "support@example.com"
}
```

### Update Status

```json
{
  "status": "In Progress"
}
```

## What This Demonstrates

- REST API design
- CRUD workflows
- SQL-backed persistence
- Basic incident/ticket lifecycle modeling
- HTTP status handling
- Separation of support-domain concepts into an API service

## Next Iteration

- Authentication and role-based authorization
- Ticket comments and audit history
- SLA timers and escalation rules
- Search and filtering
- OpenAPI/Swagger
- Automated tests
- Docker support
- PostgreSQL production profile
