#!/usr/bin/env python3
"""Upload carousel slides or a Reel to Cloudinary and print public URLs.

Instagram's API only accepts media at a public https URL, so every image or
video has to live somewhere public before n8n can post it.

    export CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>
    python3 upload.py carousel/slide-*.png --folder ig/2026-10-28-carousel
    python3 upload.py reel.mp4 --folder ig/2026-10-28-reel

Prints the URLs comma-separated, ready to paste into the media_urls column.
"""

import argparse
import hashlib
import json
import mimetypes
import os
import sys
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path


def creds():
    raw = os.environ.get("CLOUDINARY_URL", "")
    u = urllib.parse.urlparse(raw)
    if u.scheme != "cloudinary" or not (u.username and u.password and u.hostname):
        sys.exit("Set CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name> (Cloudinary dashboard).")
    return u.username, u.password, u.hostname


def sign(params, secret):
    payload = "&".join(f"{k}={params[k]}" for k in sorted(params))
    return hashlib.sha1((payload + secret).encode()).hexdigest()


def upload(path, folder, key, secret, cloud):
    kind = "video" if (mimetypes.guess_type(path)[0] or "").startswith("video") else "image"
    params = {"timestamp": str(int(time.time())), "folder": folder, "public_id": Path(path).stem}
    fields = dict(params, api_key=key, signature=sign(params, secret))
    boundary = uuid.uuid4().hex
    body = b""
    for k, v in fields.items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
             f"filename=\"{Path(path).name}\"\r\nContent-Type: {ctype}\r\n\r\n").encode()
    body += Path(path).read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(f"https://api.cloudinary.com/v1_1/{cloud}/{kind}/upload", data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)["secure_url"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--folder", default="instagram")
    args = ap.parse_args()
    key, secret, cloud = creds()
    urls = [upload(f, args.folder, key, secret, cloud) for f in sorted(args.files)]
    print(",".join(urls))


if __name__ == "__main__":
    main()
