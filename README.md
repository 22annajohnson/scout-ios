# scout-ios
Scout V2 consumer iOS app built with Swift and SwiftUI.

## App foundation

Open `Scout.xcodeproj` in Xcode 16 or later, select the Scout scheme and an iOS
simulator, then Run. The minimum deployment target is iOS 17. Device signing
requires your own development team; no team or credentials are committed.

The initial screen is a launch scaffold, not a functioning player discovery or
authentication flow. It reads bundled app metadata and makes no network requests.

## Boundaries

- `App/`: executable entry point and dependency composition root.
- `Core/Domain`: value types and provider interfaces (`ScoutDomain`).
- `Core/Data`: concrete providers (`ScoutData`), depending only on domain types.
- `Core/DesignSystem`: `Tokens/Atoms/Molecules/Organisms` (`ScoutDesignSystem`).
- `Features/`: feature models/views (`ScoutFeatures`), depending on domain and
  design-system modules, never concrete data providers.
- `Resources/`: app-owned assets.
- `Tests/`: dependency-injection unit tests and a simulator launch smoke test.

The local Swift package enforces these dependency directions. There are no remote
package dependencies to resolve yet. Shared Xcode project/scheme files are source
configuration; build output and user workspace state are not.

The Java/Spring modular-monolith backend currently has no API contracts. No
proposed endpoint, authentication integration, or component schema is implemented
by this bootstrap. Those integrations must follow published backend contracts.
