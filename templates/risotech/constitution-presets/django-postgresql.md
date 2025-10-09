# Constitution Preset: Django + PostgreSQL

This preset provides governance rules optimized for Django backend applications with PostgreSQL.

---

## CORE Rules

### Database Migrations Required

**Tier:** `core`

All database schema changes must go through Django migrations. Never modify the database schema directly.

**Rationale:** Migrations provide version control for schema, enable rollbacks, and ensure consistency across environments.

**Examples:**
- Run `makemigrations` after model changes
- Review generated migrations before applying
- Test migrations in development before production
- Never edit migration files after they're applied
- Use data migrations for complex data transformations

---

### SQL Injection Prevention

**Tier:** `core`

Always use Django ORM or parameterized queries. Never construct SQL with string formatting or concatenation.

**Rationale:** SQL injection is a critical security vulnerability that can expose or destroy all data.

**Examples:**
- Use ORM: `User.objects.filter(email=email)`
- Parameterized: `cursor.execute("SELECT * FROM users WHERE email = %s", [email])`
- Never: `cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")`
- Use Q objects for complex queries

---

### Authentication Security

**Tier:** `core`

Use Django's built-in authentication system. Never store passwords in plain text. Use strong password validators.

**Rationale:** Django's auth system is battle-tested and secure. Rolling your own authentication is dangerous.

**Examples:**
- Use `django.contrib.auth` for user management
- Configure PASSWORD_HASHERS appropriately
- Enable password validators in settings
- Use Django's login_required decorator
- Implement rate limiting for authentication endpoints

---

### Environment Variables for Secrets

**Tier:** `core`

All secrets (SECRET_KEY, database passwords, API keys) must be in environment variables, never in code or version control.

**Rationale:** Committing secrets is a critical security breach that can't be fully undone.

**Examples:**
- Use python-decouple or django-environ
- Keep .env file in .gitignore
- Use different secrets per environment
- Rotate secrets periodically
- Use secrets manager in production (AWS Secrets Manager, etc.)

---

### Input Validation

**Tier:** `core`

Validate all user inputs using Django Forms or DRF Serializers. Never trust client-side validation alone.

**Rationale:** Client-side validation can be bypassed. Server-side validation prevents malicious data and data corruption.

**Examples:**
- Use Form classes for HTML forms
- Use Serializers for API endpoints
- Define field validators and clean methods
- Return appropriate error messages
- Log validation failures for monitoring

---

## HIGH-PRIORITY Rules

### Database Indexes

**Tier:** `high-priority`

Add database indexes for frequently queried fields and foreign keys. Monitor slow queries and add indexes as needed.

**Rationale:** Missing indexes cause performance problems that get worse as data grows.

**Examples:**
- Add `db_index=True` to filtered fields
- Use `Meta.indexes` for composite indexes
- Index foreign keys automatically (Django default)
- Use `django-debug-toolbar` to identify slow queries
- Review query plans with `EXPLAIN ANALYZE`

---

### Transaction Management

**Tier:** `high-priority`

Use database transactions for operations that must be atomic. Use `transaction.atomic()` appropriately.

**Rationale:** Partial database updates can leave data in inconsistent state.

**Examples:**
- Wrap related operations in `@transaction.atomic()`
- Use transactions for financial operations
- Understand ATOMIC_REQUESTS setting implications
- Handle transaction rollback properly
- Test transaction behavior

---

### Django REST Framework for APIs

**Tier:** `high-priority`

Use Django REST Framework (DRF) for building APIs. Follow REST conventions and DRF best practices.

**Rationale:** DRF provides consistent API patterns, serialization, and authentication handling.

**Examples:**
- Use ViewSets for CRUD operations
- Define Serializers for data validation
- Use proper HTTP methods and status codes
- Implement pagination for list endpoints
- Use DRF authentication and permissions

---

### Query Optimization

**Tier:** `high-priority`

Use `select_related` and `prefetch_related` to avoid N+1 queries. Monitor query count in views.

**Rationale:** N+1 queries cause severe performance problems and database load.

**Examples:**
- Use `select_related` for forward ForeignKey
- Use `prefetch_related` for reverse FK and M2M
- Use `only()` and `defer()` to limit fields
- Monitor queries with django-debug-toolbar
- Set up query count alerts

---

### Testing Coverage

**Tier:** `high-priority`

Write tests for models, views, and business logic. Aim for 80%+ coverage. Use Django's test framework.

**Rationale:** Tests prevent regressions and enable confident refactoring.

**Examples:**
- Test models with TestCase
- Test views with Client or RequestFactory
- Test API endpoints with APIClient
- Use factories (factory_boy) for test data
- Run tests in CI/CD pipeline

---

### Celery for Background Tasks

**Tier:** `high-priority`

Use Celery for long-running tasks, scheduled jobs, and async processing. Never block HTTP requests with slow operations.

**Rationale:** Blocking requests leads to timeouts and poor user experience.

**Examples:**
- Use Celery for email sending
- Use Celery for report generation
- Use Celery Beat for scheduled tasks
- Monitor task execution and failures
- Set appropriate task timeouts

---

## FLEXIBLE Rules

### Class-Based vs Function-Based Views

**Tier:** `flexible`

Use Class-Based Views (CBVs) for standard CRUD operations. Use Function-Based Views (FBVs) for simple or unique logic.

**Rationale:** Both have their place. CBVs reduce boilerplate for common patterns, FBVs are clearer for custom logic.

**Examples:**
- CBV: Use generic views (ListView, CreateView, etc.)
- FBV: Simple views with custom logic
- Don't force CBVs where FBVs are clearer
- Be consistent within related views

---

### Model Manager Patterns

**Tier:** `flexible`

Create custom managers for complex query logic. Keep models focused on data, managers on querying.

**Rationale:** Custom managers improve code organization and reusability.

**Examples:**
- Create managers for common filters
- Use managers for soft-delete pattern
- Chain manager methods for complex queries
- Consider querysets for more flexibility

---

### Serializer Nesting Depth

**Tier:** `flexible`

Balance between nested serializers and separate endpoints based on use case and performance.

**Rationale:** Deep nesting is convenient but can cause performance issues. Flat is more flexible but requires more requests.

**Examples:**
- Nest for related data commonly accessed together
- Use separate endpoints for deep relationships
- Provide both options for different use cases
- Monitor query performance of nested serializers

---

### File Upload Storage

**Tier:** `flexible`

Use django-storages with S3/GCS for production file uploads. Local storage acceptable for development.

**Rationale:** Cloud storage scales better and works with multiple application servers.

**Examples:**
- Configure MEDIA_ROOT for local development
- Use django-storages with boto3 for S3
- Set appropriate file permissions
- Implement virus scanning for uploads

---

### API Versioning Strategy

**Tier:** `flexible`

Choose versioning strategy (URL path, header, or query param) based on API consumers and stability.

**Rationale:** Different versioning strategies fit different use cases. Pick one and be consistent.

**Examples:**
- URL: `/api/v1/users/`
- Header: `Accept: application/vnd.api+json; version=1`
- Param: `/api/users/?version=1`
- Version when breaking changes needed

---

### Admin Customization

**Tier:** `flexible`

Customize Django admin for internal tools. Consider building custom admin interface for complex needs.

**Rationale:** Django admin is powerful for simple cases but may not fit complex workflows.

**Examples:**
- Customize list_display, list_filter, search_fields
- Add custom admin actions
- Use inline formsets for related objects
- Build custom views when admin isn't enough

---

## Django Specific Best Practices

### Settings Organization
- Split settings into base, development, production
- Use environment variables for configuration
- Never commit development settings values
- Document required environment variables

### Security Settings
- Set DEBUG=False in production
- Configure ALLOWED_HOSTS properly
- Use HTTPS in production (SECURE_SSL_REDIRECT)
- Set secure cookie flags (SECURE, HTTPONLY, SAMESITE)
- Configure CORS if needed (django-cors-headers)

### Database Configuration
- Use connection pooling (pgbouncer)
- Set appropriate connection limits
- Configure database backup strategy
- Use read replicas for heavy read workloads

### Caching Strategy
- Use Redis for cache backend
- Cache expensive queries
- Cache template fragments
- Set appropriate cache timeouts
- Use cache versioning for invalidation

### Logging
- Configure structured logging
- Log to external service (Sentry, CloudWatch)
- Log errors and slow queries
- Don't log sensitive data
- Use appropriate log levels

### Static Files
- Use WhiteNoise for serving static files
- Configure CDN for static assets
- Use ManifestStaticFilesStorage
- Compress and minify CSS/JS
- Set far-future cache headers

### Deployment
- Use gunicorn or uwsgi for WSGI server
- Use nginx for reverse proxy
- Configure health check endpoints
- Use containers (Docker) for consistency
- Implement zero-downtime deployments

### Monitoring
- Monitor application performance (New Relic, DataDog)
- Monitor database performance
- Set up alerts for errors and slow responses
- Track user metrics and business KPIs
