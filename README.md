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

# Pack Deployment Instructions

This script should be used for all pack deployments: updates and new packs.

# Word Review Checklist

1. Look over the word database and verify the following.
    1. Run spellcheck!
    1. All IDs for words are unique
    1. Pack title is appropriate for display

## New Pack Process

First test this deployment process without step 1!

1. Follow the Word Review Checklist
1. Make sure the icon is uploaded to Amazon S3 in packs/icons/ directory
and correctly permissioned.
1. Open aws.py and modify the PACKDATA_DIR to the production directoy.
1. Modify the aws.upload_pack function to the correct meta data for the new pack.

        {"_id": 100-149 for standard purchasable packs,
        "name": name,
        "path": "packs/" + filename + ".json",
        "icon_path": "packs/icons/packicon_classic1.png",
        "description": <VIEWABLE DESCRIPTION OF PACK>,
        "size": <NUMBER OF CARDS>,
        "purchase_type": <ALL PURCHASABLE PACKS ARE 1>,
        "version": 1,
        "action_string": "BUY"}

1. Run python buzzbackend/ and follow in-app instructions.
1. Verify that the shipped pack words in the spreadsheet are marked as shipped.

    *FREE PACKS:* Even free packs should probably be purchase_type 1. This is because
    Amazon lets you do free entitled content. Players will have it tied to their
    account so we can charge later if we want.

1. Go to Amazon Mobile Developers console and add the IAP item, with correct
path for pack icon along with other meta data.


## Pack Update Process

First test this deployment process without step 1!

1. Follow the Word Review Checklist
1. Open aws.py and modify the PACKDATA_DIR to the production directoy.
1. Run python buzzbackend/ and follow in-app instructions.
1. Verify that the shipped pack words in the spreadsheet are marked as shipped.
1. At this point, new installs will get the pack, but existing installs won't.
To push this to existing installs, manually tick up the version number in
packs.json so they'll be recognized as needing an update.
