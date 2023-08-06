from abc import ABC
from flowtask.utils import cPrint
from flowtask.template import (
    getTemplateHandler,
    TemplateHandler
)

class TemplateSupport(ABC):
    """TemplateSupport.

    Adding Support for Jinja2 Template parser on Components.
    """
    use_template: bool = False

    def __init__(
            self,
            **kwargs
    ):
        try:
            self.use_template: bool = bool(kwargs['use_template'])
            del kwargs['use_template']
        except KeyError:
            self.use_template: bool = False
        # Template directory
        try:
            template_dir = kwargs['template_idr']
            del kwargs['template_idr']
        except KeyError:
            template_dir = None
        # Template Parser:
        self._templateparser: TemplateHandler = None
        if self.use_template is True:
            self._templateparser = getTemplateHandler(
                newdir=template_dir
            )
            cPrint(
                "Using Jinja2 Template Parser."
            )
