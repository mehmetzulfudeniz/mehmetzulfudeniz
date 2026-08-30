# GitHub Portfolio Audit

This document records the curation strategy for the public GitHub profile.

## Tier 1 — Feature

| Repository / Project | Status | Portfolio role |
| --- | --- | --- |
| `portfolio-projects/cash-technology-lab` | Active, tested | Primary cash technology / Python / device integration evidence |
| `portfolio-projects/cash-center-operations-api` | Active | Primary cash-center workflow / C# / ASP.NET evidence |
| `portfolio-projects/support-diagnostic-toolkit` | Active, tested | Primary Support Engineer / Python evidence |
| `portfolio-projects/support-portal` | Active, CI-built | Primary C# / ASP.NET / SQL evidence |
| `portfolio-projects/android-support-app` | Active, CI-built | Primary Kotlin / modern Android evidence |
| `InstagramClone` | Existing project, cleanup completed | Java / Android / Firebase evidence |
| `FriutSalad` | Existing project, documented | Java / LibGDX / Android game-development evidence |
| `Snake` | Refactored | Small Python/OOP project |

## Cash Technology Positioning

The profile now contains original software for cash-processing environments without redistributing vendor-owned code:

- public-spec BPS device simulation profiles
- denomination, authentication, fitness, orientation and serial-capture workflows
- vendor-neutral cash-device gateway abstraction
- device health, reject-rate and service monitoring
- tamper-evident SHA-256 chained audit records
- operator processing sessions
- deposit receiving and reconciliation
- variance detection
- cash-center KPIs

G+D/BPS/M evo/Compass/Eco product names are used only for public industry context. No proprietary G+D source code, firmware, binary, credential, license material, or reverse-engineered protocol is included.

## Tier 2 — Learning / Security Labs

These projects should not be pinned as primary software-engineering work.

| Repository | Recommendation |
| --- | --- |
| `BufferOverflow` | Keep only as an explicitly authorized security lab; do not feature |
| `Keylogger` | Archive or keep strictly as a documented security-learning artifact; do not feature |
| `Backdoor` | Archive or keep strictly as a documented security-learning artifact; do not feature |
| `middleMan` | Archive or keep strictly as an ARP security lab; do not feature |
| `juice-shop` | Keep as a clearly attributed OWASP fork / training environment; never present as original work |

## Tier 3 — Archive Candidates

| Repository | Reason |
| --- | --- |
| `CryptoView` | No active implementation on the current default branch |
| `NFTgenerator` | Inactive concept / no active implementation |

## Completed Improvements

- Published and expanded the dedicated profile README.
- Added Support Diagnostic Toolkit, Support Portal, and Android Support App.
- Added Cash Technology Lab with public-spec device profiles, processing engine, gateway, monitoring, audit log, CLI, and tests.
- Added Cash Center Operations API for device telemetry, sessions, deposits, reconciliation, and KPIs.
- Added documentation to existing projects.
- Refactored the Snake implementation for readability and OOP structure.
- Removed tracked Android Studio metadata from `InstagramClone`.
- Removed the tracked Firebase client configuration from `InstagramClone` and updated setup instructions.
- Removed generated release artifacts from `FriutSalad` source control.
- Added repository-wide generated-file exclusions for the profile project workspace.
- Added CI validation for Python, .NET, Android, and cash-technology projects.
- Clearly separated original engineering work from security training/forked code.

## GitHub UI Actions Still Required

The connected GitHub API used for this rebuild does not expose repository pinning, repository renaming, or archive-state updates. In the GitHub web UI:

1. Move `cash-technology-lab`, `cash-center-operations-api`, `support-diagnostic-toolkit`, `support-portal`, and `android-support-app` into standalone repositories when repository creation is available.
2. Pin the cash-technology projects first if targeting G+D, cash-in-transit, banking technology, service engineering, or cash-center roles.
3. Archive `CryptoView` and `NFTgenerator` unless they are intentionally revived.
4. Strongly consider archiving `Keylogger`, `Backdoor`, and `middleMan` from the public recruiter-facing profile.
5. Keep `juice-shop` only as an attributed fork for security learning.

## Target Recruiter Signal

The public profile should communicate, in this order:

1. Cash technology, cash-processing systems and operational software
2. Practical troubleshooting and Support Engineering ability
3. C# / ASP.NET backend development
4. Python automation, device integration and diagnostics
5. Android/Kotlin development
6. Existing Android/Firebase and game-development experience
7. Defensive security knowledge as a secondary learning area
