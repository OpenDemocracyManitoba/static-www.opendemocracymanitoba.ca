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

## Secret scan

The Phase A §7.2 scan (no `.git`, `.env`, `.ftpconfig`, `.htpasswd`, `debug.log`, `*.php`, `*.sql*`; no `DB_PASSWORD`/`AUTH_KEY`/private keys/`phpinfo()`/`mysql_connect` in any text file) found nothing.

Source: the export tarball `src/www.opendemocracymanitoba.ca.tar.gz`, sha256 `bef07534fe3a043aea860e7b8b072a512b035fb12a5a8aa3b58fa018cd73b41a`.
