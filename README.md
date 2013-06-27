# Buzz Backend

This is intended to be a supporting application for curating and deploying
"packs" of cards for Buzzwords. Currently, the application is run using the
following command:

    $ python curate.py

When run, it will prompt for a username and password to authenticate to the
master spreadsheet. The credentials will be saved in ~/.buzzbackconfig and
loaded from there if such a file is present. The file takes the form:

    [Credentials]
    email = email@email.com
    password = secret
