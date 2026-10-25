# www.opendemocracymanitoba.ca (static archive)

Static copy of **www.opendemocracymanitoba.ca**, taken from olddroplet (`odm-nginx-ruby-php-2018`, 159.203.24.194) on 2026-10-24, before the server was retired. Static Open Democracy Manitoba website.

`site/` is the served web root as it was on disk (13 files), minus the files listed below. No crawl was needed: this site was already static.

## Serving

Serve `site/` as static files from the domain root.

## Left out of `site/`

* `.git/`
* `books.zip`

These were left out because they were not site content: version control, PHP, or (per the archive plan) files that should not be public. The full web root is kept in a private archive repo.

## Links to internal or old hosts

Left as they are (Phase A doesn't rewrite content):

* `http://www.manitobaelection.ca`: 1 files, e.g. `index.html`

## External dependencies mirrored

In Phase B of the olddroplet migration (R4, 2026-10-24), the stylesheets every page needs to render were copied into `site/_ext/` by `python3 -I mirror_deps.py www.opendemocracymanitoba.ca --apply`, and the pages now load the copies (root-relative links):

* `https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css` → `/_ext/cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css` (4 HTML files)
* `https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css` → `/_ext/stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css` (1 HTML files)

Tailwind CSS and Bootstrap are under the MIT License. Other third-party resources were left as they were.

## Secret scan

The Phase A §7.2 scan (no `.git`, `.env`, `.ftpconfig`, `.htpasswd`, `debug.log`, `*.php`, `*.sql*`; no `DB_PASSWORD`/`AUTH_KEY`/private keys/`phpinfo()`/`mysql_connect` in any text file) found nothing.

Source: the export tarball `src/www.opendemocracymanitoba.ca.tar.gz`, sha256 `bef07534fe3a043aea860e7b8b072a512b035fb12a5a8aa3b58fa018cd73b41a`.
