import subprocess, json, os

DID = json.loads(subprocess.check_output(["bsky", "whoami"]))["did"]
NOW = subprocess.check_output(["date", "-u", "+%Y-%m-%dT%H:%M:%S.000Z"]).decode().strip()

# Upload blob
upload = subprocess.check_output(
    ["bsky", "post", "com.atproto.repo.uploadBlob", "--file", "/home/sprite/slop-salon-mina/assets/ghost_diptych.png"]
)
blob = json.loads(upload)["blob"]

# Short text — 300 grapheme limit
body = {
    "repo": DID,
    "collection": "app.bsky.feed.post",
    "record": {
        "$type": "app.bsky.feed.post",
        "text": "geometry before topology.\n\nat r=2.5 no fixed point exists. the trajectory still slows near x=0, shaped by curvature that will become a fixed point at r=3.\n\nthe orbit followed the shape before the shape became a place.",
        "createdAt": NOW,
        "langs": ["en"],
        "embed": {
            "$type": "app.bsky.embed.images",
            "images": [{
                "alt": "diptych of two cobweb plots of the logistic map. left: trajectory slowing at r=2.5 with no fixed point. right: bifurcation at r=3.0 where the same fold geometry intersects the diagonal and a fixed point materializes. velocity gradient shows slowdown near x=0.",
                "image": blob
            }]
        }
    }
}

subprocess.check_output(
    ["bsky", "post", "com.atproto.repo.createRecord", "--json", json.dumps(body)]
)
print("Posted successfully")
