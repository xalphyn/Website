# XALPHYN — Official Artist Portfolio (V6 launch candidate)

A lightweight, zero-third-party-dependency static site generated with Python 3. The editable project contains `build.py`, `src/pages/`, and `src/assets/`. The `dist/` directory is a generated site for static hosting.

## Run locally

Extract the **source ZIP**, enter the `xalphyn-final` folder, then:

```bash
python3 build.py
python3 -m http.server 8000 -d dist
```

Visit http://localhost:8000/ . Stop the server with Ctrl+C. Re-run `python3 build.py` after editing the source or configuration and refresh your browser.

If you extract the **static hosting ZIP**, go to the folder containing `index.html` and run `python3 -m http.server 8000` (no `build.py` in the static ZIP).

## Pages and content

- Home — XALPHYN music artist introduction.
- Profile — illustrated XALPHYN PFP, bio, founder/creator roles, and linked social platforms.
- About — XALPHYN music journey and the distinct roles of SBW and Programming Hub.
- Communities — SBW (music community of artists sharing non-copyright tracks) and Programming Hub (Discord-only developer community).
- Articles — XALPHYN, SBW, Programming Hub and verified Medium links when added.
- Q&A — only owner-supplied facts.
- Contact — **Netlify Forms** enquiry submission (not an exposed mail address) plus a separate NGL link.
- Privacy and a noindex thank-you screen.

## Enquiry form: IMPORTANT

The contact form uses Netlify's built-in Forms feature, requiring a **Netlify-hosted deployment with Form detection enabled**. Form definition is included in the generated static HTML. There is no database or secret embedded in the frontend. The form includes an automatic Netlify spam filter and honeypot. On localhost, submission is intentionally blocked because no backend exists. Vercel-only deployment also does **not** enable this form; you'd need to replace the handler.

After publishing on Netlify:

1. Open your site's **Forms** page, enable **Form detection** if needed, then redeploy.
2. Confirm `xalphyn-enquiry` appears as an active form.
3. Submit one real-looking test enquiry from the public website and verify its arrival under **Forms > Submissions** (also check Spam).
4. For private notification delivery, visit **Forms > Submission notifications > Add notification** and enter your private recipient email **there only**. Do NOT put that address into public HTML, metadata, JavaScript, configuration or the repository.
5. Verify that the form redirects to `/contact/thank-you/` after a real submission. This confirmation page is excluded from the sitemap and marked noindex.
6. Monitor usage and spam; Netlify service limits apply. If you use a custom Netlify domain, Git-linked builds automatically mark the form as enabled; for manual uploads the built HTML must be configured appropriately.

The user-supplied NGL link is separate. NGL is not guaranteed technically untraceable.

## Direct Medium article links

The public Medium profile is linked. **Exact individual story URLs could not be independently verified**, so none have been guessed. To add them, edit `site.config.json`:

```json
"medium_articles": [
  {
    "title": "Your article title",
    "summary": "One or two factual sentences from the actual article.",
    "url": "https://medium.com/@xalphyn/actual-article-slug-and-id"
  }
]
```

Use only published and working story URLs. The build will automatically render direct article cards on `/articles/`. Do not include the example URL unchanged.

## SEO and deployment

For Git-connected Netlify: `netlify.toml` builds the site with `python3 build.py` and publishes `dist`. Netlify exposes the public site URL through its `URL` variable. The builder emits page-specific canonical URLs, OG images, Person/WebSite/Article/FAQ and Breadcrumb schema where applicable, `robots.txt` and `sitemap.xml` when given a real HTTPS origin.

For manual deploy after the hostname is known:

```bash
XALPHYN_SITE_URL=https://YOUR-REAL-DEPLOYMENT.netlify.app python3 build.py
```

Upload the **contents** of `dist/`, not the source. Check `/sitemap.xml`, then verify in Google Search Console and Bing Webmaster Tools. Preview builds add `noindex`. Rankings are not guaranteed by metadata or merely owning a provider subdomain.

## Editing and privacy

- `src/pages/*.html` — paragraphs and layout.
- `src/assets/site.css` — monochrome theme and animations.
- `src/assets/site.js` — menu, copy interactions, scroll progress, localhost form guard.
- `site.config.json` — social URLs, NGL, Medium article links, identity information.
- `pages.json` — page titles and descriptions.
- `src/assets/xalphyn-pfp.webp` — illustrated public artist avatar; also used for favicon and Open Graph image assets.

The package contains **no personal-face photograph** and **no private recipient email address**. The older releases and archives remain separate and should not be deployed.

## Social logos

Bundled platform logos are sourced from Font Awesome Free Brands with attribution. The personal Discord username and its icon entry were removed. Two less-common platforms (Audiomack and Substack) use labelled monochrome initials instead of an inaccurately recreated logo. Replace those with the respective official brand marks if you obtain approved assets. See `BRAND_ICON_ATTRIBUTION.md`.

## Quality checks

```bash
python3 build.py
python3 verify_site.py
```

After deploying, test actual contact-form persistence and all external links yourself. The `verify_site.py` static validator does not establish backend delivery or search indexing.

## V6 changes

- SynthBeatsWaves is presented as a **music community of artists providing non-copyright tracks**. The planned website and actual music releases are central; Discord is not its defining feature.
- Programming Hub is presented separately as a **Discord developer community** founded to connect programmers.
- Exact owner-supplied Spotify link is a **user profile**, not a Spotify artist music catalog.
- No owner contact email or personal Discord username is included in public site files.
- The local contact form has no backend; use the hosted Netlify Forms workflow to receive enquiries.
- Read `DEPLOY-SEO-GUIDE.md` before public launch.
