#!/usr/bin/env node
/**
 * Apply (or dry-run) the latest pending action intent.
 * Default: local receipt only. --adapter slack|github posts for real
 * (Slack incoming webhook / GitHub issue comment) — env-gated, HOLD on placeholder.
 */
import { loadDotEnv, readSkillEnv } from "./config/env.js";
import {
  applyActionIntent,
  loadLastPendingIntent,
  loadPendingIntentById,
} from "./action/store.js";
import {
  formatAdapterText,
  resolveGithubTarget,
  resolveSlackTarget,
  sendToGithubIssue,
  sendToSlack,
} from "./action/adapters.js";

function printHelp(): void {
  console.log(`
Stage Manager — apply-action
Turn a closed-set CS decision into a system handoff (POC).

Usage:
  npm run apply-action -- --last --dry-run
  npm run apply-action -- --last
  npm run apply-action -- --last --adapter slack
  npm run apply-action -- --last --adapter github
  npm run apply-action -- --id <intent_id> --dry-run

Flags:
  --last            Use most recent pending action intent
  --id <id>         Use a specific pending intent_id
  --dry-run         Print/record what would be sent — no "executed_local", no network
  --adapter <name>  slack (SLACK_WEBHOOK_URL) or github (GITHUB_TOKEN/REPO/ISSUE)
  --help

Seam:
  Decision → data/actions/pending/*.json → apply-action → data/actions/executed/*
  Live adapters: slack (incoming webhook) · github (issue comment) — env-gated,
  placeholder values HOLD (exit 2). Zendesk / Salesforce shapes documented at the seam.
`);
}

function parse(argv: string[]): {
  last: boolean;
  id?: string;
  dryRun: boolean;
  help: boolean;
  adapter?: "slack" | "github";
} {
  const out = {
    last: false,
    dryRun: false,
    help: false,
    id: undefined as string | undefined,
    adapter: undefined as "slack" | "github" | undefined,
  };
  const readAdapter = (v: string | undefined): "slack" | "github" => {
    if (v !== "slack" && v !== "github") {
      throw new Error(`--adapter must be slack or github (got: ${v ?? "nothing"})`);
    }
    return v;
  };
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
    else if (a === "--adapter") out.adapter = readAdapter(argv[++i]);
    else if (a.startsWith("--adapter=")) out.adapter = readAdapter(a.slice(10));
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

  let sent: { effect: "slack_webhook_posted" | "github_comment_posted"; detail: string } | undefined;

  if (args.adapter === "slack") {
    const target = resolveSlackTarget(env.slackWebhookUrl);
    if ("hold" in target) {
      if (args.dryRun) {
        console.log(`Adapter dry-run (slack): would POST once SLACK_WEBHOOK_URL is set (HOLD: ${target.hold}).`);
        console.log(`--- payload.text ---\n${formatAdapterText(loaded.intent)}\n---`);
      } else {
        console.error(`HOLD: ${target.hold} — set SLACK_WEBHOOK_URL in .env (see .env.example).`);
        process.exit(2);
      }
    } else if (args.dryRun) {
      console.log("Adapter dry-run (slack): target configured — no network call in dry-run.");
      console.log(`--- payload.text ---\n${formatAdapterText(loaded.intent)}\n---`);
    } else {
      const res = await sendToSlack(loaded.intent, target.url);
      if (!res.ok) {
        console.error(`Failure: Slack webhook returned HTTP ${res.status}.`);
        process.exit(3);
      }
      sent = { effect: "slack_webhook_posted", detail: `HTTP ${res.status}` };
    }
  } else if (args.adapter === "github") {
    const target = resolveGithubTarget({
      token: env.githubToken,
      repo: env.githubRepo,
      issue: env.githubIssue,
    });
    if ("hold" in target) {
      if (args.dryRun) {
        console.log(`Adapter dry-run (github): would comment once GITHUB_TOKEN/GITHUB_REPO/GITHUB_ISSUE are set (HOLD: ${target.hold}).`);
        console.log(`--- comment body ---\n${formatAdapterText(loaded.intent)}\n---`);
      } else {
        console.error(`HOLD: ${target.hold} — set GITHUB_TOKEN, GITHUB_REPO, GITHUB_ISSUE in .env (see .env.example).`);
        process.exit(2);
      }
    } else if (args.dryRun) {
      console.log(`Adapter dry-run (github): would comment on ${target.repo}#${target.issue} — no network call in dry-run.`);
      console.log(`--- comment body ---\n${formatAdapterText(loaded.intent)}\n---`);
    } else {
      const res = await sendToGithubIssue(loaded.intent, target);
      if (!res.ok) {
        console.error(`Failure: GitHub API returned HTTP ${res.status}.`);
        process.exit(3);
      }
      sent = { effect: "github_comment_posted", detail: `${target.repo}#${target.issue} HTTP ${res.status}` };
    }
  }

  const { receipt, receiptPath, intentPath } = await applyActionIntent({
    dataDir: env.dataDir,
    intent: loaded.intent,
    file: loaded.file,
    dryRun: args.dryRun,
    sent,
  });

  console.log(
    [
      args.dryRun
        ? "=== Action dry-run ==="
        : sent
          ? `=== Action applied (${sent.effect}) ===`
          : "=== Action applied (local POC) ===",
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
