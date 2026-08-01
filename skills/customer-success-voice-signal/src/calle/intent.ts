import type { AccountEvent, CallIntent, DecisionOption } from "../schemas.js";
import { CallIntentSchema } from "../schemas.js";
import { pickOptions } from "../policy/options.js";

const RESULT_SCHEMA = {
  type: "object",
  required: ["option_id", "decision", "decision_label"],
  properties: {
    option_id: {
      type: "string",
      enum: ["1", "2", "3"],
      description: "The closed-set choice the CS owner selected (1, 2, or 3).",
    },
    decision: {
      type: "string",
      description: "Stable decision id matching the chosen option.",
    },
    decision_label: {
      type: "string",
      description: "Human-readable label of the chosen option.",
    },
    notes_short: {
      type: "string",
      description: "Optional short note from the CS owner.",
    },
  },
} as const;

/**
 * Build a CALL-E task as the Stage Manager.
 * Never instructs a call to the customer — CS owner only.
 */
export function buildCallIntent(
  event: AccountEvent,
  calleeE164: string,
  options?: DecisionOption[],
): CallIntent {
  const opts = options ?? event.option_set ?? pickOptions(event.trigger_id);
  if (opts.length !== 3) {
    throw new Error("Stage Manager requires exactly 3 closed-set line readings (1/2/3).");
  }

  const lines = opts
    .map((o) => `Option ${o.option_id}: ${o.decision_label} (decision=${o.decision})`)
    .join("\n");

  const task = [
    `You are the Stage Manager for customer-success-voice-signal.`,
    `This is a cue for the Customer Success owner only — never call the customer.`,
    `Call ${event.cs_owner.name} at the provided recipient number.`,
    `Identify yourself as Stage Manager for account ${event.account.name}.`,
    `Cue type: ${event.trigger_id}.`,
    `Give this brief (3–5 sentences, no secrets dump): ${event.brief}`,
    `Summary line: ${event.summary}`,
    event.ticket_id ? `Ticket reference: ${event.ticket_id}.` : null,
    `Ask for one decision. Present exactly these closed-set line readings:`,
    lines,
    `Have them press or say 1, 2, or 3. Confirm the choice, then hang up.`,
    `Return structured result with option_id, decision, and decision_label matching the chosen line.`,
  ]
    .filter(Boolean)
    .join("\n");

  return CallIntentSchema.parse({
    persona: "Stage Manager",
    trigger_id: event.trigger_id,
    account_id: event.account.id,
    account_name: event.account.name,
    cs_owner_id: event.cs_owner.id,
    cs_owner_name: event.cs_owner.name,
    callee_e164: calleeE164,
    task,
    options: opts,
    result_schema: RESULT_SCHEMA,
    never_call_customer: true,
    metadata: {
      event_id: event.event_id,
      ticket_id: event.ticket_id ?? null,
      severity: event.severity,
    },
  });
}

export { RESULT_SCHEMA };
