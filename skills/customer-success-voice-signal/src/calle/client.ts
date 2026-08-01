import { CalleClient, type Call } from "@call-e/calle";
import type { CallIntent } from "../schemas.js";

export interface CurtainUpConfig {
  apiKey: string;
  baseUrl?: string;
  region?: string;
  locale?: string;
}

export interface CurtainUpResult {
  call: Call;
  structured: Record<string, unknown> | null;
}

/**
 * Curtain-up: place a real CALL-E call via CalleClient.createAndWait.
 * Dress rehearsal must never invoke this.
 */
export async function curtainUp(
  intent: CallIntent,
  config: CurtainUpConfig,
): Promise<CurtainUpResult> {
  if (!config.apiKey) {
    throw new Error("CALLE_API_KEY is required for curtain-up.");
  }

  const client = new CalleClient({
    apiKey: config.apiKey,
    baseUrl: config.baseUrl,
  });

  const call = await client.calls.createAndWait({
    task: intent.task,
    recipients: [
      {
        phones: [intent.callee_e164],
        region: config.region ?? "US",
        locale: config.locale ?? "en-US",
      },
    ],
    resultSchema: intent.result_schema,
    metadata: {
      skill: "customer-success-voice-signal",
      persona: "Stage Manager",
      trigger_id: intent.trigger_id,
      account_id: intent.account_id,
      cs_owner_id: intent.cs_owner_id,
      never_call_customer: true,
      ...intent.metadata,
    },
  });

  const structured =
    (call.structuredResult as Record<string, unknown> | null) ??
    (call.recipients[0]?.structuredResult as Record<string, unknown> | null) ??
    null;

  return { call, structured };
}
