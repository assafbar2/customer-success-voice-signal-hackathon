import type {
  AccountEvent,
  CallIntent,
  DecisionOption,
  DecisionResult,
} from "../schemas.js";
import { DecisionResultSchema } from "../schemas.js";
import type { RingMode } from "../policy/shouldRing.js";

export interface ToDecisionInput {
  event: AccountEvent;
  intent: CallIntent;
  options: DecisionOption[];
  mode: RingMode;
  callRunId?: string | null;
  structured?: Record<string, unknown> | null;
  holdReason?: string | null;
  /** CALL-E call/recipient summary when structured result is missing */
  callSummary?: string | null;
  taskCompleted?: boolean | null;
  /** Transcript turns for fallback option parsing */
  transcriptTexts?: string[];
  /** Dress rehearsal may simulate a choice (default option 1). */
  simulatedOptionId?: "1" | "2" | "3";
  /** Provider failure audit (never a human decision). */
  failure?: { category: string; summary: string } | null;
}

const WORD_TO_OPTION: Record<string, "1" | "2" | "3"> = {
  "1": "1",
  one: "1",
  first: "1",
  "2": "2",
  two: "2",
  second: "2",
  "3": "3",
  three: "3",
  third: "3",
};

function looksLikeVoicemailOrNoAnswer(summary: string | null | undefined): boolean {
  if (!summary) return false;
  const s = summary.toLowerCase();
  return (
    s.includes("voicemail") ||
    s.includes("not available") ||
    s.includes("no answer") ||
    s.includes("didn't answer") ||
    s.includes("did not answer") ||
    s.includes("unreachable") ||
    s.includes("did not connect") ||
    s.includes("didn't connect") ||
    s.includes("no transcript") ||
    s.includes("busy or unavailable") ||
    s.includes("may be busy")
  );
}

/** True when a bare digit/word is clearly not a line reading (e.g. "3 other fires"). */
function isSpuriousDigitContext(text: string, index: number, matched: string): boolean {
  const token = matched.trim();
  const after = text.slice(index + matched.length, index + matched.length + 32).toLowerCase();
  if (
    /^\s*(other|others|more|fires|tickets|accounts|people|things|hours|minutes|days|weeks|calls|options?)\b/.test(
      after,
    )
  ) {
    return true;
  }
  const before = text.slice(Math.max(0, index - 24), index).toLowerCase();
  if (
    /\b(have|had|got|with|and|plus|another)\s*$/.test(before) &&
    (/^\d$/.test(token) || /^(one|two|three)$/i.test(token))
  ) {
    return true;
  }
  return false;
}

/**
 * Gated transcript → option. Prefer explicit "option N" / word forms.
 * Rejects embedded counts like "3 other fires". Takes the last *confident* hit.
 */
export function optionFromTranscript(
  texts: string[] | undefined,
  options: DecisionOption[],
): DecisionOption | null {
  if (!texts?.length) return null;
  const joined = texts.join(" \n ");

  const patterns: RegExp[] = [
    /\boption\s*([123])\b/gi,
    /\b(?:uh+[,.]?\s*)?(one|two|three)\b/gi,
    /\b([123])\s*(?:please|thanks|thank you)?\b/gi,
    /\b(?:the\s+)?(first|second|third)(?:\s+one)?\b/gi,
  ];

  let lastId: "1" | "2" | "3" | null = null;
  for (const re of patterns) {
    re.lastIndex = 0;
    let m: RegExpExecArray | null;
    while ((m = re.exec(joined)) !== null) {
      const raw = m[1].toLowerCase();
      const id = WORD_TO_OPTION[raw];
      if (!id) continue;
      const captureOffset = Math.max(0, m[0].toLowerCase().lastIndexOf(raw));
      const tokenIndex = m.index + captureOffset;
      if (isSpuriousDigitContext(joined, tokenIndex, raw)) continue;
      if (/^(one|two|three)$/.test(raw)) {
        const before = joined.slice(Math.max(0, tokenIndex - 14), tokenIndex).toLowerCase();
        if (/\b(first|second|third)\s+$/.test(before)) continue;
      }
      lastId = id;
    }
  }

  if (!lastId) return null;
  return options.find((o) => o.option_id === lastId) ?? null;
}

type StructuredParse =
  | { kind: "ok"; option: DecisionOption }
  | { kind: "contradiction" }
  | { kind: "none" };

/**
 * Prefer option_id. If decision/label disagree with that option → contradiction (unclear).
 */
export function parseStructuredOption(
  options: DecisionOption[],
  structured: Record<string, unknown> | null | undefined,
): StructuredParse {
  if (!structured || Object.keys(structured).length === 0) return { kind: "none" };

  const optionId = String(structured.option_id ?? "");
  const byId = options.find((o) => o.option_id === optionId);
  if (!byId) {
    // No usable option_id — do not silently trust mismatched decision/label alone for live
    return { kind: "none" };
  }

  const decision =
    structured.decision !== undefined && structured.decision !== null
      ? String(structured.decision)
      : null;
  const label =
    structured.decision_label !== undefined && structured.decision_label !== null
      ? String(structured.decision_label)
      : null;

  if (decision && decision !== byId.decision) return { kind: "contradiction" };
  if (label && label.toLowerCase() !== byId.decision_label.toLowerCase()) {
    return { kind: "contradiction" };
  }
  return { kind: "ok", option: byId };
}

function unclearResult(
  input: ToDecisionInput,
  label: string,
  notes: string | null,
): DecisionResult {
  const { event, mode } = input;
  return DecisionResultSchema.parse({
    trigger_id: event.trigger_id,
    account_id: event.account.id,
    account_name: event.account.name,
    cs_owner_id: event.cs_owner.id,
    call_run_id: input.callRunId ?? null,
    decision: "unclear",
    decision_label: label,
    option_id: "unknown",
    notes_short: notes,
    follow_up_at: null,
    completed_at: new Date().toISOString(),
    mode,
    hold_reason: null,
  });
}

/**
 * Map CALL-E structured result (or dress-rehearsal preview) → DecisionResult.
 *
 * Rules:
 * - taskCompleted === true + consistent structured → accept
 * - taskCompleted === false → never a normal 1/2/3 (voicemail→no_answer, else unclear)
 * - contradictory structured fields → unclear
 * - dress rehearsal may simulate option 1
 */
export function toDecision(input: ToDecisionInput): DecisionResult {
  const { event, options, mode } = input;

  if (input.holdReason) {
    return DecisionResultSchema.parse({
      trigger_id: event.trigger_id,
      account_id: event.account.id,
      account_name: event.account.name,
      cs_owner_id: event.cs_owner.id,
      call_run_id: null,
      decision: "hold",
      decision_label: "HOLD",
      option_id: "hold",
      notes_short: input.holdReason,
      follow_up_at: null,
      completed_at: new Date().toISOString(),
      mode,
      hold_reason: input.holdReason,
    });
  }

  if (input.failure) {
    return DecisionResultSchema.parse({
      trigger_id: event.trigger_id,
      account_id: event.account.id,
      account_name: event.account.name,
      cs_owner_id: event.cs_owner.id,
      call_run_id: input.callRunId ?? null,
      decision: "failure",
      decision_label: `CALL-E failure (${input.failure.category})`,
      option_id: "unknown",
      notes_short: input.failure.summary,
      follow_up_at: null,
      completed_at: new Date().toISOString(),
      mode,
      hold_reason: null,
    });
  }

  const vm = looksLikeVoicemailOrNoAnswer(input.callSummary);
  const taskFailed = input.taskCompleted === false;
  const taskOk = input.taskCompleted === true;

  if (mode === "dress_rehearsal") {
    const sim =
      options.find((o) => o.option_id === (input.simulatedOptionId ?? "1")) ?? options[0];
    return DecisionResultSchema.parse({
      trigger_id: event.trigger_id,
      account_id: event.account.id,
      account_name: event.account.name,
      cs_owner_id: event.cs_owner.id,
      call_run_id: "dress_rehearsal",
      decision: sim.decision,
      decision_label: sim.decision_label,
      option_id: sim.option_id,
      notes_short: "Dress rehearsal preview — no live ring.",
      follow_up_at: null,
      completed_at: new Date().toISOString(),
      mode,
      hold_reason: null,
    });
  }

  // Incomplete task: never claim a human chose 1/2/3
  if (taskFailed) {
    if (vm) {
      return DecisionResultSchema.parse({
        trigger_id: event.trigger_id,
        account_id: event.account.id,
        account_name: event.account.name,
        cs_owner_id: event.cs_owner.id,
        call_run_id: input.callRunId ?? null,
        decision: "no_answer",
        decision_label: "No line reading — voicemail / no answer",
        option_id: "unknown",
        notes_short: input.callSummary ? input.callSummary.slice(0, 280) : null,
        follow_up_at: null,
        completed_at: new Date().toISOString(),
        mode,
        hold_reason: null,
      });
    }
    return unclearResult(
      input,
      "Unclear — task not completed",
      input.callSummary
        ? input.callSummary.slice(0, 280)
        : "taskCompleted=false; refusing to record a line reading",
    );
  }

  const parsed = parseStructuredOption(options, input.structured);
  if (parsed.kind === "contradiction") {
    return unclearResult(
      input,
      "Unclear — contradictory structured result",
      input.structured ? JSON.stringify(input.structured).slice(0, 200) : null,
    );
  }

  let matched: DecisionOption | null =
    parsed.kind === "ok" ? parsed.option : null;

  // Prefer structured when taskCompleted is true or unknown; transcript only as fallback
  if (!matched && (taskOk || input.taskCompleted == null)) {
    matched = optionFromTranscript(input.transcriptTexts, options);
  }

  if (!matched) {
    const decision = vm ? "no_answer" : "unclear";
    const decision_label = vm
      ? "No line reading — voicemail / no answer"
      : "Could not map line reading";
    return DecisionResultSchema.parse({
      trigger_id: event.trigger_id,
      account_id: event.account.id,
      account_name: event.account.name,
      cs_owner_id: event.cs_owner.id,
      call_run_id: input.callRunId ?? null,
      decision,
      decision_label,
      option_id: "unknown",
      notes_short: input.callSummary
        ? input.callSummary.slice(0, 280)
        : input.structured
          ? JSON.stringify(input.structured).slice(0, 200)
          : "No structured result from CALL-E",
      follow_up_at: null,
      completed_at: new Date().toISOString(),
      mode,
      hold_reason: null,
    });
  }

  // taskCompleted must be true to accept a normal decision when SDK provided the flag
  if (input.taskCompleted === true || input.taskCompleted == null) {
    const notes =
      input.structured && typeof input.structured.notes_short === "string"
        ? input.structured.notes_short
        : null;
    return DecisionResultSchema.parse({
      trigger_id: event.trigger_id,
      account_id: event.account.id,
      account_name: event.account.name,
      cs_owner_id: event.cs_owner.id,
      call_run_id: input.callRunId ?? null,
      decision: matched.decision,
      decision_label: matched.decision_label,
      option_id: matched.option_id,
      notes_short: notes,
      follow_up_at: null,
      completed_at: new Date().toISOString(),
      mode,
      hold_reason: null,
    });
  }

  return unclearResult(input, "Unclear line reading — no valid 1/2/3", null);
}

export function previewIntentSummary(intent: CallIntent): string {
  const lines = intent.options
    .map((o) => `  ${o.option_id}. ${o.decision_label}`)
    .join("\n");
  return [
    `Persona: ${intent.persona}`,
    `Cue: ${intent.trigger_id}`,
    `Account: ${intent.account_name} (${intent.account_id})`,
    `Call sheet: ${intent.cs_owner_name} (CS only — never customer)`,
    `Line readings:`,
    lines,
  ].join("\n");
}
