---
layout: single
title: "Terra Support Tutorial"
permalink: /workshops/support-terra/
author_profile: false
description: "Reference guide for working with SpatVector and SpatRaster objects using Terra and tidyverse tooling."
---

{% include base_path %}

> This tutorial accompanies the “Happy R: package terra” workshop by Florian Teste & Jérémy Lamouroux. It walks through the essentials of Terra, tidyterra, ggplot2, and dplyr for raster and vector analysis.

## Render the notebook

- [Download `support_terra.qmd`]({{ '/files/support_terra.qmd' | relative_url }})

Render it locally to run the full set of examples:

```bash
# Quarto
quarto render files/support_terra.qmd --to html --output-dir workshops

# Or from R
Rscript -e "rmarkdown::render('files/support_terra.qmd', output_dir = 'workshops')"
```

Required packages:

```r
install.packages(c("terra", "tidyterra", "ggplot2", "dplyr"))
```

## Key Concepts

### SpatVector vs. SpatRaster
- `SpatVector` stores vector geometries (boundaries, roads) with attributes.
- `SpatRaster` handles gridded data (elevation, remote-sensing layers) with cell values.

### Packages Covered
- **terra** for GDAL-backed raster/vector operations.
- **ggplot2** and **tidyterra** for visualization.
- **dplyr**, **geodata**, **gridExtra**, **ggspatial** for data wrangling and cartography.

## Hands-on Workflow
1. Import rasters with `rast()` and rename layers.
2. Save outputs via `writeRaster()` when required.
3. Crop, project, mosaic, and merge rasters using Terra utilities.
4. Apply local operations (math, reclassification) and global stats (min/max/mean).
5. Extract values for points/polygons and compute zonal summaries.

## Visualization & Mapping
- Build base maps with `geom_spatraster()` / `geom_spatvector()` from tidyterra.
- Combine plots using `gridExtra::grid.arrange()`.
- Add north arrows, scale bars, and annotations via ggspatial helpers.
- Optionally explore interactive maps with Leaflet/Mapview extras.

## Agenda

1. **Understanding `SpatVector` and `SpatRaster`**  
   Learn how Terra represents vector and raster data, and how metadata (attributes, geometry) is stored.
2. **Package overview**  
   - `terra` for GDAL-backed raster/vector operations  
   - `ggplot2` for declarative plotting  
   - `tidyterra` for tidyverse-friendly `geom_spat*` wrappers  
   - `dplyr` for data manipulation pipelines
3. **Practical exercises**  
   - Import and inspect raster data  
   - Visualise rasters with tidyterra + ggplot2  
   - Explore vector layers and attribute data  
   - Perform spatial transformations, reclassification, and summaries  
   - Export outputs for downstream analysis

The Quarto file includes collapsible code blocks, navigation, and custom styling to help you follow along or reuse snippets in your own projects.


