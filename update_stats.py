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

def _block(txt, key):
    """Return the JSON object that follows '"key":' in txt (balanced braces)."""
    m = re.search(rf'"{key}"\s*:\s*\{{', txt)
    if not m:
        return None
    i = m.end() - 1; depth = 0
    for j in range(i, len(txt)):
        depth += (txt[j] == "{") - (txt[j] == "}")
        if depth == 0:
            try:
                return json.loads(txt[i:j + 1])
            except ValueError:
                return None

def _parse_gfg(html):
    txt = html.replace('\\"', '"')          # un-escape Next.js flight data
    n = re.search(r'"total_problems_solved"\s*:\s*"?(\d+)', txt)
    if not n:
        return None
    out = {"solved": int(n.group(1))}
    br = {}
    for k in ("School", "Basic", "Easy", "Medium", "Hard"):
        b = _block(txt, k)
        br[k.lower()] = len(b) if isinstance(b, dict) else 0
    if sum(br.values()) == out["solved"]:      # sanity check: must add up
        out.update({k: v for k, v in br.items() if k != "school"})
    else:
        print(f"note: GFG breakdown {br} != total {out['solved']}; keeping old breakdown")
    return out

def gfg():
    for url in (f"https://www.geeksforgeeks.org/profile/{GFG_USER}",
                f"https://www.geeksforgeeks.org/user/{GFG_USER}/"):
        html = http(url)
        out = _parse_gfg(html)
        if out:
            return out
        print(f"debug: {url} -> {len(html)} bytes, "
              f"next_data={'__NEXT_DATA__' in html}, has_total={'total_problems_solved' in html}")
    raise RuntimeError("could not find GFG stats in profile page")

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