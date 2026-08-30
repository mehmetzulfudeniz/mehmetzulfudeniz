using System.Collections.Concurrent;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var sessions = new ConcurrentDictionary<Guid, ProcessingSession>();
var deposits = new ConcurrentDictionary<Guid, Deposit>();
var devices = new ConcurrentDictionary<string, DeviceStatus>(StringComparer.OrdinalIgnoreCase);

app.MapGet("/health", () => Results.Ok(new
{
    status = "ok",
    service = "cash-center-operations-api",
    utc = DateTimeOffset.UtcNow
}));

app.MapGet("/api/devices", () => Results.Ok(devices.Values.OrderBy(x => x.DeviceId)));

app.MapPut("/api/devices/{deviceId}", (string deviceId, DeviceStatusUpdate update) =>
{
    var status = new DeviceStatus(
        DeviceId: deviceId,
        Profile: update.Profile.Trim(),
        Online: update.Online,
        TemperatureC: update.TemperatureC,
        ProcessedTotal: Math.Max(0, update.ProcessedTotal),
        RejectTotal: Math.Max(0, update.RejectTotal),
        ServiceDue: update.ServiceDue,
        LastError: string.IsNullOrWhiteSpace(update.LastError) ? null : update.LastError.Trim(),
        UpdatedAt: DateTimeOffset.UtcNow);

    devices[deviceId] = status;
    return Results.Ok(status);
});

app.MapPost("/api/sessions", (CreateSession request) =>
{
    if (string.IsNullOrWhiteSpace(request.OperatorId) || string.IsNullOrWhiteSpace(request.DeviceId))
        return Results.BadRequest(new { error = "operatorId and deviceId are required" });

    var session = new ProcessingSession(
        Id: Guid.NewGuid(),
        OperatorId: request.OperatorId.Trim(),
        DeviceId: request.DeviceId.Trim(),
        Currency: request.Currency.Trim().ToUpperInvariant(),
        Status: "open",
        StartedAt: DateTimeOffset.UtcNow,
        ClosedAt: null,
        CountedValue: 0m,
        CountedNotes: 0,
        RejectNotes: 0);

    sessions[session.Id] = session;
    return Results.Created($"/api/sessions/{session.Id}", session);
});

app.MapGet("/api/sessions", () => Results.Ok(sessions.Values.OrderByDescending(x => x.StartedAt)));

app.MapGet("/api/sessions/{id:guid}", (Guid id) =>
    sessions.TryGetValue(id, out var session) ? Results.Ok(session) : Results.NotFound());

app.MapPost("/api/sessions/{id:guid}/count", (Guid id, CountUpdate update) =>
{
    if (!sessions.TryGetValue(id, out var session)) return Results.NotFound();
    if (session.Status != "open") return Results.Conflict(new { error = "session is closed" });
    if (update.AcceptedNotes < 0 || update.RejectedNotes < 0 || update.AcceptedValue < 0)
        return Results.BadRequest(new { error = "count values cannot be negative" });

    var updated = session with
    {
        CountedNotes = session.CountedNotes + update.AcceptedNotes,
        RejectNotes = session.RejectNotes + update.RejectedNotes,
        CountedValue = session.CountedValue + update.AcceptedValue
    };
    sessions[id] = updated;
    return Results.Ok(updated);
});

app.MapPost("/api/sessions/{id:guid}/close", (Guid id) =>
{
    if (!sessions.TryGetValue(id, out var session)) return Results.NotFound();
    if (session.Status == "closed") return Results.Ok(session);

    var updated = session with { Status = "closed", ClosedAt = DateTimeOffset.UtcNow };
    sessions[id] = updated;
    return Results.Ok(updated);
});

app.MapPost("/api/deposits", (CreateDeposit request) =>
{
    if (request.ExpectedAmount < 0) return Results.BadRequest(new { error = "expectedAmount cannot be negative" });

    var deposit = new Deposit(
        Id: Guid.NewGuid(),
        CustomerReference: request.CustomerReference.Trim(),
        Currency: request.Currency.Trim().ToUpperInvariant(),
        ExpectedAmount: request.ExpectedAmount,
        CountedAmount: null,
        Status: "received",
        ReceivedAt: DateTimeOffset.UtcNow,
        ReconciledAt: null);

    deposits[deposit.Id] = deposit;
    return Results.Created($"/api/deposits/{deposit.Id}", deposit);
});

app.MapGet("/api/deposits", () => Results.Ok(deposits.Values.OrderByDescending(x => x.ReceivedAt)));

app.MapPost("/api/deposits/{id:guid}/reconcile", (Guid id, ReconcileDeposit request) =>
{
    if (!deposits.TryGetValue(id, out var deposit)) return Results.NotFound();
    if (request.CountedAmount < 0) return Results.BadRequest(new { error = "countedAmount cannot be negative" });

    var variance = request.CountedAmount - deposit.ExpectedAmount;
    var updated = deposit with
    {
        CountedAmount = request.CountedAmount,
        Status = variance == 0 ? "reconciled" : "variance",
        ReconciledAt = DateTimeOffset.UtcNow
    };
    deposits[id] = updated;

    return Results.Ok(new
    {
        deposit = updated,
        variance,
        matched = variance == 0
    });
});

app.MapGet("/api/kpis", () =>
{
    var deviceItems = devices.Values.ToArray();
    var sessionItems = sessions.Values.ToArray();
    var depositItems = deposits.Values.ToArray();

    var processed = deviceItems.Sum(x => x.ProcessedTotal);
    var rejected = deviceItems.Sum(x => x.RejectTotal);

    return Results.Ok(new
    {
        devices = new
        {
            total = deviceItems.Length,
            online = deviceItems.Count(x => x.Online),
            serviceDue = deviceItems.Count(x => x.ServiceDue),
            processedTotal = processed,
            rejectTotal = rejected,
            rejectRate = processed == 0 ? 0d : (double)rejected / processed
        },
        sessions = new
        {
            open = sessionItems.Count(x => x.Status == "open"),
            closed = sessionItems.Count(x => x.Status == "closed"),
            countedValue = sessionItems.Sum(x => x.CountedValue)
        },
        deposits = new
        {
            total = depositItems.Length,
            reconciled = depositItems.Count(x => x.Status == "reconciled"),
            withVariance = depositItems.Count(x => x.Status == "variance")
        }
    });
});

app.Run();

record DeviceStatus(
    string DeviceId,
    string Profile,
    bool Online,
    double TemperatureC,
    long ProcessedTotal,
    long RejectTotal,
    bool ServiceDue,
    string? LastError,
    DateTimeOffset UpdatedAt);

record DeviceStatusUpdate(
    string Profile,
    bool Online,
    double TemperatureC,
    long ProcessedTotal,
    long RejectTotal,
    bool ServiceDue,
    string? LastError);

record ProcessingSession(
    Guid Id,
    string OperatorId,
    string DeviceId,
    string Currency,
    string Status,
    DateTimeOffset StartedAt,
    DateTimeOffset? ClosedAt,
    decimal CountedValue,
    int CountedNotes,
    int RejectNotes);

record CreateSession(string OperatorId, string DeviceId, string Currency);
record CountUpdate(int AcceptedNotes, int RejectedNotes, decimal AcceptedValue);

record Deposit(
    Guid Id,
    string CustomerReference,
    string Currency,
    decimal ExpectedAmount,
    decimal? CountedAmount,
    string Status,
    DateTimeOffset ReceivedAt,
    DateTimeOffset? ReconciledAt);

record CreateDeposit(string CustomerReference, string Currency, decimal ExpectedAmount);
record ReconcileDeposit(decimal CountedAmount);
