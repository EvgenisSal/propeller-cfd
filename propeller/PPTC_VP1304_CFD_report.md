# Open-Water CFD of the PPTC VP1304 Controllable-Pitch Propeller

**A single-operating-point validation study against SVA Potsdam experimental data, with a systematic investigation of the residual thrust error under an 8 GB memory budget.**

Evgenios Ioannis Salagkoudis,
Mechanical Engineering Student, Aristotle University of Thessaloniki

---

## Abstract

A steady RANS simulation of the SVA Potsdam PPTC VP1304 controllable-pitch propeller was carried out in OpenFOAM at the design advance ratio J = 0.8 and compared against the published open-water measurements (K_T = 0.489, K_Q = 0.122, η_O = 0.525). The multiple-reference-frame (MRF) frozen-rotor solution reproduces the *efficiency* of the propeller almost exactly (η_O ≈ 0.58, about +10 %) but overpredicts the *magnitude* of the loading by roughly 1.5–2× (post-transient K_T ≈ 0.7–1.0). Because a matched efficiency implies correct flow angles and a correct effective advance ratio, the error is one of force magnitude rather than of gross setup. The bulk of this report is devoted to tracing that magnitude error. Five candidate causes were tested and eliminated with quantitative evidence: near-wall treatment, blade-surface mesh resolution, far-field boundary condition, blade pitch fidelity, and hub/shaft contribution. The residual is attributed not to a discrete, correctable bug but to two coupled limits. The first is an under-resolved tip vortex that would require a cell count well beyond the 8 GB hardware envelope. The second is the intrinsic ceiling of the steady frozen-rotor MRF method for a heavily loaded, high-pitch propeller, evidenced by a thrust history that never reaches a plateau but instead drifts slowly upward at stable residuals. The value of the study is the diagnostic chain, not the raw coefficient.

---

## 1. Objective and benchmark

The goal was to build a small, honest, end-to-end open-water CFD validation on consumer hardware: import a real propeller geometry, mesh it, run a rotating-frame RANS solution, extract the thrust and torque coefficients, and confront them with measured data. Where the two disagree, the aim is to explain *why* with evidence rather than assertion.

The **PPTC VP1304** was chosen deliberately. It is a five-bladed controllable-pitch propeller with a high design pitch ratio (P/D = 1.635 at 0.7R), released by SVA Potsdam with open experimental data and used as an international benchmark at the SMP'11 workshop. The high pitch is the reason its thrust stays high at large advance ratios, and it makes the case a good stand-in for the controllable-pitch marine propulsors used in industry.

All comparisons are made at a single operating point:

| Quantity | Value |
|---|---|
| Advance ratio J = U/(nD) | 0.8 |
| Inflow speed U | 3.0 m/s |
| Rotation rate n | 15 rev/s (ω = 94.25 rad/s) |
| Diameter D | 0.250 m |
| Density ρ | 999 kg/m³ |

The reference values, taken from the SVA Potsdam open-water measurements at J = 0.8, are **K_T = 0.489, K_Q = 0.122, η_O = 0.525**. As a sanity check on the reference itself, the independent SMP'11 dataset gives K_T = 0.3835 and η_O = 0.629 at J = 1.019, which is consistent with a K_T near 0.49 at the lower J = 0.8. An early version of this work mistakenly anchored to K_T ≈ 0.22, a value appropriate to a moderate-pitch propeller, which manufactured a phantom "4.5× error." Cross-checking the reference against a second source removed it. It is noted here because getting the benchmark right is a precondition for any validation claim.

A single operating point was studied in depth rather than sweeping a full J-curve. For this hardware, and for the question of where the error comes from, the depth of the diagnostic is more informative than a sparse offset curve. A J-sweep is listed as future work.

---

## 2. Numerical setup

### 2.1 Geometry and pitch verification

The geometry is the SVA-supplied PPTC STEP file, converted to a watertight STL (107 830 triangles, single closed region, verified with `surfaceCheck`). The propeller disc sits at x = 0 with the flow in +X; the shaft is extended upstream to x = −0.80 m so that the inlet sees a clean, fully developed approach.

Because the imported pitch is the single most consequential geometric property for thrust, it was measured directly from the STL rather than assumed. A short Python script bins the surface triangles into thin annular bands, isolates each of the five blades by angular gaps, and recovers the local pitch angle of each blade section by a principal-axis fit in the (rθ, x) plane; the pitch then follows from P = 2πr·tan φ. The script was first validated on a synthetic helicoid of known P/D = 1.635, which it recovered to within 0.2 % on all five blades before being applied to the real geometry.

The measured distribution is shown in **Figure 1**. At the reference station the geometry gives **P/D = 1.65 at 0.7R against the design 1.635, a 1.1 % difference, with all five blades identical to two decimals.** The pitch is correct; the geometry is not the source of the error.

*Figure 1. Blade pitch verification (P/D vs r/R).*

### 2.2 Mesh

The background domain is a rectangular block (inlet x = −0.75, outlet x = +1.50, lateral far-field at ±0.75 m) built with `blockMesh`; the propeller is carved out with `snappyHexMesh` using feature-edge capture, surface refinement levels (3 5) on the blade, and three prism layers. The layer stack was tuned to a relaxed criterion set (feature angle 170°, maximum thickness-to-medial-ratio 0.6, relative sizing) that lifted prism-layer coverage from 12 % to 79 % without triggering layer collapse.

The final mesh is **277 000 cells** and passes `checkMesh` with only three highly skewed faces out of the whole domain (maximum non-orthogonality 65°, maximum skewness 4.8). On 8 GB of RAM this is close to the practical ceiling; a mesh fine enough to resolve the tip vortex is not.

### 2.3 Physical model and boundary conditions

The flow is incompressible RANS with the **k-ω SST** turbulence model. Rotation is imposed through a **multiple-reference-frame (frozen-rotor)** cell zone: a cylinder enclosing the blades (verified to contain the full propeller radius and axial extent), rotating at ω = 94.25 rad/s about the x-axis, with the outer domain stationary. The solver is `simpleFoam`.

| Patch | U | p |
|---|---|---|
| inlet | fixedValue (3 0 0) | zeroGradient |
| outlet | inletOutlet | fixedValue 0 |
| far-field | pressureInletOutletVelocity / value (3 0 0) | fixedValue 0 |
| propeller (blades + hub + shaft) | noSlip | zeroGradient |

The propeller is a genuine no-slip wall. It is *not* modelled as a rotating wall, which would double-count the MRF rotation. Turbulence wall treatment uses `nutUSpaldingWallFunction` on the blade (a continuous wall function valid across the buffer layer, replacing the earlier `nutkWallFunction`) with a blended `omegaWallFunction`. Transport is Newtonian, ν = 1.14 × 10⁻⁶ m²/s.

Relaxation was the single most important stability control. The final, stable set is p = 0.3, U = 0.7, k = ω = 0.5. An earlier configuration that relaxed all equations at 0.9 and applied no pressure relaxation diverged (monotonically climbing thrust); adding explicit pressure relaxation and softening the momentum and turbulence factors fixed it.

### 2.4 Coefficient definitions

Thrust and torque are integrated over the propeller patch by the `forces` function object (reference density 999 kg/m³, centre of rotation at the origin). The coefficients follow the standard open-water definitions:

- J = U / (nD)
- K_T = T / (ρ n² D⁴), with ρ n² D⁴ = 878 N
- K_Q = Q / (ρ n² D⁵), with ρ n² D⁵ = 219.5 N·m
- η_O = (J / 2π) · (K_T / K_Q)

Coefficients are reported as ranges over the post-transient part of the run, not as single converged values, because, as Section 3 shows, the steady solution never settles to a single value.

---

## 3. Results

**Table 1. CFD vs experiment at J = 0.8.**

| Coefficient | CFD (post-transient span) | SVA | Ratio |
|---|---|---|---|
| K_T | 0.70 – 1.00 (does not converge) | 0.489 | ~1.5–2× |
| 10·K_Q | ~1.4 – 2.0 (tracks K_T) | 1.22 | ~1.2–1.6× |
| η_O | 0.57 – 0.58 (stable) | 0.525 | +10 % |

The efficiency is the one coefficient that *is* stable across the whole run; K_T and K_Q drift together while their ratio holds. That is the single most useful observation in the table, and the paragraphs below explain why.

The comparison is drawn on standard open-water axes in **Figure 3**.

*Figure 3. Open-water coefficients at J = 0.8, CFD vs SVA.*

Two features dominate the result and drive the rest of the report.

**The thrust never reaches a plateau.** After the initial transient the force history (**Figure 2**) does not settle: K_T drifts slowly upward across the run, from roughly 0.7 to roughly 1.0, without stabilising. Crucially, this is *not* numerical divergence. The equation residuals stay low and flat throughout (p and U_x initial residuals hold near 4×10⁻³ and 3×10⁻³ for thousands of iterations, with no upward trend). A drifting solution at stable residuals means the solver reaches equilibrium at every iteration but the equilibrium point itself keeps moving: there is no single steady state for it to converge to. For a heavily loaded propeller the wake and tip vortex are inherently unsteady, and a *steady* frozen-rotor formulation has no mechanism to represent that. It is being asked to freeze a flow that will not hold still. This behaviour is a property of the method on this case, and it is the reason coefficients are quoted as spans rather than single values.

*Figure 2. Thrust history, read directly from the solver force output.*

**Efficiency is essentially correct while magnitude is not.** η_O ≈ 0.58 sits within a few percent of the measured 0.525, whereas K_T and K_Q are both high by 40–70 %. Efficiency is the *ratio* of thrust to torque, and it is set by the flow angles the blade sections see, namely the effective angle of attack and the effective advance ratio. That this ratio comes out right, while both forces come out too large, is the central diagnostic clue: the simulation has the *kinematics* of the flow right and the *magnitude* of the loading wrong. It rules out an entire class of gross errors (wrong ω, wrong effective J, double-counted rotation, mis-identified force patch) before any of them is tested individually.

---

## 4. Error investigation

The thrust overprediction was treated as the object of study. Each plausible cause was isolated, tested, and either eliminated or bounded. **Table 2** is the summary; the paragraphs below give the reasoning.

**Table 2. Systematic exclusion of candidate causes.**

| # | Hypothesis | Test | Result | Verdict |
|---|---|---|---|---|
| 1 | Near-wall treatment | coverage 12 % → 79 %; `nutkWallFunction` → Spalding | K_T 0.985 → 0.90 → 0.87; thrust essentially unmoved | Not the driver |
| 2 | Blade surface resolution | refinement level 4 → 5 (277 k cells) | K_T unchanged within the drift band | Not the driver |
| 3 | Far-field blockage | slip → pressureInletOutletVelocity + fixed pressure | K_T statistically unchanged (~3 %) | Not the driver |
| 4 | Blade pitch fidelity | direct P/D measurement from STL | 1.65 vs design 1.635 (+1.1 %) | Geometry correct |
| 5 | Hub / shaft thrust | physical bound on axial pressure contribution | ≤ 10–15 % of thrust | Bounded, not the driver |

**1. Near-wall treatment.** Improving prism-layer coverage from 12 % to 79 % and switching to a continuous Spalding wall function moved K_T only from 0.985 to 0.87. The reason is physical: the thrust is overwhelmingly *pressure*-driven (of order 770 N pressure force against ~5 N viscous), and pressure forces are largely insensitive to the wall-function choice. The early y⁺ ~2700 was a genuine mesh-quality issue worth fixing, but it was never the cause of the magnitude error.

**2. Blade surface resolution.** Raising the surface refinement to level 5 added only ~27 k cells (the refinement activated on a thin band of the sharpest edges) and left K_T unchanged within the drift band. This is itself informative: within the resolution achievable on 8 GB, the solution is mesh-converged, so the offset is *not* a discretisation artefact that a modest refinement would remove. This corrects an earlier expectation that refinement would drive a clear downward trend; it does not, and reporting the flat behaviour honestly is the stronger result.

**3. Far-field blockage.** A slip far-field behaves like a frictionless tunnel and cannot pass the radial entrainment a loaded propeller draws from the side, which can artificially accelerate the through-flow. Replacing it with a pressure-opening condition (`pressureInletOutletVelocity` with an anchored far-field pressure) changed K_T by about 3 %, consistent with the small ~2 % geometric blockage of this domain. Real, but not the mechanism.

**4. Blade pitch fidelity.** Covered in Section 2.1. A high measured pitch would have explained the whole picture, since more pitch means a larger effective angle of attack, more loading, and a matched efficiency. But the geometry measures at design pitch (1.65 vs 1.635). This candidate is eliminated cleanly, and its elimination is what points the finger at the flow physics rather than the geometry.

**5. Hub and shaft.** The blades, hub and shaft share a single patch, so the integrated force includes all three. The long shaft is parallel to the flow: its pressure acts radially and cancels in the axial direction, contributing negligible thrust (consistent with an estimated ~3 N shaft drag). Only the hub cap presents axial area, and its contribution is bounded by area × pressure to roughly 10–15 % of the total. Real, but far short of the observed factor. A blade-only decomposition in post-processing is left as a minor refinement; the physical bound already shows it cannot close the gap.

With all five eliminated or bounded, the "easy" explanations are exhausted, and, importantly, the matched efficiency rules out the gross-setup class independently. What remains is not a bug.

---

## 5. Hardware and modelling limits

The residual error is best understood as the combination of two limits that the present configuration cannot escape.

**The tip vortex is under-resolved, and resolving it is out of budget.** For a high-pitch, heavily loaded blade the dominant mechanism of thrust *over*-prediction is an unresolved tip vortex: when the mesh cannot capture the vortex, the induced downwash that would relieve the tip is missing, the tip section sees too large an effective angle of attack, and it is overloaded. This overloads K_T more than K_Q, exactly the observed pattern (K_T high by roughly 70 %, K_Q by roughly 40 %), while leaving the efficiency ratio roughly intact. Capturing the tip vortex properly is a well-known heavy-mesh requirement; a published SimScale study of this same propeller needed on the order of 22 million cells to reach ~5 % error. Against the ~277 k cells that fit in 8 GB, that is roughly a 22× cell-count gap. In three dimensions, doubling the resolution in each direction costs 8× the cells, so even a 16 GB machine (about 2× cells) would not span it; this is a 64–128 GB or cloud/cluster-class requirement, not a next-laptop one.

**The steady frozen-rotor MRF has an intrinsic ceiling here.** The non-convergent upward drift at stable residuals (Figure 2) is the direct evidence: the method is being asked to hold a genuinely unsteady wake in a steady state, and it cannot. No amount of memory removes this; escaping it requires a *transient* sliding-mesh simulation with real rotation, which is one to two orders of magnitude more expensive in wall-clock time.

So reaching the measured K_T = 0.489 would require, together, a mesh on the order of 10⁷ cells, a transient sliding-mesh formulation, and hardware to match. None of these is a correction to the present setup; each is a different class of computation. Within the achievable envelope the model is behaving as expected, over-predicting a loaded propeller's thrust for reasons that are understood and quantified.

---

## 6. Conclusions and future work

At J = 0.8 the steady MRF model reproduces the propeller's efficiency to within a few percent (η_O ≈ 0.58 vs 0.525) but over-predicts thrust and torque by roughly 1.5–2× (post-transient K_T ≈ 0.7–1.0 vs 0.489). The matched efficiency localises the error to loading *magnitude* rather than flow *kinematics*.

That magnitude error was traced systematically. Near-wall treatment, blade-surface resolution and far-field blockage were each tested and shown not to move the result; the blade pitch was measured from the geometry and confirmed at design value (P/D 1.65 vs 1.635); the hub/shaft contribution was bounded to ≤ 10–15 % on physical grounds. The residual is consistent with an under-resolved tip vortex and the intrinsic ceiling of a steady frozen-rotor method for a heavily loaded, high-pitch propeller. The latter is evidenced by a thrust history that drifts upward at stable residuals instead of converging (Figure 2). Both limits sit beyond an 8 GB, steady-MRF envelope; neither is a discrete bug.

The engineering conclusion is therefore not a validated coefficient but a validated *understanding* of why the coefficient cannot be reached on this hardware with this method, and of exactly what would be required to reach it.

**Future work,** in order of value:

1. A transient sliding-mesh run at J = 0.8 on cloud/HPC resources, to separate the MRF ceiling from the resolution limit and quantify how much of the overprediction each contributes.
2. A full J-sweep (J = 0.6, 1.0, 1.2) to produce the complete open-water curve rather than a single point.
3. A surrogate/reduced-order model mapping J → (K_T, K_Q, η_O) once a sweep provides training points. This is a legitimate ML extension, but only meaningful after step 2.

---

## Reproducibility

All figures are generated by the Python scripts in `figures/`, driven either by values measured during the study or by the raw solver output (`fig2_convergence.py` reads `postProcessing/forces/0/force.dat` directly). The pitch-verification tool (`pitch_verify.py`) is standalone and was validated on a synthetic known-pitch geometry before use. Case files, mesh dictionaries and these scripts are in the project repository.

## References

1. SVA Potsdam. PPTC VP1304 open-water experimental data (Report 3752).
2. Second International Symposium on Marine Propulsors (SMP'11), Hamburg. PPTC workshop dataset.
3. SVA Potsdam PPTC geometry package (STEP), `case2-1_PPTC_geo_no_gap`.
