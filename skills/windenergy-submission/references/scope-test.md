# Scope Alignment Test

Use `journal-profiles.md` first. This file gives a detailed Renewable Energy
scope test and reusable wind-power boundary checks for the other target
journals.

## RE Aims and Scope (verbatim summary)

*Renewable Energy* seeks to promote and disseminate knowledge on the various topics and technologies of **renewable energy systems** and **components**. The journal aims to serve researchers, engineers, economists, manufacturers, NGOs, associations and societies to help them keep abreast of new developments and to apply **alternative energy solutions** to current practices.

*Renewable Energy* is an international, multi-disciplinary journal in **renewable energy engineering** and **research**.

## RE Coverage areas

The journal explicitly covers:

1. Biomass Conversion
2. Photovoltaic Technology Conversion
3. Solar Thermal Applications
4. **Wind Energy Technology**
5. Desalination
6. Solar and Low Energy Architecture
7. Climatology and Meteorology
8. Geothermal Technology
9. Wave, Tide and Ocean Thermal Energies
10. Hydro Power
11. Hydrogen Production Technology and Fuel Cells
12. Socio-economic and Policy Issues

Other related topics are welcome **provided they are within the context of the broader multi-disciplinary scope**.

## The scope gate

A paper is within scope **only if**:

1. It is concerned with **power generation**
2. The power is generated in a **renewable or sustainable** way

### Out-of-scope example (from RE Guide)

> A paper concerning development and characterisation of a material for use in a renewable energy system, **without any measure of the energy that this new material will convert**, would be out of scope.

This is critical: materials papers, algorithm papers, and policy papers must all connect to actual power generation from renewable sources.

## Scope assessment process

### Step 1. Read the manuscript's central claim

Identify the primary research question, method, and conclusion.

### Step 2. Answer the three gate questions

| # | Question | Required answer |
|---|----------|----------------|
| 1 | Does the paper concern power generation? | Yes |
| 2 | Is the power generated renewably or sustainably? | Yes |
| 3 | Does it fall within at least one RE coverage area? | Yes |

If all three are "Yes" - the paper is likely in scope.
If any is "No" - the paper may be out of scope.

### Step 3. Check for common scope boundary cases

| Paper type | In scope if | Out of scope if |
|-----------|-------------|-----------------|
| Materials for solar cells | Measures energy conversion efficiency | Only characterizes material properties |
| Wind forecasting algorithm | Predicts power output from wind farms | Only predicts wind speed without power context |
| AI/ML method | Applied to renewable energy generation or integration | Generic ML benchmark with no energy application |
| Policy analysis | Directly relates to renewable power deployment | General environmental policy without energy focus |
| Grid integration study | Integrates renewable generation sources | Only studies conventional fossil fuel grid |
| Condition monitoring | Monitors wind turbines or solar panels | Generic fault detection with no energy system |
| Environmental impact | Specifically for renewable energy installations | General environmental study |
| Economic analysis | Economic viability of renewable energy systems | General energy economics without renewable focus |
| Wake modeling | Models wake effects to optimize wind farm power | Pure fluid dynamics without power generation |

### Step 4. SDG alignment (bonus)

RE welcomes contributions supporting:
- **SDG 7**: Affordable and Clean Energy
- **SDG 13**: Climate Action

Mentioning SDG alignment in the cover letter and introduction can strengthen the scope fit argument.

### Step 5. Report

```text
## Scope Alignment Assessment

### Gate Questions
| # | Question | Answer | Evidence |
|---|----------|--------|----------|
| 1 | Power generation? | Yes/No | [from manuscript] |
| 2 | Renewable/sustainable? | Yes/No | [from manuscript] |
| 3 | RE coverage area? | Yes/No | [area name] |

### Coverage area(s)
- [Primary area, e.g., Wind Energy Technology]
- [Secondary area, e.g., Climatology and Meteorology]

### SDG alignment
- SDG 7: [connection]
- SDG 13: [connection]

### Boundary assessment
[Any scope edge cases or risks]

### Recommendation
[IN SCOPE / LIKELY IN SCOPE / BORDERLINE / LIKELY OUT OF SCOPE / OUT OF SCOPE]

### Alternative journals (if borderline or out of scope)
- Applied Energy (broader energy systems)
- Energy Conversion and Management (conversion focus)
- Energy (general energy research)
- Wind Energy (wind-specific)
- IEEE Trans. Sustainable Energy (power engineering focus)
```

## Common wind energy scope patterns

### In scope (strong fit)
- Wind power forecasting with validation on real wind farms
- Wind farm layout optimization with power output maximization
- Wake effect modeling with measured power loss quantification
- Wind turbine condition monitoring using SCADA power data
- Wind resource assessment connecting wind data to energy yield
- Wind farm control strategies optimizing total power output

### In scope (moderate fit, needs careful framing)
- New ML architecture applied to wind power prediction (must show power results)
- Meteorological study for wind energy siting (must connect to generation)
- Wind turbine blade aerodynamics (must include power performance data)

### Borderline / likely out of scope
- Pure atmospheric boundary layer research without wind energy context
- General time-series forecasting methods using wind as example but no power data
- Wind turbine structural health monitoring without power generation relevance

## QA checklist

- [ ] All three gate questions answered
- [ ] At least one RE coverage area identified
- [ ] Power generation connection explicit
- [ ] Scope boundary cases considered
- [ ] Alternative journals suggested (if borderline)
