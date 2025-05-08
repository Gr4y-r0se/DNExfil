# 🕵️‍♂️ DNExfil

**DNExfil** is a toolset for reconstructing exfiltrated data embedded within DNS queries — a stealthy and resilient data exfiltration vector. It is designed to work with logs captured via **Burp Collaborator**.

---

## 📦 Features

- 🧠 Parses DNS requests containing base64url fragments
- 🔓 Reconstructs exfiltrated files from DNS logs
- ⚙️ Supports sorting using numeric indexes from DNS subdomains
- 🛠 CLI flags for automation, scripting, and HTML `data:` URI generation
- 💻 Lightweight, dependency-free (standard library only)

---

## 🚀 Installation

```bash
git clone https://github.com/yourusername/DNExfil.git
cd DNExfil
python3 dnexfil.py --help
```

---

## ⚙️ Usage

### 🔍 Reconstruct file from Burp DNS log:

```bash
python3 dnexfil.py --input burp_dns_log.csv --output secret_file.txt
```

### 🌐 Convert an HTML file to a base64 data URI:

```bash
python3 dnexfil.py --input payload.html --data-uri
```

---

## 📤 Exporting DNS Log from Burp Collaborator

1. Open **Burp Collaborator Client** inside Burp Suite.
2. Click **"Export as CSV"**.
3. Save the file (e.g., `burp_log.csv`) and pass it to DNExfil:

```bash
python3 dnexfil.py --input burp_log.csv
```

---

## 📝 DNS Payload Format (Expected)

Your exfiltrator (e.g. JavaScript running `fetch()`) should craft DNS queries like:

```
Host: <index>.<binaryMask>.<base64Chunk>.<domain>
```

Example:
```
Host: 012.010101.dGhpcyBpcyBhIHRlc3Q.d.example.net
```

- `012` → index for ordering
- `010101` → binary mask indicating casing
- `dGhpcyBpcyBhIHRlc3Q` → base64url chunk (uncased)
- `d.example.net` → your collaborator domain

`raw.html` provides an example of this. 

---

## 📂 Output

- Reconstructed file (text) is written to `--output` (default: `output.txt`)
- If `--data-uri` is passed, the encoded string is printed to stdout

---

## 📄 License

[MIT License](LICENSE) — use at your own risk. See `LICENSE` file for details.

---

## 🤝 Acknowledgments

- Inspired by covert exfiltration techniques over DNS.
- Integrates seamlessly with Burp Suite's Collaborator for red-team use. (This is noisy though so be warned)

---

🔗 Pull requests and improvements welcome!  
💬 Questions? File an issue or ping [@gr4y-r0se](https://github.com/gr4y-r0se).
