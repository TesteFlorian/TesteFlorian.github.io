# UX/UI Improvement Plan with RCI Loops

## 1. Objectives
- Elevate first-contact storytelling for research, publications, and teaching with focused calls to action.
- Reduce navigation friction on desktop and mobile while keeping URLs stable.
- Establish a lightweight design system (colors, typography, spacing, icon usage) that is easy to extend.
- Meet target accessibility bar (WCAG 2.1 AA) and document compliance checks.
- Modernize front-end tooling to remove legacy jQuery dependencies where practical without breaking build pipelines.
- Provide transparent analytics notice and opt-out while retaining observability.

## 2. Baseline Pain Points
- **Navigation/IA:** Sidebar lists are long; mobile experience collapses into dense link stacks with little prioritization.
- **Visual hierarchy:** Similar card layouts and limited accent usage make it hard to distinguish key achievements.
- **Accessibility:** No skip link, limited focus styling, and inconsistent `aria` semantics on toggles.
- **Performance/tooling:** Heavy reliance on bundled jQuery plugins; build scripts target Node 0.10 with outdated dev dependencies.
- **Analytics transparency:** GoatCounter runs without an on-page disclosure or control for visitors.

## 3. Workstreams and Deliverables

| Workstream | Key Tasks | Deliverables | Success Metrics |
|------------|-----------|--------------|-----------------|
| IA & Navigation | Map key journeys, redesign desktop sidebar into grouped sections, create mobile top-nav + in-page TOC | Wireframes, updated layouts, regression checklist | < 3 clicks to reach publications; SUS ≥ 75 from internal review |
| Visual System | Define color palette, typography scale, component spacing tokens; update hero and cards | Design tokens doc, updated SCSS partials, component gallery | Visual QA pass; meets contrast AA |
| Content & CTAs | Craft hero summary, highlight top 3 CTAs per page, standardize resource buttons | Updated markdown with CTA blocks, button partial | 100% core pages include summary + CTAs |
| Accessibility | Add skip link, keyboard focus states, `aria-expanded` toggles, audit landmark roles | Accessibility checklist, axe/devtools reports | No WCAG 2.1 Level A/AA violations |
| Front-end Modernization | Replace SmoothScroll/Stickyfill with native alternatives, migrate bundler to modern tool (e.g., esbuild/Vite) while keeping fallback | New build scripts, module entrypoint, legacy shim | Lighthouse performance ≥ 90 mobile |
| Analytics & Privacy | Draft privacy blurb, implement opt-out toggle storing consent, document CSP allowances | Privacy page snippet, consent component, CSP doc | Opt-out stored; analytics blocked when opted out |

## 4. Implementation Phasing
- **Phase 0 – Audit (Week 1):** Complete heuristic evaluation, collect metrics (page load, Lighthouse, axe). Output baseline report.
- **Phase 1 – IA & Navigation (Weeks 2-3):** Implement desktop/mobile nav redesign. RCI Loop 1 before shipping.
- **Phase 2 – Visual + Content (Weeks 4-5):** Apply design tokens, update hero sections, add CTAs. RCI Loop 2.
- **Phase 3 – Accessibility (Week 6):** Implement skip links, focus styles, ARIA updates; run automated and manual testing. RCI Loop 3.
- **Phase 4 – Tooling + Analytics (Weeks 7-8):** Modernize JS pipeline, integrate consent mechanism, document CSP. RCI Loop 4 and final consolidated review.

## 5. RCI Loop Structure
Each loop contains:
1. **Plan:** Define slice scope, exit criteria, and test plan; capture baseline metrics.
2. **Implement:** Execute code changes with peer pairing where feasible.
3. **Critique:** Cross-functional review (UX, accessibility, performance, security). Use checklist + metrics comparison; record findings in issue tracker.
4. **Improve:** Address critical findings immediately; schedule non-blocking optimizations with owners and deadlines.

### RCI Participants
- **Lead Engineer (you):** Implementation owner, compiles metrics, coordinates fixes.
- **UX Reviewer:** Evaluates flow, visual hierarchy, mobile ergonomics.
- **Accessibility Consultant (can be internal checklist role):** Runs axe, keyboard drills, screen-reader spot checks.
- **Performance/Security Reviewer:** Verifies bundle size, Lighthouse, and analytics consent flow.

### Decision Rules
- Blocking issues (WCAG failure, navigation regression, TTI regression >10%) must be fixed before release.
- Non-blocking items require documented follow-up with target release sprint.
- Metrics logged in `/docs/ux_ui_metrics.md` (create during Phase 0).

## 6. Tooling & Environment Updates
- Introduce Node 18+ toolchain with package manager lockfile; add npm scripts for lint, build, test.
- Adopt Stylelint + Prettier (optional dev-time) for SCSS consistency; ensure opt-in to avoid runtime dependency bloat.
- Configure automated CI checks: build, axe-core CLI smoke tests, Lighthouse CI on key pages.

## 7. Risk & Mitigation
- **Backward Compatibility:** Maintain legacy layouts during phased rollout by gating new nav behind feature flag until tested.
- **Timeline Creep:** Keep each workstream scoped to 2-week window; enforce RCI loop completion before moving on.
- **Resource Availability:** Document review responsibilities ahead of each loop; provide async review template for distributed collaborators.

## 8. Next Actions
1. Create baseline metrics document (`docs/ux_ui_metrics.md`) with current audits.
2. Open tracking issues per workstream referencing this plan.
3. Schedule Phase 0 RCI kickoff with reviewers and align on tool access (Lighthouse, axe, etc.).

