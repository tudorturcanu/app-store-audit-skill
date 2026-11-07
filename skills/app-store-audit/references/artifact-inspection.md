# Inspect release settings and artifacts

Use on macOS when source configuration or an existing archive is available. Replace example paths, scheme, and configuration with the project's actual release choices; do not assume the scheme's Archive action uses a configuration named Release. Prefer existing CI output if local package access or Xcode is unavailable. These commands collect evidence, not compliance verdicts.

## Repeatable inventory

For an unpacked `.xcarchive` or `.app`, use the standard-library Python helper from this skill directory:

```sh
python3 scripts/inventory_archive.py '/path/App.xcarchive' > '/tmp/app-inventory.json'
```

Choose an output path outside the inspected artifact. The helper does not build, sign, change the artifact, invoke Xcode, or contact services. It inventories app/extension/framework/resource bundles and privacy manifests, reads XML or binary plists, and emits selected identity fields, purpose-string key names, privacy declarations, and SHA-256 hashes of inspected plist bytes. It omits arbitrary custom Info.plist values. It does not extract `.ipa` files.

Exit `0` means collection completed without reported gaps; `1` means partial inventory with `collection_errors` or `skipped_symlinks`; `2` means invalid invocation/input. Inspect the JSON even on exit `1`. None of these statuses means an app passed or failed review. Symlinks are deliberately not followed, so versioned frameworks can need manual inspection of their real files. Oversized plists (over 4 MiB), unreadable files, malformed contents, and excessive nesting are explicit gaps; collection continues for other files. No listed framework or manifest is proof that all statically linked SDKs have been identified.

Use each relative path and hash as an evidence locator. Hashes cover inspected files only; connect them to archive/CI provenance separately. Review selected fields before sharing the inventory. Purpose-string presence does not validate wording or localization; use the targeted commands below for values, signed entitlements, and further investigation.

For helper changes, run `python3 -m unittest discover -s tests -v` from this skill directory. The fixture tests exercise actual nested bundle files and error paths without an Xcode project or production archive.

## Resolved settings

```sh
xcodebuild -list -json -workspace '/path/App.xcworkspace'
xcodebuild -showBuildSettings -json \
  -workspace '/path/App.xcworkspace' -scheme 'App' \
  -configuration 'Release' -destination 'generic/platform=iOS' \
  -disableAutomaticPackageResolution -skipPackageUpdates
```

Use `-project '/path/App.xcodeproj'` instead of `-workspace` for a standalone project. Read the shared scheme's ArchiveAction and configuration inputs first. Settings queries may still fetch missing pinned packages or write caches; the flags prevent automatic version changes and update checks, not all network access. If dependencies cannot be resolved, retain that gap rather than altering lockfiles or configurations to obtain output.

Inspect each relevant target's `PRODUCT_BUNDLE_IDENTIFIER`, `MARKETING_VERSION`, `CURRENT_PROJECT_VERSION`, `SDKROOT`, `IPHONEOS_DEPLOYMENT_TARGET`, `TARGETED_DEVICE_FAMILY`, `INFOPLIST_FILE`, `GENERATE_INFOPLIST_FILE`, `INFOPLIST_KEY_*`, `CODE_SIGN_ENTITLEMENTS`, and signing settings. Generated plist values and build scripts may change final contents. Local resolved settings describe this invocation, not the toolchain or configuration that produced an existing archive. Avoid publishing entire settings dumps: they may contain secrets.

## Archive identity and bundled values

```sh
archive_path='/path/App.xcarchive'
plutil -p "$archive_path/Info.plist"
find "$archive_path/Products/Applications" -type d -name '*.app' -print
```

Select the intended main app from the inventory rather than taking the first result:

```sh
app_path='/path/App.xcarchive/Products/Applications/App.app'
plutil -p "$app_path/Info.plist"
find "$app_path" -type d \( -name '*.appex' -o -name '*.framework' -o -name '*.app' \) -print
find "$app_path" -type f -name 'PrivacyInfo.xcprivacy' -print
```

Inspect `CFBundleIdentifier`, `CFBundleShortVersionString`, `CFBundleVersion`, `MinimumOSVersion`, `UIDeviceFamily`, permission strings, `DTSDKName`, `DTXcode`, and `DTXcodeBuild` where present. Inspect each extension/embedded app's plist separately and localized `InfoPlist.strings` where relevant. Missing optional build metadata is a provenance gap, not automatically a violation.

Associate the archive with CI run/build logs and source revision, including local changes if known. Version/build labels alone cannot establish a commit match. Do not infer successful export, installation, or upload from a valid archive directory.

## Signed entitlements and privacy manifests

```sh
codesign --display --entitlements :- "$app_path"
codesign --display --verbose=4 "$app_path"
```

Repeat for relevant extensions and embedded executable bundles. Displaying a signature does not verify its validity or entitlement eligibility. Where local integrity is in question, `codesign --verify --strict --verbose=2 "$app_path"` supplies a separate integrity check; nested components need their own checks. Neither proves App Store acceptance. Capture exit status and diagnostics; missing access or an unavailable artifact is Unverified, not evidence of invalid signing.

For each manifest path returned above:

```sh
plutil -lint '/path/to/PrivacyInfo.xcprivacy'
plutil -p '/path/to/PrivacyInfo.xcprivacy'
```

Plist syntax validity does not prove Apple's schema, accurate declarations, permitted API reasons, or SDK signature requirements. Compare each shipped SDK/manifest with the current official requirements and actual API/data use. Static SDK code can be linked into the main executable; absence of a framework directory does not establish absence of an SDK. Repository manifests do not prove inclusion in the shipped artifact, and manifests do not replace App Privacy disclosures.

Simulator checks do not validate a device archive. Local signature checks and upload validation do not establish review compliance. Report each evidence boundary separately.
