# REMEMBER! Change the EXPECTED_ID to the user running the www-data
gcc forward_app.c
chown :www-data a.out
chmod o-rx a.out
chmod u+s a.out