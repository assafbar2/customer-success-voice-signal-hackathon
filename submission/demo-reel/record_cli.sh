#!/usr/bin/env bash
# On-camera CLI path. Dress rehearsal only. No --live. No Slack. No secrets.
set -u
cd /workspace/skills/customer-success-voice-signal
export TERM=xterm-256color
export PS1='$ '
printf '\033]0;Stage Manager\007'
clear
sleep 0.8
printf '\n  STAGE MANAGER  ·  dress rehearsal  ·  no ring\n\n'
sleep 0.8
printf '$ npm run signal -- --fixture stuck_support_acme.json\n'
sleep 0.5
npm run signal -- --fixture stuck_support_acme.json
sleep 4
printf '\n$ npm run signal -- --last\n'
sleep 0.4
npm run signal -- --last
sleep 5
printf '\n  Prompt book is the writeback. Slack does not fire.\n\n'
sleep 3
touch /tmp/stage-manager-cli-done
exit 0
