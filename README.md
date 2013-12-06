# Buzz Backend

This is intended to be a supporting application for curating and deploying
"packs" of cards for Buzzwords. Currently, the application is run using the
following command (with buzzbackend somewhere that python can find it):

    $ python -m buzzbackend

When run, it will prompt for a username and password to authenticate to the
master spreadsheet. The credentials will be saved in ~/.buzzbackconfig and
loaded from there if such a file is present. The file takes the form:

    [Credentials]
    email = email@email.com
    password = secret

Note that if you use Google's 2 Step Verification you will need to generate an
application specific password and use that.

When deploying packs to AWS, you need to make sure that you set up the
necessary access keys as such:

    export AWS_ACCESS_KEY_ID=<key>
    export AWS_SECRET_ACCESS_KEY=<key>

# Deployment Instructions

This script should be used for all pack deployments: updates and new packs.

1. First open aws.py and modify the PACKDATA_DIR to the production directoy.
2. Run python buzzbackend/ and follow in-app instructions.