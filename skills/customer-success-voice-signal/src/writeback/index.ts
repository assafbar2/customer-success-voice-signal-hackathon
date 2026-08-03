import { appendFile, mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import type { CallIntent, DecisionResult } from "../schemas.js";
import type { RingMode } from "../policy/shouldRing.js";
import { cueDedupeKey } from "../policy/shouldRing.js";
import type { AccountEvent } from "../schemas.js";

export interface WritebackPaths {
  dataDir: string;
  promptBook: string;
  showReport: string;
  cueHistory: string;
}

export function resolveWritebackPaths(dataDir: string): WritebackPaths {
  return {
    dataDir,
    promptBook: path.join(dataDir, "prompt-book.ndjson"),
    showReport: path.join(dataDir, "show-report.md"),
    cueHistory: path.join(dataDir, "cue-history.ndjson"),
  };
}

async function ensureDataDir(dataDir: string): Promise<void> {
  await mkdir(dataDir, { recursive: true });
}

/** Append one prompt-book line (always — dress rehearsal and curtain-up). */
export async function appendPromptBook(
  dataDir: string,
  entry: {
    at: string;
    mode: RingMode;
    intent: CallIntent;
    result: DecisionResult;
  },
): Promise<string> {
  const paths = resolveWritebackPaths(dataDir);
  await ensureDataDir(dataDir);
  const line = JSON.stringify({
    at: entry.at,
    mode: entry.mode,
    trigger_id: entry.intent.trigger_id,
    account_id: entry.intent.account_id,
    account_name: entry.intent.account_name,
    cs_owner_id: entry.intent.cs_owner_id,
    persona: entry.intent.persona,
    decision: entry.result.decision,
    decision_label: entry.result.decision_label,
    option_id: entry.result.option_id,
    call_run_id: entry.result.call_run_id,
    hold_reason: entry.result.hold_reason ?? null,
  });
  await appendFile(paths.promptBook, `${line}\n`, "utf8");
  return paths.promptBook;
}

/** Rewrite show report markdown with latest cue outcome. */
export async function writeShowReport(
  dataDir: string,
  result: DecisionResult,
  extras?: { preview?: string; note?: string },
): Promise<string> {
  const paths = resolveWritebackPaths(dataDir);
  await ensureDataDir(dataDir);

  const prior = await readFile(paths.showReport, "utf8").catch(() => "");
  const block = [
    `## Cue — ${result.completed_at}`,
    "",
    `| Field | Value |`,
    `| --- | --- |`,
    `| Mode | ${result.mode === "curtain_up" ? "Curtain up" : "Dress rehearsal"} |`,
    `| Trigger | \`${result.trigger_id}\` |`,
    `| Account | ${result.account_name} (\`${result.account_id}\`) |`,
    `| CS owner | \`${result.cs_owner_id}\` |`,
    `| Option | ${result.option_id} |`,
    `| Decision | ${result.decision_label} (\`${result.decision}\`) |`,
    `| Call run | ${result.call_run_id ?? "—"} |`,
    `| HOLD | ${result.hold_reason ?? "—"} |`,
    "",
    extras?.preview ? `### Call sheet preview\n\n\`\`\`\n${extras.preview}\n\`\`\`\n` : "",
    extras?.note ? `> ${extras.note}\n` : "",
    "---",
    "",
  ].join("\n");

  const header =
    prior.trim().length > 0
      ? ""
      : `# Show report — customer-success-voice-signal\n\nStage Manager cue log. Newest entries are prepended.\n\n`;

  await writeFile(paths.showReport, header + block + prior, "utf8");
  return paths.showReport;
}

/**
 * Append cue-history for dedupe.
 * Dress rehearsal does NOT append (so demos re-run).
 * Curtain-up HOLDs (live gate, house dark, placeholder, etc.) must NOT append —
 * only dial attempts / completed live cues poison the dedupe key.
 */
export async function appendCueHistory(
  dataDir: string,
  event: AccountEvent,
  mode: RingMode,
  opts?: { recordDedupe?: boolean },
): Promise<string | null> {
  if (mode !== "curtain_up") return null;
  if (opts?.recordDedupe === false) return null;
  const paths = resolveWritebackPaths(dataDir);
  await ensureDataDir(dataDir);
  const line = JSON.stringify({
    at: new Date().toISOString(),
    key: cueDedupeKey(event),
    trigger_id: event.trigger_id,
    account_id: event.account.id,
    event_id: event.event_id,
  });
  await appendFile(paths.cueHistory, `${line}\n`, "utf8");
  return paths.cueHistory;
}

export async function loadRecentCueKeys(
  dataDir: string,
  dedupeMinutes: number,
  now = new Date(),
): Promise<Set<string>> {
  const paths = resolveWritebackPaths(dataDir);
  const raw = await readFile(paths.cueHistory, "utf8").catch(() => "");
  const keys = new Set<string>();
  const cutoff = now.getTime() - dedupeMinutes * 60_000;
  for (const line of raw.split("\n")) {
    if (!line.trim()) continue;
    try {
      const row = JSON.parse(line) as { at?: string; key?: string };
      if (!row.at || !row.key) continue;
      if (new Date(row.at).getTime() >= cutoff) keys.add(row.key);
    } catch {
      // skip bad lines
    }
  }
  return keys;
}

export async function writeback(args: {
  dataDir: string;
  mode: RingMode;
  event: AccountEvent;
  intent: CallIntent;
  result: DecisionResult;
  preview?: string;
  note?: string;
}): Promise<{ promptBook: string; showReport: string; cueHistory: string | null }> {
  const at = new Date().toISOString();
  const promptBook = await appendPromptBook(args.dataDir, {
    at,
    mode: args.mode,
    intent: args.intent,
    result: args.result,
  });
  const showReport = await writeShowReport(args.dataDir, args.result, {
    preview: args.preview,
    note: args.note,
  });
  // HOLD must not poison dedupe — only live dial outcomes record the cue key.
  const recordDedupe =
    args.result.option_id !== "hold" && args.result.decision !== "hold";
  const cueHistory = await appendCueHistory(args.dataDir, args.event, args.mode, {
    recordDedupe,
  });
  return { promptBook, showReport, cueHistory };
}
