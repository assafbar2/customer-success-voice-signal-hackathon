# Stage Manager — temporary judge site

Static landing page for CALL-E hackathon judges.

## Local

```bash
cd site
python3 -m http.server 4173
# open http://localhost:4173
```

## Deploy — Vercel (recommended temporary URL)

No Vercel token in this agent environment — you deploy once from your account:

1. Open: https://vercel.com/new  
2. Import `assafbar2/customer-success-voice-signal-hackathon`  
3. Set **Root Directory** to `site` (or leave repo root — root `vercel.json` sets `outputDirectory: site`)  
4. Deploy  

One-click style:  
https://vercel.com/new/clone?repository-url=https://github.com/assafbar2/customer-success-voice-signal-hackathon&root-directory=site

## Deploy — GitHub Pages

Workflow: `.github/workflows/pages.yml`  
After first run, enable Pages in repo **Settings → Pages → Source: GitHub Actions**.  
URL shape: `https://assafbar2.github.io/customer-success-voice-signal-hackathon/`

## Content rules

- Brand-first Stage Manager hero  
- No API keys / phones  
- Points at skill CLI + PR #1  
