# Cover Letter — JMLR / FoCM submission

**To:** The Editor, *Journal of Machine Learning Research* (JMLR) — primary target
**Alt. To:** The Editor, *Foundations of Computational Mathematics* (FoCM) — alternate target
**From:** Rohan Fossé and Gaël Pallares, CESI LINEACT (EA 7527), Montpellier, France
**Date:** [submission date]
**Re:** Submission of "A universal spectral lower bound on the leave-node-out generalisation error of graph-supervised learning"

---

Dear Editor,

We are pleased to submit our manuscript **"A universal spectral lower bound on the leave-node-out generalisation error of graph-supervised learning"** for consideration at *JMLR*. The work is a full-length article (~18 pp main + ~10 pp Supplementary Information) and has not been submitted elsewhere.

**The contribution.** Generalisation bounds for supervised learning come, with rare exceptions, in two methodological lanes — VC/Rademacher and information-theoretic — both of which produce *upper* bounds on excess risk. Quantitative *lower* bounds, characterising an irreducible floor below which no learner can go, are rare, and to our knowledge none exists in spectral graph-supervised form for the leave-node-out evaluation protocol that is operationally standard in materials informatics, recommender systems with cold-start, and urban mobility transferability. We prove a universal lower bound of this form: under any feature-restricted learner with hypothesis class $\mathcal{H}_d$ and target signal $\mathbf{y}$ on a graph with Laplacian $L$, the expected leave-node-out loss is bounded below by $(1 - R^2_{\mathrm{spec}}(\mathcal{H}_d, \mathbf{y})) \cdot \mathrm{Var}(\mathbf{y})$, exact in expectation. We then prove (via the transductive Rademacher of El-Yaniv & Pechyony 2009) that any ERM saturates this lower bound up to a Berry–Esseen slack of order $M^2/\sqrt{N-n}$, which is itself minimax-tight. The pair of bounds is the Cramér–Rao analog for graph-supervised regression under leave-node-out. Empirically, Spearman $\rho(R^2_{\mathrm{spec}}, \Delta R^2_{\mathrm{LSO}}) = +1.000$ on the 8-task MatBench v0.1 panel (exact $p = 4.96 \times 10^{-5}$), with cross-domain replication on bike-share, MovieLens, and QSAR pilots.

**Why JMLR.** The contribution is methodological, fundamentally theoretical, and accompanied by a rigorous empirical falsifiability programme — three properties that characterise the JMLR niche. The bound's Cramér–Rao framing positions the program as a foundational theoretical contribution that should be of interest to JMLR's broad statistical-learning audience; the 8-task empirical validation panel and cross-domain anchors satisfy JMLR's expectation of substantive empirical content. We are equally open to *Foundations of Computational Mathematics* should JMLR's editorial pipeline prefer to redirect.

**Companion empirical paper.** A companion paper instantiating Corollary C1 on the specific materials-property-prediction domain is in submission to *Machine Learning: Science and Technology* (MLST, IOP Publishing); see Fossé & Pallares 2026, Zenodo DOI [10.5281/zenodo.20355996](https://doi.org/10.5281/zenodo.20355996), repository [github.com/cycling-data-lab/materials-applicability-bound](https://github.com/cycling-data-lab/materials-applicability-bound). The present manuscript supersedes and abstracts that work; its empirical section cross-references the MLST paper's 8-task panel as Corollary C1's empirical anchor, but is self-contained at the theoretical level.

All code, derived outputs, formal-proof research notes (notes/01–04, ~25 pp of supplementary mathematical content), and the LaTeX source of both the manuscript and the SI are openly archived at [github.com/cycling-data-lab/structural-bounds-framework](https://github.com/cycling-data-lab/structural-bounds-framework). A Zenodo DOI will be minted on submission acceptance via the GitHub–Zenodo bridge.

Sincerely,
Rohan Fossé (corresponding author, <rfosse@cesi.fr>, ORCID [0009-0002-2195-0198](https://orcid.org/0009-0002-2195-0198))
Gaël Pallares (ORCID [0009-0002-8680-604X](https://orcid.org/0009-0002-8680-604X))

---

## Suggested reviewers

Per the JMLR submission portal's optional reviewer-suggestion field, in declining order of fit:

1. **Antonio Ortega** (USC) — graph signal processing, sampling theory on graphs (Anis–Gadde–Ortega 2016 is a foundational reference for our framework).
2. **Yonina C. Eldar** (Weizmann) — generalised sampling, subspace priors (Tanaka–Eldar 2020 IEEE TSP underpins the arbitrary-subspace extension we use in Appendix A of the SI).
3. **Maxim Raginsky** (UIUC) — information-theoretic generalisation bounds (Xu–Raginsky 2017 is the closest methodological neighbour in the information-theoretic lane our spectral lane complements).
4. **Steve Hanneke** (Purdue) — theory of active learning (Hanneke 2014 is the standard reference for the label-complexity rate our Corollary C3 reproduces in the graph setting).

We respectfully request that the manuscript not be assigned to reviewers whose interests are primarily in continuous-Hilbert-space noisy inverse-problem theory (Bauer–Pereverzev style), as these reviewers may expect the rate-analysis machinery of that lane, which we explicitly do not invoke (and explain why in Appendix E of the SI). The relevant minimax theory for our problem is the finite-population empirical-risk one, not the inverse-problem one.

---

## Reproducibility statement

All numerical results in the manuscript are reproducible from publicly archived scripts. Master random seed = 42. Python 3.12 with pinned dependencies (`requirements.txt`). Per-row reproducibility map for the empirical Table 1 is in Appendix D of the SI, naming the exact script per repository per row. Figure 1 is generated by `experiments/d01_spectral_projection_figure.py` in the submission repository; it executes in under 1 s and produces `figures/fig1_spectral_projection.pdf`.

---

*This cover letter is held in the repository at [cover_letter.md](./cover_letter.md). Replace `[submission date]` before pasting into the JMLR / FoCM submission portal.*
