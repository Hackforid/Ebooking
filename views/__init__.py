# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from mako import exceptions


class BaseHandler(RequestHandler):

    def render(self, template_name, **kwargs):
        lookup = self.application.template_lookup

        env_kwargs = dict(
            handler=self,
            request=self.request,
            locale=self.locale,
            _=self.locale.translate,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.application.reverse_url,
        )
        env_kwargs.update(kwargs)

        try:
            template = lookup.get_template(template_name)
            self.finish(template.render(**env_kwargs))
        except:
            self.finish(exceptions.html_error_template().render())
