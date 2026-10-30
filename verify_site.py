#!/usr/bin/env python3
"""Verify public-facing content, assets, link paths and identity privacy invariants."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import json
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'
class Inspector(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.assets=[];self.images=[];self.headings=[];self.canon=[];self.ld=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='img':
            self.images.append(a)
            self.assets.append(a.get('src',''))
        if tag in ('script','link'):
            if a.get('src'):self.assets.append(a['src'])
            if a.get('rel') in ('stylesheet','icon','apple-touch-icon'):self.assets.append(a.get('href',''))
            if a.get('rel')=='canonical':self.canon.append(a.get('href',''))
        if tag=='h1':self.headings.append('h1')

def main():
    manifest=json.loads((ROOT/'pages.json').read_text())
    pages=sorted(OUT.rglob('index.html'))
    assert len(pages)==len(manifest),(len(pages),len(manifest))
    for forbidden in ('avatar.webp','favicon.svg','selfie','1000060471','personal-portrait'):
        for path in list((ROOT/'src').rglob('*'))+list(OUT.rglob('*')):
            assert forbidden not in str(path).lower(),path
    for name in ('xalphyn-pfp.webp','social-preview.png','favicon.ico','favicon-32.png','apple-touch-icon.png'):
        assert (OUT/'assets'/name).is_file(),name
    assert not (ROOT/'src/assets/avatar.webp').exists()
    for page in pages:
        raw=page.read_text(encoding='utf-8')
        parsed=Inspector();parsed.feed(raw)
        assert parsed.headings.count('h1')==1,(page,parsed.headings)
        assert not any(x in raw.lower() for x in ('class="brand-symbol">x','class="footer-mark">x','class="x-center"','favicon.svg','avatar.webp')),(page,'leftover X placeholder or old asset')
        for image in parsed.images:assert 'alt' in image,(page,image)
        for path in parsed.links+parsed.assets:
            if not path or path.startswith(('#','mailto:','tel:','data:')):continue
            u=urlparse(path)
            if u.scheme:
                assert u.scheme=='https',path
                continue
            target=unquote(u.path).lstrip('/')
            location=OUT/target
            if target.endswith('/') or not location.suffix:location=location/'index.html'
            assert location.exists(),(str(page.relative_to(OUT)),path,str(location))
        assert '/assets/xalphyn-pfp.webp' in raw,page
        assert '/assets/favicon.ico' in raw,page
    assert 'ngl.link/xalphyn1' in (OUT/'contact/index.html').read_text()
    for platform in ('YouTube','Instagram','Threads','Facebook','Reddit','Bluesky','Substack','Medium','Discord'):
        assert platform in (OUT/'index.html').read_text(),platform
    print('PASS:',len(pages),'pages; all assets/links; public PFP only; no old X identity placeholders; icon social footer; NGL')
if __name__=='__main__':main()
