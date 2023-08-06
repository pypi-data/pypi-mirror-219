.. role:: underline
   :class: underline

{% set lite = " Lite" if not is_full_version else "" %}

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Kevlar System Inspector{{ lite }} System Report
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Star Lab’s Kevlar System Inspector{{ lite }} identified {{ report.failure_count
}} issues with your system. Please see the detailed report for further information.
{% if not is_full_version %}
The Lite version of Kevlar System Inspector does not include several tests, but
you can request the full version of Kevlar System Inspector from Star Lab at no
cost when you `contact us`__.  Kevlar System Inspector Lite is completely
risk-free and there is no obligation to purchase anything after use. Star Lab
wants every business to have access to the best possible security solutions,
and our Kevlar System Inspector is just one of the ways we demonstrate our
commitment to that belief.

.. __: https://www.starlab.io/contact-us-kevlar-system-inspector-user
{% endif %}
