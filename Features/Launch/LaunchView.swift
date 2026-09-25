import ScoutDesignSystem
import SwiftUI

/// Neutral launch scaffold, replaced by the authenticated feature flow in later tickets.
public struct LaunchView: View {
    private let model: LaunchModel

    public init(model: LaunchModel) {
        self.model = model
    }

    public var body: some View {
        NavigationStack {
            ScrollView {
                VStack {
                    ScoutTitle("Scout")
                        .accessibilityIdentifier("launch.title")
                    Text("Find your next game.")
                    Text("Version \(model.appInfo.version) (\(model.appInfo.build))")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                        .accessibilityIdentifier("launch.version")
                }
                .frame(maxWidth: .infinity)
                .padding()
            }
        }
    }
}
