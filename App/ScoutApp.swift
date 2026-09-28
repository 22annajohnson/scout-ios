import ScoutFeatures
import SwiftUI

@main
struct ScoutApp: App {
    private let dependencies = AppDependencies.live()

    var body: some Scene {
        WindowGroup {
            LaunchView(model: dependencies.makeLaunchModel())
        }
    }
}
