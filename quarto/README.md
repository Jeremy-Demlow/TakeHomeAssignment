# Introduction To The Template

This template is for use by the team to create and manage Quarto websites documenting our repositories as website that can be hosted individually and managed as part of the development cycle.

There are several key components to the template, each one will be discussed and outlined below.

## Components

### _quarto.yml

This file contains the website level configuration details for the template, which we'll cover below.

#### Project

```yaml
project:
  type: website
  output-dir: rendered-output
```

This covers the project level configuration details, which for Quarto includes where the rendered results go, as well as the project type.

#### Website

```yaml
website:
  title: "template"
  sidebar:
    style: "docked"
    search: true
    collapse-level: 1
    tools:
      - icon: github
        href: "companyname.com"
        aria-label: GitHub
    contents:
      - href: index.qmd
        text: Project Overview
      - auto: subsection
      - auto: FY23
```

This covers the website specific configurations for the Quarto project. There are several important pieces here which will need to be managed as you work with the project. The first is the website title, this is modified by the ```title``` attribute. The second element is the sidebar. As you add additional sections and pages, you'll need to add them to the ```contents``` section, as needed. Additionally, make sure to modify the GitHub tool href to point to the relevant repository link. For help with sidebars, please reference the Quarto documentation [here](https://quarto.org/docs/websites/website-navigation.html#side-navigation).

#### Format

```yaml
format:
  html:
    theme: cosmo
    css: styles.css
    toc: true
```

This covers the formatting options for the website. More details on what is available here is available in the Quarto [docs](https://quarto.org/docs/reference/formats/html.html). Any choices here are personal preference.

### styles.css

This is the css file used to style the site, you can update this as needed to fit the style guidelines of your project.

### *.qmd

These files make up the actual meet of the documentation site. They use traditional markup for the contents of the page, with options defined in a header fenced by ```---```. Markdown options available in Quarto can be found [here](https://quarto.org/docs/authoring/markdown-basics.html).
