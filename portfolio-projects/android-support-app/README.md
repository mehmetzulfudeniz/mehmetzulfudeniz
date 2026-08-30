# Android Support App — Support Health

A small Android utility for first-line endpoint diagnostics, built as a portfolio project for Android and Technical Support Engineering roles.

## Current MVP

- Enter an HTTPS endpoint
- Run an HTTP reachability check
- Display HTTP response code
- Measure response latency
- Handle connectivity and URL errors
- Keep UI state in a ViewModel with StateFlow
- Run network work off the main thread with coroutines

## Architecture

`Compose UI → ViewModel → coroutine/IO diagnostic operation → StateFlow → UI`

## Stack

- Kotlin 2.3.21
- Android Gradle Plugin 9.3.0
- compileSdk / targetSdk 37
- Jetpack Compose BOM 2026.08.00
- Material 3
- Lifecycle ViewModel 2.11.0
- Kotlin Coroutines through lifecycle-viewmodel-ktx

## Open in Android Studio

Open the `android-support-app` directory as a Gradle project and let Android Studio sync dependencies.

## Roadmap

- DNS resolution diagnostics
- TCP port checks through a support-safe endpoint workflow
- TLS certificate details and expiry
- REST API JSON validation
- Room-backed diagnostic history
- Shareable incident report
- MVVM repository layer
- Automated ViewModel tests
- CI build workflow

## Portfolio Value

This project demonstrates modern Android UI development while solving a realistic support-engineering problem rather than acting as a purely visual sample application.
