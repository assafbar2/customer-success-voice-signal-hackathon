# Stage Manager — temporary judge site

Static landing page for CALL-E hackathon judges.

## Local

```bash
cd site
python3 -m http.server 4173
# open http://localhost:4173
```

## Deploy — Vercel (use the repo you already have)

The old `/new/clone` link **duplicates** a repo. Don’t use that.

**Correct path — import existing GitHub repo:**

1. Open **https://vercel.com/new**  
2. **Import** `assafbar2/customer-success-voice-signal-hackathon` (same repo — not “Clone”)  
3. Set **Root Directory** → `site`  
4. Deploy  

Or from the Vercel dashboard: Add New Project → Import Git Repository → pick this repo → Root Directory `site`.

## Deploy — GitHub Pages (enough for this use-case)

**Yes — GitHub Pages is enough.** Judges only need a public URL. You do **not** need Vercel.

1. Merge or push `site/` + `.github/workflows/pages.yml` (already on the PR branch).  
2. Repo **Settings → Pages → Source: GitHub Actions**.  
3. Run the workflow (push or Actions → “Deploy Stage Manager site…” → Run).  
4. URL: `https://assafbar2.github.io/customer-success-voice-signal-hackathon/`

Vercel is optional (custom domain / faster preview). Pages is fine for a hackathon landing page.

## Content rules

- Brand-first Stage Manager hero  
- No API keys / phones  
- Points at skill CLI + PR #1  
