# Constitution Preset: React + TypeScript

This preset provides governance rules optimized for React and TypeScript projects.

---

## CORE Rules

### Type Safety is Mandatory

**Tier:** `core`

All code must use TypeScript with strict mode enabled. No `any` types except for truly dynamic cases (which must be documented).

**Rationale:** TypeScript prevents entire classes of runtime errors and makes refactoring safer. Strict mode catches the most issues.

**Examples:**
- Enable `"strict": true` in tsconfig.json
- Use explicit types for function parameters and return values
- Use `unknown` instead of `any` when type is uncertain
- Document why `any` is used in the rare cases it's needed

---

### Component Testing Required

**Tier:** `core`

All React components must have tests covering their main functionality and edge cases. Minimum 80% coverage for component logic.

**Rationale:** Untested components lead to regressions and make refactoring dangerous. UI bugs are expensive to fix in production.

**Examples:**
- Test component rendering with different props
- Test user interactions (clicks, inputs, etc.)
- Test conditional rendering logic
- Use React Testing Library for user-centric tests

---

### No Direct DOM Manipulation

**Tier:** `core`

Never use direct DOM manipulation (document.querySelector, etc.) except in documented edge cases. Use React refs when direct access is needed.

**Rationale:** Direct DOM manipulation breaks React's reconciliation and causes hard-to-debug issues.

**Examples:**
- Use state and props to control UI
- Use refs with useRef() for DOM access when necessary
- Integrate third-party libraries through proper React wrappers
- Document any exceptions with clear justification

---

### Security: Prevent XSS

**Tier:** `core`

Never use dangerouslySetInnerHTML without sanitization. Validate and sanitize all user inputs.

**Rationale:** XSS vulnerabilities can compromise user data and application security.

**Examples:**
- Use proper React rendering (JSX escapes by default)
- If HTML rendering is needed, use DOMPurify
- Validate inputs on both client and server
- Use Content Security Policy headers

---

## HIGH-PRIORITY Rules

### Functional Components Preferred

**Tier:** `high-priority`

Use functional components with hooks instead of class components unless there's a specific need (e.g., error boundaries).

**Rationale:** Hooks provide cleaner code, better reusability, and are the future of React. Class components are legacy.

**Examples:**
- Use useState, useEffect, useContext instead of class lifecycle
- Create custom hooks for reusable logic
- Use error boundaries (classes) only for error handling
- Migrate existing class components gradually

---

### Proper State Management

**Tier:** `high-priority`

Use appropriate state management based on scope: local state for component-specific, Context for app-wide, Redux/Zustand for complex global state.

**Rationale:** Misplaced state leads to prop drilling, performance issues, and maintenance problems.

**Examples:**
- Local state with useState for component UI
- Context for theme, auth, i18n
- Global state library for complex application state
- Avoid lifting state higher than necessary

---

### Component Decomposition

**Tier:** `high-priority`

Components should be small and focused. Split large components into smaller ones. Keep components under 250 lines.

**Rationale:** Small components are easier to test, reuse, and maintain. Large components become unmaintainable.

**Examples:**
- Extract repeated UI patterns into components
- Separate container (logic) from presentational components
- Use composition over prop drilling
- Create a component library for common patterns

---

### Performance: Memoization

**Tier:** `high-priority`

Use React.memo, useMemo, and useCallback to prevent unnecessary re-renders in performance-critical components.

**Rationale:** Unnecessary re-renders hurt performance, especially in large lists or complex UIs.

**Examples:**
- Wrap expensive components with React.memo
- Memoize expensive calculations with useMemo
- Stabilize callbacks with useCallback when passed to children
- Profile before optimizing (don't premature optimize)

---

### Accessibility Standards

**Tier:** `high-priority`

All interactive elements must be keyboard accessible and have proper ARIA labels. Test with screen readers.

**Rationale:** Accessible apps reach more users and often have better UX for everyone.

**Examples:**
- Use semantic HTML (button, nav, main, etc.)
- Add aria-label to icon buttons
- Ensure keyboard navigation works
- Test with eslint-plugin-jsx-a11y

---

### TypeScript: No Type Assertions

**Tier:** `high-priority`

Avoid type assertions (`as Type`) unless absolutely necessary. Use type guards and proper typing instead.

**Rationale:** Type assertions bypass TypeScript's safety and can hide bugs.

**Examples:**
- Use type guards (typeof, instanceof) instead
- Define proper types upfront
- Use discriminated unions for complex types
- Document why assertion is needed if used

---

## FLEXIBLE Rules

### CSS-in-JS vs CSS Modules

**Tier:** `flexible`

Choose between styled-components, Emotion, CSS Modules, or Tailwind based on team preference and project needs.

**Rationale:** All approaches work well when used consistently. Team familiarity matters more than the specific choice.

**Examples:**
- styled-components for component-scoped styles
- Tailwind for utility-first approach
- CSS Modules for traditional CSS with scoping
- Pick one and stick with it

---

### File Organization

**Tier:** `flexible`

Organize by feature or by type based on project size. Be consistent within the project.

**Rationale:** Organization matters for maintainability, but the specific pattern is less important than consistency.

**Examples:**
- Feature-based: `features/auth/components/LoginForm.tsx`
- Type-based: `components/LoginForm.tsx`, `hooks/useAuth.ts`
- Hybrid: Use features for large areas, types for shared
- Document the chosen structure in README

---

### Props Interface Naming

**Tier:** `flexible`

Name props interfaces with or without "Props" suffix based on team preference (e.g., `ButtonProps` vs `Button`).

**Rationale:** Both conventions work. Consistency within codebase matters most.

**Examples:**
- With suffix: `interface ButtonProps { ... }`
- Without suffix: `interface Button { ... }` and `type ButtonComponent = React.FC<Button>`
- Choose one pattern and enforce with linter
- Document in style guide

---

### Hook Return Type

**Tier:** `flexible`

Return arrays or objects from custom hooks based on use case and ergonomics.

**Rationale:** Arrays for tuple-like returns (useState style), objects for many values. Both valid.

**Examples:**
- Array: `const [user, setUser] = useUser()`
- Object: `const { user, loading, error } = useUser()`
- Prefer objects when returning >2 values
- Be consistent across similar hooks

---

### Component File Structure

**Tier:** `flexible`

Place component code, styles, and tests in same directory or separate directories based on team preference.

**Rationale:** Co-location helps find related files, but separation can be cleaner for large components.

**Examples:**
- Co-located: `Button/index.tsx`, `Button/Button.test.tsx`, `Button/styles.ts`
- Separated: `components/Button.tsx`, `__tests__/Button.test.tsx`
- Consider project size and complexity
- Document convention

---

### Default vs Named Exports

**Tier:** `flexible`

Use default exports for components or named exports for better refactoring, based on team preference.

**Rationale:** Both work. Named exports enable better IDE refactoring but require more boilerplate.

**Examples:**
- Default: `export default Button`
- Named: `export { Button }`
- Named is better for tree-shaking and refactoring
- Default is more concise

---

## Stack-Specific Recommendations

### Build Configuration
- Use Vite for faster development builds
- Use webpack for complex configurations
- Enable source maps in development
- Optimize bundle size for production

### Testing Stack
- Jest + React Testing Library (recommended)
- Vitest as faster Jest alternative
- Playwright or Cypress for E2E tests
- Mock Service Worker for API mocking

### Code Quality
- ESLint with typescript-eslint
- Prettier for formatting
- Husky for pre-commit hooks
- lint-staged for faster linting

### Performance
- Code splitting with React.lazy
- Image optimization (next/image or similar)
- Bundle analysis with webpack-bundle-analyzer
- Performance monitoring (Lighthouse CI)
