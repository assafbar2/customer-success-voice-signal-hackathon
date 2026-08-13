# Sentry portfolio

What a sentrant can **have**, **gain**, **lose**, **get billed for**.  
Moves target an `id` — not a vibe, not just a brand name.

`ship seer.autofix` · `take replay.mobile` · `price logs` · `break sdk.python` · `tell seer.code_review`

Seer is not one blob. “Review my PR”, “fix this”, “run it from Cursor via MCP” are different lives.

---

## Signals they send (we bill these)

| id | What |
| --- | --- |
| `errors` | Issues. The original. |
| `spans` | Traces. Frontend → backend → the other service. |
| `logs` | Logs next to the error, not in another tab. |
| `replay.web` | Session Replay, web. |
| `replay.mobile` | Session Replay, mobile. |
| `profile.continuous` | This *function* on line 42 is slow. |
| `profile.ui` | UI profiling. |
| `metrics` | Counters / gauges from their code. Trace-connected. |
| `attachments` | Minidumps, screenshots, whatever they uploaded. |
| `crons` | Did the job run. |
| `uptime` | Is the endpoint up. |
| `agents` | *Their* agents: LLM calls, tools, tokens, MCP servers they run. |
| `feedback` | User Feedback widget. “Can you reproduce that?” — no. |
| `drains` | Logs/traces forwarded from Vercel / Cloudflare / Heroku. No SDK change. |

---

## Detect

| id | What |
| --- | --- |
| `issues` | Grouping, filter, assign, ignore, merge. |
| `issues.suspect_commits` | The commit that probably did it. |
| `issues.fingerprint` | How we glue events into one issue. |
| `snapshots` | Visual diffs on every PR. Unintended UI change. |
| `size_analysis` | Mobile build got fatter. CI check. Recommendations. |

---

## Debug

| id | What |
| --- | --- |
| `trace_explorer` | Search / filter / aggregate spans. |
| `replays` | Watch the session (see signals for web vs mobile). |
| `profiling` | Line-level CPU in prod. |
| `metrics.explore` | Spike → click through to traces. |

---

## Measure

| id | What |
| --- | --- |
| `dashboards` | Custom + pre-built (frontend / backend / mobile / AI). |
| `releases` | This deploy made crash-free drop. Adoption. Failure rate. |
| `stats` | Usage, quotas, what they’re actually sending. |
| `web_vitals` | The frontend is slow in the wild. |

---

## Seer — capabilities, not a sticker

| id | What they actually *do* |
| --- | --- |
| `seer.explain` | Why it failed, not just where. Root cause. |
| `seer.ask` | Plain language at the telemetry. “Why is checkout slow.” |
| `seer.issue_scan` | Will a code change even fix this. |
| `seer.autofix` | Draft the fix. |
| `seer.pr` | Open the PR / MR with that fix. |
| `seer.handoff.cursor` | Hand the context to Cursor. |
| `seer.handoff.copilot` | Same, Copilot. |
| `seer.handoff.claude` | Same, Claude. |
| `seer.review` | Review the PR against *production* errors/traces. Catch it before merge. |
| `seer.mcp` | From the editor: pull issues, traces, logs, trigger Seer. Don’t leave Cursor. |
| `seer.local` | Repro locally, telemetry hits Sentry, Seer looks at it before commit. |
| `seer.auto` | It just runs on issues it thinks it can fix. No click. |

Price Seer as a thing (`price seer`) and still ship/take the pieces (`take seer.auto`, `ship seer.review`).

---

## Watch and shout

| id | What |
| --- | --- |
| `alerts.email` | Mail. |
| `alerts.slack` | Slack. |
| `alerts.pagerduty` | PagerDuty. |
| `alerts.issue_tracker` | Jira / Linear / GitHub issues — *their* tracker, not ours. |
| `alerts.anomaly` | Anomaly detection. |
| `monitors.crons` | Cron monitors. |
| `monitors.uptime` | Uptime monitors. |
| `monitors.metrics` | Metric monitors. |
| `notifications` | Sentry notification settings. |
| `toolbar` | Sentry Toolbar on their own site. |

---

## Platform / plumbing

| id | What |
| --- | --- |
| `sdk.*` | The SDK they actually installed. Breaks live here. |
| `wizard` | `npx @sentry/wizard`. |
| `source_maps` | JS source maps. Missing = they hate us. |
| `debug_files` | Native / mobile symbols. |
| `dynamic_sampling` | We kept a sample, not everything. |
| `spike_protection` | We dropped the spike so the bill didn’t. |
| `quotas` | The cap. The email. The rage. |
| `spend_allocation` | Who on their team gets to burn the quota. |
| `relay` | Their Relay. Self-hosted / data control. |
| `build_distribution` | Ship mobile builds to testers. |
| `codecov` | Coverage. Sentry family. Stack traces that say “you never tested this.” |
| `mcp.sentry` | Sentry as an MCP *server* — agents talk to *us*. |
| `mcp.monitor` | We monitor *their* MCP servers. |
| `integrations.github` | Suspect commits, PRs, Seer apps. |
| `integrations.gitlab` | Same, GitLab. |
| `integrations.slack` | Alerts. |
| `integrations.linear` | |
| `integrations.jira` | |
| `self_hosted` | They run it. Different universe. |

---

## How a person holds this

Not `products: [seer]`. Split:

```yaml
using:
  signals: [errors, spans, logs]
  capabilities: [issues.suspect_commits, alerts.slack, seer.explain]
```

Growing = more ids on.  
**Ship** adds an id they didn’t have.  
**Take** removes one they did.  
**Price** changes what that id costs or which plan it lives on.  
**Break** is usually `sdk.*` or an API under one of these.  
**Ask / Tell** can be about any id.

A 23-year-old Next founder *trying*: `errors` only.  
A 55-year-old Rails boss *in*: `errors`, `spans`, `alerts.pagerduty`, `releases`.  
A corporate-India team *in*: `errors`, `spans`, `seer.mcp` in Cursor, never `replay.web` (PII fear).  
That’s three different lives. “They use Seer” would have lied.
