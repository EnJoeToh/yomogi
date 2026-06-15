from jinja2 import Environment, PackageLoader, select_autoescape

from yomogi.commands.scenario.models import Node

DEFAULT_TEMPLATE = "scenario_classic.html"

_ENVIRONMENT = Environment(
    loader=PackageLoader("yomogi.commands.scenario", "templates"),
    autoescape=select_autoescape(("html", "xml")),
)


def render_html(
    nodes: list[Node],
    *,
    page_title: str | None = None,
    template_name: str = DEFAULT_TEMPLATE,
) -> str:
    template = _ENVIRONMENT.get_template(template_name)
    return template.render(nodes=nodes, page_title=page_title)
