from abc import ABC, abstractmethod
from typing import Dict, Any

from jinja2 import Template


class BaseEmailSender(ABC):

    def render_template(self, template_path, context: Dict[str,Any]):
        with open(template_path, 'r') as f:
            template = Template(f.read(), autoescape=True)
            return template.render(context)

    @abstractmethod
    def send_one(self, subject: str, recipient: str, body: str):
        pass
