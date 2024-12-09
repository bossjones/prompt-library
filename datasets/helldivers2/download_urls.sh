#!/usr/bin/env bash

python parse_sitemap.py

mkdir -p helldivers_wiki || true

while IFS= read -r url
do
    wget --wait=1 --random-wait --no-clobber --no-check-certificate \
         --directory-prefix=helldivers_wiki \
         --reject "index.php*,api.php*,rest.php*,*?action=*,*?veaction=*,*?diff=*,*?oldid=*,*?curid=*,*?search=*,*?feed=*,*?from=*,*?redirect=*,*?pagefrom=*,*?filefrom=*,*?uselang=*,*?useskin=*,*?printable=*,Special:*,Special%3A*,special:*,MediaWiki:*,Data:*,Data%3A*" \
         "$url"
done < urls_to_download.txt
