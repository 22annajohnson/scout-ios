import Foundation
import ScoutDomain

/// Reads only bundled metadata. This foundation makes no backend requests.
public struct BundleAppInfoProvider: AppInfoProviding {
    private let info: AppInfo

    public init(bundle: Bundle = .main) {
        info = AppInfo(
            version: bundle.object(forInfoDictionaryKey: "CFBundleShortVersionString") as? String ?? "—",
            build: bundle.object(forInfoDictionaryKey: "CFBundleVersion") as? String ?? "—"
        )
    }

    public func appInfo() -> AppInfo { info }
}
