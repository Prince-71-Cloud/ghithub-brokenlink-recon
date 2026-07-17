## 🔗 GitHub Broken Link Scanner

Scans public GitHub repositories for broken links found across source files.

### Features

- 🔍 Scans public repositories of a user/org
- 📄 Walks the default-branch file tree for each repository
- 🔗 Extracts URLs from source files across the repository
- 🔍 Validates URLs through a local backend with HEAD and GET fallback
- ✅ Classifies links as `valid`, `broken`, or `review`
- 🚫 Identifies broken links (4xx, 5xx, network errors)
- 📊 Real-time scan progress
- 📁 Export results as CSV
- 🔑 Requires GitHub Personal Access Token (repo scope)

### Quick Start

1. Install Python 3 on the machine that will host the scanner.
2. Clone this repository.
3. Start the scanner server:

```bash
python3 server.py
```

4. Open `http://127.0.0.1:8000/broken-link-scanner.html`
5. Enter a GitHub Personal Access Token with `repo` scope.
6. Enter a GitHub username or organization.
7. Click `Start Scanning`.
8. Use the `Valid / Invalid / All` filter in the Review Sheet as needed.
9. Click `Download CSV` to export the visible rows.

### Requirements

- GitHub Personal Access Token with `repo` scope
- Modern browser with JavaScript enabled
- Python 3 for the local backend validator

### Self-Hosting

This scanner needs a small backend because URL validation runs through `/api/validate-url`.
The simplest setup is to host the repo on your own server and run:

```bash
python3 server.py --port 8000
```

Then open the scanner in a browser on the same host.

If you want to deploy it behind your own domain or reverse proxy, make sure the server can:

- serve `broken-link-scanner.html`
- serve the `assets/` files
- respond to `POST /api/validate-url`

The frontend reads that API from the same origin when the page is hosted over HTTP(S).

### Notes

- Only public repositories are scanned
- Requires a GitHub token (rate limits are too low without one)
- URL validation runs through `server.py` and uses HEAD with GET fallback
- Binary and large files are skipped
- GitHub tree responses can be truncated on very large repositories
- The scanner is not fully static by itself; it needs `server.py` or an equivalent API host

---

## 📁 Project Structure

```
ghithub-brokenlink-recon/
├── index.html                    # GHIntel React app entry
├── broken-link-scanner.html      # GitHub Broken Link Scanner
├── server.py                     # Local backend validator + static server
├── assets/
│   ├── index-OOTXXkeu.js         # GHIntel React app bundle
│   └── index-DPHGUY3Y.css        # GHIntel styles
└── README.md
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

Run `python3 server.py`, then open `http://127.0.0.1:8000/broken-link-scanner.html`.

### Optional: Custom Port

```bash
python3 server.py --port 8080
```

Then open `http://127.0.0.1:8080/broken-link-scanner.html`.

---

## ⚠️ Legal & Ethics

- Only scans **public** GitHub data
- Requires explicit user consent (user provides their own token)
- Use responsibly and in accordance with GitHub's Terms of Service
- Respect rate limits and GitHub's API guidelines
- Do not use for unauthorized reconnaissance

---

## 🤝 Credit

Developed by Aman Bhuiyan, a bug bounty hunter and security researcher known as `IceCream`.

GitHub: [Prince-71-Cloud](https://github.com/Prince-71-Cloud)

---

## 📝 License

No separate `LICENSE` file is included in this snapshot.
