---
layout: single
title: "TP Terra – Guided Spatial Simulation Exercises"
permalink: /workshops/tp-terra/
author_profile: false
description: "Hands-on worksheet for learning Terra, tidyterra, and geodata in R."
---

{% include base_path %}

> This workshop runs in English. All code examples assume an R (≥4.2) environment with the packages `terra`, `tidyterra`, `geodata`, and `ggplot2`.

## Render the notebook yourself

Download the original Quarto notebook and render it locally so you can execute and modify each step:

- [Download `TP_terra.qmd`]({{ '/files/TP_terra.qmd' | relative_url }})

```bash
# Quarto (preferred)
quarto render files/TP_terra.qmd --to html --output-dir workshops

# Or from an interactive R session
Rscript -e "rmarkdown::render('files/TP_terra.qmd', output_dir = 'workshops')"
```

Required packages:

```r
install.packages(c("terra", "tidyterra", "geodata", "ggplot2"))
```

## 1. Load libraries

```r
library(terra)
library(tidyterra)
library(geodata)
library(ggplot2)
```

## 2. Import the nitrogen raster

Download global wheat yield data (Monfreda et al.) and store it as a `SpatRaster`.

```r
gph <- geodata::crop_monfreda("wheat", "yield", path = tempdir())
```

## 3. Visualise the raster

Build a quick map using `ggplot2` and `tidyterra`.

```r
# Replace with your plotting code
gph |> ggplot() + geom_spatraster() + scale_fill_viridis_c()
```

## 4. Inspect resolution and extrema

```r
resolution <- terra::res(gph)
max_value  <- terra::global(gph, "max", na.rm = TRUE)
min_value  <- terra::global(gph, "min", na.rm = TRUE)
```

## 5. Reproject to a new CRS

Select a projection from <https://epsg.io/> and apply it with `project()`.

```r
target_crs <- "EPSG:3857"
gph_proj   <- terra::project(gph, target_crs)
```

## 6. Rename the raster layer

```r
names(gph) <- "wheat_yield"
```

## 7. Compute descriptive statistics

```r
raster_mean    <- terra::global(gph, "mean", na.rm = TRUE)
raster_summary <- terra::summary(gph)
```

## 8. Reclassify raster values

Use a matrix of breakpoints to collapse values into classes.

```r
reclass_matrix <- matrix(c(
  -Inf, 0,   0,
   0,   5,   1,
   5,  10,   2,
  10,  Inf,  3
), ncol = 3, byrow = TRUE)

reclassified <- terra::classify(gph, reclass_matrix)
```

## 9. Apply arithmetic operations

```r
multiplied_raster <- gph * 3
```

## 10. Plot a histogram of raster values

```r
histogram <- ggplot() +
  geom_histogram(data = as.data.frame(gph, xy = FALSE), aes(wheat_yield), bins = 30)
```

## 11. Export the raster

```r
terra::writeRaster(gph, filename = "wheat_yield.tif", overwrite = TRUE)
```

## 12. Import vector data

```r
path_vect <- system.file("ex/lux.shp", package = "terra")
lux_shp   <- terra::vect(path_vect)
```

## 13. Extract Luxembourg metrics

Clip the raster to the Luxembourg boundary and compute per-canton summaries.

```r
cropped_raster      <- terra::crop(gph, lux_shp)
mean_yield_by_canton <- terra::extract(gph, lux_shp, fun = mean, na.rm = TRUE)
```

## 14. Overlay raster and vector layers

```r
plot_map <- ggplot() +
  geom_spatraster(data = cropped_raster) +
  geom_spatvector(data = lux_shp, fill = NA, colour = "black")
```

## Additional resources

- Terra documentation: <https://rspatial.org/terra/>
- tidyterra reference: <https://dieghernan.github.io/tidyterra/>
- geodata package: <https://cran.r-project.org/package=geodata>


[📄 Open rendered notebook]({{ '/workshops/TP_terra.html' | relative_url }}){: .btn .btn--accent target='_blank' rel='noopener' }

### Notes
- Rendered HTML in `/workshops/` is version-controlled; review it for unexpected scripts before publishing.
- Regenerate the notebook whenever source `.qmd` changes (see `docs/workshop_rendering.md`).
