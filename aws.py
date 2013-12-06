#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# Library:   buzzbackend
#
# Copyright 2013 Siramix Labs
#
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 ( the "License" );
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################

from boto.s3.key import Key
from boto.s3.connection import S3Connection
import json

# S3 bucket we're using
BUCKET_NAME = 'siramix.buzzwords'
PACKDATA_DIR = 'bw-packdata-test'

def get_pack_key():
    """Get the json index from aws.
    """
    conn = S3Connection()
    bucket = conn.get_bucket(BUCKET_NAME)
    return bucket.get_key('%s/packs.json' % PACKDATA_DIR)

def upload_file(path, contents):
    """Upload a file to S3 given the name and contents.
    """
    conn = S3Connection()
    bucket = conn.get_bucket(BUCKET_NAME)
    pack_key = Key(bucket)
    pack_key.key = path
    pack_key.set_contents_from_string(contents)
    return pack_key


def upload_pack(name, filename, contents):
    """Upload the pack and update the index.
    """
    pack_key = get_pack_key()
    pack_contents = pack_key.get_contents_as_string()
    pack_found = False

    for line in pack_contents.split('\n'):
        cur_pack = json.loads(line)
        if cur_pack['path'] == 'packs/%s.json' % filename:
            pack_found = True
            print "Pack already exists. Make sure version and " \
            "other meta data is updated if making an update."
    if not pack_found:
        print "Pack does not exist. Adding new pack to packs.json."
        new_pack = {"_id": 1111,
                    "name": name,
                    "path": "packs/" + filename + ".json",
                    "icon_path": "packs/icons/packicon_classic1.png",
                    "description": "Test pack",
                    "size": 10,
                    "purchase_type": 1,
                    "version": 1,
                    "price": "BUY"}
        pack_contents += '\n' + json.dumps(new_pack)
        print "Pack index added: %s" % json.dumps(new_pack)

    pack_index_path = '%s/packs.json' % (PACKDATA_DIR)
    pack_key = upload_file(pack_index_path, pack_contents)
    pack_key.set_acl('public-read')
    print "Pack index file pushed to %s." % pack_index_path
    carddata_path = '%s/packs/%s.json' % (PACKDATA_DIR, filename)
    carddata_key = upload_file(carddata_path, contents)
    carddata_key.set_acl('public-read')
    print "Pack file pushed to %s." % (carddata_path)


def delete_logs():
    """Delete log files from S3.
    """
    conn = S3Connection()
    bucket = conn.get_bucket(BUCKET_NAME)
    for key in bucket.list():
        if 'bw' not in key.name:
            key.delete()
