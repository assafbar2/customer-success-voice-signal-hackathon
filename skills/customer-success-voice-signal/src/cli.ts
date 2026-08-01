#!/usr/bin/env node
import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import { loadDotEnv, readSkillEnv, SKILL_ROOT } from "./config/env.js";
import { runSignal } from "./runSignal.js";
import { resolveWritebackPaths } from "./writeback/index.js";

const EXIT_OK = 0;
const EXIT_HOLD = 2;
const EXIT_FAILURE = 3;

interface CliArgs {
  fixture?: string;
  trigger?: string;
  live: boolean;
  dryRun: boolean;
  places: boolean;
  list: boolean;
  last: boolean;
  verbose: boolean;
  help: boolean;
}

function printHelp(): void {
  console.log(`
Stage Manager — customer-success-voice-signal

Usage:
  npm run signal -- [options]
  npm run dry-run -- --fixture <file>

Options:
  --fixture <file>   Cue fixture under fixtures/ (e.g. stuck_support_acme.json)
  --trigger <id>     Filter/list by trigger_id
  --live             Request curtain-up (requires type/env PLACES)
  --dry-run          Force dress rehearsal (default)
  PLACES             Confirm live gate when used with --live
  --list             List fixtures on the call sheet
  --last             Show last prompt-book / show-report entries
  --verbose          Print full call sheet preview
  --help             This cue sheet

Exit codes:
  0  ok (dress rehearsal or curtain-up)
  2  HOLD (policy / live gate / house dark)
  3  failure

Modes:
  Dress rehearsal  Default. No ring. Does not append cue-history.
  Curtain up       --live AND PLACES (env SIGNAL_CONFIRM=PLACES or argv PLACES).
`);
}

function parseArgs(argv: string[]): CliArgs {
  const args: CliArgs = {
    live: false,
    dryRun: false,
    places: false,
    list: false,
    last: false,
    verbose: false,
    help: false,
  };

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--help" || a === "-h") args.help = true;
    else if (a === "--live") args.live = true;
    else if (a === "--dry-run") args.dryRun = true;
    else if (a === "--list") args.list = true;
    else if (a === "--last") args.last = true;
    else if (a === "--verbose" || a === "-v") args.verbose = true;
    else if (a === "PLACES" || a === "--places") args.places = true;
    else if (a === "--fixture" || a === "-f") {
      args.fixture = argv[++i];
    } else if (a.startsWith("--fixture=")) {
      args.fixture = a.slice("--fixture=".length);
    } else if (a === "--trigger" || a === "-t") {
      args.trigger = argv[++i];
    } else if (a.startsWith("--trigger=")) {
      args.trigger = a.slice("--trigger=".length);
    } else if (a.endsWith(".json") && !args.fixture) {
      args.fixture = a;
    }
  }
  return args;
}

async function listFixtures(trigger?: string): Promise<void> {
  const dir = path.join(SKILL_ROOT, "fixtures");
  const files = (await readdir(dir)).filter((f) => f.endsWith(".json")).sort();
  console.log("Call sheet — fixtures:");
  for (const f of files) {
    const raw = JSON.parse(await readFile(path.join(dir, f), "utf8")) as {
      fixture_id?: string;
      trigger_id?: string;
      account?: { name?: string };
    };
    if (trigger && raw.trigger_id !== trigger) continue;
    console.log(
      `  ${f}  cue=${raw.trigger_id ?? "?"}  account=${raw.account?.name ?? "?"}  id=${raw.fixture_id ?? "?"}`,
    );
  }
}

async function showLast(dataDir: string): Promise<void> {
  const paths = resolveWritebackPaths(dataDir);
  try {
    const book = await readFile(paths.promptBook, "utf8");
    const lines = book.trim().split("\n").filter(Boolean);
    const last = lines[lines.length - 1];
    console.log("Last prompt-book entry:");
    console.log(last ?? "(empty)");
  } catch {
    console.log("Prompt book empty — no cues yet.");
  }
  try {
    const report = await readFile(paths.showReport, "utf8");
    console.log("\nShow report (head):");
    console.log(report.split("\n").slice(0, 24).join("\n"));
  } catch {
    console.log("Show report not written yet.");
  }
}

async function loadFixture(name: string): Promise<unknown> {
  const file = name.endsWith(".json") ? name : `${name}.json`;
  const full = path.isAbsolute(file)
    ? file
    : path.join(SKILL_ROOT, "fixtures", file);
  const text = await readFile(full, "utf8");
  return JSON.parse(text);
}

async function main(): Promise<void> {
  loadDotEnv();
  const env = readSkillEnv();
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    printHelp();
    process.exit(EXIT_OK);
  }

  if (args.list) {
    await listFixtures(args.trigger);
    process.exit(EXIT_OK);
  }

  if (args.last) {
    await showLast(env.dataDir);
    process.exit(EXIT_OK);
  }

  if (!args.fixture) {
    // If --trigger only, pick first matching fixture
    if (args.trigger) {
      const dir = path.join(SKILL_ROOT, "fixtures");
      const files = (await readdir(dir)).filter((f) => f.endsWith(".json"));
      for (const f of files) {
        const raw = JSON.parse(await readFile(path.join(dir, f), "utf8")) as {
          trigger_id?: string;
        };
        if (raw.trigger_id === args.trigger) {
          args.fixture = f;
          break;
        }
      }
    }
  }

  if (!args.fixture) {
    console.error("Stage Manager needs a cue. Pass --fixture <file> or --list.");
    printHelp();
    process.exit(EXIT_FAILURE);
  }

  let raw: unknown;
  try {
    raw = await loadFixture(args.fixture);
  } catch (err) {
    console.error(
      `Failure: cannot read fixture — ${err instanceof Error ? err.message : String(err)}`,
    );
    process.exit(EXIT_FAILURE);
  }

  const outcome = await runSignal({
    raw,
    env,
    liveFlag: args.live,
    placesTyped: args.places,
    dryRunFlag: args.dryRun,
    verbose: args.verbose,
    log: (msg) => console.log(msg),
  });

  console.log(outcome.message);

  if (outcome.exit === "ok") process.exit(EXIT_OK);
  if (outcome.exit === "hold") process.exit(EXIT_HOLD);
  process.exit(EXIT_FAILURE);
}

main().catch((err) => {
  console.error(`Failure: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(EXIT_FAILURE);
});
