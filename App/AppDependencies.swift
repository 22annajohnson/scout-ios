import ScoutData
import ScoutDomain
import ScoutFeatures

/// The composition root is the only place that selects concrete data providers.
struct AppDependencies {
    let appInfoProvider: any AppInfoProviding

    static func live() -> AppDependencies {
        AppDependencies(appInfoProvider: BundleAppInfoProvider())
    }

    func makeLaunchModel() -> LaunchModel {
        LaunchModel(appInfoProvider: appInfoProvider)
    }
}
