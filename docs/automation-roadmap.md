# Release Automation Roadmap

## PyPI Trusted Publisher

1. Enable GitHub Actions OIDC in the `ios-simulator-cleaner` project settings.
2. On PyPI, create a new project (manual one-time) and add a Trusted Publisher with:
   - Owner: `kakashysen`
   - Repository: `kakashysen/ios-simulator-cleaner`
   - Workflow: `.github/workflows/release.yml`
3. Configure the existing `.github/workflows/release.yml` workflow (added in v0.1.0+) to use the trusted publisher once PyPI authorisation is in place.

## Tap Auto-bump

1. Add a workflow in the tap repository that watches for releases via `repository_dispatch`.
2. Use `brew bump-formula-pr` (or `homebrew/actions/bump-formula-pr`) to update the formula automatically with the new version and SHA.
3. Require human review before merging to keep the tap trustworthy.

## Testing Enhancements

- Add unit tests for non-interactive helpers (e.g., `get_directory_size`).
- Consider snapshot tests for table output to ensure UX does not regress.

With these pieces in place, PyPI publishes and tap updates can become one-click (or fully automated) after tagging a release.
