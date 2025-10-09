# [PROJECT_NAME] Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

<!--
RisoTech Tiered Constitution:
If using RisoTech mode (SPECIFY_RISOTECH_MODE=true or SPECIFY_TIERED_CONSTITUTION=true),
organize principles into three tiers for better prioritization:

- CORE: Non-negotiable rules (security, testing, compliance)
- HIGH-PRIORITY: Strong recommendations requiring documented justification to deviate
- FLEXIBLE: Guidelines that can be adapted based on context

Use /speckit.constitution-upgrade to convert existing constitution to tiered format.
Use /speckit.constitution-validation to validate artifacts against constitution.
-->

## CORE Principles
<!-- CORE rules are non-negotiable and must be followed in all circumstances -->

### [PRINCIPLE_1_NAME]
**Tier:** `core`
<!-- Example: I. Test-First Development (NON-NEGOTIABLE) -->

[PRINCIPLE_1_DESCRIPTION]
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

**Rationale:** [WHY_IS_THIS_CORE]
<!-- Example: Testing before implementation prevents regressions and ensures requirements are met -->

**Examples:**
- [EXAMPLE_1]
- [EXAMPLE_2]
<!-- Example: Write unit tests before implementing features; All tests must pass before merging -->

---

### [PRINCIPLE_2_NAME]
**Tier:** `core`
<!-- Example: II. Security First -->

[PRINCIPLE_2_DESCRIPTION]
<!-- Example: Security must be considered at every stage; Never commit secrets; Validate all inputs -->

**Rationale:** [WHY_IS_THIS_CORE]

**Examples:**
- [EXAMPLE_1]
- [EXAMPLE_2]

---

### [PRINCIPLE_3_NAME]
**Tier:** `core`
<!-- Example: III. Data Privacy & Compliance -->

[PRINCIPLE_3_DESCRIPTION]

**Rationale:** [WHY_IS_THIS_CORE]

**Examples:**
- [EXAMPLE_1]
- [EXAMPLE_2]

---

## HIGH-PRIORITY Principles
<!-- HIGH-PRIORITY rules should be followed unless there's a strong, documented reason to deviate -->

### [PRINCIPLE_4_NAME]
**Tier:** `high-priority`
<!-- Example: IV. Code Review Required -->

[PRINCIPLE_4_DESCRIPTION]

**Rationale:** [WHY_IS_THIS_HIGH_PRIORITY]

**Examples:**
- [EXAMPLE_1]
- [EXAMPLE_2]

---

### [PRINCIPLE_5_NAME]
**Tier:** `high-priority`
<!-- Example: V. Performance Standards -->

[PRINCIPLE_5_DESCRIPTION]

**Rationale:** [WHY_IS_THIS_HIGH_PRIORITY]

**Examples:**
- [EXAMPLE_1]
- [EXAMPLE_2]

---

## FLEXIBLE Guidelines
<!-- FLEXIBLE rules are guidelines that can be adapted based on context -->

### [PRINCIPLE_6_NAME]
**Tier:** `flexible`
<!-- Example: VI. Technology Stack Preferences -->

[PRINCIPLE_6_DESCRIPTION]

**Rationale:** [WHY_IS_THIS_FLEXIBLE]

**Examples:**
- [EXAMPLE_1]
- [EXAMPLE_2]

---

## [SECTION_2_NAME]
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

[SECTION_2_CONTENT]
<!-- Example: Technology stack requirements, compliance standards, deployment policies, etc. -->

## [SECTION_3_NAME]
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

[SECTION_3_CONTENT]
<!-- Example: Code review requirements, testing gates, deployment approval process, etc. -->

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

[GOVERNANCE_RULES]
<!-- Example: All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->