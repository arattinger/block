# -*- coding: utf-8 -*-
import mistune
from jinja2 import Template

with open('tests/markdown/test1.md', 'r') as f:
    data = f.read()
html_inner = mistune.markdown(data)

with open('new_templates/base.html', 'r') as f:
    template_base = f.read()
template = Template(template_base)

with open('test.html', 'w') as f:
    f.write(template.render({
        'title': 'This is a test document',
        'content': html_inner,
    }))
