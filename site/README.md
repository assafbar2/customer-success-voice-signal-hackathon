# Stage Manager — temporary judge site

Static landing page for CALL-E hackathon judges.

## Local

```bash
cd site
python3 -m http.server 4173
# open http://localhost:4173
```

## Deploy — GitHub Pages (this is what we use)

1. `site/` + `.github/workflows/pages.yml` are on `main` after merge.  
2. Repo **Settings → Pages → Source: GitHub Actions**.  
3. Actions → “Deploy Stage Manager site…” → ensure green.  
4. URL: **https://assafbar2.github.io/customer-success-voice-signal-hackathon/**

No Vercel. If you created a Vercel project by mistake, delete it in the [Vercel dashboard](https://vercel.com/dashboard) (Project → Settings → Delete).

## Content rules

- Brand-first Stage Manager hero  
- No API keys / phones  
- Points at skill CLI + GitHub repo  
