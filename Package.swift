// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "ScoutModules",
    platforms: [.iOS(.v17)],
    products: [
        .library(name: "ScoutDomain", targets: ["ScoutDomain"]),
        .library(name: "ScoutData", targets: ["ScoutData"]),
        .library(name: "ScoutDesignSystem", targets: ["ScoutDesignSystem"]),
        .library(name: "ScoutFeatures", targets: ["ScoutFeatures"])
    ],
    targets: [
        .target(name: "ScoutDomain", path: "Core/Domain"),
        .target(name: "ScoutData", dependencies: ["ScoutDomain"], path: "Core/Data"),
        .target(name: "ScoutDesignSystem", path: "Core/DesignSystem", exclude: ["README.md"]),
        .target(name: "ScoutFeatures", dependencies: ["ScoutDomain", "ScoutDesignSystem"], path: "Features")
    ]
)
