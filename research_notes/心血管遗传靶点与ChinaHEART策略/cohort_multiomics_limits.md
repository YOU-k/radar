# What large cohorts plus multi-omics can and cannot deliver for CVD (as of Sept 2026)

Scope: plasma proteomics (Olink/SomaScan), NMR metabolomics, PRS, MR (drug-target/cis-pQTL, colocalization). Sources: web (primary papers/abstracts via Europe PMC, journal pages, trial press releases) plus the local curated evidence base `/data/yy_data/radar/background/cardio-omics/report.md` (92 papers; cited below as "local [n]" with the underlying DOI). Items marked **[UNVERIFIED]** come from background knowledge and could not be re-checked in this session.

---

## Q1. Proteomic/metabolomic risk scores (UKB-PPP, deCODE, 2024-2026 papers): what are the actual gains over clinical scores?

### Takeaway
Across UKB-derived studies, adding plasma proteins to SCORE2/PREVENT-type models raises the C-index by about +0.03 to +0.07 when the analysis is done carefully (sex-specific, sparse models, clinical baseline kept). Larger deltas (+0.10) come from comparisons against weak baselines. NMR metabolomics adds about +0.015 to +0.02. Nearly all of this evidence comes from one cohort (UKB, Olink, European, healthy-volunteer). No study yet shows that measuring proteins changes treatment decisions or outcomes, and no guideline recommends it.

### Cited Findings
**Resources**
- UKB-PPP (Sun et al., Nature 2023): Olink Explore 3072 in 54,219 participants, 2,941 analytes / 2,923 unique proteins. It reported 14,287 primary pQTLs, 81% of them previously undescribed, and included ancestry-specific mapping in non-Europeans — [Sun 2023 Nature](https://www.nature.com/articles/s41586-023-06592-6); local [26].
- Eldjarn et al., Nature 2023: Olink (UKB, >50k) was compared with SomaScan v4 (Iceland, 36k), with 1,514 individuals measured on both. The platforms were only modestly correlated. Both had cis-pQTLs for a similar number of assays (2,101 Olink vs 2,120 SomaScan), but the share of assays with a cis-pQTL was 72% for Olink vs 43% for SomaScan. Many proteins had platform-discordant genomic associations — [Eldjarn 2023 Nature](https://www.nature.com/articles/s41586-023-06563-x) (abstract via Europe PMC). SomaScan was more precise (median CV 9.9% vs 16.5%) — [secondary summary, PubMed 39040172](https://pubmed.ncbi.nlm.nih.gov/39040172/).
- In 3,976 Chinese adults (CKB) measured on both platforms for 2,168 proteins, the median cross-platform rho was **0.29**. Of 1,694 one-to-one matched proteins, 765 (Olink) and 513 (SomaScan) had cis-pQTLs, and only 400 had colocalising cis-pQTLs on both. Olink found 279 proteins associated with IHD and SomaScan 154. Adding proteins to conventional risk factors for IHD raised the C-statistic from 0.845 to 0.862 with Olink (NRI 12.2%) and to 0.863 with SomaScan (NRI 16.4%) — [Nat Commun 2025](https://www.nature.com/articles/s41467-025-56935-2).

**Prediction deltas**
- Carrasco-Zanini et al., Nat Med 2024: 41,931 UKB-PPP participants, 218 diseases. Sparse 5–20-protein models beat basic clinical models for 67 diseases, with a median ΔC of **0.07** (range 0.02–0.31). They also beat clinical-plus-37-clinical-assay models for 52 diseases. The biggest gains were in non-CVD diseases (myeloma, NHL); among cardiac outcomes only dilated cardiomyopathy was highlighted. Six diseases were replicated in EPIC-Norfolk — [Nat Med 2024](https://doi.org/10.1038/s41591-024-03142-z); local [28].
- Sex-specific signature (UKB, 47,382 people, Olink; 2,085 usable proteins): 18 proteins raised SCORE2's C-index from 0.713 to **0.778** (+0.065). WFDC2 and GDF15 contributed more than NT-proBNP — [J Adv Res 2025, PMC12766183](https://pmc.ncbi.nlm.nih.gov/articles/PMC12766183/).
- 117-protein ProtRS (UKB-PPP, 44,431 people, 1,460 proteins): C-index 0.769, vs SCORE2 0.667, PREVENT 0.645 and FRS 0.672. Adding it to the baseline moved C from 0.669 to 0.774 (**ΔC 0.105**). Note the unusually low baselines (PREVENT 0.645) — [J Adv Res 2026](https://doi.org/10.1016/j.jare.2026.06.034); local [9].
- "Modest" result (UKB, 38,380 people, 2,919 proteins, XGBoost): SCORE2 AUC 0.740. Adding **114 proteins** gave 0.771 (NRI 0.140), while adding just 10 conventional risk factors gave 0.767 (NRI 0.053). Most of the protein gain can therefore be matched by better clinical covariates — [medRxiv 2024](https://doi.org/10.1101/2024.03.13.24304196); local [10].
- Inflammation panel (CRP plus 73 Olink inflammation proteins): SCORE2 C rose from 0.716 to 0.750 in UKB internal validation, with a second European cohort — [PubMed 40801988](https://pubmed.ncbi.nlm.nih.gov/40801988/).
- Circulation 2024 (UKB, 51,859 people, 13.6-year follow-up, 4,857 MACE): NT-proBNP HR 1.68 per SD. A protein-plus-age/sex LASSO model beat PREVENT on C, NRI and calibration — [Circulation 2024](https://doi.org/10.1161/CIRCULATIONAHA.124.070454); local [29].
- 202-protein CAD score: internal AUC rose from 0.750 to 0.789. The external baseline was 0.717, and the full text on external gain was not retrieved — [JAHA 2026](https://doi.org/10.1161/JAHA.125.047248); local [30].
- AF (outside CAD, for context): a 165-protein score took C from 0.771 to 0.816 on top of CHARGE-AF + NT-proBNP + PRS, with external validation in ARIC (n=11,012) — [Circulation 2025](https://doi.org/10.1161/circulationaha.124.073457); local [33].
- NMR metabolomics: 13 of 249 Nightingale metabolites added to SCORE2 moved C from 0.691 to **0.710** in UKB (n=187,039) and from 0.673 to **0.688** in ESTHER (n=5,578). GlycA contributed most — [medRxiv 2024](https://doi.org/10.1101/2024.04.29.24306593); local [49].
- ESC review (EHJ 2023): targeted proteomics and lipidomics are not in any guideline, and existing studies lack clinical-utility evidence — [EHJ 2023](https://doi.org/10.1093/eurheartj/ehad161); local [13].

### Inferences
- A realistic ΔC for proteomics over a well-specified clinical score is about **0.03–0.065**. Reported ΔC ≥0.10 mostly reflects weak or mis-specified baselines (e.g., PREVENT C=0.645 in a UKB subset) and should be treated with suspicion.
- Much of the "signal" comes from markers of prevalent subclinical disease and organ damage (NT-proBNP, GDF15, WFDC2, cystatin-like renal markers). This is prediction of current disease state, not new aetiology. It overlaps with measures that are cheap already (NT-proBNP, hs-troponin, eGFR, CRP).
- Platform discordance is large enough (median rho 0.29 in CKB) that a score built on Olink cannot be assumed to port to SomaScan, or to a clinical immunoassay, without recalibration and often re-derivation.
- Proteomics beats NMR metabolomics on ΔC (~0.03–0.07 vs ~0.015–0.02). The local report notes that no head-to-head cost-per-event-prevented comparison exists.

### Gaps
- No RCT or implementation study has tested proteomic-score-guided therapy for CVD.
- There are almost no external validations outside UKB/EPIC-Norfolk/ESTHER/KORA, and East Asian cohorts hold essentially no prediction-model external validation. CKB appears only as a 1,937-person association replication (local [12]) and a platform comparison. ChinaHEART has a 28-protein MSD nested case–control study for carotid plaque (local [87], BMJ Open 2026).
- Cost-effectiveness analyses for proteomic screening were not found.

---

## Q2. PRS for CAD: clinical utility evidence, ancestry transferability, East Asian performance, AHA/ESC statements

### Takeaway
The CAD PRS reliably adds about ΔC +0.01–0.02 (NRI a few %) over clinical scores. Its population-level yield is small: about 1 extra CVD event prevented per 5,750 people screened. Targeting the intermediate-risk group raises this to about 1 per 340. The only outcome-level RCT evidence is a very small trial (MI-GENES, 11 total MACE). Performance in East Asians is similar in ΔC but relies on much smaller GWAS. ESC (2025) and AHA (2022) do not recommend routine use.

### Cited Findings
- UKB, 306,654 people without CVD or statins: the conventional model had C 0.710. PRS added **+0.012** (95% CI 0.009–0.015), with continuous NRI about 10% in cases and 12% in non-cases. Population-wide PRS screening would prevent **1 extra event per ~5,750 screened**. Screening only the intermediate-risk (5–<10%) group would prevent **1 per ~340**, i.e. 7% more events prevented. The gain was about 1.5× that of adding CRP. European-only; no health economics — [Sun et al., PLoS Med 2021](https://doi.org/10.1371/journal.pmed.1003498); local [22].
- ESC clinical consensus statement (EHJ 2025;46:1372): typical ΔC is **+0.01 to +0.03**. Categorical NRI in the summarised studies ranged from 1.1–9.7% up to 16.2%, with +6.3% for SCORE2 integration and +3.5% categorical / +25.8% continuous in the Chinese study. ESC guidelines "do not currently advocate their use in routine clinical practice". Possible roles are people near a treatment threshold and younger adults with strong family history. PRS perform best in Europeans — [ESC CCS 2025](https://academic.oup.com/eurheartj/article/46/15/1372/8001983).
- AHA scientific statement (Circulation 2022): PRS are entering clinical settings, but clinical utility, equity and implementation remain unresolved — [AHA 2022](https://doi.org/10.1161/CIR.0000000000001077); local [37].
- East Asian metaPRS (Lu et al., EHJ 2022): 540 variants, trained in 2,800 cases / 2,055 controls, validated in 41,271 China-PAR participants (13.0-year mean follow-up, 1,303 CAD cases). Top vs bottom quintile HR 2.91 (2.43–3.49), lifetime risk 15.9% vs 5.8%. Added to the clinical score: **ΔC ≈ 1%, NRI 3.5%**. Intermediate-clinical-risk people with high PRS reached a 10-year risk of 4.6%, vs 4.8% for high-clinical-risk people with intermediate PRS — [EHJ 2022](https://doi.org/10.1093/eurheartj/ehac093); local [38].
- CKB (~100k genotyped): the best PRS gave "minimal improvement" over the traditional model, attributed to the lack of large Chinese CAD GWAS — [Chin Med J 2023](https://doi.org/10.1097/CM9.0000000000002694); local [11]. Correction to the local report: the ΔC ~0.01 / NRI 3.5% figures quoted for [11] actually match Lu 2022 [38]. The two Chinese studies therefore agree numerically and differ mainly in framing ("minimal" vs "improves stratification").
- Multi-ancestry GPS_Mult (Patel et al., Nat Med 2023): built from 269k cases / 1.178M controls plus >2M related-trait GWAS. It improves prediction in all ancestries, but non-European performance is still lower and incident-disease prediction weaker — [Nat Med 2023](https://doi.org/10.1038/s41591-023-02429-x); local [36].
- Multi-ethnic ASCVD-IRT (PRS + PCE) NRI: White 2.7%, Black 2.5%, South Asian 8.7%, Hispanic 7.5% with CI crossing 0 — [Am J Cardiol 2021](https://doi.org/10.1016/j.amjcard.2021.02.032); local [23].
- MI-GENES RCT (Mayo; n=203 randomized to Framingham-only vs integrated risk incl. PRS): at 6 months the PRS arm had more statin initiation and lower LDL-C. Over 9.5-year median follow-up there were 9 vs 2 MACE (HR 0.20, 95% CI 0.04–0.94, P=0.042). The event count is tiny, making this hypothesis-generating — [MI-GENES 10-yr, PMC11275655](https://pmc.ncbi.nlm.nih.gov/articles/PMC11275655/). Note: the "MI-GENiUS" named in the brief appears to be MI-GENES; no trial called "GENRE" was found. The Italian "GENRISK/high-PRS personalized prevention" pilot RCT (EHJ Open 2022) is another small feasibility study — [EHJ Open 2022](https://academic.oup.com/ehjopen/article/2/6/oeac079/6912223).
- Treatment-effect heterogeneity: in statin trials, relative risk reduction increased across genetic-risk strata (13% low, 29% intermediate, 48% high) — [Mega et al., Lancet 2015](https://thelancet.com/journals/lancet/article/PIIS0140-6736(14)61730-X/fulltext). A pragmatic PRS-guided statin trial (EE-PRS, Estonia) has published a protocol only — [EE-PRS protocol](https://pmc.ncbi.nlm.nih.gov/articles/PMC13218102/).
- ESCALATE (Australia): non-randomised implementation of PRS-triaged CAC scanning in 1,000 people aged 45–65. Only protocol and design have been published; no outcomes yet — [AHJ 2023 protocol](https://doi.org/10.1016/j.ahj.2023.06.009); local [89][90].

### Inferences
- The case for the PRS is not discrimination. It rests on being lifelong and measured once, on its value in young people before clinical risk factors appear, and on possible statin-benefit enrichment. These are exactly the claims with the weakest RCT evidence.
- For Chinese populations, an East Asian PRS gives about ΔC 0.01 on top of China-PAR. Whether that justifies genotyping depends on cost and on using it as a CAC or lipid-lowering triage tool, which is untested in China.

### Gaps
- There is no adequately powered RCT with hard endpoints for PRS-guided prevention.
- No East Asian implementation trial was found.
- The large-scale PRS-guided RCTs mentioned in the literature do not appear to have reported yet, and their status is unverified.

---

## Q3. Causal target discovery yield: how many observational protein associations survive MR/colocalization, and how well has drug-target MR predicted CVD trials?

### Takeaway
Only about 7–8% of observational protein–CVD associations get MR support, and about 3% survive colocalization. The one systematic UKB+CKB example: 636 associated proteins, 47 with MR support, 18 colocalized. At program level, genetic support raises drug approval odds about 2.6× (Minikel 2024). But the 2026 CVD trial record shows the ceiling. MR correctly predicted failure of HDL-raising and likely predicted apoB-proportional CETP benefit. Yet two genetically strongly supported targets have just posted neutral outcome trials: IL-6 (ZEUS, Aug 2026) and Lp(a) (pelacarsen HORIZON, Sep 2026). MR predicts a lifelong small perturbation, not what a drug does when started late, in secondary prevention, on top of background therapy.

### Cited Findings
**Yield**
- UKB, 52,164 people, 2,919 proteins, with 1,937-person replication in CKB: 636 proteins associated with any CVD (MI/IS/HF), 126 with all three, and 118 replicated in CKB. MR supported **47**, and **18** colocalized (e.g., FGF5, PROCR, FURIN). The authors state that most observational associations are non-causal and that some MR-supported proteins are poorly expressed in heart or artery — [Nat Cardiovasc Res 2024](https://doi.org/10.1038/s44161-024-00545-6); local [12]. So 47/636 = 7.4% and 18/636 = 2.8%.
- In CKB, only 400 of 1,694 matched proteins have colocalising cis-pQTLs on both Olink and SomaScan — [Nat Commun 2025](https://www.nature.com/articles/s41467-025-56935-2). So the pool of instrumentable proteins that agree across platforms is itself only about 24% of matched proteins.
- UKB-PPP + deCODE cis-pQTL MR (5,813 proteins) against arteriosclerosis traits and 8 CVD endpoints prioritised just **10 proteins**. Risk-increasing: ANGPTL4, APOB, BRAP, LPA, ZPR1. Risk-decreasing: DUSP13, FN1, IL6R, MMP12. Most are already known lipid or inflammation targets — [Cardiovasc Res 2026 / medRxiv 2025](https://doi.org/10.1093/cvr/cvag095); local [43].
- Lipid-target genetics (Nat Commun 2021): of 341 lipid-associated drug targets, 30 were robustly prioritised for CHD, including NPC1L1 and PCSK9. The authors note that concordance with trials is highest when MR says a biomarker is not causal — [Nat Commun 2021](https://www.nature.com/articles/s41467-021-25731-z).
- Minikel et al., Nature 2024: drug mechanisms with human genetic support are **2.6×** more likely to succeed from phase I to approval. The effect varies by therapy area and grows with confidence in the causal gene, but is largely independent of effect size or allele frequency — [Nature 2024](https://www.nature.com/articles/s41586-024-07316-0).
- Systematic MR-vs-RCT comparison (Sobczyk, Davey Smith, Gaunt; BMJ Open 2023): 26 exposure–outcome pairs, 54 MR and 77 RCT publications. Only 3 drugs had both MR and RCT evidence (PCSK9 mAbs, mipomersen, ustekinumab). There was substantial concordance for several pairs and discordance for others. Automated triangulation was hampered because only 13% of RCTs posted results — [BMJ Open 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10533809).

**Trial track record (CVD)**
- HDL-C: Mendelian-randomization evidence against HDL causality (Voight et al., Lancet 2012) preceded or accompanied failed HDL-raising trials (niacin, dalcetrapib, torcetrapib) **[UNVERIFIED this session; Voight 2012 doi:10.1016/S0140-6736(12)60312-2]**. This is the canonical "MR predicted the null" case.
- CETP: factorial MR (Ference et al., JAMA 2017; 102,837 people, 13,821 events) showed that CETP-variant benefit tracks apoB/non-HDL reduction, not HDL rise. This is consistent with REVEAL (anacetrapib) — [JACC review 2018](https://www.jacc.org/doi/10.1016/j.jacc.2018.10.072). REVEAL itself showed about a 9% relative reduction in major coronary events at 4.1 years, rising to about 20% in extended follow-up **[UNVERIFIED this session; the search-engine summary giving "18%" is not a primary source]**. Obicetrapib (PREVAIL) primary completion is about Nov 2026, with results not yet reported — [ClinicalTrials.gov NCT05202509](https://clinicaltrials.gov/study/NCT05202509). A pooled phase 3 MACE analysis was hypothesis-generating — [JACC 2025](https://www.jacc.org/doi/10.1016/j.jacc.2025.07.056).
- IL-6 / IL6R: the IL6R Asp358Ala MR (Lancet 2012) supported IL-6 signalling as causal for CHD **[UNVERIFIED numbers this session]**. **ZEUS** (ziltivekimab, n≈6,376 with ASCVD + CKD + hsCRP ≥2 mg/L) reported 3-point MACE HR **0.99 (0.88–1.11)** despite lowering IL-6 and CRP as expected, with more serious infections. Novo's CSO: "the expected biological effect ... did not result in MACE benefits." HERMES (HF) and ARTEMIS (post-MI) are due in H1 2027 — [TCTMD, Aug 2026](https://www.tctmd.com/news/zeus-trial-ziltivekimab-fails-reduce-mace-ascvd-patients); [HCPLive](https://www.hcplive.com/view/ziltivekimab-fails-to-reduce-mace-risk-in-phase-3-zeus-trial). Full data had not yet been presented at the time of these reports.
- Lp(a): genetics (LPA variants, Mendelian and observational) strongly implicated Lp(a) as causal (e.g., UKB 43-SNP LPA GRS — [JAMA Cardiol 2020](https://doi.org/10.1001/jamacardio.2020.5398); local [41]). **Lp(a)HORIZON** (pelacarsen, n=8,323, established CVD, Lp(a) ≥70 mg/dL, subgroup ≥90 mg/dL) **did not meet its primary 4-point MACE endpoint** (topline 4 Sep 2026). No HR or percent Lp(a) lowering has been released yet, and full data are awaited at a congress — [Novartis 4 Sep 2026](https://www.novartis.com/news/media-releases/novartis-announces-lpahorizon-phase-iii-topline-results-pelacarsen-patients-elevated-lpa-and-established-cardiovascular-disease-cvd); [NLA](https://www.lipid.org/resource/top-line-results-from-the-phase-3-lpahorizon-trial/). Olpasiran (OCEAN(a)-Outcomes) and lepodisiran results were not found in this search (gap).
- PCSK9 and NPC1L1: genetic prediction was confirmed by FOURIER/ODYSSEY and IMPROVE-IT — [Sobczyk 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10533809); [Nat Commun 2021](https://www.nature.com/articles/s41467-021-25731-z).

### Inferences
- Scorecard for CVD: MR gets the **direction** right for lipid targets (PCSK9, NPC1L1, HMGCR, CETP via apoB) and for HDL nulls. It has **not** reliably predicted **magnitude or trial success** for non-LDL targets. The two most genetically validated non-LDL targets (IL-6, Lp(a)) both returned neutral phase 3 results in Aug–Sep 2026.
- Plausible explanations for Lp(a) and IL-6, to be checked against the full data:
  - (a) Absolute exposure reduction needed. MR-based estimates suggested very large Lp(a) reductions (on the order of 50–100 mg/dL) are required for a clinically meaningful MACE effect. This is a known published estimate **[UNVERIFIED this session]**.
  - (b) Lifetime vs late-life exposure.
  - (c) Secondary prevention on intensive background therapy.
  - (d) Target engagement in plasma vs tissue.
  - (e) CKD-specific population in ZEUS.
- Both failures should be framed as "genetic support ≠ trial success at a given dose, duration and population", not as MR being wrong about causality. Genetics predicts perturbation of lifelong exposure.
- Proteins chosen for prediction (NT-proBNP, GDF15, WFDC2) and those chosen by MR (LPA, APOB, IL6R, PCSK9) barely overlap (local report §6). Prediction and target discovery are separate products from the same data.

### Gaps
- Full HR/CI and Lp(a)-lowering magnitude for HORIZON; full ZEUS publication; OCEAN(a) and PREVAIL results. All are pending as of late Sep 2026.
- No CVD-specific quantitative study was found giving the rate at which cis-pQTL MR hits later succeed in phase 2/3.

---

## Q4. Known failure modes (pleiotropy, weak instruments, trans-pQTL, platform, epitope, reverse causation, selection bias)

### Takeaway
The biggest practical threats are platform/epitope artefacts in pQTLs, trans-/pleiotropic instruments, and non-representative sampling in UKB. Each can create or erase apparent causal protein effects. These problems hit cohort proteogenomics directly and are not fixed by larger N.

### Cited Findings
- **Platform discordance.**
  - Olink vs SomaScan median rho 0.29 (CKB, 2,168 proteins). Correlation depends on abundance and data quality — [Nat Commun 2025](https://www.nature.com/articles/s41467-025-56935-2).
  - Cis-pQTL support was 72% of Olink assays vs 43% of SomaScan, and many proteins had platform-specific genomic associations that "may influence conclusions drawn from the integration of protein levels with the study of diseases" — [Eldjarn 2023](https://www.nature.com/articles/s41586-023-06563-x).
  - As the platforms expand coverage (SomaScan 7k/11k, Olink Explore HT), the comparison changes — [PubMed 39040172](https://pubmed.ncbi.nlm.nih.gov/39040172/).
- **Epitope effects.** Protein-altering variants can change affinity-reagent binding without changing protein abundance, producing spurious cis-pQTLs. This is why concordance across both platforms, plus conditioning on missense variants, is used as a sensitivity check (Eldjarn 2023; Sun 2023). Exact proportions were not retrieved this session (gap).
- **Participation/collider bias in UKB.** Weighting UKB to be representative (14 harmonized variables; n_eff about 95k–102k vs 263k–284k unweighted) changed SNP effect sizes and yielded new loci for 12/19 traits. It shifted genetic correlations by up to 0.31 and MR estimates by up to 0.15 SD for socio-behavioural traits, while h² changed by ≤5% — [Schoeler et al., Nat Hum Behav 2023](https://www.nature.com/articles/s41562-023-01579-9). The UKB response rate was about 5.5% with a documented healthy-volunteer effect **[UNVERIFIED; Fry et al., AJE 2017]**. The metabolomics study excluding ages 40–49 to reduce healthy-volunteer bias is an example of mitigation — local [52].
- **Population stratification, assortative mating and indirect genetic effects.** Within-sibship GWAS of 178,086 siblings in 19 cohorts found smaller effects than population GWAS for height, education, smoking and other traits. This altered genetic correlations and MR estimates (e.g., the education–BMI rg fell toward 0) — [Howe et al., Nat Genet 2022](https://www.nature.com/articles/s41588-022-01062-7).
- **Tissue relevance.** Some MR-supported plasma proteins show weak expression in heart or artery — local [12]. Plasma levels may not reflect activity in the vessel wall.
- **Drug-target MR pitfalls** (weak/trans instruments, LD with neighbouring genes, instrument-outcome confounding, non-linear or dose-duration mismatch) are reviewed in BMC Medicine Oct 2024 ("common pitfalls in drug target MR") — [DOAJ record](https://doaj.org/article/7b25030b6f094cc48073ca0e8a6b8685) — and in the EHJ 2023 CVD MR review — [EHJ 2023](https://academic.oup.com/eurheartj/article/44/47/4913/7343270).
- **Reverse causation in observational proteomics.** The strongest predictive proteins (NT-proBNP HR 1.68/SD; local [29]) mark existing cardiac stress. Adding "10 conventional risk factors" nearly matched 114 proteins (local [10]). Both suggest the signals partly reflect prevalent subclinical disease.

### Inferences
- A defensible cis-pQTL MR pipeline for CVD targets in 2026 should require:
  - cis-only instruments;
  - colocalization (PP.H4 high) on at least one platform, and ideally both or replication across ancestries;
  - exclusion of protein-altering variants in the instrument, or conditioning on them (epitope check);
  - a phenome-wide scan for on-target adverse effects;
  - triangulation with rare-variant LoF burden (e.g., UKB WES).
- UKB selection bias matters most for behaviour-linked exposures and for absolute risk calibration. It matters less for strong-instrument protein cis-MR, but that is unquantified for proteins specifically (gap).

### Gaps
- No quantitative estimate was found of the fraction of UKB-PPP cis-pQTLs driven by epitope effects.
- No study was found that quantifies selection bias specifically on protein–CVD MR estimates.

---

## Q5. What cross-sectional/one-timepoint cohort omics fundamentally cannot answer, and which methods raise the ceiling

### Takeaway
A single baseline plasma sample in a volunteer cohort cannot resolve:
- **tissue specificity** (plasma ≠ plaque or myocardium);
- **dynamics and timing** (when an intervention works; lifetime vs late exposure);
- **dose and duration** mapping from lifelong genetic perturbation to a drug started at 60;
- **heterogeneity of treatment effect**. Only RCTs, or emulations anchored to RCTs, provide this.

Repeated measures, within-family designs, multi-ancestry fine-mapping and target-trial emulation raise the ceiling. None of them replaces a trial.

### Cited Findings
- Genetic support predicts program success (2.6×) but is "largely unaffected by genetic effect size" — [Minikel 2024](https://www.nature.com/articles/s41586-024-07316-0). Genetics tells you whether a target is right, not how much drug to give or when.
- ZEUS: target engagement (IL-6/CRP lowered) produced no MACE change, HR 0.99 — [TCTMD 2026](https://www.tctmd.com/news/zeus-trial-ziltivekimab-fails-reduce-mace-ascvd-patients). HORIZON: Lp(a) lowered, primary endpoint missed — [Novartis 2026](https://www.novartis.com/news/media-releases/novartis-announces-lpahorizon-phase-iii-topline-results-pelacarsen-patients-elevated-lpa-and-established-cardiovascular-disease-cvd). Both illustrate the timing and population gap between lifelong genetic exposure and late-life therapy.
- **Longitudinal trajectories beat baseline-only values.** In the Kailuan T2DM cohort (n=16,378), functional PCA of 4-year risk-factor trajectories improved ML CVD prediction over baseline — [Cardiovasc Diabetol 2025](https://doi.org/10.1186/s12933-025-02611-0); local [19]. UKB-PPP includes a repeat-imaging and COVID subset with repeat proteomics (1,268 samples) — local [26].
- **Life-course exposure.** In CKB, early-adulthood BMI related to CVD independently of later weight change — [Lancet Public Health 2024](https://doi.org/10.1016/s2468-2667(24)00043-4); local [88]. A mid-life omics snapshot misses exposures that are already fixed by then.
- **Within-family designs** remove stratification and indirect effects — [Howe 2022](https://www.nature.com/articles/s41588-022-01062-7).
- **Participation weighting** corrects part of the UKB selection bias — [Schoeler 2023](https://www.nature.com/articles/s41562-023-01579-9).
- **Multi-ancestry data.**
  - Cross-ancestry AF GWAS (BBJ 9,826 cases + European 77,690 cases) found 5 new Japanese loci — [Nat Genet 2023](https://doi.org/10.1038/s41588-022-01284-9); local [35].
  - Ancestry-specific pQTL mapping in UKB-PPP improved localisation — [Eldjarn 2023](https://www.nature.com/articles/s41586-023-06563-x).
  - A cross-population proteome-wide MR of 2,922 proteins across 5 CVDs used population-specific instruments — [Mol Genet Genomics 2026](https://doi.org/10.1007/s00438-026-02458-4); local [42].
- **Target-trial emulation / RCT-benchmarked RWE.** DISCO (AI-ECG phenotypic matching) replicated PARADIGM-HF — [EHJ 2025 abstract](https://doi.org/10.1093/eurheartj/ehaf784.4614); local [91]. It remains an abstract, and residual confounding cannot be excluded.

### Inferences
- The ceiling-raising package for a Chinese cohort programme (e.g., ChinaHEART) could include:
  - (1) repeat proteomics in a subset, to separate stable (genetically anchored) from state proteins;
  - (2) East Asian cis-pQTL maps, to cut platform/epitope and LD artefacts and enable East-Asian-specific drug-target MR. CKB already shows cross-platform colocalisation for only 400 proteins;
  - (3) family or sibling subsamples where they exist;
  - (4) linkage to prescription and outcome data for target-trial emulation of existing drugs whose targets MR flags (PCSK9, IL-6, SGLT2, GLP-1R);
  - (5) pre-registered triangulation against pending trials (PREVAIL, OCEAN(a), HERMES/ARTEMIS) as calibration tests of the MR pipeline.
- Tissue specificity requires tissue-resolved molecular QTLs (plaque or myocardium eQTL/pQTL, single-cell), which a blood-only cohort cannot supply.

### Gaps
- Almost no published repeated-measure proteomics (≥2 timepoints) CVD prediction studies at scale were identified this session.
- No published sibling-based protein MR for CVD was found.
- Full details of Lp(a)HORIZON/ZEUS are needed to decide whether the failures reflect dose, timing or wrong causal model.

---

## Quick-reference numbers

| Item | Number | Source |
|---|---|---|
| Proteomics ΔC over SCORE2 (sex-specific, 18 proteins) | 0.713 → 0.778 | PMC12766183 |
| Proteomics ΔC (114 proteins vs +10 clinical vars) | 0.740 → 0.771 vs 0.767 | local [10] |
| Proteomics ΔC reported large | 0.669 → 0.774 | local [9] |
| Median ΔC across 67 diseases (Nat Med 2024) | 0.07 (0.02–0.31) | local [28] |
| IHD in CKB, Olink/SomaScan | 0.845 → 0.862 / 0.863; NRI 12.2% / 16.4% | Nat Commun 2025 |
| NMR metabolomics ΔC | 0.691 → 0.710 (UKB); 0.673 → 0.688 (ESTHER) | local [49] |
| PRS ΔC (UKB) | +0.012; NNS 5,750 (all) / 340 (intermediate) | PLoS Med 2021 |
| PRS ΔC (China-PAR, East Asian) | ≈+0.01; NRI 3.5%; top/bottom quintile HR 2.91 | EHJ 2022 |
| Obs → MR → coloc (UKB/CKB) | 636 → 47 → 18 | local [12] |
| Olink vs SomaScan rho (CKB) | median 0.29 | Nat Commun 2025 |
| cis-pQTL support Olink vs SomaScan | 72% vs 43% | Eldjarn 2023 |
| Genetic support approval RR | 2.6× | Minikel 2024 |
| ZEUS (IL-6) MACE HR | 0.99 (0.88–1.11) | TCTMD Aug 2026 |
| Lp(a)HORIZON | primary missed, n=8,323 | Novartis 4 Sep 2026 |
| MI-GENES MACE | 9 vs 2, HR 0.20 (0.04–0.94) | PMC11275655 |
