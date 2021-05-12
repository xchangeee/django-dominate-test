from django.views.generic import TemplateView


class BootstrapPageView(TemplateView):
    template_name = "testapp.pages.BootstrapPage"
    template_engine = "dominate"


class ApplicationPageView(TemplateView):
    template_name = "testapp.pages.ApplicationPage"
    template_engine = "dominate"


class ApplicationLoggedInView(TemplateView):
    template_name = "testapp.pages.ApplicationLoggedInPage"
    template_engine = "dominate"

