---
layout: archive
title: "Research"
permalink: /research/
author_profile: true
# header:
#   og_image: "research/ecdf.png"
---


<div style="text-align: justify; max-width: 900px; margin: 0 auto;">
<h2 style="margin-top:0;">Research Interests</h2>

<p>
I am passionate about harnessing remote sensing, artificial intelligence, and statistical analysis to address critical challenges in agriculture, food security, and environmental sustainability. My research centers on the synergy between these fields, with a particular focus on the biosphere.
</p>

<h3>Forecasting & Decision Support</h3>
<p>
My work involves developing innovative methods for forecasting crop yield and price variations using satellite-derived data. By leveraging high-resolution satellite imagery and state-of-the-art machine learning algorithms—including deep learning and autonomous AI agents—I aim to deliver early, accurate, and actionable predictions. The integration of AI agents enables continuous monitoring, rapid anomaly detection, and automated decision support, significantly enhancing the timeliness and reliability of insights for stakeholders. This research has the potential to inform strategic planning, improve food security, and optimize resource allocation in agricultural systems.
</p>

<h3>Beyond Agriculture</h3>
<p>
Beyond agriculture, I am actively exploring the application of remote sensing and AI in other domains, such as land-cover classification, vegetation health monitoring, environmental anomaly detection, and sustainable natural resource management. I am particularly interested in the deployment of autonomous AI agents that can analyze large-scale geospatial data, interpret complex environmental patterns, and support real-time decision-making across diverse ecosystems.
</p>
</div>

{% include base_path %}

{% assign ordered_pages = site.research | sort:"order_number" %}

{% for post in ordered_pages %}
  {% include archive-single.html type="grid" %}
{% endfor %}