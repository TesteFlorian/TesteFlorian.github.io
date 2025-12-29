---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
description: "Peer-reviewed publications on geospatial intelligence, crop yield forecasting, and satellite-based machine learning by Florian Teste."
---

{% include base_path %}

The articles below capture my work on geospatial intelligence, food security forecasting, and environmental monitoring. Each entry links to the preprint or journal version along with structured citation details. A downloadable CV with full bibliographic information is available on the [CV page]({{ base_path }}/cv/).

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}
