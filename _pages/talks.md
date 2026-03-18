---
layout: archive
title: "Talks and presentations"
permalink: /talks/
author_profile: false
description: "Conference talks and presentations on satellite-based forecasting, geospatial intelligence, and applied AI research."
---

{% if site.talkmap_link == true %}

<p style="text-decoration:underline;"><a href="/talkmap.html">See a map of all the places I've given a talk!</a></p>

{% endif %}

This page collects conference and invited talks. Hands-on sessions and rendered notebooks are separated onto the dedicated [Workshops]({{ '/workshops/' | relative_url }}) page so talks remain focused on external presentations and invited speaking.

{% assign talks = site.talks | where: "content_type", "talk" | sort: "date" | reverse %}
{% assign current_year = "" %}

{% if talks %}
### Conferences & Talks
{% for post in talks %}
  {% capture talk_year %}{{ post.date | date: "%Y" }}{% endcapture %}
  {% unless talk_year == current_year %}
#### {{ talk_year }}
    {% assign current_year = talk_year %}
  {% endunless %}
  {% include archive-single-talk.html %}
{% endfor %}
{% else %}
<p>No talks published yet.</p>
{% endif %}
