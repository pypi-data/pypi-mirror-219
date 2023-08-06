========
Warnings
========

{% if report.warnings|length > 1 %}
The following warnings were generated while running tests:
{% else %}
The following warning was generated while running tests:
{% endif %}
{% for warning in report.warnings %}

.. warning::

{{ warning.message | string | indent(width=3, first=true) }}
{% endfor %}

