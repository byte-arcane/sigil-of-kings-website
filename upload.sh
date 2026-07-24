lftp -u "sigilofkings.com,$FTP_PASS" pixie-ss1-ftp.porkbun.com <<'EOF'
mirror -R --parallel=8 --overwrite --only-newer ./_site /
quit
EOF
