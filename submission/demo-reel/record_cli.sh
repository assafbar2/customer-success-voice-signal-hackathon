#!/usr/bin/env bash
# On-camera CLI path. No --live. No Slack send. No secrets.
set -u
cd /workspace/skills/customer-success-voice-signal
export TERM=xterm-256color
export PS1='$ '
printf '\033]0;Stage Manager\007'
clear
sleep 1

printf '\n  STAGE MANAGER\n  Live writeback already in the prompt book — CS owner only.\n\n'
sleep 1
printf '$ npm run signal -- --last\n'
sleep 0.4
npm run signal -- --last
sleep 3

clear
printf '\n  Dress rehearsal — default. No ring. No API key.\n\n'
sleep 0.6
printf '$ npm run signal -- --fixture stuck_support_acme.json\n'
sleep 0.4
npm run signal -- --fixture stuck_support_acme.json
sleep 2

printf '\n$ npm run signal -- --list\n'
sleep 0.3
npm run signal -- --list
sleep 2

printf '\n$ npm run apply-action -- --last --dry-run\n'
sleep 0.4
npm run apply-action -- --last --dry-run
sleep 2

printf '\n  Prompt book is the writeback.\n  Slack does not fire. Customer was never called.\n\n'
sleep 5
exit 0
