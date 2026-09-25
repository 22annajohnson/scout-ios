/// Non-sensitive metadata needed by the launch feature.
public struct AppInfo: Equatable, Sendable {
    public let version: String
    public let build: String

    public init(version: String, build: String) {
        self.version = version
        self.build = build
    }
}

public protocol AppInfoProviding: Sendable {
    func appInfo() -> AppInfo
}
