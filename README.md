# django-dominate

Test to see if [dominate](https://github.com/Knio/dominate/) can be used as a replacement for django templates.

## Setup

```plain
$ pipenv sync --dev
$ pipenv run python ./tstprj/manage.py runserver
```

## Overview

Django creates HTML documents using HTML template files and context data provided by the view.
A template engine (e.g. `DjangoTemplates`) takes a template file and context data as an input and generates the final HTML string.

Dominate uses python classes and context manager magic to describe the structure of HTML documents and provides a `render()` method to convert that structure into a HTML string.

Django supports custom template backends.
Template engine backend classes must implement a `get_template(template_name)` method that returns a `Template` object for the given template name string.
The template name is not restricted in any way.
The returned `Template` object must implement a `render(context)` method, which will render the template with view-specific data to a string.

This project includes

- a django template engine backend that accepts python paths in template names and uses dominate-based classes to render the final document
- a set of base classes to describe HTML documents in a composable way, similar to django template blocks

## Example

### Step 1: Configure dominate template engine in `settings.py`:

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        [...]
    },
    {
        "BACKEND": "testapp.dominate.Dominate",
        "DIRS": [],
        "APP_DIRS": False,
        "OPTIONS": {},
    },
]
```

Note that `DIRS`, `APP_DIRS` and `OPTIONS` are not required but otherwise some parts in django seem to complain.

### Step 2: Describe HTML document using dominate

To e.g. create a new HTML page that includes bootstrap:

```python7
class ApplicationPage(BootstrapPage):
    def title(self, context):
        return "Application"

    def body(self, context):
        p("Hello World")
```

The Project provides the following classes:

- `HTMLPage` - base class that works together with the template engine and implements `render(context)` to create the final document string
- `BootstrapPage` - inherits from `HTMLPage` and adds bootstrap `<style>` and `<script>` references
- `ApplicationPage` - inherits from `BootstrapPage`, example for an application base page that adds application `<style>` and `<script>` references and shows different content based on the user agent
- `ApplicationLoggedInPage` - inherits from `ApplicationPage`, example for an application specific page, adds bootstrap navigation bar

### Step 3: Django view

Create a template view using a specific engine:

```python
class ApplicationPageView(TemplateView):
    template_name = "testapp.pages.ApplicationPage"
    template_engine = "dominate"
```

And add to `urls.py`:

```python
urlpatterns = [
    [...]
    path("bootstrap-page", BootstrapPageView.as_view(), name="bootstrap-page"),
]
```
