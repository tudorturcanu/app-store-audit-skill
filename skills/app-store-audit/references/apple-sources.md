# Official source map

Open sources during each audit. These are discovery links, not a cached requirements baseline. Follow redirects and relevant links; search developer.apple.com for moved documentation. Record when substantive content was actually retrieved. Apple-hosted forum opinions are not published requirements.

## Core sources for a full audit

- [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/): current rules, conditions, and exceptions; survey the full structure.
- [Submitting](https://developer.apple.com/app-store/submitting/): submission readiness and platform/build requirements.
- [Upcoming requirements](https://developer.apple.com/news/upcoming-requirements/): enforcement dates and future changes.
- [Apple Developer news](https://developer.apple.com/news/): recent announcements; follow underlying requirements.
- [App Store Connect Help](https://developer.apple.com/help/app-store-connect/): submission workflow, metadata, regional settings, and required fields.

## Feature-specific sources

| Area | Official starting point | Resolve during the audit |
| --- | --- | --- |
| Privacy disclosures | [App privacy details](https://developer.apple.com/app-store/app-privacy-details/) | Data types, purposes, linkage, tracking, exceptions, partner practices |
| Privacy manifests | [Privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files) | Placement, declarations, required-reason APIs and permitted reasons through linked documentation |
| Third-party SDKs | [SDK requirements](https://developer.apple.com/support/third-party-SDK-requirements/) | Current list, scope, manifests, signatures, repackaged SDKs |
| Tracking | [AppTrackingTransparency](https://developer.apple.com/documentation/apptrackingtransparency) | Tracking definition, authorization and affected behavior |
| Accounts | [Account deletion](https://developer.apple.com/help/app-review/guideline-reference/5-1-1-account-deletion) | Deletion flow, retention, timing, sign-in token handling |
| Subscriptions | [Subscriptions](https://developer.apple.com/app-store/subscriptions/) | Purchase presentation, disclosures, lifecycle, linked rules |
| Store media | [Screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications) | Current devices, sizes, formats, scaling; consult Connect Help for previews/icons |
| Age ratings | [Set an app age rating](https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating/) | Questionnaire, definitions, regional ratings, overrides |
| Encryption | [Export compliance](https://developer.apple.com/help/app-store-connect/manage-app-information/overview-of-export-compliance) | Encryption inventory, questionnaire, exemptions, documentation |
| EU distribution | [DSA trader requirements](https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements) | Status, verification, contact information |
| Interface quality | [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) | Usability/accessibility guidance, distinguished from submission rules |

For external purchases, alternative payments/distribution, reader apps, regional age assurance, AI/data sharing, kids, health, finance, gambling, VPN, extensions, or special entitlements, start with the current guideline and follow Apple's linked regional/program documentation. Establish storefront, category, approved entitlements, contract/program enrollment, and effective date before applying exceptions. App Store, TestFlight, alternative distribution, and notarization have distinct scopes.

Use “not stated” for unstated effective dates in the source register; crawl timestamps are not effective dates. Claim changes since a prior audit only with an earlier snapshot or dated Apple announcement.
