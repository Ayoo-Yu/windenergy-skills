# Python Workflow

Use Matplotlib, Seaborn, or Plotly only when interactivity is explicitly needed.

```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.linewidth": 0.8,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
})
```

Export:

```python
fig.savefig("figure.svg", bbox_inches="tight")
fig.savefig("figure.png", dpi=300, bbox_inches="tight")
```

For wind power curves, show cut-in, rated, and cut-out regions only when the
values are known or explicitly assumed.

For full-paper workflows, store the figure style metadata in the figure map:
font family, minimum font size, line width, palette id, and legend policy.
