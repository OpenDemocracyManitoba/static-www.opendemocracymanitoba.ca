"""Phase B (owner decision, 2026-10-25): drop files that aren't part of the site (test uploads, dev docs, server config, unused theme, unrelated demos).
Usage: python3 -I drop_unrelated.py <host> [--apply]   (from the repo root; dry run by default)
Each host has an explicit list (exact paths and directory prefixes). Refuses to run if a kept file references a dropped one,
or if a listed path is missing."""
import os, re, sys, urllib.parse

APPLY = '--apply' in sys.argv[1:]
host = next(a for a in sys.argv[1:] if not a.startswith('--'))
# host -> [(path or dir/ prefix, why)]
DROP = {
    '2011.manitobaelection.ca': [
        ('uploads/politician_image/1/', 'test upload (the Windows `Koala.jpg` sample photo), not a candidate'),
        ('images/test/', 'unreferenced test copies of the historic maps'),
        ('images/rails.png', 'Rails default `public/` file'),
        ('javascripts/prototype.js', 'Rails default `public/` file, never loaded'),
        ('javascripts/ajax_buttons.js', 'unreferenced script'),
        ('stylesheets/sass/application.sass', 'stylesheet source, not served by the app'),
    ],
    '2014.winnipegelection.ca': [
        ('doc/', 'graphviz model/controller diagrams of the Rails app (developer docs)'),
        ('uploads/tmp/', 'upload cache left behind by the image uploader'),
        ('index.html.old', 'an old copy of the home page, unreferenced'),
    ],
    'www.winnipegelection.ca': [
        ('nginx/', 'the server\'s nginx vhost config, not site content'),
        ('css/', 'unused 2018 landing-page theme'),
        ('img/', 'unused 2018 landing-page theme'),
        ('vendor/', 'unused 2018 landing-page theme (Bootstrap, Font Awesome, jQuery, Simple Line Icons)'),
    ],
    'www.opendemocracymanitoba.ca': [
        ('square/', 'teaching demos (shape transformer, credit card validator) unrelated to ODM, linked from nowhere else'),
        ('_ext/cdn.jsdelivr.net/', 'the Tailwind CSS mirror (Phase B R4), used only by `square/`'),
    ],
}[host]

files = sorted(os.path.relpath(os.path.join(r, f), 'site') for r, _, fs in os.walk('site') for f in fs)
drop, why = [], {}
for p, w in DROP:
    hit = [f for f in files if (f.startswith(p) if p.endswith('/') else f == p)]
    if not hit:
        sys.exit(f'refusing: {p} not found in site/')
    drop += hit
    why[p] = (w, len(hit))
keep = [f for f in files if f not in drop]

# Needle per dropped file: its basename when that's unique in the tree and has a web-file extension, otherwise its path
# (the nginx file is named after the domain, which every page mentions).
WEB = re.compile(r'\.(html?|old|css|sass|scss|less|js|map|json|png|jpe?g|gif|svg|ico|eot|ttf|otf|woff2?)$', re.I)
base_count = {}
for f in files:
    base_count[os.path.basename(f)] = base_count.get(os.path.basename(f), 0) + 1
needles = set()
for f in drop:
    b = os.path.basename(f)
    n = b if base_count[b] == 1 and WEB.search(b) else f
    needles |= {n.encode(), urllib.parse.quote(n).encode()}
needle = re.compile(b'|'.join(re.escape(n) for n in sorted(needles)))
users = [f for f in keep if needle.search(open(os.path.join('site', f), 'rb').read())]

print(f'{"APPLY" if APPLY else "dry run"} {host}: {len(drop)} files')
for p, (w, n) in why.items():
    print(f'  {p} ({n}): {w}')
if users:
    sys.exit(f'refusing: kept files reference dropped ones: {users[:10]}')

if APPLY:
    for f in drop:
        os.remove(os.path.join('site', f))
    for r, ds, fs in sorted(os.walk('site'), reverse=True):   # deepest first
        if r != 'site' and not os.listdir(r):
            os.rmdir(r)
    section = ('## Unrelated files removed\n\n'
               'Owner decision (Phase B, 2026-10-25): files that aren\'t part of the site were removed by '
               f'`python3 -I drop_unrelated.py {host} --apply` ({len(drop)} files). No remaining file references them.\n\n'
               + ''.join(f'* `{p}` ({n} file{"s" if n > 1 else ""}): {w}\n' for p, (w, n) in why.items()))
    r = open('README.md').read()
    i = r.find('\n## Hosting\n')
    open('README.md', 'w').write(r[:i + 1] + section + '\n' + r[i + 1:])
