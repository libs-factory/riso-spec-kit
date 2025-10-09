# User Story: [STORY_NAME]

**Story ID:** US-###
**EPIC:** [EPIC_NAME] ([EPIC-###])
**Priority:** [P1/P2/P3] ([Must Have / Should Have / Nice to Have])
**Status:** [Draft / Ready / In Progress / Complete]
**Estimated Tasks:** [X]
**Estimated Effort:** [Y] hours
**Actual Effort:** [Z] hours (if complete)
**Created:** [DATE]
**Updated:** [DATE]

---

## User Story

```
As a [ROLE/PERSONA]
I want to [ACTION/GOAL]
So that [BUSINESS_VALUE/BENEFIT]
```

**Context & Background:**
[Additional context about why this story matters, business drivers, user pain points addressed]

---

## Acceptance Criteria

### Functional Requirements

- [ ] **AC1:** [Specific, testable criterion]
  - **Given:** [Precondition]
  - **When:** [Action]
  - **Then:** [Expected result]

- [ ] **AC2:** [Specific, testable criterion]
  - **Given:** [Precondition]
  - **When:** [Action]
  - **Then:** [Expected result]

- [ ] **AC3:** [Specific, testable criterion]
  - **Given:** [Precondition]
  - **When:** [Action]
  - **Then:** [Expected result]

### Non-Functional Requirements

- [ ] **Performance:** [Metric and target]
- [ ] **Security:** [Security requirement]
- [ ] **Accessibility:** [Accessibility requirement]
- [ ] **Usability:** [Usability requirement]

---

## Independent Test Scenario

**Scenario Name:** [Test scenario title]

```gherkin
Feature: [Feature being tested]

Scenario: [Specific scenario]
  Given [Initial state/context]
    And [Additional context if needed]
  When [User action]
    And [Additional action if needed]
  Then [Expected outcome]
    And [Additional verification]
    And [Final state verification]
```

**Test Data Required:**
- [Test data item 1]
- [Test data item 2]

**Expected Results:**
- [Specific measurable result 1]
- [Specific measurable result 2]

---

## Dependencies

### Story Dependencies
**Depends On:**
- [ ] US-### ([Story name]) - [Reason for dependency]
- [ ] US-### ([Story name]) - [Reason for dependency]

**Blocks:**
- US-### ([Story name]) - [What this story provides]

**Related:**
- US-### ([Story name]) - [How they're related]

### Technical Dependencies
- [ ] [Component/Service name]: [What's needed]
- [ ] [External system]: [Integration requirement]
- [ ] [Infrastructure]: [Environment/setup needed]

### Data Dependencies
- [ ] [Entity/Table]: [Must exist first]
- [ ] [Migration]: [Schema changes needed]
- [ ] [Seed data]: [Test data required]

---

## Technical Approach

### Components Affected
- **Models:** [Entity/model names]
- **Services:** [Service names]
- **APIs:** [Endpoint paths]
- **UI:** [Component names]
- **Database:** [Tables/collections]

### Implementation Strategy
1. [Step 1 - e.g., "Create data model for X"]
2. [Step 2 - e.g., "Implement service layer for Y"]
3. [Step 3 - e.g., "Build API endpoint for Z"]
4. [Step 4 - e.g., "Create UI component for W"]

### Key Files to Create/Modify
- `path/to/file1.ext` - [Purpose]
- `path/to/file2.ext` - [Purpose]
- `path/to/file3.ext` - [Purpose]

---

## Tasks Breakdown

### Setup Tasks
- [ ] **T001:** [Setup task 1 - e.g., "Initialize project dependencies"]
- [ ] **T002:** [Setup task 2 - e.g., "Configure database schema"]

### Test Tasks (TDD Approach)
- [ ] **T003:** Write unit tests for [component]
- [ ] **T004:** Write integration tests for [API/service]
- [ ] **T005:** Write E2E tests for [user workflow]

### Implementation Tasks
- [ ] **T006:** Implement [data model]
- [ ] **T007:** Implement [service logic]
- [ ] **T008:** Implement [API endpoint]
- [ ] **T009:** Implement [UI component]

### Integration Tasks
- [ ] **T010:** Connect [component A] to [component B]
- [ ] **T011:** Integrate with [external system]
- [ ] **T012:** Configure [middleware/logging]

### Polish Tasks
- [ ] **T013:** Add error handling and validation
- [ ] **T014:** Optimize performance
- [ ] **T015:** Write documentation

---

## Validation Checklist

### Code Quality
- [ ] Unit tests written and passing (≥80% coverage)
- [ ] Integration tests written and passing
- [ ] E2E tests written and passing
- [ ] Code reviewed and approved
- [ ] No linting errors
- [ ] No security vulnerabilities (static analysis passed)

### Functionality
- [ ] All acceptance criteria met
- [ ] Edge cases handled
- [ ] Error messages user-friendly
- [ ] Validation rules enforced

### Performance
- [ ] Performance targets met ([specific metric])
- [ ] No N+1 queries (if applicable)
- [ ] Caching implemented where needed
- [ ] Load tested for expected volume

### Documentation
- [ ] Code comments added for complex logic
- [ ] API documentation updated
- [ ] User-facing documentation written
- [ ] Architecture diagrams updated (if needed)

### Constitution Compliance
- [ ] CORE rules validated
- [ ] HIGH-PRIORITY rules documented (if deviated)
- [ ] Security requirements met
- [ ] Accessibility standards met

---

## Definition of Done

**Story is considered DONE when:**
- [ ] All tasks completed
- [ ] All acceptance criteria met
- [ ] All validation checklist items passed
- [ ] Code merged to main branch
- [ ] Deployed to staging environment
- [ ] Product owner accepted story
- [ ] Documentation complete

---

## Notes & Decisions

**[DATE]:** [Decision or note]
- **Impact:** [How this affects implementation]
- **Rationale:** [Why this decision was made]

**[DATE]:** [Technical challenge encountered]
- **Solution:** [How it was resolved]
- **Lessons Learned:** [What to do differently]

---

## Related Resources

**Design Artifacts:**
- [Link to spec.md]
- [Link to data-model.md]
- [Link to API contract]
- [Link to wireframes/mockups]

**External References:**
- [Link to documentation]
- [Link to library/framework docs]
- [Link to research/ADR]

**Related Issues:**
- [Link to bug report]
- [Link to feature request]

---

**Generated by:** `/speckit.story` command
**Template Version:** 0.1.0
**Last Updated:** [DATE]
