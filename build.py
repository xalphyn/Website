#!/usr/bin/env python3
"""Dependency-free static builder for the XALPHYN artist website."""
from pathlib import Path
from html import escape
from urllib.parse import urlparse
import json
import shutil
import os

ROOT = Path(__file__).resolve().parent
config = json.loads((ROOT / 'site.config.json').read_text(encoding='utf-8'))
pages = json.loads((ROOT / 'pages.json').read_text(encoding='utf-8'))
SITE_NAME = str(config.get('site_name') or 'XALPHYN')
raw_url = str(os.environ.get('XALPHYN_SITE_URL') or config.get('site_url') or os.environ.get('URL') or '').strip().rstrip('/')
# Netlify's URL environment variable is the production site's stable primary origin.
# Branch deploys are not accidentally indexed as the official identity site.
IS_PREVIEW = os.environ.get('CONTEXT', '').lower() in ('deploy-preview', 'branch-deploy')
parsed = urlparse(raw_url)
if raw_url and (parsed.scheme != 'https' or not parsed.netloc or parsed.path not in ('', '/')):
    raise SystemExit('site_url must be an HTTPS origin without any path')
SITE_URL = raw_url
OUT = ROOT / 'dist'
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(ROOT / 'src' / 'assets', OUT / 'assets')

nav_items = [('', 'Home'), ('profile', 'Profile'), ('about', 'About'), ('communities', 'Communities'), ('articles', 'Articles'), ('qa', 'Q&A'), ('contact', 'Contact')]

def valid_link(url):
    p = urlparse(url)
    return p.scheme == 'https' and bool(p.netloc) and not p.username and not p.password

def social_footer_icons():
    """Compact logo-only set of public accounts, repeated in every page footer."""
    links=[]
    for item in config.get('socials', []):
        name = str(item.get('name') or 'Platform')
        safe_name = escape(name, quote=True)
        icon = str(item.get('icon') or '').lower()
        if not icon.isalnum() or (icon not in ('audiomack','substack') and not (ROOT / 'src/assets/icons' / f'{icon}.svg').exists()):
            continue
        img = (f'<span class="platform-monogram" aria-hidden="true">{"AM" if icon == "audiomack" else "S"}</span>' if icon in ('audiomack','substack') else f'<img src="/assets/icons/{icon}.svg" alt="" aria-hidden="true" width="21" height="21">')
        url = str(item.get('url') or '').strip()
        if valid_link(url):
            links.append(f'<a class="footer-social" href="{escape(url,quote=True)}" target="_blank" rel="noopener noreferrer me" title="{safe_name}" aria-label="XALPHYN on {safe_name} (opens in new tab)">{img}<span class="footer-tooltip" aria-hidden="true">{escape(name)}</span></a>')
    return '\n'.join(links)

def social_profile_pills():
    links = []
    for item in config.get('socials', []):
        name = str(item.get('name') or '')
        icon = str(item.get('icon') or '').lower()
        if not icon.isalnum() or (icon not in ('audiomack','substack') and not (ROOT/'src/assets/icons'/f'{icon}.svg').exists()):
            continue
        label=escape(name, quote=True)
        symbol=(f'<span class="platform-monogram" aria-hidden="true">{"AM" if icon == "audiomack" else "S"}</span>' if icon in ('audiomack','substack') else f'<img src="/assets/icons/{icon}.svg" alt="" width="22" height="22" loading="lazy">')
        url=str(item.get('url') or '').strip()
        if valid_link(url):
            links.append(f'<a class="social-pill" href="{escape(url,quote=True)}" title="{label} @XALPHYN" target="_blank" rel="noopener noreferrer">{symbol}<span>{escape(name)}</span><span class="outmark" aria-hidden="true">↗</span></a>')
    return '\n'.join(links)

def medium_spotlights():
    profile_url = str(config.get('medium_profile_url') or '').strip()
    result = []
    for item in config.get('medium_spotlights', []):
        url = str(item.get('article_url') or '').strip()
        exact = valid_link(url)
        href = url if exact else profile_url
        if not valid_link(href):
            continue
        label = 'Read the full story on Medium' if exact else 'Browse XALPHYN on Medium'
        badge = 'DIRECT MEDIUM ARTICLE' if exact else 'TOPIC PREVIEW · MEDIUM'
        result.append(f'<a class="card medium-item" href="{escape(href,quote=True)}" target="_blank" rel="noopener noreferrer" data-reveal><span class="article-number">{badge} / {escape(item.get("category","Writing"))}</span><h3>{escape(item.get("title","Medium article"))}</h3><p>{escape(item.get("preview",""))}</p><span class="item-bottom"><span>{label}</span><span aria-hidden="true">↗</span></span></a>')
    return '\n'.join(result)

def medium_article_links():
    """Only show independently supplied and verified direct Medium article URLs."""
    blocks=[]
    for item in config.get('medium_articles', []):
        article_url = str(item.get('url') or '').strip()
        if not valid_link(article_url) or urlparse(article_url).hostname not in ('medium.com','xalphyn.medium.com'):
            continue
        title = escape(str(item.get('title') or 'Read on Medium'))
        summary = escape(str(item.get('summary') or 'Original article by XALPHYN.'))
        blocks.append(f'<a class="card medium-item" href="{escape(article_url,quote=True)}" target="_blank" rel="noopener noreferrer"><span class="article-number">MEDIUM / ORIGINAL ARTICLE</span><h3>{title}</h3><p>{summary}</p><span class="item-bottom">Read the full story ↗</span></a>')
    if blocks: return ''.join(blocks)
    return '<p class="micro-note medium-note">Individual Medium story links are awaiting confirmation. In the meantime, browse the author profile below for published writing.</p>'

def social_json():
    return [str(i['url']) for i in config.get('socials', []) if i.get('schema') and valid_link(str(i.get('url') or ''))]

def nav(slug):
    elements = []
    for href, label in nav_items:
        active = slug == href or (href == 'articles' and slug.startswith('articles/'))
        classes = 'nav-link' + (' is-active' if active else '')
        aria = ' aria-current="page"' if active else ''
        elements.append(f'<a class="{classes}" href="/{href + "/" if href else ""}"{aria}>{label}</a>')
    return '\n'.join(elements)

def url_of(slug):
    return SITE_URL + '/' + (slug + '/' if slug else '')

def layout(page, main):
    slug = page['slug']
    title = escape(page['title'])
    desc = escape(page['description'],quote=True)
    page_url = escape(url_of(slug),quote=True) if SITE_URL else ''
    canonical = f'<link rel="canonical" href="{page_url}">' if SITE_URL and not page.get('noindex') and not IS_PREVIEW else ''
    og_url = f'<meta property="og:url" content="{page_url}">' if SITE_URL else ''
    gtoken = str(config.get('google_site_verification') or '').strip()
    google_verify = f'<meta name="google-site-verification" content="{escape(gtoken,quote=True)}">' if gtoken else ''
    og_image = f'''<meta property="og:image" content="{escape(SITE_URL,quote=True)}/assets/social-preview.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="XALPHYN, independent music artist, with an illustrated monochrome avatar">
<meta name="twitter:image" content="{escape(SITE_URL,quote=True)}/assets/social-preview.png">''' if SITE_URL else ''
    robot = '<meta name="robots" content="noindex, nofollow">' if page.get('noindex') or IS_PREVIEW else '<meta name="robots" content="index, follow, max-image-preview:large">'
    site_id = url_of('') + '#website'
    person_id = url_of('profile') + '#artist'
    person_data = {'@context':'https://schema.org','@type':'Person','@id':person_id,
        'name':'XALPHYN','alternateName':'@XALPHYN','description':'Emerging music artist and founder of SynthBeatsWaves, a non-copyright music community of artists; creator of Programming Hub.',
        'url':url_of('profile'),'image':SITE_URL+'/assets/xalphyn-pfp.webp',
        'knowsAbout':['music','SynthBeatsWaves','Programming Hub'],
        **({'sameAs':social_json()} if social_json() else {})} if SITE_URL and slug in ('','profile') else None
    site_data = {'@context':'https://schema.org','@type':'WebSite','@id':site_id,'name':SITE_NAME,
        'url':url_of(''),'inLanguage':'en'} if SITE_URL and not slug else None
    profile_data = {'@context':'https://schema.org','@type':'ProfilePage','@id':url_of('profile')+'#profile',
        'url':url_of('profile'),'mainEntity':{'@id':person_id},'about':{'@id':person_id},
        'name':page['title']} if SITE_URL and slug == 'profile' else None
    article_data = {'@context':'https://schema.org','@type':'Article','@id':url_of(slug)+'#article',
        'headline':page['title'].split(' — ')[0],'description':page['description'],
        'mainEntityOfPage':{'@type':'WebPage','@id':url_of(slug)},'inLanguage':'en',
        'author':{'@type':'Person','@id':person_id,'name':SITE_NAME,'url':url_of('profile')}} if SITE_URL and slug.startswith('articles/') else None
    faq_data = None
    if SITE_URL and slug == 'qa':
        faq_pairs=[
        ('Who is XALPHYN?', 'XALPHYN is an emerging independent music artist and founder of SynthBeatsWaves and Programming Hub.'),
        ('What is SynthBeatsWaves?', 'A community of artists founded by XALPHYN to provide non-copyright music tracks to listeners and content creators.'),
        ('What is XALPHYN’s favorite social app?', 'Threads.'),
        ('What is XALPHYN’s favorite color?', 'Black.'),
        ('How can I contact XALPHYN?', 'Use the private enquiry form on the official website or send an anonymous message through NGL.')]
        faq_data={'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faq_pairs]}
    breadcrumb_data = None
    if SITE_URL and slug and not page.get('noindex'):
        parts = slug.split('/')
        crumbs=[{'@type':'ListItem','position':1,'name':'Home','item':url_of('')}]
        if len(parts)==2:
            crumbs.append({'@type':'ListItem','position':2,'name':'Articles','item':url_of('articles')})
        crumbs.append({'@type':'ListItem','position':len(crumbs)+1,'name':page['title'].split(' — ')[0],'item':url_of(slug)})
        breadcrumb_data={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':crumbs}
    ld = '\n'.join('<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False).replace('<','\\u003c')+'</script>' for d in (site_data,person_data,profile_data,article_data,faq_data,breadcrumb_data) if d)
    avatar = '<img src="/assets/xalphyn-pfp.webp" alt="XALPHYN illustrated monochrome artist avatar" width="1024" height="1024" loading="lazy" decoding="async">'
    banner_class = ' has-banner' if (ROOT/'src/assets/banner.webp').exists() else ''
    main=(main.replace('{{SOCIAL_TILES}}','')
        .replace('{{MEDIUM_SPOTLIGHTS}}',medium_spotlights()).replace('{{MEDIUM_ARTICLE_LINKS}}',medium_article_links()).replace('{{SOCIAL_PILLS}}',social_profile_pills()).replace('{{AVATAR}}',avatar)
        .replace('{{BANNER_CLASS}}',banner_class))
    ngl_url = str(config.get('ngl_url') or '').strip()
    if not valid_link(ngl_url):
        raise SystemExit('Set ngl_url to a full HTTPS link in site.config.json')
    main = main.replace('{{NGL_URL}}',escape(ngl_url,quote=True))
    # Netlify sets NETLIFY=true for Git-linked production builds (including custom domains).
    if os.environ.get('NETLIFY', '').lower() == 'true':
        main = main.replace('data-enquiry-form>', 'data-enquiry-form data-netlify-form-host="true">')
    sbw_url = str(config.get('sbw_site_url') or '').strip()
    sbw_link = f'<a class="btn btn-secondary" href="{escape(sbw_url,quote=True)}" target="_blank" rel="noopener noreferrer">Visit the SBW website ↗</a>' if valid_link(sbw_url) else '<span class="soon-pill">Separate SBW website in development</span>'
    main = main.replace('{{SBW_LINK}}',sbw_link)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#050505">
<meta name="description" content="{desc}">
<title>{title}</title>
{canonical}
{google_verify}
{robot}
<meta property="og:type" content="{'article' if slug.startswith('articles/') else 'website'}">
<meta property="og:site_name" content="{escape(SITE_NAME,quote=True)}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
{og_url}
{og_image}
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="{'summary_large_image' if SITE_URL else 'summary'}">
<meta name="author" content="XALPHYN">
<link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="48x48" href="/assets/favicon-48.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/site.css" as="style">
<link rel="stylesheet" href="/assets/site.css">
{ld}
<script defer src="/assets/site.js"></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="ambient" aria-hidden="true"></div><div class="scroll-progress" aria-hidden="true"></div>
<div class="site-wrap">
<header class="site-header">
  <a class="brand" href="/" aria-label="XALPHYN home"><span class="brand-symbol"><img src="/assets/xalphyn-pfp.webp" alt="" width="42" height="42" decoding="async"></span><span>XALPHYN<span class="brand-point">.</span></span></a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-navigation" aria-label="Open menu"><span></span><span></span><span></span></button>
  <nav class="main-nav" id="primary-navigation" aria-label="Main navigation">{nav(slug)}</nav>
  <a class="header-note" href="/contact/">Leave a note <span aria-hidden="true">↗</span></a>
</header>
<main id="main" class="page-main">{main}</main>
<footer class="footer">
  <div class="footer-top"><div><span class="footer-mark"><img src="/assets/xalphyn-pfp.webp" alt="XALPHYN artist avatar" width="66" height="66" loading="lazy" decoding="async"></span><strong>An independent music identity.</strong><p>Sound. Identity. Expression.</p></div><a class="footer-up" href="#main" aria-label="Back to top">↑</a></div>
  <div id="social-links" class="footer-links" aria-label="XALPHYN official social accounts">
    <div class="footer-links-label"><span>FIND ME ONLINE</span><span>All platforms · @XALPHYN</span></div>
    <div class="footer-social-row">{social_footer_icons()}</div>
  </div>
  <div class="footer-bottom"><span>© <span data-year>2026</span> XALPHYN. All rights reserved.</span><span>Artist · SynthBeatsWaves · Programming Hub</span><a href="/privacy/">Privacy</a></div>
</footer>
</div><div class="copy-toast" role="status" aria-live="polite" aria-atomic="true"></div>
</body>
</html>'''

for page in pages:
    slug = page['slug']
    fragment=(ROOT/'src/pages'/page['src']).read_text(encoding='utf-8')
    out_dir = OUT/slug
    out_dir.mkdir(parents=True,exist_ok=True)
    (out_dir/'index.html').write_text(layout(page,fragment),encoding='utf-8')
    if slug == '404':
        (OUT/'404.html').write_text(layout(page,fragment),encoding='utf-8')
robots='User-agent: *\nAllow: /\n'
if SITE_URL and not IS_PREVIEW:
    robots+=f'Sitemap: {SITE_URL}/sitemap.xml\n'
    locs='\n'.join(f'  <url><loc>{escape(url_of(p["slug"]))}</loc></url>' for p in pages if not p.get('noindex'))
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+locs+'\n</urlset>\n',encoding='utf-8')
(OUT/'robots.txt').write_text(robots,encoding='utf-8')
(OUT/'site.webmanifest').write_text(json.dumps({'name':'XALPHYN — Official Website','short_name':'XALPHYN','start_url':'/','display':'standalone','background_color':'#050505','theme_color':'#050505','icons':[{'src':'/assets/icon-192.png','sizes':'192x192','type':'image/png'},{'src':'/assets/icon-512.png','sizes':'512x512','type':'image/png'}]},indent=2),encoding='utf-8')
if IS_PREVIEW:
    (OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n',encoding='utf-8')
print(f'Built {len(pages)} pages in {OUT}')
print('SEO site origin:', SITE_URL or 'NOT SET: add the actual deployed HTTPS origin to site.config.json or XALPHYN_SITE_URL')
print('Search-indexing mode:', 'NOINDEX preview' if IS_PREVIEW else 'production (pending deployment and indexing)')
