import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { normalizeEvent } from "../ingest/normalize.js";
import { buildCallIntent } from "./intent.js";
import { pickOptions } from "../policy/options.js";
import { toDecision } from "../map/toDecision.js";

const createAndWait = vi.fn();

vi.mock("@call-e/calle", () => ({
  CalleClient: class {
    calls = { createAndWait };
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
    createAndWait.mockReset();
  });

  it("sends Stage Manager payload and maps structured result", async () => {
    const event = normalizeEvent(fixture);
    const options = pickOptions(event.trigger_id);
    const intent = buildCallIntent(event, "+14155552671", options);

    createAndWait.mockResolvedValue({
      id: "call_mock_1",
      status: "completed",
      summary: null,
      taskCompleted: true,
      structuredResult: {
        option_id: "1",
        decision: "take_over_chat",
        decision_label: "Take over in chat now",
      },
      recipients: [
        {
          structuredResult: null,
          summary: null,
          attempts: [],
        },
      ],
    });

    const { call, structured } = await curtainUp(intent, {
      apiKey: "test_key_not_live",
      region: "US",
      locale: "en-US",
    });

    expect(createAndWait).toHaveBeenCalledTimes(1);
    const payload = createAndWait.mock.calls[0][0] as {
      task: string;
      recipients: Array<{ phones: string[] }>;
      resultSchema: unknown;
      metadata: Record<string, unknown>;
    };
    expect(payload.task).toMatch(/Stage Manager/);
    expect(payload.recipients[0].phones).toEqual(["+14155552671"]);
    expect(payload.metadata).toMatchObject({
      skill: "customer-success-voice-signal",
      persona: "Stage Manager",
      never_call_customer: true,
      trigger_id: "stuck_support",
    });
    expect(payload.resultSchema).toBeTruthy();
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
    expect(decision.decision).toBe("take_over_chat");
  });

  it("surfaces CALL-E API failures without hanging", async () => {
    const event = normalizeEvent(fixture);
    const intent = buildCallIntent(event, "+14155552671");
    createAndWait.mockRejectedValue(new Error("CALL-E 401 unauthorized"));

    await expect(
      curtainUp(intent, { apiKey: "bad_key" }),
    ).rejects.toThrow(/CALL-E 401/);
  });

  it("rejects missing API key before dialing", async () => {
    const event = normalizeEvent(fixture);
    const intent = buildCallIntent(event, "+14155552671");
    await expect(curtainUp(intent, { apiKey: "" })).rejects.toThrow(/CALLE_API_KEY/);
    expect(createAndWait).not.toHaveBeenCalled();
  });
});
