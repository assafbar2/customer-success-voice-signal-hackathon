import type { AccountEvent, CsOwner } from "../schemas.js";

export type RingMode = "dress_rehearsal" | "curtain_up";

export type HoldReason =
  | "not_owned"
  | "opt_out"
  | "severity_below_threshold"
  | "house_dark"
  | "already_cued"
  | "placeholder_phone"
  | "live_gate_missing";

export interface ShouldRingInput {
  event: AccountEvent;
  owner: CsOwner;
  now?: Date;
  mode: RingMode;
  /** Curtain-up only: house dark from env (overrides owner quiet hours when set). */
  houseDark?: { start: string; end: string };
  recentCueKeys?: Set<string>;
  dedupeMinutes?: number;
}

export interface ShouldRingResult {
  ring: boolean;
  hold: boolean;
  reason?: HoldReason;
  note?: string;
}

const RING_SEVERITIES = new Set(["high", "critical"]);

/** Placeholder / demo numbers that must never receive a live ring. */
const PLACEHOLDER_PATTERNS = [
  /^\+1555555/,
  /^\+1555010/,
  /^\+1000000/,
  /55501\d{2}$/,
];

export function isPlaceholderPhone(e164: string): boolean {
  return PLACEHOLDER_PATTERNS.some((re) => re.test(e164));
}

export function requireLivePhone(e164: string): void {
  if (isPlaceholderPhone(e164)) {
    throw new Error(
      `HOLD: placeholder phone on the call sheet (${maskPhone(e164)}). Set CS_OWNER_E164 to a real E.164 before curtain-up.`,
    );
  }
  if (!/^\+[1-9]\d{7,14}$/.test(e164)) {
    throw new Error(`HOLD: invalid E.164 on the call sheet.`);
  }
}

export function maskPhone(e164: string): string {
  if (e164.length < 6) return "***";
  return `${e164.slice(0, 3)}***${e164.slice(-2)}`;
}

/**
 * House dark = quiet hours. Enforced only on curtain-up.
 * Dress rehearsal may run at night with a note.
 */
export function enforceHouseDark(
  now: Date,
  window: { start: string; end: string },
): boolean {
  const minutes = now.getHours() * 60 + now.getMinutes();
  const [sh, sm] = window.start.split(":").map(Number);
  const [eh, em] = window.end.split(":").map(Number);
  const start = sh * 60 + sm;
  const end = eh * 60 + em;

  if (start === end) return false;
  if (start < end) {
    return minutes >= start && minutes < end;
  }
  // Overnight window (e.g. 22:00 → 07:00)
  return minutes >= start || minutes < end;
}

export function cueDedupeKey(event: AccountEvent): string {
  return `${event.trigger_id}:${event.account.id}`;
}

/**
 * Policy gate before the Stage Manager cues CALL-E.
 */
export function shouldRing(input: ShouldRingInput): ShouldRingResult {
  const { event, owner, mode } = input;
  const now = input.now ?? new Date();

  if (!owner.opt_in_phone) {
    return { ring: false, hold: true, reason: "opt_out", note: "CS owner opted out of phone cues." };
  }

  if (!owner.id || owner.id !== event.cs_owner.id) {
    return { ring: false, hold: true, reason: "not_owned", note: "Account is not on this owner's call sheet." };
  }

  if (!RING_SEVERITIES.has(event.severity)) {
    return {
      ring: false,
      hold: true,
      reason: "severity_below_threshold",
      note: `Severity ${event.severity} is below the ring threshold (high|critical).`,
    };
  }

  const recent = input.recentCueKeys;
  if (recent?.has(cueDedupeKey(event))) {
    return {
      ring: false,
      hold: true,
      reason: "already_cued",
      note: "This cue was already rung recently (dedupe).",
    };
  }

  if (mode === "curtain_up") {
    if (isPlaceholderPhone(owner.e164)) {
      return {
        ring: false,
        hold: true,
        reason: "placeholder_phone",
        note: "Curtain-up refuses placeholder phones. Set CS_OWNER_E164.",
      };
    }

    const houseDark =
      input.houseDark ??
      (owner.quiet_hours
        ? { start: owner.quiet_hours.start, end: owner.quiet_hours.end }
        : undefined);

    if (houseDark && enforceHouseDark(now, houseDark)) {
      return {
        ring: false,
        hold: true,
        reason: "house_dark",
        note: `House dark (${houseDark.start}–${houseDark.end}). HOLD the live cue.`,
      };
    }
  } else {
    // Dress rehearsal: allow house-dark hours with a note
    const houseDark =
      input.houseDark ??
      (owner.quiet_hours
        ? { start: owner.quiet_hours.start, end: owner.quiet_hours.end }
        : undefined);
    if (houseDark && enforceHouseDark(now, houseDark)) {
      return {
        ring: true,
        hold: false,
        note: `Dress rehearsal during house dark (${houseDark.start}–${houseDark.end}) — no live ring.`,
      };
    }
  }

  return { ring: true, hold: false };
}
