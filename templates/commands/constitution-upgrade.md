---
description: Upgrade constitution to tiered structure (RisoTech mode) or migrate between constitution versions/formats.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are upgrading the project constitution to use the tiered RisoTech structure or migrating between constitution formats. This command transforms a flat constitution into a structured, tiered one with CORE, HIGH-PRIORITY, and FLEXIBLE rules.

Follow this execution flow:

### 1. Assess Current Constitution

- Read existing constitution from `/memory/constitution.md`
- Determine current format:
  - **Flat format**: Single list of principles without tiers
  - **Tiered format**: Already has CORE/HIGH-PRIORITY/FLEXIBLE sections
  - **Missing**: No constitution exists
- Extract current version number and amendment history
- Identify all existing principles/rules

### 2. Determine Upgrade Path

Based on assessment:

**Case A: No Constitution Exists**
- Inform user that no constitution found
- Suggest creating one with `/speckit.constitution`
- Optionally offer to create from RisoTech templates:
  - Load templates from `/templates/risotech/core.md`
  - Load templates from `/templates/risotech/high-priority.md`
  - Load templates from `/templates/risotech/flexible.md`
  - Combine and customize for project

**Case B: Flat Constitution Exists**
- Perform tier classification on existing rules
- Map each principle to appropriate tier
- Preserve all existing principles
- Add missing essential rules from RisoTech templates

**Case C: Already Tiered**
- Inform user constitution is already tiered
- Offer to rebalance tiers if requested
- Suggest adding missing rules from templates

### 3. Tier Classification Algorithm

For each existing principle, classify into tiers using these criteria:

**CORE (Non-negotiable)**
- Security-related rules
- Data privacy/compliance requirements
- Critical quality gates (testing, code review)
- Legal/regulatory requirements
- Accessibility mandates
- Version control discipline
- Error handling fundamentals

**HIGH-PRIORITY (Strong recommendation)**
- Performance standards
- Documentation requirements
- Dependency management
- CI/CD pipeline requirements
- API design consistency
- Monitoring/observability
- Environment separation

**FLEXIBLE (Guidelines)**
- Technology stack preferences
- Code organization patterns
- Comment density guidelines
- Design pattern usage
- Build tool choices
- Refactoring frequency
- Logging verbosity

### 4. Perform Classification

For flat constitution upgrade:

1. Parse each principle section
2. Analyze content for classification signals:
   - Keywords: "must", "required", "mandatory" → likely CORE
   - Keywords: "should", "recommended" → likely HIGH-PRIORITY
   - Keywords: "consider", "prefer", "guideline" → likely FLEXIBLE
   - Subject matter (security, compliance) → CORE
   - Subject matter (performance, docs) → HIGH-PRIORITY
   - Subject matter (style, patterns) → FLEXIBLE

3. If classification uncertain, default to HIGH-PRIORITY
4. Present classification to user for approval before finalizing

### 5. Generate Tiered Constitution

Create new constitution with structure:

```markdown
# Project Constitution

**Version:** [INCREMENT VERSION - MAJOR bump for structure change]
**Ratification Date:** [Original date]
**Last Amended:** [Today's date]

## Overview

This constitution defines the governing principles for [PROJECT_NAME], organized into three priority tiers:

- **CORE**: Non-negotiable rules that must be followed in all circumstances
- **HIGH-PRIORITY**: Strong recommendations that require documented justification to deviate
- **FLEXIBLE**: Guidelines that can be adapted based on context

---

## CORE Rules

### [Rule 1 Title]

**Tier:** `core`

[Description]

**Rationale:** [Why this is non-negotiable]

**Examples:**
- [Example 1]
- [Example 2]

---

[... more CORE rules ...]

---

## HIGH-PRIORITY Rules

[... HIGH-PRIORITY rules with same format ...]

---

## FLEXIBLE Rules

[... FLEXIBLE rules with same format ...]

---

## Governance

### Amendment Process

[How to propose and approve changes to this constitution]

### Tier Reclassification

Rules can be reclassified between tiers through the amendment process. Reclassification requires:
- Clear rationale for the change
- Team consensus
- Version increment (MINOR for tier changes)

### Compliance Review

[How and when compliance is checked]
```

### 6. Preserve History

In the upgraded constitution:
- Add HTML comment at top with migration details
- Document which rules were classified into which tiers
- Note any principles that were ambiguous
- Record the classification rationale

Example:
```html
<!--
CONSTITUTION UPGRADE REPORT
===========================
Upgraded from: v1.2.3 (flat) to v2.0.0 (tiered)
Upgrade Date: 2025-10-08
Performed by: /speckit.constitution-upgrade

Classification Summary:
- 8 principles → CORE tier
- 10 principles → HIGH-PRIORITY tier
- 5 principles → FLEXIBLE tier

New rules added from RisoTech templates:
- Accessibility Standards (CORE)
- API Design Consistency (HIGH-PRIORITY)
- UI Framework Choices (FLEXIBLE)

Manual review recommended for:
- "Code Organization" - classified as FLEXIBLE (review if should be HIGH-PRIORITY)
-->
```

### 7. Template Synchronization

After upgrading constitution:
- Check `/templates/plan-template.md` for constitution references
- Check `/templates/spec-template.md` for principle alignment
- Check `/templates/tasks-template.md` for compliance sections
- Update any hardcoded principle references to use tier-aware language

### 8. Enable RisoTech Mode

Inform user about enabling RisoTech features:

```bash
# Enable RisoTech mode (activates all features)
export SPECIFY_RISOTECH_MODE=true

# Or enable just tiered constitution
export SPECIFY_TIERED_CONSTITUTION=true
```

Add to project documentation or `.env` file.

### 9. Validation

Before finalizing:
- Ensure every rule has a tier assignment
- Verify tier assignments are appropriate
- Check that rationales are clear
- Confirm version increment is correct (MAJOR for structure change)
- Validate markdown formatting

### 10. User Output

Provide comprehensive summary:

```markdown
# Constitution Upgrade Complete

## Summary
- **Previous Version:** v1.2.3 (flat structure)
- **New Version:** v2.0.0 (tiered structure)
- **Rules Classified:** 23 total

## Tier Distribution
- **CORE:** 8 rules
- **HIGH-PRIORITY:** 10 rules
- **FLEXIBLE:** 5 rules

## What Changed
1. All existing principles preserved and classified by priority
2. Added [X] new rules from RisoTech templates
3. Enhanced rationale sections for clarity
4. Added examples for each rule

## Next Steps
1. Review the upgraded constitution at `/memory/constitution.md`
2. Enable RisoTech mode: `export SPECIFY_RISOTECH_MODE=true`
3. Run `/speckit.constitution-applying` to validate existing artifacts
4. Consider using `/speckit.clarify` for enhanced clarification workflows

## New Commands Available
- `/speckit.constitution-applying` - Validate artifacts against constitution
- `/speckit.constitution-upgrade` - This command (for future migrations)

## Files Modified
- `/memory/constitution.md` - Upgraded to tiered structure
- [List any other files updated]

Commit message suggestion:
`docs: upgrade constitution to v2.0.0 with tiered structure (RisoTech)`
```

## Backward Compatibility

The upgrade process:
- **Preserves** all existing principles
- **Adds** tier metadata without removing content
- **Enhances** with rationales and examples
- **Maintains** governance and amendment sections
- **Increments** version appropriately (MAJOR)

Existing workflows continue to work but gain:
- Tiered validation in `/speckit.constitution-applying`
- Better guidance on which rules are flexible
- Clearer prioritization for compliance

## Error Handling

**No constitution file:**
- Offer to create from templates
- Guide through initial setup

**Already tiered:**
- Inform user
- Offer to rebalance if requested
- Show current tier distribution

**Classification conflicts:**
- Present ambiguous cases to user
- Ask for guidance
- Document final decisions

## Example Usage

```bash
# Standard upgrade from flat to tiered
/speckit.constitution-upgrade

# Upgrade and enable all RisoTech features
/speckit.constitution-upgrade Enable RisoTech mode with all enhancements

# Review classification suggestions before applying
/speckit.constitution-upgrade Show classification plan without applying

# Add missing RisoTech templates to existing tiered constitution
/speckit.constitution-upgrade Add recommended rules from RisoTech templates
```

## Integration with Other Commands

- **Before `/speckit.specify`**: Tiered constitution provides better guidance
- **Before `/speckit.plan`**: HIGH-PRIORITY rules inform technical decisions
- **With `/speckit.tasks`**: CORE rules generate validation sub-tasks
- **During `/speckit.implement`**: Constitution checks prevent non-compliant code
