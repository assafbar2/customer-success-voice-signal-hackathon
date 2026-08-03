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
    .map((o) => `${o.option_id}: ${o.decision_label}`)
    .join("\n");

  const task = [
    `You are the Stage Manager. Warm, brief, headset energy — not corporate.`,
    `Call the Customer Success owner only. Never call the end customer.`,
    `Open: "Hi ${event.cs_owner.name}. Stage Manager. You're up for ${event.account.name}."`,
    `One short apology for the interrupt, then the cue sheet (no secret dumps, no internal ids):`,
    event.brief,
    `Plain summary: ${event.summary}`,
    event.ticket_id ? `Ticket: ${event.ticket_id}.` : null,
    `Then say: "Line reading. Say 1, 2, or 3 — or one, two, or three."`,
    `Speak ONLY these three options — do not invent options, do not read database field names like decision=…:`,
    lines,
    `If they say anything other than 1, 2, or 3, ask once more for 1, 2, or 3, then hang up if still unclear.`,
    `Confirm the choice in one sentence, say you're logging it to the prompt book, then: "Clear. Break a leg — or just open the ticket." Hang up.`,
    `Voicemail / automated unavailable: brief "Stage Manager will try again," hang up. Do not invent a line reading.`,
    `Fill structured result option_id ("1"|"2"|"3"), decision, and decision_label to match the chosen line only.`,
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
