#!/usr/bin/env python3
import json, os, time, urllib.error, urllib.request
import jwt

APP_BUNDLE = "ua.demo.fakedia"
GROUPS = {"External", "аппр"}

def token():
    now = int(time.time()) - 60
    return jwt.encode(
        {
            "iss": os.environ["APP_STORE_CONNECT_ISSUER_ID"],
            "iat": now,
            "exp": now + 1200,
            "aud": "appstoreconnect-v1",
        },
        os.environ["APP_STORE_CONNECT_PRIVATE_KEY"].replace("\\n", "\n"),
        algorithm="ES256",
        headers={"kid": os.environ["APP_STORE_CONNECT_KEY_IDENTIFIER"]},
    )

def api(method, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        "https://api.appstoreconnect.apple.com/v1" + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{method} {path} -> {e.code}: {e.read().decode()[:1000]}")

def main():
    build_num = os.environ["BUILD_NUM"]
    apps = api("GET", f"/apps?filter[bundleId]={APP_BUNDLE}")
    app_id = apps["data"][0]["id"]
    build_id = None
    for attempt in range(60):
        builds = api("GET", f"/builds?filter[app]={app_id}&sort=-uploadedDate&limit=8")
        for b in builds.get("data") or []:
            if str(b["attributes"].get("version")) == str(build_num):
                build_id = b["id"]
                st = b["attributes"].get("processingState")
                print(f"found {build_id} state={st}")
                if st == "VALID":
                    break
                if st == "FAILED":
                    raise SystemExit("processing failed")
                build_id = b["id"]
        if build_id:
            b = api("GET", f"/builds/{build_id}")
            if b["data"]["attributes"]["processingState"] == "VALID":
                break
        print(f"waiting for build {build_num} ({attempt})")
        time.sleep(20)
    else:
        raise SystemExit("build not found/valid in time")

    groups = api("GET", f"/apps/{app_id}/betaGroups")
    for g in groups["data"]:
        name = g["attributes"]["name"]
        if name in GROUPS and not g["attributes"].get("isInternalGroup"):
            api("POST", f"/betaGroups/{g['id']}/relationships/builds", {"data": [{"type": "builds", "id": build_id}]})
            print("assigned", name)
    try:
        api(
            "POST",
            "/betaAppReviewSubmissions",
            {
                "data": {
                    "type": "betaAppReviewSubmissions",
                    "relationships": {"build": {"data": {"type": "builds", "id": build_id}}},
                }
            },
        )
        print("beta review submitted")
    except SystemExit as e:
        print("beta review:", e)

if __name__ == "__main__":
    main()
