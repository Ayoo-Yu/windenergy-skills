# Template Index

Use these lightweight figure blueprints instead of carrying large off-domain
demo assets.

## Power Curve

Inputs: wind speed, power, turbine rated power, optional operating-region labels.
Output: scatter or hexbin plus empirical median curve.

## Forecast Versus Actual

Inputs: timestamp, observed power, forecast power, optional prediction interval.
Output: line plot with a short representative window and error inset.

## Workflow Or Evidence Pipeline

Inputs: research object, fair comparison unit, methods or method families,
diagnostics, and boundary analyses.
Output: compact workflow figure that shows what is compared, how evidence is
computed, and where conclusions are bounded. Keep code filenames in the
reproducibility appendix.

## Error Distribution

Inputs: horizon, model, error metric, optional wind-speed bin.
Output: boxplot, violin plot, or ridgeline by horizon/model.

## Ablation Heatmap

Inputs: model variant, dataset/site, metric.
Output: heatmap with lower-is-better or higher-is-better direction declared.

## Evidence Portfolio

Inputs: manuscript claims, figure roles, source data, and target journal.
Output: figure plan with workflow, data or task overview, method comparison,
condition boundary, mechanism evidence, robustness, and deployment guidance
covered when these claim types appear.

## Wake/Layout Graph

Inputs: turbine coordinates, wind direction, edge weights or adjacency.
Output: scatter layout with directional arrows or weighted graph edges.
