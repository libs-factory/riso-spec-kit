# EPIC Breakdown: [EPIC_NAME]

**EPIC ID:** [EPIC-###]
**Complexity:** EPIC (30+ tasks)
**Estimated Effort:** [X] hours
**Priority:** [P1/P2/P3]
**Created:** [DATE]

## Original Requirement

```text
[Original feature description that triggered EPIC classification]
```

## Why This is an EPIC

**Complexity Indicators:**
- [ ] Estimated 30+ implementation tasks
- [ ] Multiple distinct user workflows
- [ ] Cross-cutting architectural changes
- [ ] Multiple team/domain dependencies
- [ ] High technical complexity
- [ ] Significant data model changes

**Breakdown Rationale:**
[Explanation of why this needs decomposition into user stories]

---

## Decomposed User Stories

### Story 1: [STORY_NAME] (P1 - MVP)
**Story ID:** US-001
**Priority:** P1 (Must Have - MVP)
**Estimated Tasks:** [X]
**Estimated Effort:** [Y] hours

**User Story:**
```
As a [ROLE]
I want to [ACTION]
So that [BENEFIT]
```

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Independent Test Scenario:**
```
Given [CONTEXT]
When [ACTION]
Then [EXPECTED_RESULT]
```

**Depends On:** None (MVP foundation)

---

### Story 2: [STORY_NAME] (P1)
**Story ID:** US-002
**Priority:** P1 (Must Have)
**Estimated Tasks:** [X]
**Estimated Effort:** [Y] hours

**User Story:**
```
As a [ROLE]
I want to [ACTION]
So that [BENEFIT]
```

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Independent Test Scenario:**
```
Given [CONTEXT]
When [ACTION]
Then [EXPECTED_RESULT]
```

**Depends On:** US-001 (requires [specific dependency])

---

### Story 3: [STORY_NAME] (P2)
**Story ID:** US-003
**Priority:** P2 (Should Have)
**Estimated Tasks:** [X]
**Estimated Effort:** [Y] hours

**User Story:**
```
As a [ROLE]
I want to [ACTION]
So that [BENEFIT]
```

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Independent Test Scenario:**
```
Given [CONTEXT]
When [ACTION]
Then [EXPECTED_RESULT]
```

**Depends On:** US-001, US-002 (requires [specific dependencies])

---

### Story 4: [STORY_NAME] (P3)
**Story ID:** US-004
**Priority:** P3 (Nice to Have)
**Estimated Tasks:** [X]
**Estimated Effort:** [Y] hours

**User Story:**
```
As a [ROLE]
I want to [ACTION]
So that [BENEFIT]
```

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Independent Test Scenario:**
```
Given [CONTEXT]
When [ACTION]
Then [EXPECTED_RESULT]
```

**Depends On:** US-003 (optional enhancement)

---

## Story Dependency Graph

```
┌─────────┐
│ US-001  │ (MVP - No dependencies)
│ (P1)    │
└────┬────┘
     │
     ├──────┬──────┐
     │      │      │
┌────▼───┐ ┌▼────┐ ┌▼─────┐
│ US-002 │ │US-003│ │US-005│ (Depends on US-001)
│ (P1)   │ │(P2)  │ │(P2)  │
└────┬───┘ └──┬───┘ └──────┘
     │        │
     └────┬───┘
          │
     ┌────▼───┐
     │ US-004 │ (Depends on US-002, US-003)
     │ (P3)   │
     └────────┘
```

**Parallel Implementation Opportunities:**
- **Wave 1:** US-001 (sequential - MVP foundation)
- **Wave 2:** US-002, US-003, US-005 (parallel - all depend only on US-001)
- **Wave 3:** US-004 (sequential - depends on multiple stories)

---

## Shared Components

### Data Models
**Entity:** [ENTITY_NAME]
- **Used By:** US-001, US-002, US-003
- **Implementation Priority:** Setup Phase (before any story)
- **Fields:**
  - field1: type
  - field2: type

**Entity:** [ENTITY_NAME_2]
- **Used By:** US-002, US-004
- **Implementation Priority:** US-002 Phase
- **Fields:**
  - field1: type
  - field2: type

### Services/APIs
**Service:** [SERVICE_NAME]
- **Used By:** US-001, US-002, US-003
- **Implementation Priority:** US-001 Phase
- **Methods:**
  - method1()
  - method2()

### Infrastructure
**Component:** [INFRA_COMPONENT]
- **Used By:** All stories
- **Implementation Priority:** Setup Phase
- **Description:** [Purpose and scope]

---

## Implementation Strategy

### MVP Scope (Iteration 1)
**Goal:** Deliver minimal viable functionality
**Stories:** US-001 only
**Success Criteria:**
- [ ] User can [core action]
- [ ] Basic [feature] works end-to-end
- [ ] Foundation for future stories established

**Expected Delivery:** [X] days

### Iteration 2 (Core Features)
**Goal:** Complete P1 must-have features
**Stories:** US-002, US-003 (parallel)
**Success Criteria:**
- [ ] [Key feature 2] functional
- [ ] [Key feature 3] functional
- [ ] System handles [primary use cases]

**Expected Delivery:** [Y] days

### Iteration 3 (Enhancements)
**Goal:** Add P2 should-have features
**Stories:** US-005, US-006
**Success Criteria:**
- [ ] [Enhancement 1] available
- [ ] User experience improved
- [ ] Performance meets targets

**Expected Delivery:** [Z] days

### Iteration 4 (Polish)
**Goal:** Add P3 nice-to-have features
**Stories:** US-004
**Success Criteria:**
- [ ] [Enhancement 2] available
- [ ] Edge cases handled
- [ ] Production-ready quality

**Expected Delivery:** [W] days

---

## Cross-Story Considerations

### Security & Compliance
- **CORE Rule:** [Relevant constitution rule]
- **Impact:** All stories must comply
- **Validation:** [How to verify]

### Performance Requirements
- **Target:** [Performance metric]
- **Critical Stories:** US-001, US-002
- **Validation:** [How to measure]

### Testing Strategy
- **Unit Tests:** Per story (≥80% coverage)
- **Integration Tests:** After each iteration
- **E2E Tests:** After MVP, Iteration 2, Final

### Documentation
- **API Docs:** Generated after US-001, US-002
- **User Guide:** After each iteration
- **Architecture Docs:** Updated with each new component

---

## Risk Assessment

### High Risk
**Risk:** [Description]
- **Impact:** [Consequences]
- **Affected Stories:** US-001, US-003
- **Mitigation:** [Strategy]

### Medium Risk
**Risk:** [Description]
- **Impact:** [Consequences]
- **Affected Stories:** US-002
- **Mitigation:** [Strategy]

### Low Risk
**Risk:** [Description]
- **Impact:** [Consequences]
- **Affected Stories:** US-004
- **Mitigation:** [Strategy]

---

## Success Metrics

**MVP Success (US-001):**
- [ ] [Metric 1]: [Target]
- [ ] [Metric 2]: [Target]

**Full EPIC Success:**
- [ ] All P1 stories delivered
- [ ] [Overall metric 1]: [Target]
- [ ] [Overall metric 2]: [Target]
- [ ] User satisfaction: [Target]

---

## Notes & Decisions

**[DATE]:** Decision to [decision]
- **Rationale:** [Why]
- **Impact:** [Stories affected]

**[DATE]:** Dependency discovered: [description]
- **Affected Stories:** US-002, US-003
- **Resolution:** [How handled]

---

**Generated by:** `/speckit.epic` command
**Template Version:** 0.1.0
**Last Updated:** [DATE]
