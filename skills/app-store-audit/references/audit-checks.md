# Evidence checklist

These are investigation prompts, not independent requirements. Verify live Apple rules and exceptions before recording failures. Add checks introduced by the current guidelines or app features.

## Release artifact

Inspect project/workspace or generated configuration, release schemes/settings, Info.plist inputs, entitlements, assets, dependency lockfiles, and available archive/export logs. Resolve generated values and build-script changes. Compare actual SDK/toolchain, minimum OS, and device families with dated submission rules. Inspect identifiers, versions, app/extension relationships, signing/capabilities, embedded frameworks, and packaging against current validation requirements.

Use [artifact-inspection.md](artifact-inspection.md) for command examples and interpretation limits. Inspect bundled manifests and actual dependencies; record artifact provenance separately from version/build labels. Keep archive validation and upload results as separate checks.

## Privacy and data flow

Inventory first-party code, SDKs, backend calls, analytics/ads, and external AI services. Trace data through recipients and retention, including remote feature flags and environment-specific endpoints. If server configuration or partner behavior is unavailable, mark those portions unverified rather than inferring them from a client default. Compare behavior with App Privacy answers, policy text, manifests, prompts, and observed traffic when available.

- Inspect sensitive-resource purpose strings/localization, permission timing, denial paths, and behavior before consent.
- For required-reason API candidates, verify actual use and the exact allowed reason in current Apple documentation. Do not invent codes or select a reason solely to pass validation.
- Inspect transitive/shipped SDK manifests and signatures under the current SDK rules.
- A manifest does not replace Connect disclosures. Missing a tracking prompt is not automatically a failure; establish whether tracking occurs.
- Do not infer “no collection” from absent analytics code. Servers, logs, WebViews, and partners need evidence.

## Accounts

Trace onboarding, login alternatives, creation, and deletion. Check the current login-service rule and exceptions before requiring a provider. Verify deletion end to end, backend effects, retention explanations, and relevant token revocation. Logout or a UI-only delete button does not establish deletion. Use test accounts for destructive flows.

## Commerce

Classify digital functionality/content, physical goods, services, and other business models. Establish storefront and program conditions before evaluating payment routing or external links.

For purchases/subscriptions, compare product IDs/configuration, localized price and period, trial/renewal terms, entitlement delivery, restoration where applicable, management/cancellation access, and terms/privacy links. Exercise successful, cancelled, pending, failed, restored, and expired states with available test tooling. A local StoreKit configuration does not prove Connect products or production receipt handling are ready.

## Runtime and reviewer access

Exercise release flows, including first launch, login, loading/empty/error states, permissions, purchases, and backend connectivity. Inspect device-family layouts, OS compatibility, accessibility, and localization. State actual devices/environments tested and distinguish fresh install from upgrade when retained permissions, credentials, or migrated data affect a finding. Sample representative combinations based on affected flows; do not extrapolate one account, locale, device, or storefront to all supported combinations without evidence.

Check reviewer access, hardware/setup needs, feature navigation, and review notes. Evaluate completeness, functionality, metadata accuracy, content rights, and hidden behavior against applicable rules. Static inspection does not establish runtime behavior.

## Store metadata and Connect

Compare release behavior with descriptions, screenshots/previews, localized fields, support/privacy URLs, categories, age-rating answers, availability, and review details. Open links and inspect media; filenames are insufficient. Fetch current field/asset specifications.

Inspect agreements and commerce configuration when evidence/access exists. Determine encryption declarations from actual cryptography, including dependencies; never set exemption flags merely to bypass a questionnaire. Verify regional trader and other declarations against business evidence or Connect state.

## Conditional feature routing

| Trigger | Investigate under current feature-specific rules |
| --- | --- |
| User content/social features | Moderation, reporting, blocking, support, age controls |
| Children/age-sensitive features | Audience, recipients, parental mechanisms, advertising, regional obligations |
| AI/third-party processing | Data destinations, disclosure/consent, content, product claims |
| Health/finance/gambling/crypto/regulated services | Claims, responsible entity, licenses, territories, program evidence |
| Downloaded software/mini apps/emulation/browser engines | Execution model, native API access, content, program conditions |
| Location/background/push/VPN/hardware | Purpose, actual use, controls, capability eligibility |
| Extensions/widgets/App Clips/watch/other targets | Per-target bundles, capabilities, data sharing, platform rules |

## False-positive controls

- Missing text matches do not prove missing generated configuration or functionality.
- Do not require accounts, subscriptions, tracking prompts, or one login provider universally.
- Do not extend regional exceptions worldwide or mix distribution-channel rules.
- A rejection establishes Apple's stated concern, not unrelated violations.
