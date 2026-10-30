# XALPHYN — Deploy and SEO Launch Guide

## 1. Recommended path: GitHub → Netlify

Use **the editable source project** and keep `build.py`, `site.config.json`, `pages.json`, `src/`, and `netlify.toml` at the repository root. Do not upload the outer ZIP to a repository without extracting it.

From inside `xalphyn-final/`, optionally verify locally:

```bash
python3 build.py
python3 verify_site.py
python3 -m http.server 8000 -d dist
```

The local preview runs at http://localhost:8000. The contact form deliberately does **not** send from localhost.

Create a GitHub repository, then follow this workflow from the source folder:

```bash
git init
git add .
git commit -m "Launch XALPHYN artist website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

Replace `YOUR-USERNAME` and `YOUR-REPO` with actual values. You may use GitHub's upload interface instead. The repository can be private if your Netlify Git connection has access. Never commit owner email or private credentials.

In https://app.netlify.com/ choose **Add new project → Import an existing project → GitHub**, select the repository and deploy. The existing `netlify.toml` contains:

- Build command: `python3 build.py`
- Publish directory: `dist`

Netlify assigns a real `https://...netlify.app` production hostname. The build uses Netlify's `URL` environment variable to generate canonical URLs and sitemap automatically. Choose a recognizable site name if it is available. If you add a paid domain in future, rebuild with the new canonical origin and set permanent redirects. No domain purchase is required.

## 2. Activate and test the enquiry form

The static contact page includes a form named `xalphyn-enquiry`, `data-netlify="true"`, a hidden `form-name` field, and a honeypot. This works only after correct Netlify form processing.

1. Under the Netlify project, open **Forms** and select **Enable form detection** (if disabled). Redeploy after enabling.
2. Confirm `xalphyn-enquiry` is listed as detected.
3. Send a realistic test through `https://YOUR-SITE.netlify.app/contact/`. Confirm it reaches Netlify's form submissions and the `/contact/thank-you/` page. Check the spam list if missing.
4. To receive private email notifications, open **Forms → Submission notifications** and set the recipient address **in the Netlify dashboard only**, never in the public site, HTML, GitHub repository or JS.
5. If you deploy this project to Vercel instead, the current Netlify-only contact backend will **not** work. Replace it with a properly authenticated or hosted form service first.

Do not share your private notification email in public screenshots or source. Netlify Forms has plan usage limits.

## 3. Confirm SEO technical output

After the Git-linked production build, open:

- `https://YOUR-SITE.netlify.app/`
- `https://YOUR-SITE.netlify.app/robots.txt`
- `https://YOUR-SITE.netlify.app/sitemap.xml`
- `https://YOUR-SITE.netlify.app/profile/`
- `https://YOUR-SITE.netlify.app/articles/synthbeatswaves/`

Inspect page source to confirm `<link rel="canonical">` uses the actual production origin, the Open Graph sharing image loads, and `application/ld+json` is present. `robots.txt` should reference the real sitemap. Contact confirmation and 404 pages are noindex and omitted from the sitemap.

If Netlify's detected URL is not your intended canonical hostname, set `XALPHYN_SITE_URL` to the correct `https://...` origin as a Netlify build environment variable and redeploy. Never use sample URLs as real canonical URLs.

## 4. Google Search Console

1. Go to https://search.google.com/search-console and add a **URL-prefix** property with your exact HTTPS site origin, including `https://`.
2. Verify ownership using a supported method, such as an HTML verification file placed in `src/assets`? **Do not place verification files there**: they would be deployed under `/assets/`, not `/`. To add Google's HTML verification file at the root, put it in `src/` as a separate root-level asset and extend `build.py` to copy it into `dist/`, or instead use an available HTML meta-tag verification method in the template head. The verification must be present on the actual public deployment; follow Search Console's prompts for the exact token.
3. Under **Sitemaps**, enter `sitemap.xml`.
4. Use **URL Inspection** for the homepage and the main profile page; request indexing if needed.
5. Monitor Pages/Indexing and Search Performance for search queries containing `XALPHYN`. Submission is not guaranteed indexing or rank.

### Easier ownership verification for this exact builder

In `site.config.json`, fill `google_site_verification` with the exact code issued by Google. `build.py` emits the corresponding `<meta>` verification tag. Rebuild and deploy before clicking Verify in Search Console. Never fabricate or guess the code.

## 5. Bing Webmaster Tools

1. Open https://www.bing.com/webmasters/ and sign in.
2. Import the verified site from Google Search Console, or add the site manually and verify ownership.
3. Confirm or submit `https://YOUR-SITE.netlify.app/sitemap.xml`.
4. Track discovered URLs and indexing status over time.

## 6. Final public identity checklist

- [ ] Every social handle-based URL opens the owner's real profile; remove unverified accounts from `site.config.json`.
- [ ] Spotify points to the correct **user profile**. Do not call it an artist release page.
- [ ] Only illustrated XALPHYN identity artwork appears; no private portrait or email.
- [ ] The contact form stores a real submission privately; notifications are set in Netlify only.
- [ ] Medium direct story URLs added only after confirmation, if desired.
- [ ] `robots.txt`, `sitemap.xml`, canonical URLs, favicon and social preview are correct on the live hostname.
- [ ] Link the newly deployed website from verified YouTube, Instagram, Threads and other XALPHYN accounts to build legitimate identity references.
- [ ] Do not promise every track is usable without checking license terms.

## Helpful official references

- https://docs.netlify.com/start/quickstarts/deploy-from-repository/
- https://docs.netlify.com/manage/forms/setup/
- https://docs.netlify.com/manage/forms/notifications/
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://support.google.com/webmasters/answer/7451001
- https://www2.bing.com/webmasters/help/add-and-verify-site-12184f8b
