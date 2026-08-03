import { describe, expect, it } from "vitest";
import { CliParseError, parseArgs } from "./parseArgs.js";

describe("parseArgs", () => {
  it("parses fixture + live PLACES", () => {
    const a = parseArgs(["--fixture", "stuck.json", "--live", "PLACES"]);
    expect(a.fixture).toBe("stuck.json");
    expect(a.live).toBe(true);
    expect(a.places).toBe(true);
  });

  it("rejects unknown options", () => {
    expect(() => parseArgs(["--nope"])).toThrow(CliParseError);
  });

  it("rejects missing fixture value", () => {
    expect(() => parseArgs(["--fixture"])).toThrow(/Missing value/);
  });

  it("rejects --stdin with --fixture", () => {
    expect(() => parseArgs(["--stdin", "--fixture", "x.json"])).toThrow(/Conflicting/);
  });

  it("accepts --stdin alone", () => {
    expect(parseArgs(["--stdin"]).stdin).toBe(true);
  });
});
