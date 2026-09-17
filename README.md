# Agriculture Yield & Farmer Advisory

A CRISP-DM project that turns agricultural data into a decision-support workflow for extension programmes and county agricultural planning teams. The project has three connected components: understanding what drives yield variation, predicting a season's yield band, and classifying farmer queries by crop so they can be routed to the right specialist.

## Business Problem

Extension staff and agricultural planners need evidence-based tools to:
- Understand how rainfall, temperature, pesticide use, crop, and region relate to yield variation
- Estimate a season's likely yield band (Low / Medium / High) from information available before or at the start of the season
- Organize incoming farmer questions by crop so they can be summarized or routed efficiently

This is a **decision-support** system, not an autonomous farm-management tool. Extension staff remain responsible for interpreting the evidence and deciding what action, if any, is appropriate.

## Project Structure



├── agriculture_yield_farmer_advisory_crispdm.ipynb   # Full CRISP-DM analysis and modeling notebook
├── Agriculture_Yield_Farmer_Advisory_CRISP_DM.docx  # Written capstone report
├── app.py                                            # FastAPI prediction service
├── data_utils.py                                     # Data loading and standardization helpers
├── yield_predictor.html                              # Front-end form for the prediction API
├── demo_yield.csv                                    # Demo structured yield dataset
└── demo_farmerchat_kenya.csv                         # Demo farmer-query dataset (Kenya subset)


## Data Sources

- **Structured data:** Dataset for Crop Yield Prediction — area, year, rainfall, pesticide use, average temperature, crop, and yield.
- **Text data:** Digital Green FarmerChat Agricultural Q&A Dataset, filtered to Kenya records, used for the farmer-query classification task.

The demo CSVs included here are small stand-ins so the notebook and app run out of the box. The notebook can also pull the full structured dataset from Zenodo via `data_utils.load_yield_data()`.

Note: the structured and text datasets are connected by agricultural domain and shared entities (crop, geography), not by a row-level farm ID.

## Methodology (CRISP-DM)

1. **Business Understanding** — defined the three business questions and success criteria above.
2. **Data Understanding** — profiled the structured yield data and the farmer-query text data.
3. **Data Preparation** — standardized columns, handled invalid/missing values, and derived the yield-band target using training data only to prevent leakage.
4. **Modeling**
   - *Phase 1 — Analysis & Insight:* Spearman correlation between yield and numeric predictors; Kruskal-Wallis test for yield differences across crops.
   - *Phase 2 — Predictive Modelling:* time-aware train/test split (earlier years train, later years test); DummyClassifier baseline, Logistic Regression, and Random Forest predicting the Low/Medium/High yield band.
   - *Phase 3 — Farmer Query Classification:* TF-IDF + classifier predicting crop category from the text of a farmer's query, to support routing rather than agronomic diagnosis.
5. **Evaluation** — macro-F1 and per-class performance (not accuracy alone) for Phases 2 and 3, with confusion matrices to identify where yield bands or crop classes are confused.
6. **Deployment** — a prototype decision-support workflow: a Phase 1 dashboard, a Phase 2 prediction form, and a Phase 3 query router. This repo includes a working slice of that deployment (see below).

## Running the Prediction App

The `app.py` / `yield_predictor.html` pair is a minimal working demo of the Phase 2 deployment concept.

1. Install dependencies:
   pip install fastapi uvicorn pydantic
  
2. Start the API:
   uvicorn app:app --reload
   
   The API runs at `http://127.0.0.1:8000` and exposes a `POST /predict` endpoint.
3. Open `yield_predictor.html` in a browser. It calls the local API and displays a plain-language yield estimate.

**Note:** `app.py` currently returns a placeholder rule-based prediction (based on rainfall thresholds) rather than the trained model from the notebook. Swap in the trained Phase 2 pipeline before treating this as a real prediction service.

## Running the Notebook

pip install pandas numpy scipy scikit-learn matplotlib
jupyter notebook agriculture_yield_farmer_advisory_crispdm.ipynb


The notebook reads `demo_yield.csv` and the FarmerChat Kenya demo data by default so it runs without external downloads.

## Limitations & Next Steps

- Results here are based on demo subsets; the notebook should be re-run on the full structured and text datasets to get real row counts, missingness, and metrics.
- Structured and text data are domain-linked, not row-linked by farm ID — confirm this satisfies any project approval requirements.
- Add stronger temporal validation (rolling train/test splits) if more years of data become available.
- Add probability calibration checks before using Phase 2 predictions operationally.
- For agronomic guidance, the Phase 3 router should connect to reviewed extension materials rather than generating advice itself.
- The API's CORS policy (`allow_origins=["*"]`) and placeholder prediction logic should be tightened before any real deployment.
