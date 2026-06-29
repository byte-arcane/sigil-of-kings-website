if [ -d "_site" ]; then
    #bundle exec jekyll build

    cd _site/
find . -type f | while read -r file; do
    # Remove leading './'
    remote_path="${file#./}"

    echo "Uploading $remote_path..."
    curl --ftp-create-dirs -u "username:password" \
         --ssl-reqd \
         -T "$file" \
         "ftps://ftp.porkbun.com/$remote_path"
done

    lftp -c "
  set ftp:ssl-allow true;
  set ftp:ssl-protect-data true;
  set ftp:ssl-force true;
  set ftp:use-site-utime false;
  set ftp:use-mdtm false;
  set ftp:sync-mode off;
  open -u sigilofkings.com,$FTP_PASS ftp://pixie-ss1-ftp.porkbun.com;
  mirror -R _site/ /public_html;
  quit;
"
fi
