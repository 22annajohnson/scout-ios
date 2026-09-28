SHELL := /bin/bash
.DEFAULT_GOAL := help

PROJECT := Scout.xcodeproj
SCHEME := Scout
DERIVED_DATA ?= build/DerivedData
RESULT_BUNDLE ?= build/TestResults.xcresult
SIMULATOR_ID ?= $(shell python3 scripts/select-simulator.py)
DESTINATION = platform=iOS Simulator,id=$(SIMULATOR_ID)
XCODEBUILD = xcodebuild -project $(PROJECT) -scheme $(SCHEME) -derivedDataPath "$(DERIVED_DATA)" CODE_SIGNING_ALLOWED=NO

.PHONY: help resolve build test test-unit
help:
	@echo "make resolve    Resolve Swift package dependencies"
	@echo "make build      Build for a generic iOS simulator"
	@echo "make test-unit  Run unit tests on one available iPhone simulator"
	@echo "make test       Run unit tests and the launch smoke test"
	@echo "Override SIMULATOR_ID, DERIVED_DATA, or RESULT_BUNDLE as needed."

resolve:
	$(XCODEBUILD) -resolvePackageDependencies

build:
	$(XCODEBUILD) -destination 'generic/platform=iOS Simulator' build

test test-unit:
	@test -n "$(SIMULATOR_ID)" || (echo "No available iPhone simulator. Install an iOS runtime in Xcode." >&2; exit 1)
	@test ! -e "$(RESULT_BUNDLE)" || (echo "$(RESULT_BUNDLE) already exists. Use a new RESULT_BUNDLE path." >&2; exit 1)
	@mkdir -p "$(dir $(RESULT_BUNDLE))"
	$(XCODEBUILD) -destination "$(DESTINATION)" -parallel-testing-enabled NO -resultBundlePath "$(RESULT_BUNDLE)" $(if $(filter test-unit,$@),-only-testing:ScoutTests,) test
