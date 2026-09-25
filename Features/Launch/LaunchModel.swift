import ScoutDomain

public struct LaunchModel: Sendable {
    public let appInfo: AppInfo

    public init(appInfoProvider: any AppInfoProviding) {
        appInfo = appInfoProvider.appInfo()
    }
}
