# Research strategies for cardiovascular disease beyond cohort association modeling (as of Sept 2026)

Scope: six strategy families, each mapped to the causal chain variant → molecule → cell → tissue → individual → population → intervention. Items marked **[UNVERIFIED]** come from background knowledge and were not confirmed by a source fetched in this session. The report writer should cite them cautiously or drop them.

## Q1. What each strategy can break open, its maturity, landmark examples, and limitations

### Takeaway
Perturbation biology (CRISPRi Perturb-seq in endothelial cells or SMCs, and iPSC models) combined with single-cell/spatial atlases is the most mature route from variant to molecule to cell. It has already converted CAD GWAS loci into pathways (the CCM2/TLNRD1 → KLF2/4 program). AI imaging and ECG phenotypes give scalable quantitative traits at the individual level. Pragmatic and registry trials (SSaSS, SECURE, DANFLU-2) answer population and intervention questions cheaply. CHIP is a real but smaller-than-first-thought causal axis: HR about 1.9 in early cohorts, but only about 1.07 in 63,700 trial patients, and IL-6 blockade failed in ZEUS.

### Cited Findings

**Strategy 1: iPSC-CMs, engineered tissue, organoids and vascular cells with CRISPR screens, Perturb-seq and MPRA (layers: variant → molecule → cell)**
- Schnitzler et al., Nature 2024 (626:799-807): CRISPRi Perturb-seq of all genes within ±500 kb of 241 CAD GWAS loci in teloHAEC endothelial cells. They tested 2,285 genes with 37,637 guides in about 215,000 cells, and found 50 programs (13 EC-specific, e.g. flow response and angiogenesis). The method links variants to genes (epigenomics), genes to programs (Perturb-seq), and then scores convergence. — [PMC preprint version](https://pmc.ncbi.nlm.nih.gov/articles/PMC10170398/); [Nature](https://www.nature.com/articles/s41586-024-07022-x); [ScienceDaily](https://www.sciencedaily.com/releases/2024/02/240207120525.htm)
- Key biology: knocking down CCM2 and its newly identified partner TLNRD1 induced atheroprotective, laminar-flow-like programs via MEKK3-ERK5-KLF2/4. Validation was done in primary ECs and zebrafish. — [ResearchGate/Nature summary](https://www.researchgate.net/publication/378039791_Convergence_of_coronary_artery_disease_genes_onto_endothelial_cell_programs); [PMC10170398](https://pmc.ncbi.nlm.nih.gov/articles/PMC10170398/)
- Earlier work: multimodal CRISPR perturbation (CRISPR KO/i/a) of CAD GWAS loci in vascular ECs, PLOS Genetics 2023. — [PLOS Genet](https://journals.plos.org/plosgenetics/article?id=10.1371%2Fjournal.pgen.1010680)
- Enhancer-targeting CRISPR screens at CAD loci (medRxiv Aug 2025) suggest shared mechanisms of disease risk (preprint). — [medRxiv](https://www.medrxiv.org/content/10.1101/2025.08.28.25334684.full.pdf)
- iPSC models of noncoding CVD variants: chamber-specific (atrial vs ventricular) enhancers carrying ECG-trait (PR, QT) variants. CRISPR epigenetic editing validated AF regulatory elements. LMNA-variant iPSC atrial CMs show disrupted chromatin at AF GWAS loci. Adenine base editing reached >98% efficiency and rescued phenotypes in mutant iPSC-CMs. — [Stem Cell Reports 2025 review](https://www.cell.com/stem-cell-reports/fulltext/S2213-6711(25)00071-2); [LMNA/AF PubMed](https://pubmed.ncbi.nlm.nih.gov/42156780/); [HCM base editing](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10293165/)
- Context-adding cocultures: iPSC atrial CMs plus atrial fibroblasts to model AF (Science Advances). This responds directly to the "no fibroblast context" limitation. — [Sci Adv](https://www.science.org/doi/10.1126/sciadv.adg1222)
- Limitations (well established; no single source fetched here): fetal-like immaturity of iPSC-CMs (automaticity, immature T-tubules and Ca handling, glycolytic metabolism), no immune, fibroblast or haemodynamic context in most screens, and immortalized cell lines (teloHAEC) that may not reflect in vivo states. Throughput of Perturb-seq in iPSC-CMs is still well below that in cell lines. **[UNVERIFIED as specific numbers]**
- Maturity: high for EC/SMC CAD loci (published genome-scale screens). Medium for iPSC-CM arrhythmia and cardiomyopathy variants (locus-by-locus). Low for HFpEF, which is a multi-organ syndrome that iPSC-CMs cannot recapitulate.

**Strategy 2: single-cell and spatial heart and vascular atlases (layers: cell → tissue; links variant to cell type)**
- Litviňuková et al., Nature 2020 (588:466-472), "Cells of the adult human heart": the first large Heart Cell Atlas. — [PMC7681775](https://pmc.ncbi.nlm.nih.gov/articles/PMC7681775/). Figures of about 487k cells/nuclei, 6 regions and 14 donors are **[UNVERIFIED in this session]**.
- Kanemaru et al., Nature 2023, "Spatially resolved multiomics of human cardiac niches": 704,296 cells/nuclei for GEX (211,060 new multiome nuclei), 144,762 nuclei for ATAC, 8 regions, 25 donors aged 20-75, 75 cell states including the conduction system. — [Nature](https://www.nature.com/articles/s41586-023-06311-1); [Sanger](https://www.sanger.ac.uk/news_item/detailed-map-of-the-heart-provides-new-insights-into-cardiac-health-and-disease/); [News-Medical](https://www.news-medical.net/news/20230712/New-heart-cell-atlas-reveals-detailed-structure-of-the-human-heart.aspx)
- Chaffin et al., Nature 2022: snRNA-seq of about 600,000 LV nuclei from 11 DCM, 15 HCM and 16 non-failing hearts. The data are on Broad Single Cell Portal SCP1303. — [Nature](https://www.nature.com/articles/s41586-022-04817-8); [SCP1303](https://singlecell.broadinstitute.org/single_cell/study/SCP1303/single-nuclei-profiling-of-human-dilated-and-hypertrophic-cardiomyopathy)
- Reichart et al. (Science 2022): 880,000 nuclei from 18 control and 61 failing non-ischemic hearts with pathogenic DCM/ACM variants or idiopathic disease. The paper shows genotype-specific cell composition and transcription. — [PMC9528698](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9528698/)
- Coronary artery: paired snRNA+snATAC data from 44 human coronary arteries gave 11,182 single-cell caQTLs. Heritability enrichment puts the largest CAD genetic risk in SMCs, and a COL4A1/COL4A2 variant becomes a caQTL as SMCs de-differentiate (medRxiv Nov 2024). — [medRxiv](https://www.medrxiv.org/content/10.1101/2024.11.13.24317257v1)
- The MetaPlaq multimodal atherosclerosis atlas has more than 1M cells across scRNA, scATAC and high-resolution spatial data, and maps GWAS signals to SMC and EC states (medRxiv/PMC 2026). — [PMC13232358](https://pmc.ncbi.nlm.nih.gov/articles/PMC13232358/)
- The integrated plaque atlas has about 250k annotated cells (Nat Commun 2025). An earlier meta-analysis of 118,578 coronary and carotid cells found SMC and pericyte signatures enriched for CAD, CAC and MI heritability (Cell Reports 2023). — [Nat Commun](https://www.nature.com/articles/s41467-025-63202-x); [Cell Rep](https://www.cell.com/cell-reports/fulltext/S221112472301392X)
- Limitations: cross-sectional explant or donor tissue (end-stage disease, and transplant/LVAD selection bias). Small N of donors, which limits eQTL power. Few HFpEF samples, because HFpEF myocardium is rarely biopsied. Nuclei-based data miss cytoplasmic transcripts.

**Strategy 3: AI-ECG and imaging foundation models as scalable quantitative phenotypes (layers: tissue → individual; they feed back into variant discovery through GWAS of the derived traits)**
- EchoPrime (Nature, Nov 2025): a multi-view, video-based vision-language model trained on more than 12M echo video-report pairs. It reached state of the art on 23 benchmarks across 5 international health systems and is announced as open source. — [Nature](https://www.nature.com/articles/s41586-025-09850-x); [Cedars-Sinai](https://www.cedars-sinai.org/newsroom/a-bigger-better-ai-tool-for-interpreting-common-heart-test/)
- Other echo foundation models include EchoFM (PMC) and EchoJEPA (arXiv 2602.02603, 2026 preprint). — [EchoFM](https://pmc.ncbi.nlm.nih.gov/articles/PMC12616925/); [EchoJEPA](https://arxiv.org/html/2602.02603v1)
- EAGLE pragmatic cluster RCT of AI-ECG (Nature Medicine 2021): 120 primary-care teams and 22,641 adults. New low-EF diagnosis within 90 days rose from 1.6% to 2.1% (OR 1.32). This is evidence that AI phenotypes change care, not just prediction. — [Nat Med](https://www.nature.com/articles/s41591-021-01335-4)
- UKB CMR deep-learning GWAS:
  - Regional LV wall thickness in 42,194 people gave 72 loci, with genetic insight into HCM.
  - DL-derived LV mass in 43,230 people gave 12 loci, 11 of them novel.
  - Ascending aorta diameters at 6 locations gave 79 loci, 35 of them novel.

  Pirruccello's group used 2.3M images from 43,317 participants. — [LV thickness GWAS](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10689443/); [LV mass Nat Commun 2023](https://www.nature.com/articles/s41467-023-37173-w); [Aorta JACC](https://www.sciencedirect.com/science/article/pii/S0735109722051634)
- Limitations: models trained on single systems are prone to shortcut learning. UKB imaging covers mostly healthy European middle-aged people, so few HFpEF or AF cases are imaged. A GWAS of a derived trait inherits the model's biases. Prospective outcome benefit beyond diagnosis yield is rarely shown.

**Strategy 4: longitudinal deep phenotyping (repeat proteomics, wearables, continuous monitoring) (layers: molecule → individual trajectory)**
- UKB-PPP: Olink plasma proteomics in 54,219 participants and 2,923 proteins gave 14,287 primary pQTLs, 81% of them novel, from a consortium of 13 pharma companies (Nature 2023). A 2025 expansion to the "world's largest protein study" (about 600k samples including repeats; figure **[UNVERIFIED]**) was announced. — [Nature](https://www.nature.com/articles/s41586-023-06592-6); [AWS registry](https://registry.opendata.aws/ukbppp/); [QMUL 2025](https://www.qmul.ac.uk/media/news/2025/medicine-and-dentistry/fmd/uk-biobank-launches-the-worlds-largest-protein-study-to-unlock-new-medical-breakthroughs.html)
- Caveat: Olink measurements can disagree with clinical assays in UKB. — [PMC12687865](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12687865/)
- Apple Heart Study (NEJM 2019): 419,297 participants. 0.52% received irregular-pulse notifications. AF was present on 34% of returned patches, and PPV for concurrent notification was 0.84. — [NEJM](https://www.nejm.org/doi/full/10.1056/NEJMoa1901183); [HCPLive](https://www.hcplive.com/view/apple-heart-study-watch-device-afib-detection)
- Limitations: repeat proteomics exists in only a small subset. Wearable cohorts are biased toward young, healthy and wealthy users. Data from devices like Fitbit in All of Us are gated in a controlled workbench (no specific AF result fetched; **[UNVERIFIED]**).

**Strategy 5: pragmatic, registry-based RCTs, target-trial emulation, stratified trials and population interventions (layers: population → intervention)**
- SSaSS (NEJM 2021): cluster RCT in 600 Chinese villages with 20,995 people. Salt substitute reduced stroke from 33.65 to 29.14 per 1,000 person-years (RR 0.86, 95% CI 0.77-0.96). — [NEJM](https://www.nejm.org/doi/full/10.1056/NEJMoa2105675)
- SECURE polypill (NEJM 2022): 2,499 post-MI elderly patients. MACE 9.5% vs 12.7% (HR 0.76, 0.60-0.96). Key secondary outcome HR 0.70. — [NEJM](https://www.nejm.org/doi/full/10.1056/NEJMoa2208275); [ACC](https://www.acc.org/Latest-in-Cardiology/Articles/2022/08/25/19/13/fri-848am-SECURE-esc-2022)
- TIPS-3 polypill in primary prevention (NEJM 2021). — [NEJM](https://www.nejm.org/doi/full/10.1056/NEJMoa2028220)
- DANFLU-2: registry-based, individually randomized pragmatic trial of 332,438 Danes aged ≥65, comparing high-dose vs standard-dose flu vaccine with CV outcomes. — [AHJ design](https://www.sciencedirect.com/science/article/pii/S000287032500287X); [PMC results](https://pmc.ncbi.nlm.nih.gov/articles/PMC12579978/)
- Target-trial emulation guides for CV research (EJPC 2026) and a systematic review of TTE of diabetes CVOTs (J Clin Epi 2025) show that TTE often reproduces RCT results when protocols are explicit. — [EJPC](https://academic.oup.com/eurjpc/advance-article/doi/10.1093/eurjpc/zwag267/8691342); [JCE](https://www.jclinepi.com/article/S0895-4356(25)00205-7/fulltext)
- TASTE (Swedish registry-based RCT of thrombus aspiration, about 7,244 patients, neutral; NEJM 2013) is the classic RRCT exemplar. **[UNVERIFIED in this session]**
- Limitations: RRCTs need national registries plus trial infrastructure. TTE cannot fix unmeasured confounding or immortal-time errors without careful design. Biomarker-stratified trials need a validated biomarker first (see CHIP below).

**Strategy 6: clonal hematopoiesis and somatic mutation (layers: somatic variant → myeloid cell → vessel → individual)**
- Jaiswal et al., NEJM 2017: CHIP was associated with CHD HR 1.9 (95% CI 1.4-2.7). Early-onset MI and TET2/JAK2 carried a larger effect. — [NEJM](https://www.nejm.org/doi/full/10.1056/NEJMoa1701719)
- Mechanism: Tet2 loss drives IL-1β/IL-6/NLRP3, and IL-6 blockade alleviates atherosclerosis in Tet2-CH mice. Tet2 CHIP also raises AF risk via NLRP3 (Circulation 2024). — [JCI review](https://www.jci.org/articles/view/180066); [Circulation](https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.123.065597)
- CANTOS exploratory analysis: TET2-CHIP carriers had MACE HR 0.38 (0.15-0.96) on canakinumab (small N, hypothesis-generating). — [PubMed](https://pubmed.ncbi.nlm.nih.gov/35385050/)
- Counterweight (Nat Med 2024): in 63,700 patients from 5 TIMI trials, CHIP gave an aHR for CV events of only 1.07 (0.99-1.16) over a median of 2.5 years. CHIP was linked to first but not recurrent MI, and showed no heterogeneity of benefit for PCSK9, SGLT2, P2Y12 or FXa therapies. — [PubMed](https://pubmed.ncbi.nlm.nih.gov/39107561/)
- ZEUS phase 3 (topline Jul-Aug 2026): ziltivekimab (anti-IL-6) in more than 6,300 ASCVD+CKD patients with hsCRP ≥2 gave a MACE HR of 0.99 (0.88-1.11) despite lowering IL-6 and hsCRP. HERMES (HF) and ARTEMIS (post-MI) read out in H1 2027. — [TCTMD](https://www.tctmd.com/news/zeus-trial-ziltivekimab-fails-reduce-mace-ascvd-patients); [Novo release](https://www.globenewswire.com/news-release/2026/07/31/3336733/0/en/novo-nordisk-provides-update-on-the-zeus-phase-3-trial-in-people-with-ascvd-ckd-and-inflammation.html)
- A CHIP-stratified trial of IL-1β inhibition in TET2 CH (NCT06691217) is ongoing, with an imaging endpoint for vascular inflammation. — [ClinicalTrials.gov](https://clinicaltrials.gov/study/NCT06691217)

### Inferences
- Coverage of the causal chain: CRISPR/Perturb-seq and iPSC (variant → cell) → atlases (cell → tissue, plus locus-to-cell-type mapping) → AI-imaging/ECG phenotypes (tissue → individual, closing the loop back to GWAS) → longitudinal proteomics/wearables (individual trajectory) → pragmatic/registry RCTs and TTE (population → intervention). CHIP runs vertically through all layers as an acquired genotype.
- ZEUS weakens the "inflammation lowering for everyone" thesis and the unselected IL-6 strategy. That makes genotype-stratified designs (TET2 CHIP, IL6R variants) more rather than less important. It is also a reminder that target engagement (hsCRP) is not a validated surrogate.
- CHIP's per-person effect in older high-risk secondary-prevention patients (HR about 1.07) is much smaller than early population estimates (about 1.9). This suggests clone size, gene and age strongly modify risk, and that CHIP is more useful for primary-prevention "who/when" than for secondary-prevention drug choice.

### Gaps
- Exact Litviňuková 2020 cell and donor counts, and TASTE details, were not verified in this session.
- No fetched source gave a public genome-scale Perturb-seq dataset in iPSC-CMs. Current CM screens appear locus-limited, but this was not confirmed exhaustively.
- CMR and ECG foundation models from 2024-2026 other than EchoPrime (e.g., CMR-FM, ECG-FM, HuBERT-ECG) were not individually verified.
- Full ZEUS results (subgroups by CHIP or IL6 genotype) are not yet published.

## Q2. Which strategy best addresses HFpEF/AF "no validated target" versus ASCVD "who/when to treat"?

### Takeaway
For HFpEF and AF, the bottleneck is the variant → cell → mechanism link. Discovery therefore comes from genetics plus proteome-wide MR, together with context-rich perturbation models (iPSC atrial CM + fibroblast cocultures, EHT) and AI-derived quantitative sub-phenotypes that raise GWAS power. For ASCVD, targets already exist (LDL, Lp(a), PCSK9, inflammation), so the leverage is at the individual → population → intervention layers. The tools there are AI-ECG/imaging risk phenotypes, repeat proteomics, CHIP as a risk axis, and cheap pragmatic, registry or cluster trials (polypill, salt substitute, TTE) to decide whom to treat and when.

### Cited Findings
- HFpEF: multi-omics MR on the largest HFpEF/HFrEF genetic dataset identified 58 potential subtype-specific targets with target profiles (Nat Cardiovasc Res 2025). This shows that target discovery for HFpEF still sits at the hypothesis stage. — [Nat Cardiovasc Res](https://www.nature.com/articles/s44161-025-00609-1)
- HF proteomic MR plus colocalization nominated CAMK2D, PRKD1, PRKD3, MAPK3, TNFSF12, APOC3 and NAE1 as primary-prevention HF targets (Nat Commun 2023). — [Nat Commun](https://www.nature.com/articles/s41467-023-39253-3)
- AF: CRISPR epigenetic editing and iPSC atrial models are validating AF regulatory elements. Atrial CM + fibroblast cocultures model AF substrate. — [Stem Cell Reports](https://www.cell.com/stem-cell-reports/fulltext/S2213-6711(25)00071-2); [Sci Adv](https://www.science.org/doi/10.1126/sciadv.adg1222)
- AI phenotypes turn syndromes into quantitative traits: DL LV wall thickness GWAS (72 loci) gave HCM insight. — [PMC10689443](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10689443/)
- ASCVD "who/when": EAGLE shows that AI triage changes diagnosis rates in practice. SSaSS and SECURE show that low-cost population and strategy interventions reduce hard events. CHIP adds risk information but did not modify treatment benefit in TIMI trials. — [EAGLE](https://www.nature.com/articles/s41591-021-01335-4); [SSaSS](https://www.nejm.org/doi/full/10.1056/NEJMoa2105675); [SECURE](https://www.nejm.org/doi/full/10.1056/NEJMoa2208275); [TIMI CHIP](https://pubmed.ncbi.nlm.nih.gov/39107561/)

### Inferences
- Many HFpEF drivers are extra-cardiac (obesity, kidney, microvascular inflammation). Heart-only iPSC or atlas work is therefore insufficient, and multi-organ proteomics MR plus AI phenotyping (e.g., echo diastolic indices from EchoPrime-like models) is probably the higher-yield first step for a computational group.
- For AF, the most tractable pipeline combines GWAS loci, the atrial single-nucleus multiome (Kanemaru includes atrial regions and the conduction system), and iPSC atrial CM perturbation.

### Gaps
- There is no head-to-head evidence comparing strategy yield. This ranking is an informed synthesis, not an empirical result.

## Q3. Public datasets a bioinformatician or ML researcher can use immediately

### Takeaway
There is a strong open stack for ECG (PTB-XL, MIMIC-IV-ECG), heart single-cell data (Heart Cell Atlas / CELLxGENE, SCP1303), and CAD Perturb-seq (Schnitzler EC data). UKB imaging and proteomics need an approved application and a fee, but no wet lab.

### Cited Findings
- PTB-XL: 21,799 12-lead 10-second ECGs from 18,869 patients with cardiologist labels. Open on PhysioNet. — [PhysioNet](https://physionet.org/content/ptb-xl/1.0.3/)
- MIMIC-IV-ECG: about 800,000 diagnostic 12-lead ECGs from about 160,000 patients at 500 Hz, linkable to MIMIC-IV EHR. Credentialed access with training required. Also mirrored on AWS. — [PhysioNet](https://physionet.org/content/mimic-iv-ecg/1.0/); [AWS](https://registry.opendata.aws/mimic-iv-ecg/)
- DCM/HCM snRNA-seq (Chaffin 2022): Broad Single Cell Portal SCP1303. — [SCP1303](https://singlecell.broadinstitute.org/single_cell/study/SCP1303/single-nuclei-profiling-of-human-dilated-and-hypertrophic-cardiomyopathy)
- Heart Cell Atlas v1 and v2 (Litviňuková 2020; Kanemaru 2023) are distributed via heartcellatlas.org and CELLxGENE. — [Nature Kanemaru](https://www.nature.com/articles/s41586-023-06311-1). The exact portal listing was **[UNVERIFIED]**.
- UKB-PPP proteomics summary statistics are on the AWS Open Data registry. Individual-level UKB CMR, proteomics and genotypes are available through a UKB application. — [AWS UKB-PPP](https://registry.opendata.aws/ukbppp/)
- UKB CMR LV GWAS summary statistics are available through the Knowledge Portal Network (CVDKP). — [kp4cd](https://kp4cd.org/node/350)
- CAD endothelial Perturb-seq (2,285 genes, about 215k cells) was released with Schnitzler 2024 (GEO accession not verified here). — [PMC10170398](https://pmc.ncbi.nlm.nih.gov/articles/PMC10170398/)
- EchoPrime weights are announced as open source. — [Cedars-Sinai](https://www.cedars-sinai.org/newsroom/a-bigger-better-ai-tool-for-interpreting-common-heart-test/)
- Other resources: GTEx v8/v10 (heart LV, atrial appendage, coronary, aorta, tibial artery eQTL/sQTL), ENCODE/Roadmap cardiac chromatin, EchoNet-Dynamic (about 10k echo videos, Stanford AIMI), and CVDKP. These are standard resources but were **[UNVERIFIED in this session]**.

### Inferences
- A zero-wet-lab starter project would be to (i) take CAD/AF/HF GWAS summary statistics, (ii) score cell-type heritability with Kanemaru/Chaffin/plaque atlases (e.g., sc-linker, scDRS), (iii) intersect with the Schnitzler EC Perturb-seq programs and coronary caQTLs, and (iv) prioritize using UKB-PPP pQTL MR. A parallel ML track could train or evaluate ECG foundation models on PTB-XL and MIMIC-IV-ECG and transfer them to Chinese cohort ECGs.
- Cost barriers: UKB access costs a few thousand GBP per project (exact current fee **[UNVERIFIED]**). MIMIC needs CITI training. Everything else listed is free. The wet-lab strategies (iPSC Perturb-seq) cost roughly six to seven figures USD per genome-scale screen **[UNVERIFIED estimate]**.

### Gaps
- No public genome-scale Perturb-seq in primary human cardiomyocytes or iPSC-CMs was confirmed.
- Confirmed public repositories for coronary-artery snATAC caQTL data (the medRxiv 2024 study) were not checked.
