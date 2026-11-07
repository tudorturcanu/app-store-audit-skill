# Report findings and follow-ups

Use alongside the verdict and scope rules in SKILL.md. Scale the report to the request: a narrow recheck needs only affected findings and checks, not every section of a full audit.

Assign each finding a stable identifier at creation (`ASA-001`, `ASA-002`, …). Prioritize as **Blocker** (verified submission gate or clear violation likely to prevent acceptance), **Risk** (evidence-backed concern with uncertain interpretation/impact), or **Recommendation** (optional improvement, separate from failures). Missing access belongs in verification gaps, not a violation.

For each finding include ID, severity, linked check IDs, observed behavior and location (file/line, screen, or Connect field), applicable Apple rule and direct link when verified, why it applies, concrete remediation, and a verification step. For provisional concerns, state which rule or applicability evidence is missing and what would confirm or dismiss the concern. For recommendations, label the supporting guidance as optional rather than inventing a mandatory rule.

Include a compact coverage table by area, showing counts or IDs for each outcome, evidence boundaries, and remaining checks. Keep the underlying check details available in the report; a summary must not conceal unresolved subchecks behind an area-wide Pass. Combine details and summary for small audits. Include applicable future deadlines and a dated source register for multi-rule audits; cite sources beside claims. For a rejection, map each cited concern to finding/check IDs and evidence; draft a reviewer reply when useful without sending it.

For fix-and-audit requests, implement authorized fixes and recheck affected findings. Preserve finding IDs during follow-ups, never reuse retired IDs, and record each as resolved, still present, or unverified with current evidence. Keep historical severity and evidence distinct from the current recheck: an unresolved prior blocker stays open, but do not claim its violation was newly verified when only the earlier report is available. Do not invent an earlier severity or guideline citation. If an earlier report has no IDs, assign them once and map them to the original findings. A source fix may resolve a source finding while the corresponding submitted-build finding remains open; a proposed fix or reviewer-reply draft alone resolves neither.

## Keep decisions actionable

Group observations that share a demonstrated root cause and the same remediation into one finding, retaining each affected target, flow, and check ID. Split findings when applicability, remediation, or resolution evidence differs. Do not count a missing declaration in three affected targets as three independent issues if one shared configuration fix addresses all three; verify each affected target before closing the grouped finding.

For remaining verification, name the missing artifact or observation, why it changes the decision, and the next check. Order these by what could block submission and what unlocks other checks. Identify the needed role or access (for example, an App Store Connect administrator) without inventing an assignee. Ask for the smallest useful evidence rather than blanket access or every available export. A source-only report can list future submission checks without claiming they were part of the completed source scope.

A compact example of a verification request: “Obtain the intended build's signed app entitlements and program approval evidence to establish payment-program eligibility; then test link exposure in each enabled storefront.” This is an evidence request, not a finding of noncompliance.
