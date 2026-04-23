# Copilot Instructions

## Project Overview

This is a documentation-only site — a guide for teams migrating from Azure DevOps to GitHub. It is published via GitHub Pages using Jekyll and contains no application code, tests, or build tooling beyond the Pages deployment.

## Architecture

- `docs/` — Jekyll source directory (this is what GitHub Pages builds)
  - `index.md` — Main content, written in Markdown with YAML front matter
  - `_layouts/default.html` — Single-page HTML layout with inline CSS and JS
  - `_config.yml` — Jekyll configuration
- `.github/workflows/pages.yml` — Deploys the site on pushes to `main` that touch `docs/`

## Conventions

### Content pages

- All content pages are Markdown files in `docs/` with YAML front matter specifying `layout: default`
- Jekyll converts Markdown to HTML at build time; no pre-built HTML is committed

### Theme system

- Light/dark mode is handled entirely in `docs/_layouts/default.html` via CSS custom properties (variables) on `:root` and `[data-theme="dark"]`
- The site defaults to the user's system theme (`prefers-color-scheme`) and allows manual toggle, persisted in `localStorage`
- Two-tone background: the outer page background (`--page-bg`) is slightly different from the content area (`--content-bg`)
- When adding new styled elements, define colors as CSS custom properties in both the `:root` (light) and `[data-theme="dark"]` blocks

### Deployment

- GitHub Pages is configured to deploy via GitHub Actions (not the legacy branch-based source)
- The workflow triggers on pushes to `main` that change files under `docs/`, or via manual `workflow_dispatch`
- Jekyll build output (`_site/`, `.jekyll-cache/`) is gitignored and only exists in CI
