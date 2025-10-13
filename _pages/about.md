---
permalink: /
title: "Florian Teste"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% include base_path %}

<section class="home-hero glass-surface glass-surface--accent glass-hover">
  <div class="hero-atmosphere" aria-hidden="true">
    <span class="hero-atmosphere__orb hero-atmosphere__orb--violet"></span>
    <span class="hero-atmosphere__orb hero-atmosphere__orb--azure"></span>
    <span class="hero-atmosphere__orb hero-atmosphere__orb--amber"></span>
  </div>
  <p class="home-hero__eyebrow">Senior Geospatial Machine Learning Scientist</p>
  <h1 class="home-hero__title">Transforming raw data into actionable intelligence.</h1>
  <p class="home-hero__lead">
    I apply state-of-the-art vision transformers and large language models to massive satellite, sensor, and text streams, turning raw geospatial data into mission-ready intelligence.
  </p>
  <div class="home-hero__actions">
    <a class="btn btn--accent" href="{{ base_path }}/publications/">Explore Publications</a>
    <a class="btn btn--inverse" href="{{ base_path }}/cv/">Download CV</a>
    <a class="btn btn--light-outline" href="mailto:{{ site.author.email }}">Contact</a>
  </div>
</section>

## Professional Experience

### Promethee Earth Intelligence — Senior Geospatial Machine Learning Scientist (2025 – Present)
- Prototype GEOINT pipelines that blend SAR/optical/LiDAR with EO foundation models for vessel and flood detection.
- Build analyst-facing LLM + agent workflows (RAG, Model Context Protocol tools) for cross-source intelligence synthesis.
- Develop near–real time vessel indexing and classification models across multi-sensor imagery, improving maritime situational awareness.
- Lead incident investigations that fuse imagery, AIS, and text OSINT to surface high-confidence insights.
- Fine-tune domain LLMs to automate GEOINT reporting and thematic summarisation in production FastAPI services.

### Atos — Data Scientist & Technical Consultant (2022 – 2025)
- Directed satellite-informed financial forecasting initiatives powered by deep learning and econometric baselines.
- Designed agricultural plot delineation pipelines leveraging Sentinel imagery and neural segmentation models.
- Mentored junior scientists and supervised master students through full-cycle ML project delivery.

### Paris-Saclay University — Ph.D. Candidate, Applied Mathematics (2022 – 2025)
- Delivered production pipelines forecasting agricultural prices directly from multi-terabyte satellite streams.
- Created spatiotemporal neural architectures (CNN, LSTM, Transformers) and self-supervised feature extractors for crop monitoring.
- Achieved cross-market generalisation (US, Africa) on crop price and yield prediction; published 4+ peer-reviewed papers.

### INRAE, TETIS Lab — Deep Learning Scientist Intern (2021)
- Co-authored IEEE JSTARS publication on LiDAR + Sentinel fusion for forest attribute estimation.
- Advanced neural approaches for basal area and biomass mapping in complex forest environments.

## Research Focus

- **Geospatial intelligence systems:** End-to-end pipelines combining EO foundation backbones, causal inference, and probabilistic calibration to deliver trusted forecasts.
- **Agentic analytics:** Retrieval-augmented LLM agents with structured tool use for operational analyst support.
- **Food security forecasting:** Early-season crop yield and price prediction using multimodal satellite time series.
- **Environmental monitoring:** Multi-sensor fusion for flood, forestry, and maritime surveillance.

## Core Skills

- **Data Science & Statistical Learning:** Experiment design, causal inference, probabilistic modelling, conformal uncertainty.
- **ML & Foundation Models:** Vision Transformers, masked autoencoding, spatiotemporal transformers, multimodal fusion, PEFT/LoRA.
- **LLMs & Agents:** Fine-tuning, RAG pipelines, Model Context Protocol tooling, evaluation harnesses, structured outputs.
- **Geospatial Engineering:** Sentinel/Landsat, SAR/Optical/LiDAR fusion, STAC, GDAL, Rasterio, GeoPandas, xarray/rioxarray.
- **MLOps & Platforms:** PyTorch, FastAPI, Docker, CI/CD, GPU & DDP training, observability, dataset versioning.

## Selected Publications

{% assign featured_publications = site.publications | sort: "date" | reverse | slice: 0, 3 %}
{% for pub in featured_publications %}
- [{{ pub.title }}]({{ pub.url | relative_url }}) — {{ pub.venue }}, {{ pub.date | date: "%Y" }}
{% endfor %}
- Full list on the [publications]({{ base_path }}/publications/) page.

## Conferences & Workshops

{% assign featured_talks = site.talks | sort: "date" | reverse | slice: 0, 3 %}
{% for talk in featured_talks %}
- [{{ talk.title }}]({{ talk.url | relative_url }}) — {{ talk.venue }}, {{ talk.location }} ({{ talk.date | date: "%b %Y" }})
{% endfor %}

## Education

- Ph.D., Mathematics (AI & Remote Sensing), Paris-Saclay University, 2025.  
- M.Sc., Geomatics & Environment, Aix-Marseille University, 2021.  
- M.Sc., Geomatics with Remote Sensing and GIS, Stockholm University, 2020.

## Languages & Interests

- **Languages:** French (native), English (C1), Spanish (B2), Swedish (B1).  
- **Interests:** Boxing (12 years), trail hiking, photography.  
- **Community:** Mentor for junior data scientists and applied ML researchers.
