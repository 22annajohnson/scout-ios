import XCTest

final class LaunchTests: XCTestCase {
    @MainActor
    func testSmokeLaunch() {
        let app = XCUIApplication()
        app.launch()

        XCTAssertTrue(app.staticTexts["launch.title"].waitForExistence(timeout: 10))
        XCTAssertEqual(app.staticTexts["launch.title"].label, "Scout")
        XCTAssertTrue(app.staticTexts["launch.version"].exists)
        XCTAssertEqual(app.state, .runningForeground)
    }
}
