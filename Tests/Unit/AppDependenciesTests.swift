import ScoutDomain
import XCTest
@testable import Scout

final class AppDependenciesTests: XCTestCase {
    func testLaunchUsesInjectedProviderInsteadOfLiveBundle() {
        let expected = AppInfo(version: "test-version", build: "test-build")
        let dependencies = AppDependencies(appInfoProvider: StubAppInfoProvider(info: expected))

        XCTAssertEqual(dependencies.makeLaunchModel().appInfo, expected)
    }

    func testLiveProviderReadsApplicationMetadata() {
        let model = AppDependencies.live().makeLaunchModel()

        XCTAssertEqual(model.appInfo, AppInfo(version: "0.1.0", build: "1"))
    }
}

private struct StubAppInfoProvider: AppInfoProviding {
    let info: AppInfo
    func appInfo() -> AppInfo { info }
}
