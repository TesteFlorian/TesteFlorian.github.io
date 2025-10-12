---
layout: archive
title: "Talks and presentations"
permalink: /talks/
author_profile: true
---

{% if site.talkmap_link == true %}

<p style="text-decoration:underline;"><a href="/talkmap.html">See a map of all the places I've given a talk!</a></p>

{% endif %}

I regularly share research on satellite-enabled forecasting, geospatial intelligence, and agentic analytics with scientific and practitioner communities. This page collects conference and invited talks; hands-on workshops with rendered notebooks now live on the dedicated [Workshops]({{ '/workshops/' | relative_url }}) page.

{% assign conferences = site.talks | where_exp: "item", "item.slides_url == nil" | sort: "date" | reverse %}

{% if conferences %}
### Conferences & Talks
{% for post in conferences %}
  {% include archive-single-talk.html %}
{% endfor %}
{% else %}
<p>No talks published yet.</p>
{% endif %}
