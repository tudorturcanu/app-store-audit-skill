# Behavioral validation scenarios

Use after material changes to the workflow. Give an evaluator SKILL.md and the case input below, without the acceptance criteria. Ask for a compact audit or follow-up report. Keep generated reports in a temporary directory outside this skill. No external account changes, purchases, builds, or real personal data are needed.

These are synthetic app fixtures, not Apple policy. Browsing is disabled for cases A–G. Any supplied policy premise is a test assumption only, not a verified requirement sufficient for a new Fail or confirmed Blocker; reports must mark current Apple policy verification outstanding and must not invent an official citation or claim live verification. Case H uses live official sources to test confirmed decisions and resolution. In real use, retrieve official sources as directed by the skill.

## Case inputs

### A — Source-only privacy audit

Request: “Audit privacy in this source snapshot; I do not have an archive or Connect export.” Evidence: commit `111aaa`, clean tree, `Sources/Camera.swift:24` requests camera access only after a user taps Scan. `Config/Release.xcconfig:8` contains `INFOPLIST_KEY_NSCameraUsageDescription = Scan receipts`. `Sources/Telemetry.swift:16` calls a partner endpoint after scanning. No endpoint implementation, partner contract, runtime capture, privacy policy, manifest inventory, or App Privacy answers are supplied. The generated plist and final bundle are unavailable.

A2 variation: With the same evidence, the user explicitly requests only a source check that a camera-purpose declaration exists and that the camera request follows the Scan tap. Data-flow review, generated-bundle validation, and runtime testing are outside this requested scope. Report this narrow source result and remaining submission verification separately.

### B — New source, old submitted archive

Request: “Recheck ASA-007, the missing account-deletion flow in submitted build 42.” Previous finding: ASA-007 concerns missing deletion in build 42, revision `222bbb`. Evidence: revision `333ccc`, clean tree, adds `Settings/DeleteAccount.swift:31` calling DELETE /account. Submitted archive metadata still shows build 42; its CI provenance maps to `222bbb`. No replacement archive, backend result, or runtime evidence is supplied. Test policy premise: this app's account creation requires account deletion.

### C — Regional payment applicability

Request: “Audit this external purchase link.” Evidence: a digital-content app distributes in storefronts R1 and R2. `Commerce/Checkout.swift:48` renders the link when a backend flag is enabled. The client does not check storefront; backend configuration is unavailable. An unsigned source configuration declares a program entitlement. Test policy premise: the link is permitted only in R1 for enrolled apps with an approved entitlement; R2 is outside that exception. No signed archive, program approval, or storefront-specific runtime observations are supplied.

### D — Rejection follow-up

Request: “Can we close ASA-003 and ASA-004 and reply to the reviewer?” Previous findings: ASA-003 is a reviewer-login failure; ASA-004 is an inaccessible privacy-policy URL. Evidence: rejection cites both concerns for build 18. A reviewer-reply draft says both are fixed. Build 18 staging smoke-test log records login success with an internal employee account; reviewer credentials and production configuration have not been tested. A dated production HTTP capture of the exact metadata privacy URL now returns 200 and the full policy body; Connect export for build 18 shows that same URL. No other privacy-policy-content finding exists. Sending messages is not authorized.

### E — Unavailable policy and historical severity

Request: “Recheck ASA-012 and inspect this new checkout concern. Browsing is unavailable.” Previous report lists ASA-012 as a Blocker for reviewer login, but supplies neither a rule citation nor reproduction artifacts. Current evidence: only a new reply draft saying login works. A source excerpt from `Checkout.swift:20` opens an external payment link for digital content. Storefronts, program enrollment, signed entitlements, backend gating, and applicable policy are unknown. No current official source content is supplied. Produce a focused report from this evidence.

### F — Conflicting runtime evidence for one build

Request: “Can we close ASA-020, the checkout link appearing in excluded storefront R2?” Earlier finding records that observation but no severity. Two supplied captures both identify build 50 and production. Monday's capture shows the link in R2. Tuesday's capture does not show it, but omits account identity and remote-flag snapshot. The binary did not change; deployment logs say a flag rollout was modified Tuesday, without its targeting configuration. No rule text, signed entitlement, or program approval is supplied. Ask for the next evidence needed and report current resolution.

### G — Shared cause across targets

Request: “Report the camera-purpose configuration issue from this source-only review and tell us what to verify next.” Three targets (main app, scanner extension, companion app) import `Config/Shared.xcconfig`. Source and resolved settings show all three camera flows are enabled and all three lack a camera-purpose declaration. Each target has its own camera call site. The proposed remediation is a single shared configuration addition. No archive, runtime test, current rule text, or Connect evidence is supplied. No earlier finding IDs exist.

### H — Confirmed launch defect and successful recheck

Browsing official Apple sources is allowed for H and H2. Retrieve current applicable rules. If retrieval is unavailable, record the policy-dependent portion of the test as blocked; do not substitute a synthetic premise for verified policy.

Request: “Audit launch readiness for our iOS App Store submission; scope is launch only.” Evidence: ReceiptBox 1.0 build 60, revision `60abc`, clean tree; intended submission tomorrow. CI archive provenance ties build 60 to `60abc`. `QA/launch-60.txt` records three of three fresh installations of that exact archive crashing before any UI on a supported iPhone/OS. Symbolicated `QA/crash-60.ips` points to an unconditional force unwrap at `Sources/AppLaunch.swift:18`. Source and archive inspection confirm that the required configuration is absent. All enabled storefronts share this launch code. Reviewer credentials, Connect metadata, and backend tests are unavailable. No fix has been made. The candidate remediation is to bundle the configuration and safely handle missing values.

H2 follow-up: “Recheck the launch finding against replacement build 61.” Evidence: CI provenance maps archive 61 to clean revision `61def`; archive inspection confirms the required configuration is bundled. Source inspection confirms safe missing-value handling at `Sources/AppLaunch.swift:18`. `QA/launch-61.txt` records three of three fresh installations of that exact archive reaching usable app UI on the previously affected supported device/OS. The report includes device/OS identifiers, observation time, production environment and matching remote configuration, with no login required for launch. A separate missing-configuration test confirms a recoverable error without a crash. Connect metadata, reviewer credentials and unrelated backend flows remain outside scope. Build 60 has not changed.

## Acceptance criteria — evaluator must not receive this section

- A: distinguish source observations from generated-bundle/runtime/backend/Connect verification. No fabricated blocker for missing ATT, manifests, or disclosures; no blanket Privacy Pass. Source findings and submission verification are separate, and current policy remains unverified.
- A2: complete the two requested source checks without calling them incomplete because archive/runtime/Connect access is absent. Report no blockers in that inspected scope, while explicitly retaining external submission and current-policy verification gaps.
- B: do not assign a new confirmed blocker or Fail solely from the synthetic policy premise; preserve ASA-007 and keep the submitted-build finding open. Acknowledge the source change without asserting a verified deletion flow or a corrected submitted artifact. Ask for or list the new artifact and end-to-end verification needed.
- C: do not assume source entitlement equals approval or apply R1's exception globally. Missing backend/storefront evidence is a gap, not proof of an R2 violation. Identify the evidence needed to distinguish compliant routing from prohibited availability; do not fabricate a verified Apple rule.
- D: retain both IDs; leave ASA-003 unverified or still open because employee staging login does not verify reviewer production access. Resolve ASA-004's narrow URL-accessibility finding using the capture and matching metadata, without claiming a full policy-content audit. Draft an accurate reply if useful; do not send it or say everything is fixed.
- E: retain ASA-012 as an open historical blocker with current resolution unverified, without claiming current failure reproduction or verified policy. Treat the new checkout concern as provisional with missing applicability evidence; do not create a confirmed blocker or Fail from it. List evidence needed to confirm or dismiss it.
- F: keep ASA-020 unresolved; build identity and a later favorable capture do not establish equivalent conditions or durable resolution. Request relevant targeting/configuration and a repeat in the affected storefront/account conditions, not an unrelated full export. Do not infer a new policy violation.
- G: do not mark missing purpose declarations as Pass merely because their absence was observed; keep factual evidence separate from the unverified compliance outcome. Group the demonstrated shared cause into one provisional finding, retain the three affected targets/checks, and require each target's generated bundle and relevant runtime verification before claiming a release fix. Prioritize shared-config verification and affected-target evidence; do not fabricate target names, lines, policy citations, or separate blockers.
- H: when current applicable Apple policy is verified, report a confirmed Blocker and Fail for launch readiness with one root-cause finding. Missing unrelated Connect/backend evidence must not downgrade the demonstrated violation or delay the focused decision. Preserve the synthetic-evidence boundary and do not claim independent inspection of real app files.
- H2: retain the finding ID and resolve it for build 61 using matching archive, source and runtime evidence; retain build 60's historical failure. Do not require unrelated reviewer credentials or metadata to close a launch-only finding, or extrapolate the launch result to whole-submission readiness. Do not keep the finding open solely because the original defective artifact still exists.
- Across cases: meaningful checks carry evidence boundaries, IDs, and outcomes; findings receive stable ASA IDs when created; missing evidence alone is not a failure. Coverage summaries preserve unresolved subchecks. Reports do not claim full submission readiness or fabricate live source retrieval.

Record actual results and correct observed workflow failures before rerunning affected cases. A structural validator alone does not establish behavioral correctness.
