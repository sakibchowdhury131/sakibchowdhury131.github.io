# sakibchowdhury131.github.io

Personal academic portfolio website for Sakib Chowdhury — PhD student in Robotics at Stevens Institute of Technology, formerly Machine Learning Engineer at Celloscope. The site is a single scrolling homepage that showcases research, projects, publications, experience, and contact information as small linked blocks, with anchor-based navigation (`#about`, `#research`, `#projects`, `#publications`, `#experience`, `#contact`).

## Features

- Single-page layout: About/bio, News, Research, Projects, Publications, Experience, Education, Honors, Contact
- Research and Projects rendered as image/video + description blocks, each linking out to a full write-up when one exists
- Publications rendered as a compact citation list (title, authors, venue, PDF link, one-line description)
- Deep-dive project write-ups live under `projects/` and are linked from the homepage
- Resume page with downloadable PDF resume
- Self-contained, dependency-light CSS (no framework) embedded in `index.html`

## Tech Stack

- HTML5, CSS3, JavaScript
- Font Awesome icons
- Google Fonts (Playfair Display, Lato)
- Legacy pages (`resume.html`, `projects/*.html`) still use the [Kube CSS Framework](https://imperavi.com/kube/) / Sass build below

## Project Structure

| File / Directory | Description |
|---|---|
| `index.html` | Single-page site: about, research, projects, publications, experience, education, honors, contact |
| `resume.html` | Resume page |
| `projects/` | Standalone deep-dive write-ups for individual research projects, linked from `index.html` |
| `css/` | Compiled CSS files (Kube, Font Awesome, custom) used by legacy/subpages |
| `scss/` | Source SCSS files |
| `js/` | JavaScript files |
| `img/` | Images (avatar, project images) |
| `fonts/` | Font files |
| `sakib_resume.pdf` | Downloadable resume PDF |

## Local Development

No build step is required to view the site. Simply open `index.html` in a browser.

To recompile SCSS:

```bash
sass scss/custom.scss css/custom.min.css
```

## License

MIT
