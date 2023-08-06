# Material VA Lighthouse Plugin

This plugin styles a Material for MKDocs site using CSS from the [VA Design System](https://design.va.gov/).

## Installation
Open a terminal and run the following command:

```bash
pip install material-va-lighthouse
```

Or add the following to your `requirements.txt` file:

```text
material-va-lighthouse
```

Update your `mkdocs.yml` to include the plugin:

```yaml
plugins:
  - material-va-lighthouse
```

Update the `theme` section. Set `material` as your theme (if you're not already) 
and point the logo to the Lighthouse logo from this plugin:


```yaml
theme:
  name: material
  logo: 'assets/images/va_lighthouse_logo.png'
```

Then add an `extra_css` section to your `mkdocs.yml` that points to the CSS file from this plugin:

```yaml
theme:
  name: material
  logo: 'assets/images/va_lighthouse_logo.png'
extra_css:
  - 'assets/stylesheets/va_lighthouse.css'
```

Run `mkdocs build` and `mkdocs serve` to see the changes.
