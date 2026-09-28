"""Fetch current LeetCode + GeeksforGeeks stats into docs/stats.json.
A source that fails keeps its previous values, so the resume never breaks."""
import json, re, datetime, urllib.request

PATH, LC_USER, GFG_USER = "docs/stats.json", "SANKAR_JUTURI", "juturisankar"

def http(url, data=None, headers=None):
    h = {"User-Agent": "Mozilla/5.0", **(headers or {})}
    return urllib.request.urlopen(urllib.request.Request(url, data, h), timeout=30).read().decode()

def leetcode():
    q = "query($u:String!){matchedUser(username:$u){submitStatsGlobal{acSubmissionNum{difficulty count}}}}"
    body = json.dumps({"query": q, "variables": {"u": LC_USER}}).encode()
    r = json.loads(http("https://leetcode.com/graphql", body,
                        {"Content-Type": "application/json", "Referer": "https://leetcode.com"}))
    n = {x["difficulty"]: x["count"] for x in r["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]}
    return {"solved": n["All"], "easy": n["Easy"], "medium": n["Medium"], "hard": n["Hard"]}

def gfg():
    html = http(f"https://www.geeksforgeeks.org/profile/{GFG_USER}")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    pp = json.loads(m.group(1))["props"]["pageProps"]
    ui, sub = pp["userInfo"], pp.get("userSubmissionsInfo", {})
    out = {"solved": ui["total_problems_solved"]}
    br = {k.lower(): len(sub.get(k, {})) for k in ("Basic", "Easy", "Medium", "Hard")}
    if sum(br.values()) > 0:          # only trust the breakdown if it parsed
        out.update(br)
    return {k: v for k, v in out.items() if v is not None}

stats = json.load(open(PATH))
ok = False
for key, fn in (("leetcode", leetcode), ("gfg", gfg)):
    try:
        stats[key].update(fn()); ok = True
        print(f"{key}: updated -> {stats[key]}")
    except Exception as e:
        print(f"WARNING {key}: fetch failed ({e!r}); keeping previous values")
if ok:
    stats["updated"] = datetime.date.today().isoformat()
    json.dump(stats, open(PATH, "w"), indent=2)
