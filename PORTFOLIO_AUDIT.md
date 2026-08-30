# GitHub Portfolio Audit

This document records the curation strategy for the public GitHub profile.

## Tier 1 — Feature

| Repository / Project | Status | Portfolio role |
| --- | --- | --- |
| `portfolio-projects/support-diagnostic-toolkit` | Active MVP | Primary Support Engineer / Python evidence |
| `portfolio-projects/support-portal` | Active MVP | Primary C# / ASP.NET / SQL evidence |
| `portfolio-projects/android-support-app` | Active MVP | Primary Kotlin / modern Android evidence |
| `InstagramClone` | Existing project, cleanup completed | Java / Android / Firebase evidence |
| `FriutSalad` | Existing project, documented | Java / LibGDX / Android game-development evidence |
| `Snake` | Refactored | Small Python/OOP project |

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

- Published a dedicated profile README.
- Added three job-focused portfolio MVPs.
- Added documentation to existing projects.
- Refactored the Snake implementation for readability and OOP structure.
- Removed tracked Android Studio metadata from `InstagramClone`.
- Removed the tracked Firebase client configuration from `InstagramClone` and updated setup instructions.
- Added repository-wide generated-file exclusions for the profile project workspace.
- Added CI configuration for Python, .NET, and Android validation.
- Clearly separated original engineering work from security training/forked code.

## GitHub UI Actions Still Required

The connected GitHub API used for this rebuild does not expose repository pinning, repository renaming, or archive-state updates. In the GitHub web UI:

1. Pin the strongest repositories/projects first: profile repo, `InstagramClone`, `FriutSalad`, and `Snake` until the three portfolio MVPs are moved to standalone repositories.
2. Archive `CryptoView` and `NFTgenerator` unless they are intentionally revived.
3. Strongly consider archiving `Keylogger`, `Backdoor`, and `middleMan` from the public recruiter-facing profile.
4. Keep `juice-shop` only as an attributed fork for security learning.
5. When standalone repos are available, move each `portfolio-projects/*` project into its own repository and pin them above older learning projects.

## Target Recruiter Signal

The public profile should communicate, in this order:

1. Practical troubleshooting and Support Engineering ability
2. Android/Kotlin development
3. C# / ASP.NET backend development
4. Python automation and diagnostics
5. Existing Android/Firebase and game-development experience
6. Defensive security knowledge as a secondary learning area
