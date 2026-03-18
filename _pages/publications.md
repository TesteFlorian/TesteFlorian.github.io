---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: false
description: "Peer-reviewed publications on geospatial intelligence, crop yield forecasting, and satellite-based machine learning by Florian Teste."
---

{% include base_path %}

The articles below capture my work on geospatial intelligence, food security forecasting, and environmental monitoring. Each entry includes a short summary and a direct paper link; the full CV remains available on the [CV page]({{ base_path }}/cv/).

{% assign publications = site.publications | sort: "date" | reverse %}
{% assign current_year = "" %}
{% for post in publications %}
  {% capture publication_year %}{{ post.date | date: "%Y" }}{% endcapture %}
  {% unless publication_year == current_year %}
### {{ publication_year }}
    {% assign current_year = publication_year %}
  {% endunless %}
  {% include archive-single.html %}
{% endfor %}
