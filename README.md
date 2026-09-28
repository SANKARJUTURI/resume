# Auto-updating resume site
1. Create a GitHub repo, push this folder to it.
2. Settings → Pages → Deploy from branch → `main` / `/docs`.
3. Actions tab → "Daily stats + resume update" → Run workflow (first test). Check the log for LeetCode/GFG lines.
Your page: https://<username>.github.io/<repo>/  (PDF at /Sankar_Resume.pdf)
Edit resume text in build_resume.py; numbers come from docs/stats.json.
