#!/usr/bin/env node
/**
 * Apply (or dry-run) the latest pending action intent.
 * POC: local receipt only — does not call Zendesk / Salesforce / Slack.
 */
import { loadDotEnv, readSkillEnv } from "./config/env.js";
import {
  applyActionIntent,
  loadLastPendingIntent,
  loadPendingIntentById,
} from "./action/store.js";

function printHelp(): void {
  console.log(`
Stage Manager — apply-action
Turn a closed-set CS decision into a system handoff (POC).

Usage:
  npm run apply-action -- --last --dry-run
  npm run apply-action -- --last
  npm run apply-action -- --id <intent_id> --dry-run

Flags:
  --last       Use most recent pending action intent
  --id <id>    Use a specific pending intent_id
  --dry-run    Print/record what would be sent — no "executed_local"
  --help

Seam:
  Decision → data/actions/pending/*.json → apply-action → data/actions/executed/*
  Adapters planned: zendesk_ticket_note · salesforce_task · slack_webhook · internal_queue
  This POC never calls those systems — it proves the contract.
`);
}

function parse(argv: string[]): {
  last: boolean;
  id?: string;
  dryRun: boolean;
  help: boolean;
} {
  const out = { last: false, dryRun: false, help: false, id: undefined as string | undefined };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--help" || a === "-h") out.help = true;
    else if (a === "--last") out.last = true;
    else if (a === "--dry-run") out.dryRun = true;
    else if (a === "--id") {
      const v = argv[++i];
      if (!v) throw new Error("Missing value for --id");
      out.id = v;
    } else if (a.startsWith("--id=")) out.id = a.slice(5);
    else throw new Error(`Unknown option: ${a}`);
  }
  return out;
}

async function main(): Promise<void> {
  loadDotEnv();
  const env = readSkillEnv();
  let args;
  try {
    args = parse(process.argv.slice(2));
  } catch (err) {
    console.error(`Failure: ${err instanceof Error ? err.message : String(err)}`);
    printHelp();
    process.exit(3);
  }

  if (args.help || (!args.last && !args.id)) {
    printHelp();
    process.exit(args.help ? 0 : 3);
  }

  const loaded = args.id
    ? await loadPendingIntentById(env.dataDir, args.id)
    : await loadLastPendingIntent(env.dataDir);

  if (!loaded) {
    console.error(
      "Failure: no pending action intent. Run a dress rehearsal or curtain-up that yields option 1/2/3 first.",
    );
    process.exit(3);
  }

  const { receipt, receiptPath, intentPath } = await applyActionIntent({
    dataDir: env.dataDir,
    intent: loaded.intent,
    file: loaded.file,
    dryRun: args.dryRun,
  });

  console.log(
    [
      args.dryRun ? "=== Action dry-run ===" : "=== Action applied (local POC) ===",
      `Intent: ${loaded.intent.intent_id}`,
      `Action: ${loaded.intent.action}`,
      `Adapter: ${loaded.intent.adapter}`,
      `Account: ${loaded.intent.account_name} (${loaded.intent.account_id})`,
      `Decision: ${loaded.intent.option_id} — ${loaded.intent.decision_label}`,
      `Adapters planned: ${loaded.intent.adapters_planned.join(", ")}`,
      "",
      receipt.summary,
      `Intent file: ${intentPath}`,
      `Receipt: ${receiptPath}`,
    ].join("\n"),
  );
}

main().catch((err) => {
  console.error(`Failure: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(3);
});
