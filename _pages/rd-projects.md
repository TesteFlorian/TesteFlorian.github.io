---
layout: single
title: "Selected Projects"
permalink: /rd-projects/
author_profile: false
description: "Selected GeoAI and computer vision projects across crop forecasting, maritime monitoring, and environmental intelligence."
---

{% include base_path %}

<p class="page-kicker">Applied GeoAI case studies</p>

I build end-to-end machine learning systems that convert Earth Observation data into operational products. The projects below are the clearest cross-section of my recent work: each combines a real decision context, a technical stack, and a concrete output path through publications, talks, or internal delivery.

<div class="page-actions">
  <a class="btn btn--accent" href="{{ '/publications/' | relative_url }}">Related publications</a>
  <a class="btn btn--inverse" href="{{ '/talks/' | relative_url }}">Selected talks</a>
  <a class="btn btn--light-outline" href="{{ '/cv/' | relative_url }}">Download CV</a>
</div>

## Crop Forecasting & Market Intelligence

- **Decision context:** Produce early-season yield and price signals from open satellite data for agribusiness and food-security monitoring.
- **What I built:** Multi-terabyte ingestion pipelines, self-supervised embeddings, probabilistic regressors, and evaluation frameworks spanning the US, Malawi, and South Africa.
- **Outputs:** Peer-reviewed publications and conference talks on calibrated forecasting, feature learning, and deployment tradeoffs.

- Satellite-derived Gross Primary Production (GPP) used as the primary feature source.
- Autoencoders, beta-VAEs, ElasticNet, and probabilistic baselines benchmarked across regions.
- Focus on lead time, calibration, and transferability instead of only point accuracy.

## Maritime & Multi-Sensor Geospatial Intelligence

- **Decision context:** Build decision support tools for vessel activity monitoring, flood detection, and analyst-facing intelligence workflows.
- **What I built:** Prototype GEOINT pipelines that combine SAR, optical, LiDAR, AIS, and text sources with modern computer vision and reporting workflows.
- **Outputs:** Internal R&D systems for cross-source intelligence synthesis and operational experimentation.

- Multi-sensor fusion pipelines for vessel indexing, classification, and anomaly review.
- Analyst-oriented dashboards and automated reporting to surface high-confidence findings.
- Research-to-delivery focus: fast experimentation, interpretable outputs, and deployment readiness.

## Environmental Monitoring & Forest Analytics

- **Decision context:** Estimate structural and environmental signals from remote sensing for forestry and resilience applications.
- **What I built:** Neural models that fuse airborne LiDAR and Sentinel-2 imagery for biomass-related estimation and large-area monitoring.
- **Outputs:** Journal publication and reusable workflow patterns for combining heterogeneous EO sources.

- High-resolution fusion of LiDAR metrics with satellite imagery.
- Emphasis on robust performance in heterogeneous landscapes.
- Methods designed for practical reporting and long-term environmental tracking.
