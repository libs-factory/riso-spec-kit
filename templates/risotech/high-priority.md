# High-Priority Constitution Rules

**HIGH-PRIORITY** rules should be followed unless there is a strong, documented reason to deviate. Deviations require explicit acknowledgment and justification.

---

### Performance Optimization

**Tier:** `high-priority`

Application performance should be optimized for user experience. Page load times should be under 3 seconds, and API responses should be under 500ms for common operations.

**Rationale:** Performance directly impacts user satisfaction and conversion rates. Slow applications frustrate users and hurt business metrics.

**Examples:**
- Profile performance bottlenecks before optimizing
- Use caching strategies appropriately
- Optimize database queries with proper indexing
- Lazy-load resources when possible

---

### Documentation Standards

**Tier:** `high-priority`

All public APIs, complex algorithms, and architectural decisions must be documented. Keep documentation up to date with code changes.

**Rationale:** Good documentation reduces onboarding time, enables effective collaboration, and preserves knowledge about why decisions were made.

**Examples:**
- Document API endpoints with request/response examples
- Use JSDoc/docstrings for public functions
- Maintain an architecture decision record (ADR)
- Update README files with setup instructions

---

### Dependency Management

**Tier:** `high-priority`

Dependencies should be carefully vetted before addition. Keep dependencies up to date, but test thoroughly before upgrading major versions.

**Rationale:** Each dependency is a potential security risk and maintenance burden. Outdated dependencies can have known vulnerabilities.

**Examples:**
- Evaluate alternatives before adding new dependencies
- Use dependency scanning tools
- Pin dependency versions in production
- Review dependency licenses for compliance

---

### Continuous Integration

**Tier:** `high-priority`

All code changes must pass through CI/CD pipeline before deployment. Pipeline should include linting, testing, and security scanning.

**Rationale:** CI/CD catches issues early, ensures consistent build processes, and enables rapid, reliable deployments.

**Examples:**
- Run automated tests on every pull request
- Use static analysis tools (linters, type checkers)
- Scan for security vulnerabilities
- Enforce code coverage thresholds

---

### Code Review Process

**Tier:** `high-priority`

All code must be reviewed by at least one other developer. Reviews should focus on correctness, maintainability, and adherence to standards.

**Rationale:** Code review catches bugs, shares knowledge across the team, and maintains code quality standards.

**Examples:**
- Provide constructive, specific feedback
- Review for logic errors, not just style
- Ensure tests cover the changes
- Verify documentation is updated

---

### Database Design Principles

**Tier:** `high-priority`

Database schemas should be normalized appropriately. Use migrations for all schema changes. Implement proper indexing strategies.

**Rationale:** Good database design prevents data anomalies, improves query performance, and makes the system more maintainable.

**Examples:**
- Normalize to at least third normal form (3NF)
- Use foreign keys to enforce referential integrity
- Index columns used in WHERE and JOIN clauses
- Plan for data growth and scalability

---

### API Design Consistency

**Tier:** `high-priority`

APIs should follow REST or GraphQL conventions consistently. Use standard HTTP status codes. Provide clear error messages.

**Rationale:** Consistent API design makes integration easier, reduces documentation burden, and improves developer experience.

**Examples:**
- Use nouns for resource endpoints
- Use HTTP verbs correctly (GET, POST, PUT, DELETE)
- Return appropriate status codes (200, 201, 400, 404, 500)
- Use consistent naming conventions (camelCase or snake_case)

---

### Environment Configuration

**Tier:** `high-priority`

Separate configuration for different environments (dev, staging, production). Never mix environment configurations.

**Rationale:** Environment separation prevents accidental data corruption and enables safe testing of changes.

**Examples:**
- Use environment variables for configuration
- Maintain separate databases per environment
- Use feature flags to control rollouts
- Never use production credentials in development

---

### Monitoring and Observability

**Tier:** `high-priority`

Implement comprehensive monitoring and alerting for production systems. Track key metrics like error rates, response times, and resource utilization.

**Rationale:** You can't fix what you can't measure. Monitoring enables proactive issue detection and rapid incident response.

**Examples:**
- Log important business events
- Set up alerts for error spikes
- Track application performance metrics (APM)
- Implement distributed tracing for microservices

---

### User Experience Consistency

**Tier:** `high-priority`

Maintain consistent UI/UX patterns across the application. Follow established design systems and component libraries.

**Rationale:** Consistent UX reduces cognitive load, makes the application easier to learn, and creates a professional impression.

**Examples:**
- Use shared component libraries
- Follow platform conventions (iOS, Android, Web)
- Maintain consistent spacing and typography
- Use consistent navigation patterns
