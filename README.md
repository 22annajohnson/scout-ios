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

## Build and test

Xcode 16+ supports the project; CI selects Xcode 26.1 on `macos-15`. Install an iOS
simulator runtime in Xcode before testing. Run these commands from the repo root:

```sh
make resolve
make build
make test-unit   # focused dependency-injection tests
make test        # unit tests plus the launch smoke test
```

`make` lists commands without booting a simulator. Tests select an available iPhone
from the newest installed iOS runtime and disable parallel simulator clones. To
choose a specific device, use `make test SIMULATOR_ID=<UDID>`; find IDs with
`xcrun simctl list devices available`. `DEVELOPER_DIR` can select another Xcode.

Build output goes under `build/DerivedData`. Test results go to
`build/TestResults.xcresult`; open them in Xcode. To rerun without overwriting the
previous result, use `make test RESULT_BUNDLE=build/Retry.xcresult`.
The Makefile intentionally refuses to delete existing result bundles.

The `iOS` workflow runs dependency resolution, a simulator build, unit tests, and
the launch smoke test on pull requests to `develop` and pushes to `develop`. It
keeps result bundles for seven days, including failures, and uses read-only repo
permissions. No signing secrets or backend credentials are needed. Add and commit
Xcode's shared `Package.resolved` when remote package dependencies are introduced.

Runner toolchain reference:
[GitHub macOS 15 image](https://github.com/actions/runner-images/blob/main/images/macos/macos-15-Readme.md).
