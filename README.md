# App Store Audit Skill

[![skills.sh](https://skills.sh/b/tudorturcanu/app-store-audit-skill)](https://skills.sh/tudorturcanu/app-store-audit-skill)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-orange.svg)](https://anthropic.com)
[![Google Antigravity](https://img.shields.io/badge/Antigravity-Compatible-blue.svg)](https://deepmind.google)
[![License: MIT](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)

An agent skill that guides your AI coding assistant (Claude Code, Google Antigravity, Cursor, Codex, and other skill-compatible agents) through an evidence-based audit of iOS and iPadOS apps for **App Store submission** or **review rejection remediation**, aligned with official Apple requirements.

---

## Install

Install globally for all projects:

```bash
npx skills add tudorturcanu/app-store-audit-skill -g
```

Or install for the current project only:

```bash
npx skills add tudorturcanu/app-store-audit-skill
```

---

## When to Use

Activate the skill by asking your AI agent to audit your app for App Store submission or resolve an App Store Connect rejection:

> "Audit our iOS app before submitting to the App Store."
> "Apple rejected our build under Guideline 5.1.1 (Data Collection). Help us audit the source and fix the rejection."
> "Run a pre-submission compliance audit on this release archive."

---

## What the Skill Does

- **Evidence-Based Compliance:** Validates app behavior, privacy declarations, configuration, and build settings against official Apple App Review Guidelines.
- **Boundary-Aware Inspection:** Clearly separates what is proven in source code, release archives (`.xcarchive`), runtime flows, backend configuration, and App Store Connect metadata.
- **Pre-submission Archive Inventory:** Bundles `inventory_archive.py` to inspect `.xcarchive` bundles, frameworks, code signatures, privacy manifests (`PrivacyInfo.xcprivacy`), entitlements, and minimum OS targets without external tools.
- **Rejection Resolution:** Follows structured workflows to pinpoint root causes, reproduce reviewer concerns, verify fixes, and draft factual reviewer replies.
- **Transparent Outcomes:** Every check is explicitly marked **Pass**, **Fail**, **Unverified**, or **Not applicable**—avoiding false claims of approval.

---

## Repository Layout

```
skills/app-store-audit/
├── SKILL.md                          # Main agent instructions
├── agents/
│   └── openai.yaml                   # Agent metadata and prompt interface
├── references/
│   ├── apple-sources.md              # Live Apple guidelines, policies, and Connect sources
│   ├── artifact-inspection.md        # Source, xcconfig, and archive inspection workflow
│   ├── audit-checks.md               # Detailed compliance check criteria
│   ├── reporting.md                  # Report schema, severities, and decision rules
│   └── validation-scenarios.md       # Synthetic behavioral test cases
├── scripts/
│   └── inventory_archive.py          # Read-only archive and privacy manifest inspector
└── tests/
    └── test_inventory_archive.py     # Unit tests for archive scanner
```

---

## Running Tests

Run the bundled unit test suite:

```bash
python3 -m unittest discover -s skills/app-store-audit/tests -p 'test_*.py'
```

---

## License

[MIT](LICENSE) © 2026 Tudor Turcanu
