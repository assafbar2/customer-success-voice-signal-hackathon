import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { normalizeEvent } from "../ingest/normalize.js";
import { buildCallIntent } from "./intent.js";
import { pickOptions } from "../policy/options.js";
import { toDecision } from "../map/toDecision.js";

const create = vi.fn();
const waitForResult = vi.fn();
const listEvents = vi.fn();

vi.mock("@call-e/calle", () => ({
  CalleClient: class {
    calls = { create, waitForResult, listEvents };
    constructor(_opts: { apiKey: string; baseUrl?: string }) {
      void _opts;
    }
  },
}));

const { curtainUp } = await import("./client.js");

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const fixture = JSON.parse(
  readFileSync(path.join(root, "fixtures/stuck_support_acme.json"), "utf8"),
);

describe("curtainUp — mocked CALL-E", () => {
  beforeEach(() => {
    create.mockReset();
    waitForResult.mockReset();
    listEvents.mockReset();
    listEvents.mockResolvedValue({ object: "list", data: [], nextCursor: null });
  });

  it("create → persist path → waitForResult with idempotency", async () => {
    const event = normalizeEvent(fixture);
    const options = pickOptions(event.trigger_id);
    const intent = buildCallIntent(event, "+14155552671", options);

    create.mockResolvedValue({
      id: "call_mock_1",
      status: "queued",
      summary: null,
      taskCompleted: null,
      structuredResult: null,
      recipients: [],
    });
    waitForResult.mockResolvedValue({
      id: "call_mock_1",
      status: "completed",
      summary: null,
      taskCompleted: true,
      structuredResult: {
        option_id: "1",
        decision: "take_over_chat",
        decision_label: "Take over in chat now",
      },
      recipients: [{ structuredResult: null, summary: null, attempts: [] }],
    });

    const { call, structured } = await curtainUp(intent, {
      apiKey: "test_key_not_live",
      region: "US",
      locale: "en-US",
    });

    expect(create).toHaveBeenCalledTimes(1);
    expect(waitForResult).toHaveBeenCalledWith(
      "call_mock_1",
      expect.objectContaining({ timeoutMs: 600_000 }),
    );
    const [payload, opts] = create.mock.calls[0] as [
      { task: string; recipients: Array<{ phones: string[] }>; metadata: Record<string, unknown> },
      { idempotencyKey: string },
    ];
    expect(payload.task).toMatch(/Stage Manager/);
    expect(payload.task).toMatch(/Say 1, 2, or 3/);
    expect(payload.task).not.toMatch(/Press/);
    expect(payload.recipients[0].phones).toEqual(["+14155552671"]);
    expect(payload.metadata).toMatchObject({
      skill: "customer-success-voice-signal",
      never_call_customer: true,
    });
    expect(opts.idempotencyKey).toMatch(/^csvs:stuck_support:acct_acme:/);
    expect(call.id).toBe("call_mock_1");
    expect(structured?.option_id).toBe("1");

    const decision = toDecision({
      event,
      intent,
      options,
      mode: "curtain_up",
      callRunId: call.id,
      structured,
    });
    expect(decision.option_id).toBe("1");
  });

  it("surfaces wait failures with persisted call id in the message", async () => {
    const event = normalizeEvent(fixture);
    const intent = buildCallIntent(event, "+14155552671");
    create.mockResolvedValue({
      id: "call_open_99",
      status: "queued",
      recipients: [],
      structuredResult: null,
      summary: null,
      taskCompleted: null,
    });
    waitForResult.mockRejectedValue(new Error("timeout"));

    await expect(curtainUp(intent, { apiKey: "test_key" })).rejects.toThrow(
      /call_open_99/,
    );
  });

  it("rejects missing API key before dialing", async () => {
    const event = normalizeEvent(fixture);
    const intent = buildCallIntent(event, "+14155552671");
    await expect(curtainUp(intent, { apiKey: "" })).rejects.toThrow(/CALLE_API_KEY/);
    expect(create).not.toHaveBeenCalled();
  });
});
