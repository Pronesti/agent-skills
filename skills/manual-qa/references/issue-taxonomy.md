# Issue checklist

Use this to select relevant cases within scope, not to label every warning or deviation a bug. Requirements establish correctness; observations establish what happened.

## Severity

Use any supplied project scale; otherwise assess actual user impact and affected reach:

| Severity | Impact |
|---|---|
| critical | Data loss, security/privacy exposure, or broad core-workflow outage. |
| high | Major journey unusable for affected users, without a practical workaround. |
| medium | Material impairment with a workaround or limited reach. |
| low | Minor cosmetic/content issue without significant workflow impact. |

State uncertainty where impact or reach is unknown. A failed case is not automatically a critical issue; several cases can describe one issue.

## Coverage prompts

- **Functional:** links/redirects; form acceptance and validation; filtering, sorting, pagination; uploads/downloads; state persistence; repeated submission and stale results.
- **Feedback and recovery:** loading, empty/full states, actionable error messages, recoverable dead ends, canceled operations, interrupted sessions.
- **Visual/content:** overlap, clipping, missing assets, long/localized text, wrong labels, contrast, focus visibility, responsive layout and supported themes.
- **Accessibility:** keyboard order, focus trapping/restoration, labels and errors, supported assistive technology. Accessible names alone do not establish visual quality or full accessibility compliance.
- **Authorization:** signed-out access and authorized role boundaries; preserve user-owned state and do not invent additional identities.
- **Performance:** observed delay, jank and layout shifts, recorded with conditions and timing method when measurable. A generic 300ms/3s threshold is not a product requirement; avoid claiming memory leaks or backend causes from slowness alone.
- **Diagnostics:** native console errors, failed requests and warnings when exposed. Record relevance to the visible symptom; warnings alone do not prove a user-facing failure. No network/console access is a tooling limit, not a product bug.

For each relevant family, choose reachable cases with observable expectations. Include inaccessible requirements as coverage gaps. Source inspection, emulation, or a resized viewport cannot establish execution on an unavailable browser, device, or assistive technology.
