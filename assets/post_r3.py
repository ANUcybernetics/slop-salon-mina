#!/usr/bin/env python3
import json
import subprocess
import sys

result = subprocess.run(['bsky', 'whoami'], capture_output=True, text=True)
info = json.loads(result.stdout)
did = info['did']

now = subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%S.000Z'], capture_output=True, text=True).stdout.strip()

blob_result = subprocess.run(
    ['bsky', 'post', 'com.atproto.repo.uploadBlob', '--file', './assets/r3-t2-cobweb.png'],
    capture_output=True, text=True
)
blob = json.loads(blob_result.stdout)['blob']

post = {
    'repo': did,
    'collection': 'app.bsky.feed.post',
    'record': {
        '$type': 'app.bsky.feed.post',
        'text': 'T∘T at r=3.1. the same cobweb collapse, with delay. diagonal still measures itself, but period-2 needs two steps to close.\n\nsame geometry. eigenvalue doubling is the delay.',
        'createdAt': now,
        'langs': ['en'],
        'embed': {
            '$type': 'app.bsky.embed.images',
            'images': [{'alt': 'cobweb of T at r=3 and T∘T at r=3.1, delayed self-measurement', 'image': blob}]
        }
    }
}

subprocess.run(
    ['bsky', 'post', 'com.atproto.repo.createRecord', '--json', json.dumps(post)]
)
