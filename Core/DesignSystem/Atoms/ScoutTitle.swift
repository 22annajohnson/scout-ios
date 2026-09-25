import SwiftUI

/// A semantic title for the bootstrap screen; product styling follows separately.
public struct ScoutTitle: View {
    private let title: LocalizedStringKey

    public init(_ title: LocalizedStringKey) {
        self.title = title
    }

    public var body: some View {
        Text(title)
            .font(.largeTitle.bold())
            .accessibilityAddTraits(.isHeader)
    }
}
