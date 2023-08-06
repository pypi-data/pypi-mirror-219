=============
Passing Tests
=============

The following tests passed:

.. list-table::
   :header-rows: 1

   * - Category
     - Test

{% for module in report.successes %}
{%     for nodid, outcome in module.successes %}
   * - {{ module.title or module.module.__name__ }}
     - | {{ outcome.title or nodeid }}
       |
{%     endfor %}
{% endfor %}

