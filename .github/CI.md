# CI checks

Adapted from [ScoutSports CI](https://github.com/22annajohnson/ScoutSports/tree/2d5f77110732ccdb747e642b96e538bc5065f1f1/.github).
This is the implementation plan and migration record for the user-authorized CI port.

| Legacy check | iOS repository approach |
| --- | --- |
| Markdown validation | Port the Ruby validator; scan root and nested Markdown, including `.github`, excluding build output. |
| GitHub Actions validation | Port YAML syntax and basic workflow/job structure checks. This is not a full Actions expression or shell linter. |
| iOS change detection | Skip macOS only when every changed path is Markdown outside `Resources/`. Bundled resources always run CI, including Markdown assets. Run for all other paths, source deletions/renames, missing baselines, and manual dispatch. |
| iOS tests | Retain the existing Makefile simulator build, unit tests, launch smoke test, and result upload. |
| Dependency updates | Weekly GitHub Actions updates against `develop`, capped at two open PRs. |
| Bundler cache and Fastlane | Omitted: the new app uses direct Makefile commands and has no Ruby gems. The validators use Ruby's standard library. |
| Swift package updates | Deferred until remote Swift dependencies exist. |
| Supabase validation and deployment | Omitted entirely: no Supabase workflows, credentials, database checks, or deployment. |

## Workflow behavior

Both workflows run on pull requests to `develop`, pushes to `develop`, and manual
dispatch. Jobs are selected independently:

| Changed files | iOS build/tests | Documentation | YAML/CI guards |
| --- | --- | --- | --- |
| Markdown only, outside `Resources/` | Skip | Run | Skip |
| iOS source, tests, assets, or build configuration only | Run | Skip | Skip |
| iOS files and Markdown | Run | Run | Skip |
| `.github` tooling/configuration | Run | Run if Markdown validation or shared detection is affected | Run |
| Manual run or unavailable baseline | Run | Run | Run |

Markdown resources run both iOS and documentation checks. Markdown validation
also runs when its validator, configuration, workflow, or the shared detector changes.
Change detection uses the PR merge commit
against its base, or the push's previous commit against its new commit. Null-delimited
paths preserve unusual filenames. Unknown baselines conservatively run all checks.

The `iOS validation` job succeeds only when detection succeeded and the macOS job
either passed or was intentionally skipped for documentation-only changes. It
fails if required tests fail or detection fails. The `Repository validation` job
likewise requires documentation/configuration jobs to pass or be intentionally
skipped. The small detection and final-status jobs always run so skipped work is
distinguishable from broken filtering. Repository branch protection is
unchanged; if required checks are configured later, use `iOS validation` and
`Repository validation`.

Actions are pinned to immutable commits, have read-only repository access, and
do not persist checkout credentials. Jobs have timeouts and superseded runs are
cancelled. The existing Xcode selection and seven-day test artifact retention
are preserved. No cache is added for the current dependency-free Swift package.

## Local validation

From the repository root:

```sh
ruby .github/scripts/validate-markdown.rb
ruby .github/scripts/validate-yaml.rb
python3 -m unittest discover -s .github/tests -v
```

Fixtures cover valid/invalid Markdown and YAML, documentation-only, iOS-only, and mixed changes,
code/configuration/unknown paths, deleted files, renamed source, manual runs, and
missing baselines. Hosted CI performs the full iOS build and simulator tests.

This change extends the app foundation and build workflow already on `develop`.
