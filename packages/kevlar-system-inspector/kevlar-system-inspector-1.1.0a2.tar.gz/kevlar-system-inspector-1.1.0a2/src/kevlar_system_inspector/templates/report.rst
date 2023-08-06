.. role:: underline
   :class: underline

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Kevlar System Inspector System Report
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

{% set lite = " Lite" if not is_full_version else "" %}

Welcome to Star Lab’s Kevlar System Inspector{{ lite }}! Today malicious actors
are increasingly targeting embedded systems. With data breaches and
cyber-attacks on the rise, it is critical to ensure that your embedded system
is secure and capable of operating in hostile environments. Star Lab’s Kevlar
System Inspector{{ lite }} is designed to help you identify many
vulnerabilities often overlooked during the design of embedded systems, so you
can protect your business and your customers. Below are the results of a
comprehensive security test on your embedded operating environment.

{% if not is_full_version %}
The Lite version of Kevlar System Inspector does not include several tests, but
you can request the full version of Kevlar System Inspector from Star Lab at no
cost when you `contact us`__. Kevlar System Inspector Lite is completely
risk-free and there is no obligation to purchase anything after use. Star Lab
wants every business to have access to the best possible security solutions,
and our Kevlar System Inspector is just one of the ways we demonstrate our
commitment to that belief.

.. __: https://www.starlab.io/contact-us-kevlar-system-inspector-user
{% endif %}

.. contents:: :depth: 2

=======
Summary
=======

{% if not report.any_failures %}

**🎉 Congratulations! 🎉** 

No issues were found
{%- if not report.warnings -%}
!
{%- else -%}
; however some warnings may require your attention.
{% endif %}
Be sure to update and re-scan regularly. New checks are always being added.

{% elif report.failure_count > 1 %}

Kevlar System Inspector identified {{ report.failure_count }} issues that
require your attention.

{% else %}

Kevlar System Inspector identified 1 issue that requires your attention.

{% endif %}

==================
System Information
==================

.. list-table:: System Information
   :stub-columns: 1

   * - Kevlar System Inspector Version
     - {{ inspector_version }}{{ lite }}
{%- for name, value in system_info.items() %}
   * - {{ name }}
     - {{ value }}
{%- endfor %}

{% if report.warnings %}
{% include "warnings.rst" %}
{% endif %}

{% if report.any_failures %}
{% include "failures.rst" %}
{% endif %}

{% if report.any_successes %}
{% include "successes.rst" %}
{% endif %}

==========
Conclusion
==========

Star Lab hopes the results from Kevlar System Inspector{{ lite }} will help you
in identifying any vulnerabilities in your software and providing you with
actionable recommendations to enhance your security. Cyber threats are
constantly evolving, and it's crucial to stay vigilant and proactive in
protecting your business and your customers. Please continue to work with our
team of security experts to implement the necessary changes and improvements to
your security posture. With our ongoing support and guidance, you can stay one
step ahead of potential threats and ensure that your software remains secure.
`Contact us`__ today and experience the peace of mind that comes with knowing
your software is secure.

.. __: https://www.starlab.io/contact-us-kevlar-system-inspector-user
