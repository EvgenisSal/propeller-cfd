---
marp: true
paginate: true
---

<style>
:root {
    font-size: 20px;
}
td {
    width: 1000px;
}
table {
    width: 100%;
}
img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 60%;
}
</style>

# simpleFoam : motorBike tutorial

- Case: /Users/esalagk/cfd-projects/propeller-cfd/learning/motorBike
- Submission: 12:44:29 on Jul 15 2026
- Report time: 12:46:39 on Jul 15 2026

---

## Run information

| Property       | Value              |
|----------------|--------------------|
| Host           | Evgenioss-Laptop.local        |
| Processors     | 4      |
| Time steps     | 500  |
| Initial deltaT | 1 |
| Current deltaT | 1 |
| Execution time | 128.91  |

---

## OpenFOAM information

| Property       | Value              |
|----------------|--------------------|
| Version        | v2606     |
| API            | 2606         |
| Patch          | 0       |
| Build          | _481094fdf3-20260618       |
| Architecture   | LSB;label=32;scalar=64  |

---

## Mesh statistics

| Property          | Value                |
|-------------------|----------------------|
| Bounds            | (-5 -4 0)(15 4 8) |
| Number of cells   | 353786   |
| Number of faces   | 1124709   |
| Number of points  | 423995  |
| Number of patches | 72 |

---

## Linear solvers

| Property | Value          | tolerance(rel)   | Tolerance(abs)      |
|----------|----------------|------------------|---------------------|
| p        | `GAMG` | 1e-07 | 0.01 |
| U        | `smoothSolver` | 1e-08 | 0.1 |

---

## Numerical scehemes

The chosen divergence schemes comprised:

~~~
divSchemes
{
    default         none;
    div(phi,U)      bounded Gauss linearUpwindV grad(U);
    turbulence      bounded Gauss upwind;
    div(phi,k)      bounded Gauss upwind;
    div(phi,omega)  bounded Gauss upwind;
    div((nuEff*dev2(T(grad(U))))) Gauss linear;
}

~~~

---

## Graphs

Residuals

![](/Users/esalagk/cfd-projects/propeller-cfd/learning/motorBike/postProcessing/residualGraph1/500/residualGraph1.svg)

---

## Results

Forces

![](/Users/esalagk/cfd-projects/propeller-cfd/learning/motorBike/postProcessing/forceCoeffsGraph1/500/forceCoeffsGraph1.svg)

---

Made using Open&nabla;FOAM v2412 from https://openfoam.com

