## 🔗 GitHub Broken Link Scanner

Scans GitHub repositories for broken links in commit histories.

### Features

- 🔍 Scans public repositories of a user/org
- 📄 Parses commits and file changes per repository
- 🔗 Extracts URLs from commit diffs and file contents
- 🔍 Validates URLs via HEAD requests (with redirect following)
- 🚫 Identifies broken links (4xx, 5xx, network errors)
- 📊 Real-time scan progress
- 📁 Export results as CSV
- 🔑 Requires GitHub Personal Access Token (repo scope)

### Usage

1. Open `broken-link-scanner.html` in a browser
2. Enter a GitHub Personal Access Token (with `repo` scope)
3. Enter a GitHub username or organization
4. Click `Start Scan`
5. View results in real-time
6. Click `Export Results as CSV` to download

### Requirements

- GitHub Personal Access Token with `repo` scope
- Modern browser with JavaScript enabled

### Notes

- Only public repositories are scanned
- Requires a GitHub token (rate limits are too low without one)
- URL validation uses HEAD requests with 5 redirects max, 8s timeout
- Rate limited to 100 URLs checked per scan to avoid abuse

---

## 📁 Project Structure

```
ghintel-main/
├── index.html                    # GHIntel - GitHub Commits Email Finder (React app entry)
├── broken-link-scanner.html      # GitHub Broken Link Scanner (standalone HTML)
├── assets/
│   ├── index-OOTXXkeu.js         # GHIntel React app bundle
│   └── index-DPHGUY3Y.css        # GHIntel styles
└── .claude/                      # Claude Code configuration
```

---

## 🔧 Local Development

### GHIntel (React App)

```bash
# Serve the built assets
npx serve .
# or
python3 -m http.server 8000
```

Then open `http://localhost:8000`

### Broken Link Scanner

Simply open `broken-link-scanner.html` in a browser.

---

## ⚠️ Legal & Ethics

- Only scans **public** GitHub data
- Requires explicit user consent (user provides their own token)
- Use responsibly and in accordance with GitHub's Terms of Service
- Respect rate limits and GitHub's API guidelines
- Do not use for unauthorized reconnaissance

---

## 📝 License

MIT License - See LICENSE file for details
