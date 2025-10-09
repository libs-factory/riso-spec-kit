# Core Constitution Rules

**CORE** rules are non-negotiable and must be followed in all circumstances. Violations of core rules should block implementation.

---

### Code Quality and Maintainability

**Tier:** `core`

All code must be maintainable, readable, and follow established coding standards. Code reviews are mandatory before merging to main branches.

**Rationale:** Poor code quality leads to technical debt, bugs, and makes the codebase difficult to maintain and extend over time.

**Examples:**
- Use meaningful variable and function names
- Follow the project's style guide (linting rules)
- Keep functions small and focused on a single responsibility
- Write self-documenting code with comments only where necessary

---

### Security First

**Tier:** `core`

Security must be considered at every stage of development. Never commit sensitive data (credentials, API keys, personal information) to version control.

**Rationale:** Security vulnerabilities can lead to data breaches, financial loss, and loss of user trust. Prevention is far cheaper than remediation.

**Examples:**
- Use environment variables for sensitive configuration
- Validate and sanitize all user inputs
- Keep dependencies up to date with security patches
- Follow OWASP Top 10 guidelines

---

### Testing Requirements

**Tier:** `core`

All production code must have automated tests. Critical paths must achieve minimum 80% code coverage.

**Rationale:** Automated tests catch regressions early, document expected behavior, and enable confident refactoring.

**Examples:**
- Write unit tests for business logic
- Write integration tests for API endpoints
- Use test-driven development (TDD) for complex features
- Ensure CI/CD pipeline runs all tests before deployment

---

### Version Control Discipline

**Tier:** `core`

Use version control for all project artifacts. Commit messages must be clear and descriptive. Never force-push to shared branches.

**Rationale:** Good version control practices enable collaboration, make it easy to track changes, and provide the ability to roll back if needed.

**Examples:**
- Use conventional commit messages (feat:, fix:, docs:, etc.)
- Create feature branches for all new work
- Use pull requests for code review
- Keep commits atomic and focused

---

### Backwards Compatibility

**Tier:** `core`

Breaking changes to public APIs must be avoided. When unavoidable, they must be clearly documented and provide migration paths.

**Rationale:** Breaking changes disrupt users and downstream systems. Providing stability builds trust and reduces maintenance burden.

**Examples:**
- Version APIs appropriately (v1, v2, etc.)
- Deprecate features before removing them
- Provide clear migration documentation
- Use semantic versioning for releases

---

### Data Privacy and Compliance

**Tier:** `core`

Handle user data with respect and in compliance with relevant regulations (GDPR, CCPA, etc.). Implement data minimization principles.

**Rationale:** Privacy violations can result in legal penalties, loss of user trust, and reputational damage.

**Examples:**
- Only collect data that is necessary
- Implement proper data retention policies
- Provide users with data export and deletion capabilities
- Document all data processing activities

---

### Accessibility Standards

**Tier:** `core`

All user-facing features must meet WCAG 2.1 Level AA accessibility standards at minimum.

**Rationale:** Accessible software ensures inclusivity and is often required by law. It also improves usability for all users.

**Examples:**
- Use semantic HTML
- Ensure keyboard navigation works
- Provide text alternatives for images
- Maintain sufficient color contrast ratios

---

### Error Handling and Logging

**Tier:** `core`

All errors must be handled gracefully. Critical errors must be logged with sufficient context for debugging.

**Rationale:** Proper error handling prevents crashes and provides a good user experience. Logging enables rapid diagnosis of production issues.

**Examples:**
- Use try-catch blocks appropriately
- Log errors with stack traces and context
- Never expose internal errors to end users
- Implement monitoring and alerting for critical errors
