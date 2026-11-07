---
name: app-store-audit
description: Audit an iOS or iPadOS app for App Store submission or a review rejection using current official Apple requirements. Inspect release code, configuration, privacy, monetization, metadata, and review readiness; report evidence-backed issues and verification gaps. Use for requested App Store compliance or submission audits, not routine SwiftUI code review.
---

# App Store Audit

Produce a dated, evidence-based submission audit. Retrieve requirements from Apple during each audit; this skill is a workflow and source map, not a frozen copy of Apple's rules. Do not promise approval or claim comprehensive verification when evidence is missing.

## Establish scope

Match the depth to the request. For a full submission audit, cover the applicable areas below. For a specific rejection, start with the exact rejection text, cited guideline, affected version/build, and reviewer reproduction steps; investigate those concerns and their dependencies. For a follow-up verification, recheck the changed findings and affected flows against the new evidence. Expand to a full audit only when requested or when findings demonstrate a broader dependency; state the scope actually reviewed.

Infer available context from the project and submission materials before asking questions. For a focused request, collect only context that could change its applicability, evidence, or resolution. For a full audit, identify the app/version and release scheme, intended submission date, new app versus update, any rejection message, platforms/device families, distribution channel, storefronts, and relevant commercial terms or entitlements. Identify accounts, payments, tracking, user content, AI services, intended audience, and regulated features.

Inventory available source, dependencies, release archive, runtime/backend access, store metadata, and App Store Connect access or exports. With source alone, define a source-audit boundary and list archive, runtime, backend, and Connect verification separately. With no app, provide an audit plan without manufacturing findings. Ask only for missing context that changes applicability and continue independent checks. Do not assume worldwide availability or an approved entitlement from a code flag.

## Refresh Apple requirements

Use [references/apple-sources.md](references/apple-sources.md) to open current Review Guidelines, submission requirements, upcoming deadlines, and relevant Connect documentation. For a full audit, survey all five top-level guideline categories and follow applicable new sections; the local checklist is not exhaustive. For a focused rejection or recheck, retrieve the cited rules, relevant exceptions, and requirements affected by the change. Consult recent Apple Developer announcements affecting the planned submission.

For each applied rule record the official URL, section/page title, retrieval date, effective date when stated, and applicability conditions. Open substantive page content; search snippets and third-party summaries are discovery aids. If documentation needs JavaScript, follow an official Markdown link or use another available reader. Record inaccessible sources instead of claiming verification.

Use the user's current date/timezone and planned upload date. Separate effective rules from future announcements. Distinguish build SDK/Xcode minimums from deployment targets; the newest beta is not automatically required. Re-fetch version numbers, deadlines, screenshot/device specifications, SDK lists, age-rating rules, and regional payment conditions rather than relying on memory.

Prefer directly applicable, dated Apple rules over general summaries. If official pages conflict, report the conflict and its impact rather than silently choosing the strictest interpretation. If browsing is unavailable or prohibited, complete local checks with currency marked unverified. Distinguish factual checks (such as a URL responding or a declaration existing) from compliance judgments: facts can pass without live policy retrieval, but a new confirmed violation requires a verified applicable rule. Report an evidence-backed concern as provisional when that rule cannot be verified; do not invent a citation to complete the report.

## Inspect evidence

Select relevant checks from [references/audit-checks.md](references/audit-checks.md). Read repository instructions and release configuration first. Trace declarations to reachable behavior; text matches alone are leads. Inspect existing artifacts before building; use [references/artifact-inspection.md](references/artifact-inspection.md) for the read-only inventory helper, resolved build settings, and archive inspection. Build or exercise runtime flows when they resolve a concrete uncertainty. Tie evidence to the inspected commit/build and configuration; also record dirty working-tree changes when present.

When source, archive, runtime, and Connect evidence describe different builds or environments, keep their conclusions separate. Record mismatches and resolve which artifact is intended for submission before claiming a fix is present in it. A newer source change does not close a finding against an older submitted build. For runtime/backend/Connect evidence, record observation time and relevant account, storefront, remote configuration, and environment. The same binary can behave differently as these change. If evidence conflicts, check those conditions and reproduce the affected flow; do not silently select the newest or most favorable observation.

Track meaningful checks separately, with check ID, area, target/flow, evidence boundary (source, archive, runtime, backend, or Connect), evidence locator and build/environment, outcome, and remaining verification. Split checks when evidence supports only part of a claim: a source permission string and runtime consent behavior are separate checks. Name each check as a criterion to satisfy, not just an inspection activity. Record observations in the evidence column; confirming that a suspected defect exists is not itself a Pass. If a concerning observation is established but its applicable requirement is unverified, use Unverified for the compliance check. Assign each check an outcome:

- **Pass:** the stated criterion is satisfied by inspected evidence, with the evidence boundary stated.
- **Fail:** an observed conflict with a verified, applicable requirement.
- **Unverified:** missing evidence, access, or an applicability fact.
- **Not applicable:** explain the excluding feature, region, or distribution condition.

Separate requirements from design recommendations and optional engineering improvements. Do not turn a Human Interface Guidelines preference into a blocker without a supporting rule. Licensing, ownership, legal declarations, and trader status need appropriate evidence; they cannot be inferred from code alone.

An audit authorizes inspection and reporting; apply fixes when requested, preserving existing authorization for follow-up work. Do not submit builds, change public metadata, accept agreements, make purchases, delete real accounts, or contact reviewers merely to complete an audit. Use suitable test environments for destructive flows; redact credentials and personal data from reports.

## Report decisions

Report two conclusions:

- **Inspected scope:** “blockers found,” “no blockers found in inspected scope,” or “incomplete verification within inspected scope.” Lead with confirmed blockers even if other checks remain unresolved; disclose risks and unresolved checks beside the conclusion.
- **Submission verification:** list remaining archive, runtime, backend, Connect, or policy-currency checks relevant to the requested decision. For a focused audit, summarize broader submission areas as outside scope without turning them into required intake or an exhaustive checklist. Say “no outstanding checks identified for the stated submission scope” only when evidence covers that scope. A completed source audit can have no blockers while submission verification remains incomplete. Do not shrink an agreed full audit to make it appear complete.

State app/build, source revision and local changes, audit date, intended submission date, regions, scope, and evidence reviewed. Do not provide an approval probability or unconditional compliance certificate.

Use [references/reporting.md](references/reporting.md) for finding IDs and severity, per-check coverage, prioritized verification requests, and follow-up resolution. Keep recommendations separate from requirements and missing evidence separate from violations. Return the report in chat unless the user requests a file or the project defines a report location.

## Maintain this skill

After material workflow changes, exercise the scenarios in [references/validation-scenarios.md](references/validation-scenarios.md). These test audit decisions with synthetic evidence; they do not replace retrieving current Apple rules in a real audit.
