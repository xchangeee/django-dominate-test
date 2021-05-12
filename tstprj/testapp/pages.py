import dominate
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from dominate import tags as T
from dominate.util import text


class HTMLPage:
    def render(self, context):
        doc = dominate.document(title=self.title(context))
        with doc.head:
            self.meta(context)
            self.style(context)
            self.script(context)
        with doc:
            self.body(context)
        return doc.render()

    def title(self, context):
        return "HTML Document"

    def meta(self, context):
        T.meta(charset="utf-8")

    def style(self, context):
        pass

    def script(self, context):
        pass

    def body(self, context):
        pass


class BootstrapPage(HTMLPage):
    def title(self, context):
        return "Bootstrap Document"

    def meta(self, context):
        super().meta(context)
        T.meta(name="viewport", content="width=device-width, initial-scale=1, shrink-to-fit=no")

    def style(self, context):
        super().style(context)
        T.link(
            rel="stylesheet",
            href=staticfiles_storage.url("vendor/bootstrap/4.3.1/css/bootstrap.min.css"),
            integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
            crossorigin="anonymous",
        )
        T.link(
            rel="stylesheet", href=staticfiles_storage.url("vendor/font-awesome/4.7.0/css/font-awesome.min.css"),
        )

    def script(self, context):
        super().script(context)
        T.script(
            src=staticfiles_storage.url("vendor/jquery/3.3.1/jquery-3.3.1.slim.min.js"),
            integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
            crossorigin="anonymous",
            defer=True,
        )
        T.script(
            src=staticfiles_storage.url("vendor/popper.js/1.14.7/popper.min.js"),
            integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1",
            crossorigin="anonymous",
            defer=True,
        )
        T.script(
            src=staticfiles_storage.url("vendor/bootstrap/4.3.1/js/bootstrap.min.js"),
            integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM",
            crossorigin="anonymous",
            defer=True,
        )

    def body(self, context):
        pass


class ApplicationPage(BootstrapPage):
    def title(self, context):
        return "Application"

    def meta(self, context):
        super().meta(context)

    def style(self, context):
        super().style(context)
        T.link(rel="stylesheet", href=staticfiles_storage.url("app/css/site.css"))

    def script(self, context):
        super().script(context)
        T.script(src=staticfiles_storage.url("app/js/site.js"), defer=True),

    def body(self, context):
        if context["request"].user_agent.browser.family == "IE":
            with T.main(role="main", className="container py-4"):
                with T.div(className="row justify-content-center mb-3"):
                    with T.div(className="col-8"):
                        with T.div(className="alert alert-primary"):
                            text("Use ")
                            T.a("Chrome", href="https://www.google.com/chrome/")
                            text(" or ")
                            T.a("Firefox", href="https://www.mozilla.org/de/firefox/browsers/")
                            text(" instead")
        else:
            self.content(context)

    def content(self, context):
        pass


class ApplicationLoggedInPage(ApplicationPage):
    def content(self, context):
        with T.nav(className="navbar navbar-expand-md navbar-dark bg-dark fixed-top"):
            T.a("YoloApp", className="navbar-brand", href=reverse("logged-in-page"))

            T.button(
                T.span(className="navbar-toggler-icon"),
                type="button",
                className="navbar-toggler",
                aria_controls="navbarsExampleDefault",
                aria_expanded="false",
                aria_label="Toggle navigation",
                data_toggle="collapse",
                data_target="#navbarsExampleDefault",
            )
            with T.div(className="collapse navbar-collapse", id="navbarsExampleDefault"):
                # Navbar buttons
                with T.ul(className="navbar-nav"):
                    pass

                # User Menu on the right
                with T.ul(className="navbar-nav ml-auto"):
                    with T.li(className="nav-item dropdown"):
                        T.a(
                            str(context["request"].user),
                            href="#",
                            className="nav-link dropdown-toggle",
                            role="button",
                            aria_haspopup="true",
                            aria_expanded="false",
                            data_toggle="dropdown",
                        )
                        with T.div(className="dropdown-menu dropdown-menu-right"):
                            T.a(
                                T.i(className="fa fa-fw fa-sign-out", aria_hidden="true"),
                                text(" Logout"),
                                className="dropdown-item",
                                href=reverse("logged-in-page"),
                            )

        with T.main(role="main", className="container", style="margin-top:70px"):
            self.main(context)

    def main(self, context):
        pass
