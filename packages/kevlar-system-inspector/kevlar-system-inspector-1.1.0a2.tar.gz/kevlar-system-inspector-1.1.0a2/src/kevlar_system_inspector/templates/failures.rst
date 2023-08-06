=======
Details
=======

{% for module in report.failures %}

.. class:: test-category {{ module.tags | join(" ") }}

{%      if module.documentation is not none %}
{{ module.documentation }}
{%      else %}
-------------------------------------------------
Undocumented module: {{ module.module.__name__ }}
-------------------------------------------------
{%      endif %}

{%      for nodeid, outcome in module.failures %}

.. class:: test-item {{ outcome.tags | join(" ") }}

{%          if outcome.documentation is none %}
Undocumented test: {{ nodeid }}
===============================

**Missing documentation**
{%           else %}
{{ outcome.documentation }}
{%           endif %}

Issues Identified
-----------------

{%          for cause in outcome.failures %}
{%              if cause.is_internal %}
.. admonition:: Internal Error
   :class: test-issue

    ::

{{                  cause.message | indent(width=6, first=true) }}

{%              else %}
.. admonition:: Issue
   :class: test-issue

{{                  cause.message | indent(width=3, first=true) }}
{%              endif %}
{%          endfor %}

{%      endfor %}
{% endfor %}
