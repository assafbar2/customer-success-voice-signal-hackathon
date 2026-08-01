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

/** Last clear 1/2/3 from user-ish transcript lines. */
function optionFromTranscript(
  texts: string[] | undefined,
  options: DecisionOption[],
): DecisionOption | null {
  if (!texts?.length) return null;
  const joined = texts.join(" \n ");
  // Prefer explicit lone digits / "option N" near the end
  const candidates = [...joined.matchAll(/\b(?:option\s*)?([123])\b/gi)].map(
    (m) => m[1],
  );
  const last = candidates[candidates.length - 1];
  if (!last) return null;
  return options.find((o) => o.option_id === last) ?? null;
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

  const matched =
    matchOption(
      options,
      input.structured,
      mode === "dress_rehearsal" ? (input.simulatedOptionId ?? "1") : undefined,
    ) ?? optionFromTranscript(input.transcriptTexts, options);

  if (!matched) {
    const vm = looksLikeVoicemailOrNoAnswer(input.callSummary);
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
