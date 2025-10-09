---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH.

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Analyze feature complexity** (RisoTech Enhancement):

   If `SPECIFY_RISOTECH_MODE=true` or `SPECIFY_EPIC_DECOMPOSITION=true`:

   a. Estimate total task count based on:
      - Number of entities in spec (if mentioned)
      - Number of user stories
      - Number of functional requirements
      - Complexity of integrations

   b. Use EPIC analyzer to determine complexity:
      - SMALL (1-5 tasks): Simple feature, no decomposition needed
      - MEDIUM (6-15 tasks): Moderate feature, standard planning
      - LARGE (16-30 tasks): Complex feature, consider decomposition
      - EPIC (30+ tasks): Very complex, recommend EPIC decomposition

   c. **If LARGE or EPIC complexity detected**:
      - Inform user: "Feature complexity: [LARGE/EPIC] (~X tasks estimated)"
      - Suggest: "Consider running `/speckit.epic` after planning to decompose into user stories"
      - Note in plan.md under "Implementation Strategy" section
      - Continue with standard planning

   d. **If SMALL or MEDIUM complexity**:
      - Proceed with standard planning workflow
      - No EPIC decomposition needed

4. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - **RisoTech Enhancement**: If tiered constitution enabled, validate by tier:
     * Check CORE rules compliance (must pass - block if violated)
     * Check HIGH-PRIORITY rules (document if deviated)
     * Note FLEXIBLE guidelines considered
   - Evaluate gates (ERROR if CORE violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design
   - **RisoTech**: Suggest running `/speckit.constitution-validation` for detailed validation
   - **If LARGE/EPIC**: Add note suggesting `/speckit.epic` for story decomposition

5. **Stop and report**: Command ends after Phase 2 planning. Report:
   - Branch name
   - IMPL_PLAN path
   - Generated artifacts
   - **Complexity assessment** (if RisoTech enabled)
   - **Next steps**:
     * If EPIC/LARGE: "Run `/speckit.epic` to decompose into stories"
     * If MEDIUM/SMALL: "Run `/speckit.tasks` to generate task breakdown"

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `{AGENT_SCRIPT}`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications
