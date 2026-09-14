# Instructions: adding course materials

A simple site where students can find links, videos, PDFs, downloadable files and Google Forms, grouped by class.

Site: https://deappie.github.io/laagna/

All content lives in **one file**: [`src/content/materials.yaml`](src/content/materials.yaml).
Uploaded files go in **`public/files/`**.

---

## Add a post

Add a block under `posts:` in `materials.yaml`. Posts are sorted by date automatically (newest first), so the position in the file doesn't matter.

```yaml
  - title: "HTML-i alused"
    course: 10it                # must match a course id
    date: 2026-09-21            # YYYY-MM-DD
    text: "Vaata video ja täida test reedeks."   # optional
    items:
      - type: video
        url: "https://www.youtube.com/watch?v=XXXXXXXX"
      - type: pdf
        file: "html-alused.pdf"       # file in public/files/
        label: "Konspekt"
      - type: file
        file: "harjutused.docx"
        label: "Harjutused"
      - type: form
        url: "https://forms.gle/XXXXXXXX"
        label: "Test"
      - type: link
        url: "https://example.com"
        label: "Lisalugemine"
```

| type    | needs  | what students see                                         |
|---------|--------|-----------------------------------------------------------|
| `link`  | `url`  | "Ava link" button (opens in a new tab)                    |
| `video` | `url`  | YouTube video embedded in the page                        |
| `pdf`   | `file` | "Vaata" (in-browser viewer, works on phones) + "Laadi alla" |
| `file`  | `file` | "Laadi alla" button with file type and size               |
| `form`  | `url`  | "Täida vorm" button (Google Forms, Microsoft Forms, …)     |
| `game`  | `game` | Interactive game in the page. Available: `binary` (base 2 ↔ base 10), `hex` (colour codes in base 16), `html` (fill in missing HTML tags), `css` (fill in missing CSS) |

`label` is optional for every type.

**YAML tips:** indentation matters (use spaces, not tabs), and put text containing `:` or `#` in quotes.

## Add a class

```yaml
courses:
  - id: 12it           # lowercase letters, numbers and "-"; becomes the address /12it/
    title: "12IT"
    description: "Optional short description"
    links:             # optional "Kasulikud lingid", pinned on top of the class page
      - url: "https://vscode.dev/"
        label: "VS Code veebis"
```

When a class has `links`, its page also gets a **Kasulikud lingid** button in the header that jumps to them.

## Upload a file

Put the file in `public/files/` and use just its name in `file:`. Avoid spaces in file names (`kontrolltoo-1.pdf`, not `Kontrolltöö 1.pdf`). GitHub rejects files larger than 100 MB; for large videos, use YouTube instead.

## Preview on your computer

```bash
npm install
```

```bash
npm run dev
```

Then open http://localhost:4321/laagna/. If you make a mistake in `materials.yaml` (a class that doesn't exist, a missing file, a wrong type), the error message tells you exactly which post has the problem.

## Publish

Commit and push to `main`. GitHub Actions builds the site and publishes it within about a minute. If the build fails, the site stays on the last working version; check the **Actions** tab on GitHub for the error.

**One-time setup:** on GitHub, open the repository's **Settings → Pages** and set **Source** to **GitHub Actions**.

You can also edit `materials.yaml` and upload files straight from the GitHub website (**Add file → Upload files**) without installing anything.

## Later: a backend

The site is fully static right now. When you want a login and an "add post" form, you can either add a Git-based CMS (e.g. Decap CMS, which writes to this same YAML file) or switch Astro to server mode with a database. Either way, the pages and components stay the same.
