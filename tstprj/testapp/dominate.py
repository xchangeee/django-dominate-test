from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.backends.base import BaseEngine
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy
from django.utils.module_loading import import_string


class Dominate(BaseEngine):
    def __init__(self, params):
        params = params.copy()
        options = params.pop("OPTIONS").copy()
        super().__init__(params)

    def get_template(self, template_name):
        try:
            document_cls = import_string(template_name)
            return Template(document_cls())
        except ImportError as exc:
            raise TemplateDoesNotExist(exc.name, backend=self) from exc
        # TODO IntendationError raised when code cannot be parsed
        # except jinja2.TemplateSyntaxError as exc:
        #    new = TemplateSyntaxError(exc.args)
        #    new.template_debug = get_exception_info(exc)
        #    raise new from exc


class Template:
    def __init__(self, document):
        self.document = document

    def render(self, context=None, request=None):
        if context is None:
            context = {}
        if request is not None:
            context["request"] = request
            context["csrf_input"] = csrf_input_lazy(request)
            context["csrf_token"] = csrf_token_lazy(request)
        return self.document.render(context)
