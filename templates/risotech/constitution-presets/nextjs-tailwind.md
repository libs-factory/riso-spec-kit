# Constitution Preset: Next.js + Tailwind CSS

This preset provides governance rules optimized for Next.js applications with Tailwind CSS.

---

## CORE Rules

### App Router Convention

**Tier:** `core`

Use Next.js 13+ App Router (`app/` directory) for all new projects. Follow Next.js file conventions strictly.

**Rationale:** App Router is the future of Next.js with better performance, built-in layouts, and server components support.

**Examples:**
- Place routes in `app/` directory with proper structure
- Use `page.tsx` for routes, `layout.tsx` for layouts
- Use `loading.tsx` and `error.tsx` for loading/error states
- Follow the file-system routing conventions

---

### Server Components by Default

**Tier:** `core`

Use Server Components by default. Add 'use client' directive only when needed (interactivity, hooks, browser APIs).

**Rationale:** Server Components reduce bundle size, improve performance, and enable better data fetching patterns.

**Examples:**
- Keep data fetching in Server Components
- Add 'use client' only for interactive components
- Minimize client-side JavaScript
- Use Server Actions for mutations

---

### Environment Variables Security

**Tier:** `core`

Never expose server-side secrets to the client. Use `NEXT_PUBLIC_` prefix only for truly public variables.

**Rationale:** Exposing secrets in client bundle is a critical security vulnerability.

**Examples:**
- API keys, database URLs stay server-side only
- Only `NEXT_PUBLIC_API_URL` type vars go to client
- Validate env vars on startup
- Use `.env.local` for secrets (gitignored)

---

### Image Optimization Required

**Tier:** `core`

Always use `next/image` for images. Never use regular `<img>` tags unless there's a documented exception.

**Rationale:** next/image provides automatic optimization, lazy loading, and prevents layout shift.

**Examples:**
- Use `<Image>` component from next/image
- Provide width and height for static images
- Use priority for above-the-fold images
- Configure remote image domains in next.config.js

---

### SEO Metadata Management

**Tier:** `core`

Every page must have proper metadata (title, description, OG tags). Use Next.js metadata API.

**Rationale:** Proper SEO is essential for discoverability and social sharing.

**Examples:**
- Export metadata object from page.tsx
- Use generateMetadata for dynamic pages
- Include OpenGraph and Twitter card data
- Test with social media debuggers

---

## HIGH-PRIORITY Rules

### Tailwind Configuration

**Tier:** `high-priority`

Customize Tailwind theme in tailwind.config.js for brand colors, spacing, and breakpoints. Don't use arbitrary values excessively.

**Rationale:** Centralized theme ensures consistency and makes redesigns easier. Arbitrary values defeat the purpose of utility classes.

**Examples:**
- Define brand colors in theme.extend.colors
- Create custom spacing if needed
- Use theme values: `bg-brand-primary` not `bg-[#1234]`
- Allow arbitrary values only for one-offs

---

### Data Fetching Patterns

**Tier:** `high-priority`

Use Server Components for data fetching. Cache appropriately with revalidate options. Use parallel data fetching when possible.

**Rationale:** Proper data fetching patterns improve performance and UX.

**Examples:**
- Fetch in Server Components, not in useEffect
- Use fetch with revalidate option
- Fetch data in parallel at the same level
- Use Suspense boundaries for loading states

---

### Route Handlers for APIs

**Tier:** `high-priority`

Place API routes in `app/api/` directory. Use proper HTTP methods and status codes. Validate inputs.

**Rationale:** Consistent API structure makes the codebase maintainable and secure.

**Examples:**
- GET for reading, POST for creating, etc.
- Return appropriate status codes (200, 201, 400, 404)
- Validate request bodies with Zod or similar
- Handle errors gracefully

---

### Component Organization

**Tier:** `high-priority`

Separate page components (route handlers) from reusable components. Keep components directory organized.

**Rationale:** Clear separation makes code easier to navigate and maintain.

**Examples:**
- Pages in `app/` directory structure
- Reusable components in `components/` or `app/_components/`
- Group related components together
- Use index files for public exports

---

### Tailwind: Component Classes

**Tier:** `high-priority`

Extract repeated Tailwind patterns into components or @apply directives sparingly. Prefer composition over @apply.

**Rationale:** Components are more maintainable than @apply. @apply should be rare exceptions.

**Examples:**
- Create Button component instead of @apply button styles
- Use component props for variations
- @apply only for base styles (like form inputs)
- Keep utility-first approach

---

### Performance Budgets

**Tier:** `high-priority`

Monitor bundle size and Core Web Vitals. Set performance budgets for routes.

**Rationale:** Performance directly impacts user experience and SEO rankings.

**Examples:**
- Keep initial bundle < 100KB gzipped
- Aim for LCP < 2.5s, FID < 100ms, CLS < 0.1
- Use `next/bundle-analyzer` to monitor
- Code-split large dependencies

---

## FLEXIBLE Rules

### State Management Choice

**Tier:** `flexible`

Choose between Server State (cache), URL state (searchParams), React Context, or Zustand based on data scope and needs.

**Rationale:** Next.js provides multiple state management patterns. Choose based on the use case.

**Examples:**
- Server state for data fetching (default)
- URL params for shareable state (filters, pagination)
- Context for theme, user preferences
- Zustand for complex client state

---

### TypeScript Strictness

**Tier:** `flexible`

Use strict TypeScript mode. Consider `satisfies` operator and const assertions for better type inference.

**Rationale:** Stricter typing catches more bugs, but balance with development speed.

**Examples:**
- Enable strict mode in tsconfig.json
- Use `satisfies` for config objects
- Define proper types for API responses
- Use Zod for runtime validation

---

### Tailwind vs CSS Modules

**Tier:** `flexible`

Primarily use Tailwind. Allow CSS Modules for complex animations or third-party integrations.

**Rationale:** Consistency with Tailwind is preferred, but some cases need traditional CSS.

**Examples:**
- Use Tailwind for 95% of styling
- CSS Modules for complex keyframe animations
- CSS Modules when integrating libraries
- Document exceptions

---

### File Naming Convention

**Tier:** `flexible`

Use kebab-case for files or PascalCase for components based on team preference. Be consistent.

**Rationale:** Both conventions work. Consistency matters more than the choice.

**Examples:**
- kebab-case: `user-profile.tsx`, `api-client.ts`
- PascalCase: `UserProfile.tsx`, `ApiClient.ts`
- Next.js route files follow their convention (page.tsx)
- Document chosen convention

---

### Testing Strategy

**Tier:** `flexible`

Choose testing approach based on application criticality: unit tests, integration tests, or E2E tests.

**Rationale:** Different applications need different testing strategies.

**Examples:**
- Unit tests for utility functions
- Integration tests for API routes
- E2E tests for critical user flows
- Playwright or Cypress for E2E

---

### Internationalization

**Tier:** `flexible`

Use next-intl or similar if i18n is needed. Structure locale files appropriately.

**Rationale:** i18n is needed for some apps but not all. Choose good library when needed.

**Examples:**
- Use next-intl for type-safe translations
- Organize translations by feature
- Use server-side rendering for translated content
- Test with multiple locales

---

## Next.js Specific Best Practices

### Static vs Dynamic Rendering
- Use static rendering (default) when possible
- Use dynamic rendering (dynamic data, cookies, headers) when needed
- Use ISR (Incremental Static Regeneration) for frequently updated data
- Understand when Next.js switches to dynamic automatically

### Caching Strategy
- Understand Next.js caching layers (Request, Data, Full Route)
- Use revalidate option appropriately
- Use cache tags for fine-grained revalidation
- Clear cache when needed with revalidatePath or revalidateTag

### Edge Runtime
- Use Edge Runtime for lightweight API routes
- Understand Edge limitations (no Node.js APIs)
- Use for geolocation-based content
- Use for authentication middleware

### Middleware
- Use middleware for authentication checks
- Keep middleware lightweight
- Return responses only when needed
- Understand middleware execution order

### Deployment
- Optimize for Vercel or chosen platform
- Configure environment variables properly
- Use preview deployments for testing
- Monitor with Vercel Analytics or alternatives

### Tailwind Production
- Purge unused classes in production
- Use JIT mode (default in v3+)
- Minify with cssnano
- Monitor CSS bundle size
