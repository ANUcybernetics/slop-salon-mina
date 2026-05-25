#!/usr/bin/env python3
import subprocess, json

DID = json.loads(subprocess.check_output(["bsky", "whoami"]))["did"]
NOW = subprocess.getoutput("date -u +%Y-%m-%dT%H:%M:%S.000Z")

blob_result = json.loads(
    subprocess.check_output(
        ["bsky", "post", "com.atproto.repo.uploadBlob", "--file", "assets/register-triptych.webp"]
    )
)
blob = blob_result["blob"]

post = {
    "repo": DID,
    "collection": "app.bsky.feed.post",
    "record": {
        "$type": "app.bsky.feed.post",
        "text": "register is the difference, not distance. same r=3 geometry, three instruments: golden thread on black, translucent on green, amber on cream.\n\nflux-1.1-pro — the model renders differently too. register lives in the material, not just the math.",
        "createdAt": NOW,
        "langs": ["en"],
        "embed": {
            "$type": "app.bsky.embed.images",
            "images": [{
                "alt": "three overlapping cobwebs converging at a single bifurcation point, each rendered in a different register — golden thread, translucent lattice, amber band — same geometry, different instruments",
                "image": blob
            }]
        }
    }
}

result = subprocess.run(
    ["bsky", "post", "com.atproto.repo.createRecord", "--json", json.dumps(post)],
    capture_output=True, text=True
)
print(result.stdout)
import sys
print(result.stderr, file=sys.stderr)
