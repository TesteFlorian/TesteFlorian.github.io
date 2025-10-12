# Workshop Notebook Rendering Guide

These steps keep the embedded workshop notebooks (`support_terra.html`, `TP_terra.html`) in sync with their Quarto sources.

## Prerequisites
- R 4.2 or newer with the packages:
  `terra`, `tidyterra`, `geodata`, `ggplot2`, `dplyr`, `gridExtra`, `ggspatial`, `leaflet`, `leaflet.extras`, `mapview`.
- Quarto CLI 1.8+.

## Render notebooks
```bash
quarto render files/support_terra.qmd --to html --output-dir workshops
quarto render files/TP_terra.qmd        --to html --output-dir workshops
```

## Deploy
The `workshops/` directory is version-controlled. After rendering, commit the updated HTML files along with any raster exports created by the scripts.

## Security note
Only render notebooks from trusted sources. Review generated HTML for unexpected scripts before publishing.
