using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<SupportDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("SupportDb") ?? "Data Source=support.db"));

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<SupportDbContext>();
    db.Database.EnsureCreated();
}

app.MapGet("/health", () => Results.Ok(new
{
    status = "ok",
    service = "support-portal",
    utc = DateTimeOffset.UtcNow
}));

app.MapGet("/api/tickets", async (SupportDbContext db) =>
    Results.Ok(await db.Tickets
        .OrderByDescending(ticket => ticket.CreatedAt)
        .ToListAsync()));

app.MapGet("/api/tickets/{id:int}", async (int id, SupportDbContext db) =>
{
    var ticket = await db.Tickets.FindAsync(id);
    return ticket is null ? Results.NotFound() : Results.Ok(ticket);
});

app.MapPost("/api/tickets", async (CreateTicketRequest request, SupportDbContext db) =>
{
    if (string.IsNullOrWhiteSpace(request.Title) || string.IsNullOrWhiteSpace(request.Description))
    {
        return Results.BadRequest(new { error = "Title and description are required." });
    }

    var ticket = new Ticket
    {
        Title = request.Title.Trim(),
        Description = request.Description.Trim(),
        Priority = NormalizePriority(request.Priority),
        Status = "Open",
        Requester = request.Requester?.Trim(),
        CreatedAt = DateTimeOffset.UtcNow,
        UpdatedAt = DateTimeOffset.UtcNow
    };

    db.Tickets.Add(ticket);
    await db.SaveChangesAsync();

    return Results.Created($"/api/tickets/{ticket.Id}", ticket);
});

app.MapPatch("/api/tickets/{id:int}/status", async (int id, UpdateStatusRequest request, SupportDbContext db) =>
{
    var ticket = await db.Tickets.FindAsync(id);
    if (ticket is null)
    {
        return Results.NotFound();
    }

    var allowedStatuses = new[] { "Open", "In Progress", "Resolved", "Closed" };
    var status = allowedStatuses.FirstOrDefault(item =>
        item.Equals(request.Status?.Trim(), StringComparison.OrdinalIgnoreCase));

    if (status is null)
    {
        return Results.BadRequest(new { error = $"Status must be one of: {string.Join(", ", allowedStatuses)}" });
    }

    ticket.Status = status;
    ticket.UpdatedAt = DateTimeOffset.UtcNow;
    await db.SaveChangesAsync();

    return Results.Ok(ticket);
});

app.MapDelete("/api/tickets/{id:int}", async (int id, SupportDbContext db) =>
{
    var ticket = await db.Tickets.FindAsync(id);
    if (ticket is null)
    {
        return Results.NotFound();
    }

    db.Tickets.Remove(ticket);
    await db.SaveChangesAsync();
    return Results.NoContent();
});

app.Run();

static string NormalizePriority(string? priority)
{
    var allowed = new[] { "Low", "Medium", "High", "Critical" };
    return allowed.FirstOrDefault(item =>
        item.Equals(priority?.Trim(), StringComparison.OrdinalIgnoreCase)) ?? "Medium";
}

public sealed class SupportDbContext(DbContextOptions<SupportDbContext> options) : DbContext(options)
{
    public DbSet<Ticket> Tickets => Set<Ticket>();
}

public sealed class Ticket
{
    public int Id { get; set; }
    public required string Title { get; set; }
    public required string Description { get; set; }
    public required string Priority { get; set; }
    public required string Status { get; set; }
    public string? Requester { get; set; }
    public DateTimeOffset CreatedAt { get; set; }
    public DateTimeOffset UpdatedAt { get; set; }
}

public sealed record CreateTicketRequest(
    string Title,
    string Description,
    string? Priority,
    string? Requester);

public sealed record UpdateStatusRequest(string Status);
