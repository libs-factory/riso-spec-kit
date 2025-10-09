# Flexible Constitution Rules

**FLEXIBLE** rules are guidelines that can be adapted based on context. They represent best practices but allow for pragmatic exceptions.

---

### Technology Stack Preferences

**Tier:** `flexible`

Prefer established, well-supported technologies over cutting-edge options. Evaluate new technologies carefully before adoption.

**Rationale:** Mature technologies have better documentation, more resources, and fewer breaking changes. However, newer technologies may offer significant advantages in specific contexts.

**Examples:**
- Consider community size and support
- Evaluate long-term maintenance implications
- Balance innovation with stability
- Document reasons for technology choices

---

### Code Organization

**Tier:** `flexible`

Organize code by feature rather than by file type when it improves maintainability. Use modular architecture patterns.

**Rationale:** Feature-based organization can make related code easier to find, but may not fit all project structures.

**Examples:**
- Group related components, services, and tests
- Use clear folder hierarchies
- Consider domain-driven design principles
- Balance between flat and nested structures

---

### Comment Density

**Tier:** `flexible`

Write self-documenting code when possible. Use comments to explain "why" rather than "what". Complex algorithms should have explanatory comments.

**Rationale:** Code should be readable without excessive comments, but complex logic benefits from explanation.

**Examples:**
- Avoid obvious comments like "// increment counter"
- Explain business logic and edge cases
- Document non-obvious performance optimizations
- Keep comments up to date with code

---

### Test Coverage Targets

**Tier:** `flexible`

Aim for 80% code coverage but focus on testing critical paths. 100% coverage is not always necessary or cost-effective.

**Rationale:** High coverage is valuable, but diminishing returns exist. Focus on quality over quantity of tests.

**Examples:**
- Prioritize testing business-critical code
- Test edge cases and error conditions
- Don't test trivial getters/setters
- Use coverage as a guide, not a goal

---

### Design Pattern Usage

**Tier:** `flexible`

Use design patterns when they simplify code, not for their own sake. Avoid over-engineering simple solutions.

**Rationale:** Design patterns solve specific problems but can add unnecessary complexity if misapplied.

**Examples:**
- Use factories when object creation is complex
- Apply observer pattern for event handling
- Consider singleton pattern carefully (often an anti-pattern)
- Start simple and refactor to patterns as needed

---

### Development Workflow

**Tier:** `flexible`

Use feature branches for development. Squash commits or keep detailed history based on team preference and project needs.

**Rationale:** Workflow preferences vary by team culture and project requirements. Consistency within a project matters more than the specific approach.

**Examples:**
- Choose between squash and rebase strategies
- Define branch naming conventions
- Establish PR size guidelines
- Balance fast iteration with thorough review

---

### UI Framework Choices

**Tier:** `flexible`

Select UI frameworks based on project requirements, team expertise, and performance needs. Consider both developer experience and user experience.

**Rationale:** Different frameworks excel in different scenarios. The "best" choice depends on context.

**Examples:**
- React for large, interactive applications
- Vue for progressive enhancement
- Svelte for performance-critical apps
- Consider build size and runtime performance

---

### Build Tools and Bundlers

**Tier:** `flexible`

Use build tools that match project needs and team familiarity. Optimize build configuration for development experience and production performance.

**Rationale:** Build tool choice impacts developer productivity and application performance, but many tools can achieve similar results.

**Examples:**
- Webpack for complex configurations
- Vite for fast development server
- esbuild for speed
- Balance features with simplicity

---

### Logging Verbosity

**Tier:** `flexible`

Log at appropriate levels (debug, info, warn, error). Adjust verbosity based on environment and operational needs.

**Rationale:** Too much logging creates noise; too little makes debugging difficult. The right balance depends on the context.

**Examples:**
- Use debug level for detailed troubleshooting
- Log info for normal operations
- Warn for concerning but handled situations
- Error for failures that need attention

---

### Refactoring Frequency

**Tier:** `flexible`

Refactor code opportunistically when working in an area. Balance technical debt reduction with feature delivery.

**Rationale:** Continuous small refactorings prevent technical debt accumulation, but must be balanced with business needs.

**Examples:**
- Follow the Boy Scout Rule (leave code better than you found it)
- Refactor when adding related features
- Schedule dedicated refactoring time
- Use feature flags to enable incremental rewrites
