# sakibchowdhury131.github.io

Personal academic portfolio website for Sakib Chowdhury — M.Sc. student in Robotics at Stevens Institute of Technology and Machine Learning Engineer at Celloscope. The site showcases research, projects, publications, and contact information.

## Features

- About page with biography and research focus (robot motion control, high-speed manipulator controllers)
- Research page describing ongoing and past research work
- Projects page with interactive project cards (images/videos, descriptions, tech tags)
- Publications page listing academic papers
- Resume page with downloadable PDF resume
- Contacts page
- Responsive layout using the Kube CSS framework

## Tech Stack

- HTML5, CSS3, JavaScript
- [Kube CSS Framework](https://imperavi.com/kube/)
- Font Awesome icons
- Google Fonts (Playfair Display SC, Lato)
- Sass/SCSS for custom styles

## Project Structure

| File / Directory | Description |
|---|---|
| `index.html` | Main landing / About page |
| `research.html` | Research overview page |
| `projects.html` | Projects showcase page |
| `publications.html` | Publications listing page |
| `resume.html` | Resume page |
| `contacts.html` | Contact information page |
| `css/` | Compiled CSS files (Kube, Font Awesome, custom) |
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
