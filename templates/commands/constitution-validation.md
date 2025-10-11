---
description: Validate specification, plan, or task artifacts against the established constitution governance principles.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are validating development artifacts against the project constitution. This command ensures that specifications, plans, and tasks comply with established governance principles.

## MANDATORY COMPLIANCE REQUIREMENTS

**ABSOLUTE PROCESS ADHERENCE**: Do NOT assume or independently decide to change the process. All steps in "execution flow" below must be executed completely and in the exact order specified.

**MANDATORY TODO LIST**: Before starting execution, AI MUST create a TODO list based on the items in "execution flow" to ensure no step is missed.

Follow this execution flow:

### 1. Load Constitution

- Read the constitution file from `/memory/constitution.md`
- Parse the tiered rules structure (if using RisoTech mode with tiered constitution)
  - **CORE** rules: Non-negotiable, must be followed
  - **HIGH-PRIORITY** rules: Should be followed with documented exceptions
  - **FLEXIBLE** rules: Guidelines that can be adapted
- Extract all principle definitions, constraints, and compliance requirements

### 2. Identify Target Artifact

From user input or context, determine which artifact to validate:
- **Specification** (`/.specify/specs/[FEATURE]/spec.md`)
- **Plan** (`/.specify/specs/[FEATURE]/plan.md`)
- **Tasks** (`/.specify/specs/[FEATURE]/tasks.md`)
- **All artifacts** for comprehensive validation

If no target specified, validate all artifacts for the current feature.

### 3. Constitution Compliance Check

For each artifact, verify compliance with constitution rules:

#### For Specifications:
- Check that requirements align with core principles
- Verify security/privacy requirements are addressed
- Ensure accessibility requirements are specified
- Validate that testing approach is defined
- Check for explicit handling of error scenarios

#### For Plans:
- Verify technology choices align with approved stack (if specified in constitution)
- Check that architecture follows stated patterns and principles
- Ensure performance targets are defined and measurable
- Validate that security measures are planned
- Check for monitoring and observability approach

#### For Tasks:
- Verify each task has validation sub-tasks (if validation subtasks feature enabled)
- Check that testing requirements are specified
- Ensure code review is included in workflow
- Validate that documentation tasks are present
- Check dependency order follows logical sequence

### 4. Generate Compliance Report

Create a structured report with:

```markdown
# Constitution Compliance Report

**Artifact(s):** [List validated artifacts]
**Validation Date:** [ISO date]
**Constitution Version:** [version from constitution.md]

## Summary

- **Total Rules Checked:** [number]
- **Compliant:** [number] ✅
- **Violations:** [number] ❌
- **Warnings:** [number] ⚠️

## Detailed Findings

### CORE Rule Violations (Blockers)

[List any CORE rule violations that must be fixed before proceeding]

- **Rule:** [Rule name]
- **Artifact:** [Which file]
- **Issue:** [Specific problem]
- **Required Action:** [What needs to be done]

### HIGH-PRIORITY Warnings

[List HIGH-PRIORITY rules not followed]

- **Rule:** [Rule name]
- **Artifact:** [Which file]
- **Issue:** [Specific problem]
- **Recommendation:** [Suggested fix or justification needed]

### FLEXIBLE Guidelines

[List FLEXIBLE rules where improvements could be made]

- **Guideline:** [Rule name]
- **Suggestion:** [Possible improvement]

## Passed Checks ✅

[List all rules that passed validation]

## Recommendations

[Overall recommendations for improving compliance]

## Next Steps

[Prioritized action items based on severity]
```

### 5. Severity Levels

Classify findings by severity:
- **BLOCKER**: CORE rule violation - must fix before proceeding
- **WARNING**: HIGH-PRIORITY deviation - needs justification or fix
- **INFO**: FLEXIBLE guideline - improvement suggestion

### 6. Save Report

Save the compliance report to:
`/.specify/specs/[FEATURE]/constitution-compliance.md`

### 7. User Guidance

Provide clear output to user:
- Summary of validation results
- Count of blockers, warnings, and suggestions
- Location of detailed report
- Recommend next steps based on findings

If BLOCKERS found:
- List them clearly
- Suggest how to resolve each
- Recommend re-running validation after fixes

If no violations:
- Confirm all rules pass ✅
- Provide validation timestamp
- Suggest proceeding to next phase

## RisoTech Mode Enhancements

When `SPECIFY_RISOTECH_MODE=true` or `SPECIFY_TIERED_CONSTITUTION=true`:

1. **Tiered Validation**:
   - Load constitution using tiered structure
   - Apply different validation strictness per tier
   - CORE violations block progress
   - HIGH-PRIORITY violations require documented justification
   - FLEXIBLE guidelines are suggestions only

2. **Auto-remediation Suggestions**:
   - For common violations, suggest specific fixes
   - Offer to auto-generate missing sections (e.g., security checklist)
   - Provide constitution-compliant templates

3. **Historical Tracking**:
   - Track validation history over time
   - Show improvement trends
   - Alert on new violations introduced

## Example Usage

```bash
# Validate current feature's spec against constitution
/speckit.constitution-validation

# Validate specific artifact
/speckit.constitution-validation Check the plan for security compliance

# Validate all artifacts for a feature
/speckit.constitution-validation Validate all artifacts for feature 001-user-auth

# Quick check for blockers only
/speckit.constitution-validation Check for blocker violations only
```

## Integration Points

This command integrates with:
- `/speckit.constitution` - Uses the established constitution
- `/speckit.specify` - Validates specifications
- `/speckit.plan` - Validates plans
- `/speckit.tasks` - Validates task breakdowns
- `/speckit.implement` - Can be run before implementation to ensure compliance

## Error Handling

If constitution file is missing:
- Guide user to create one with `/speckit.constitution`
- Explain importance of having established principles
- Do not proceed with validation

If target artifact doesn't exist:
- List available artifacts
- Suggest creating missing artifact first
- Provide command to create it

## Output Requirements

Always output:
1. Clear summary (blockers/warnings/suggestions count)
2. Location of detailed report
3. Next recommended action
4. Timestamp of validation

Never:
- Fail silently
- Skip reporting passed checks (important for confidence)
- Make changes to artifacts without user approval