# Prompt improvement examples

These are fictional repository findings used to illustrate the workflow. Their paths and symbols are not evidence about the user's project. Replace them with inspected facts for every real prompt.

For each case, the light subagent inspects the target and supplied conversation history, answers investigation questions with evidence, and returns the prompt to the main agent. The main agent displays the prompt before following it. Prompt display is informational; implementation proceeds within the user's existing authorization.

## A missing control with existing filtering support

Request: "add category filter to products page".

Inspected findings: `ProductsPage.tsx` has search and pagination. `useProducts` already accepts a category ID, and its API handler applies it. The orders page has a single-select filter using `FilterSelect`; categories come from `useCategories`. The products page lacks a category control. Neighboring list filters reset pagination on selection and clearing.

```markdown
Add a category filter to the products page. The remaining change is to expose and connect the existing category filtering support in the page.

Before editing, read the project instructions and recheck ProductsPage.tsx, useProducts, its API handler, and the orders page's FilterSelect usage. If the products page already exposes a working category filter, verify it and report the evidence without changing code. If it is partly implemented, complete only the missing connection.

Reuse FilterSelect, useCategories, and the category ID accepted by useProducts. Match the orders page's filter state and interaction conventions. Keep the existing API filtering logic and domain types.

Scope is the category control, its connection to the existing query, and relevant verification. Preserve search, sorting, pagination, permissions, and existing loading/error behavior. Add no unrelated filters, category-management UI, redesign, new dependency, endpoint, or schema change. If existing support cannot satisfy the request without a wider change, explain that prerequisite before expanding the work.

Acceptance: selecting a category limits products to that category; clearing it restores the unfiltered category state. Follow the inspected list-filter convention of resetting pagination on those changes. Existing search and sorting continue to work with the filter.

Use the project's relevant checks and existing filter test pattern to verify selection, clearing, and interaction with the existing controls. Review the diff for scope and duplication, then report changed paths and checks actually run. Commit or publish only within existing authorization.
```

URL persistence, multi-select, result-count badges, and saved filters are not implied by this request. Include one only when the user requested it or it is an established requirement of the reused implementation.

## A control that exists but is not connected

Inspected findings: `ProductsPage.tsx` already renders `CategoryFilter` and tracks `categoryId`, but the `useProducts` call omits that value. The query supports it.

The prompt should say: "Connect the existing category filter state to useProducts. Keep the current control and category source. Verify selection and clearing; do not add a second filter or rewrite the backend."

It must still ask the executing agent to recheck current code and verify rather than edit if the connection has already been fixed. It should name the inspected state, query, and applicable tests in the real output.

## The requested behavior already exists

Inspected findings: the category control is rendered, its selection reaches the query and backend, and existing tests cover selection and clearing.

The subagent returns a verification-only prompt: "Confirm that the existing category filter on the products page satisfies the request. Inspect its reachable control and data path, use the relevant existing verification, and report evidence and any actual discrepancy. If the requested behavior is satisfied, make no code changes." The main agent shows it, runs the relevant verification, and reports the existing feature without adding another implementation.

Reading a test is not running it. Report the distinction. If the feature is hidden by a flag or permission, report that condition and resolve the user's intended visibility before proposing activation.

## The repository is unavailable

Return the access limitation to the main agent as a blocker. If the user explicitly wants a draft without repository access, label it unverified. It should require discovery of the products page, existing filters and query support, complete/partial/missing status, and reusable code before edits. It must not assert that `FilterSelect` or `useProducts` exists. The main agent exposes the limitation and does not treat the draft as ready for implementation.

## A decision the code cannot settle

If two products pages are plausible and the supplied conversation gives no target, the subagent returns a question about which page is intended. The main agent asks it and passes the real answer back to the same subagent. If a new interaction has no comparable convention, return the decision that affects implementation, such as single versus multiple category selection. Keep unrelated design questions out of the interview.

If prior conversation already selected the public products page and the existing convention uses single selection, the subagent answers those questions from that evidence. It does not ask them again or add multiple selection.
