# Homebrew Release Guide

This project ships a `Formula/ios-simulator-cleaner.rb` definition that can be published through a custom tap, for example `homebrew-ios-simulator-cleaner`.

Follow these steps for each release:

1. **Create a Git tag**
   ```bash
   git switch main
   git pull --ff-only
   poetry version patch  # bump if needed
   git commit -am "chore: release v$(poetry version -s)"
   git tag "v$(poetry version -s)"
   git push origin main --tags
   ```

2. **Create a GitHub release**
   - Visit <https://github.com/kakashysen/ios-simulator-cleaner/releases/new>.
   - Select the tag (e.g. `v0.1.0`).
   - Attach the Poetry artifacts from `dist/` if desired.
   - Publish the release and copy the generated source tarball URL.

3. **Update the formula**
   ```bash
   export VERSION=$(poetry version -s)
   curl -L -o /tmp/ios-simulator-cleaner.tar.gz \
     "https://github.com/kakashysen/ios-simulator-cleaner/archive/refs/tags/v${VERSION}.tar.gz"
   shasum -a 256 /tmp/ios-simulator-cleaner.tar.gz
   ```
   - Replace `REPLACE_WITH_RELEASE_TARBALL_SHA256` in `Formula/ios-simulator-cleaner.rb` with the printed digest.
   - Commit the change and push to the tap repository.

4. **Publish the tap**
   - Create (or update) the `homebrew-ios-simulator-cleaner` repository with the formula under `Formula/ios-simulator-cleaner.rb`.
   - Tag the tap repo if you follow release tags there.

5. **Test the formula**
   ```bash
   brew tap kakashysen/ios-simulator-cleaner https://github.com/kakashysen/homebrew-ios-simulator-cleaner.git
   brew install --build-from-source ios-simulator-cleaner
   ios-simulator-cleaner --version
   ```

6. **Update documentation**
   - Ensure `README.md` references the new version number if needed.
   - Announce the release wherever appropriate.

With this workflow you can publish fixes quickly while keeping the tap reproducible and automated.
