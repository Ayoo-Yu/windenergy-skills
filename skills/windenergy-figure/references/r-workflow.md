# R Workflow

Use `ggplot2` for most static manuscript charts.

```r
library(ggplot2)

theme_energy <- function(base_size = 9, base_family = "Times New Roman") {
  theme_minimal(base_size = base_size, base_family = base_family) +
    theme(
      panel.grid.minor = element_blank(),
      axis.title = element_text(size = base_size),
      legend.position = "top"
    )
}
```

Export:

```r
ggsave("figure.svg", plot = p, width = 85, height = 60, units = "mm")
ggsave("figure.png", plot = p, width = 85, height = 60, units = "mm", dpi = 300)
```

Use facets sparingly; if each panel needs a different scale or physical
interpretation, split the figure.

For full-paper workflows, include figure style metadata in the figure map:
font family, minimum font size, line width, palette id, and legend policy.
