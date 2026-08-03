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
    // Ordinals last so "the second one" wins over the trailing word "one"
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
      // "second one" — ignore the trailing "one"/"two"/"three" after an ordinal
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

function matchOption(
  options: DecisionOption[],
  structured: Record<string, unknown> | null | undefined,
  fallbackId?: "1" | "2" | "3",
): DecisionOption | null {
  if (structured) {
    const optionId = String(structured.option_id ?? "");
    const byId = options.find((o) => o.option_id === optionId);
    if (byId) return byId;

    const decision = String(structured.decision ?? "");
    const byDecision = options.find((o) => o.decision === decision);
    if (byDecision) return byDecision;

    const label = String(structured.decision_label ?? "");
    const byLabel = options.find(
      (o) => o.decision_label.toLowerCase() === label.toLowerCase(),
    );
    if (byLabel) return byLabel;
  }

  if (fallbackId) {
    return options.find((o) => o.option_id === fallbackId) ?? null;
  }
  return null;
}

/**
 * Map CALL-E structured result (or dress-rehearsal preview) → DecisionResult.
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

  const fromStructured = matchOption(
    options,
    input.structured,
    mode === "dress_rehearsal" ? (input.simulatedOptionId ?? "1") : undefined,
  );

  const vm = looksLikeVoicemailOrNoAnswer(input.callSummary);
  const taskFailed = input.taskCompleted === false;

  // Incomplete task + voicemail/no-answer → never invent from stray digits
  if (!fromStructured && taskFailed && vm) {
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

  const matched =
    fromStructured ??
    (mode === "curtain_up" ? optionFromTranscript(input.transcriptTexts, options) : null);

  if (!matched) {
    const unclear =
      (input.callSummary ?? "").toLowerCase().includes("invalid") ||
      (input.callSummary ?? "").toLowerCase().includes("out-of-range") ||
      (input.callSummary ?? "").toLowerCase().includes("not confirmed");
    const noStructured =
      !input.structured || Object.keys(input.structured).length === 0;
    const decision = vm ? "no_answer" : "unclear";
    const decision_label = vm
      ? "No line reading — voicemail / no answer"
      : unclear
        ? "Unclear line reading — no valid 1/2/3"
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
          : noStructured
            ? "No structured result from CALL-E"
            : null,
      follow_up_at: null,
      completed_at: new Date().toISOString(),
      mode,
      hold_reason: null,
    });
  }

  const notes =
    input.structured && typeof input.structured.notes_short === "string"
      ? input.structured.notes_short
      : mode === "dress_rehearsal"
        ? "Dress rehearsal preview — no live ring."
        : null;

  return DecisionResultSchema.parse({
    trigger_id: event.trigger_id,
    account_id: event.account.id,
    account_name: event.account.name,
    cs_owner_id: event.cs_owner.id,
    call_run_id: input.callRunId ?? (mode === "dress_rehearsal" ? "dress_rehearsal" : null),
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
