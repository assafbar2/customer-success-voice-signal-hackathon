import { liveGateOpen, type SkillEnv } from "./config/env.js";
import { normalizeEvent } from "./ingest/normalize.js";
import { pickOptions } from "./policy/options.js";
import {
  cueDedupeKey,
  maskPhone,
  requireLivePhone,
  shouldRing,
  type RingMode,
} from "./policy/shouldRing.js";
import { buildCallIntent } from "./calle/intent.js";
import { curtainUp } from "./calle/client.js";
import { previewIntentSummary, toDecision } from "./map/toDecision.js";
import { loadRecentCueKeys, loadRecentOwnerRingCount, writeback } from "./writeback/index.js";
import type { AccountEvent, CallIntent, DecisionResult, CsOwner } from "./schemas.js";
import { CsOwnerSchema } from "./schemas.js";

export type ExitKind = "ok" | "hold" | "failure";

export interface RunSignalArgs {
  raw: unknown;
  env: SkillEnv;
  liveFlag: boolean;
  placesTyped: boolean;
  dryRunFlag: boolean;
  verbose?: boolean;
  log?: (msg: string) => void;
}

export interface RunSignalOutcome {
  exit: ExitKind;
  mode: RingMode;
  event: AccountEvent;
  intent: CallIntent | null;
  result: DecisionResult | null;
  message: string;
}

function resolveOwner(event: AccountEvent, env: SkillEnv, mode: RingMode): CsOwner {
  if (mode === "curtain_up" && env.csOwnerE164) {
    return CsOwnerSchema.parse({
      ...event.cs_owner,
      e164: env.csOwnerE164,
      name: env.csOwnerName || event.cs_owner.name,
      id: env.csOwnerId || event.cs_owner.id,
    });
  }
  return event.cs_owner;
}

function resolveMode(args: RunSignalArgs): RingMode {
  if (args.dryRunFlag) return "dress_rehearsal";
  if (liveGateOpen({ liveFlag: args.liveFlag, placesTyped: args.placesTyped, env: args.env })) {
    return "curtain_up";
  }
  return "dress_rehearsal";
}

/**
 * Stage Manager main cue path: normalize → policy → dress rehearsal | curtain-up → writeback.
 */
export async function runSignal(args: RunSignalArgs): Promise<RunSignalOutcome> {
  const log = args.log ?? (() => undefined);
  const mode = resolveMode(args);

  if (args.liveFlag && !args.dryRunFlag && mode === "dress_rehearsal") {
    let event: AccountEvent | null = null;
    try {
      event = normalizeEvent(args.raw);
    } catch {
      /* ignore — gate HOLD takes priority messaging */
    }
    return {
      exit: "hold",
      mode: "dress_rehearsal",
      event: event as AccountEvent,
      intent: null,
      result: null,
      message:
        "HOLD: --live requires type/env PLACES (set SIGNAL_CONFIRM=PLACES or pass PLACES). Staying in dress rehearsal.",
    };
  }

  let event: AccountEvent;
  try {
    event = normalizeEvent(args.raw);
  } catch (err) {
    return {
      exit: "failure",
      mode,
      event: {
        event_id: "invalid",
        trigger_id: "stuck_support",
        account: { id: "?", name: "?", tier: "standard", health_flags: [] },
        cs_owner: {
          id: "?",
          name: "?",
          e164: "+15555550100",
          opt_in_phone: false,
        },
        severity: "low",
        summary: "invalid",
        brief: "invalid",
        metadata: {},
      },
      intent: null,
      result: null,
      message: `Failure: could not normalize cue — ${err instanceof Error ? err.message : String(err)}`,
    };
  }

  const owner = resolveOwner(event, args.env, mode);
  const recent =
    mode === "curtain_up"
      ? await loadRecentCueKeys(args.env.dataDir, args.env.dedupeMinutes)
      : new Set<string>();
  const recentOwnerRings =
    mode === "curtain_up"
      ? await loadRecentOwnerRingCount(
          args.env.dataDir,
          owner.id,
          args.env.dedupeMinutes,
        )
      : 0;

  const policy = shouldRing({
    event: { ...event, cs_owner: owner },
    owner,
    mode,
    houseDark: {
      start: args.env.houseDarkStart,
      end: args.env.houseDarkEnd,
      timezone:
        args.env.houseDarkTimezone ||
        owner.quiet_hours?.timezone ||
        undefined,
    },
    recentCueKeys: recent,
    dedupeMinutes: args.env.dedupeMinutes,
    recentOwnerRingCount: recentOwnerRings,
    ownerMaxRings: args.env.ownerMaxRings,
  });

  const options = event.option_set ?? pickOptions(event.trigger_id);
  const intent = buildCallIntent({ ...event, cs_owner: owner }, owner.e164, options);
  const preview = previewIntentSummary(intent);

  if (args.verbose) {
    log(preview);
    if (policy.note) log(`Note: ${policy.note}`);
  }

  if (!policy.ring || policy.hold) {
    const result = toDecision({
      event,
      intent,
      options,
      mode,
      holdReason: policy.reason ?? "hold",
    });
    await writeback({
      dataDir: args.env.dataDir,
      mode,
      event,
      intent,
      result,
      preview,
      note: policy.note,
    });
    return {
      exit: "hold",
      mode,
      event,
      intent,
      result,
      message: `HOLD (${policy.reason}): ${policy.note ?? "cue withheld"}`,
    };
  }

  if (mode === "dress_rehearsal") {
    const result = toDecision({
      event,
      intent,
      options,
      mode,
      simulatedOptionId: "1",
    });
    const paths = await writeback({
      dataDir: args.env.dataDir,
      mode,
      event,
      intent,
      result,
      preview,
      note: policy.note ?? "Dress rehearsal — no ring, cue-history not appended.",
    });
    log(
      [
        "=== Dress rehearsal (no ring) ===",
        preview,
        "",
        `Simulated line reading: ${result.option_id} — ${result.decision_label}`,
        `Prompt book: ${paths.promptBook}`,
        `Show report: ${paths.showReport}`,
        policy.note ? `Note: ${policy.note}` : null,
        `Call sheet phone (masked): ${maskPhone(owner.e164)}`,
      ]
        .filter(Boolean)
        .join("\n"),
    );
    return {
      exit: "ok",
      mode,
      event,
      intent,
      result,
      message: "Dress rehearsal complete — house ready, no live ring.",
    };
  }

  // Curtain-up
  try {
    requireLivePhone(owner.e164);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    const result = toDecision({
      event,
      intent,
      options,
      mode,
      holdReason: "placeholder_phone",
    });
    await writeback({
      dataDir: args.env.dataDir,
      mode,
      event,
      intent,
      result,
      preview,
      note: msg,
    });
    return {
      exit: "hold",
      mode,
      event,
      intent,
      result,
      message: msg,
    };
  }

  if (!args.env.calleApiKey) {
    return {
      exit: "failure",
      mode,
      event,
      intent,
      result: null,
      message: "Failure: CALLE_API_KEY missing — cannot curtain-up.",
    };
  }

  log(`Curtain up — cueing CALL-E for ${maskPhone(owner.e164)} (CS owner only).`);
  try {
    const { call, structured } = await curtainUp(intent, {
      apiKey: args.env.calleApiKey,
      baseUrl: args.env.calleBaseUrl,
      region: args.env.calleRegion,
      locale: args.env.calleLocale,
      dataDir: args.env.dataDir,
      onStatus: (msg) => log(msg),
    });
    const result = toDecision({
      event,
      intent,
      options,
      mode,
      callRunId: call.id,
      structured,
      callSummary: call.summary ?? call.recipients[0]?.summary ?? null,
      taskCompleted: call.taskCompleted,
      transcriptTexts: call.recipients[0]?.attempts?.[0]?.transcriptTurns
        ?.filter((t) => t.speaker === "user")
        .map((t) => t.text ?? "")
        .filter(Boolean),
    });
    const paths = await writeback({
      dataDir: args.env.dataDir,
      mode,
      event,
      intent,
      result,
      preview,
      note: `Curtain-up complete. Dedupe key ${cueDedupeKey(event)}.`,
    });
    log(
      [
        "=== Curtain up ===",
        `Call run: ${call.id}`,
        `Status: ${call.status}`,
        `Decision: ${result.option_id} — ${result.decision_label}`,
        `Prompt book: ${paths.promptBook}`,
        `Show report: ${paths.showReport}`,
        paths.cueHistory ? `Cue history: ${paths.cueHistory}` : null,
      ]
        .filter(Boolean)
        .join("\n"),
    );
    return {
      exit: "ok",
      mode,
      event,
      intent,
      result,
      message: "Curtain-up complete — decision in the prompt book.",
    };
  } catch (err) {
    return {
      exit: "failure",
      mode,
      event,
      intent,
      result: null,
      message: `Failure during curtain-up: ${err instanceof Error ? err.message : String(err)}`,
    };
  }
}
