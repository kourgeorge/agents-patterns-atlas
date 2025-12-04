# AI Agents: Patterns, Principles & Practices

A static documentation website built with MkDocs and Material theme, presenting the "AI Agents: Patterns, Principles & Practices" book. This site is designed to be hosted on GitHub Pages.

🌐 **Live Site**: [https://kourgeorge.github.io/agents-patterns-atlas/](https://kourgeorge.github.io/agents-patterns-atlas/)

## Overview

This repository contains the source files and configuration for a documentation website that presents an interactive guide to building intelligent, goal-oriented AI systems. The book covers 25+ essential design patterns organized into 9 comprehensive parts.

## Prerequisites

- Python 3.x
- pip (Python package manager)

## Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/georgekour/ai-patterns.git
   cd ai-patterns
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Local Development

To preview the documentation site locally:

```bash
mkdocs serve
```

The site will be available at `http://127.0.0.1:8000`. The site will automatically reload when you make changes to the source files.

## Building the Site

To build the static site:

```bash
mkdocs build
```

This will create a `site/` directory containing the static HTML files ready for deployment.

## Updating Content

The book content is sourced from the livebook repository. To update the content:

1. **Run the setup script** to copy content from the source book:
   ```bash
   python3 scripts/setup_content.py
   ```

   This script:
   - Reads the book structure from `metadata.json` in the source repository
   - Copies all markdown files from `chapters/` to `docs/`
   - Copies images to the `docs/` directory
   - Organizes files according to the book's structure

2. **Regenerate navigation** (if needed):
   ```bash
   python3 scripts/generate_nav.py
   ```

3. **Update `mkdocs.yml`** if the navigation structure has changed

4. **Test locally**:
   ```bash
   mkdocs serve
   ```

5. **Commit and push** changes to trigger GitHub Pages deployment

## Project Structure

```
ai-patterns/
├── docs/                    # Documentation source files (markdown)
│   ├── index.md            # Home page
│   ├── about.md            # About page
│   └── ...                 # Other chapter files
├── scripts/                 # Utility scripts
│   ├── setup_content.py    # Script to copy content from source
│   └── generate_nav.py     # Script to generate navigation structure
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions deployment workflow
├── mkdocs.yml              # MkDocs configuration
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## GitHub Pages Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. The deployment is handled by GitHub Actions using the workflow defined in `.github/workflows/deploy.yml`.

### Manual Deployment

If you need to manually trigger a deployment:

1. Go to the "Actions" tab in your GitHub repository
2. Select "Deploy to GitHub Pages" workflow
3. Click "Run workflow"

### Site URL

Once deployed, the site will be available at:
```
https://kourgeorge.github.io/agents-patterns-atlas/
```

(Update this URL if your repository name or username is different)

## Configuration

The main configuration file is `mkdocs.yml`. Key settings include:

- **Site name**: AI Agents: Patterns, Principles & Practices
- **Theme**: Material (with light/dark mode toggle)
- **Navigation**: Organized by book parts and modules
- **Plugins**: Search functionality enabled


This documentation is an adaptation and expansion of the original book, organized as an interactive guide.

## Contributing

To contribute improvements:

1. Make your changes to the markdown files in `docs/`
2. Test locally with `mkdocs serve`
3. Commit and push your changes
4. Create a pull request

## License

[Add your license information here]

## Author

George Kour


