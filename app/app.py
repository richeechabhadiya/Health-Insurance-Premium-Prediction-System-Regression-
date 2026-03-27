# # import streamlit as st
# # import pandas as pd
# # import joblib, os, logging
# # from pathlib import Path

# # from src.utils.predict import Predictor
# # from src.utils.metrics import risk_level, compare_with_avg
# # # UI wrappers (use local app.* wrappers which call src modules)
# # try:
# #     # preferred when running as a package
# #     from .recommendation import get_recommendations
# #     from .simulation import simulate
# #     from .ui_components import render_header, two_column_layout, result_card
# #     from .explanation import explain_with_shap
# # except Exception:
# #     # fallback: load modules directly from files beside this script
# #     import importlib.util
# #     base = Path(__file__).resolve().parent

# #     def _load_module(name, path):
# #         spec = importlib.util.spec_from_file_location(name, str(path))
# #         mod = importlib.util.module_from_spec(spec)
# #         spec.loader.exec_module(mod)
# #         return mod

# #     rec_mod = _load_module('app.recommendation', base / 'recommendation.py')
# #     get_recommendations = rec_mod.get_recommendations

# #     sim_mod = _load_module('app.simulation', base / 'simulation.py')
# #     simulate = sim_mod.simulate

# #     ui_mod = _load_module('app.ui_components', base / 'ui_components.py')
# #     render_header = ui_mod.render_header
# #     two_column_layout = ui_mod.two_column_layout
# #     result_card = ui_mod.result_card

# #     expl_mod = _load_module('app.explanation', base / 'explanation.py')
# #     explain_with_shap = expl_mod.explain_with_shap

# # # configure simple logging to help debugging in streamlit logs
# # logging.basicConfig(level=logging.INFO)
# # log = logging.getLogger(__name__)

# # # Header
# # render_header()

# # # Resolve repo root and model paths using absolute paths so streamlit's
# # # working directory doesn't break relative imports.
# # repo_root = Path(__file__).resolve().parents[1]
# # model_path = repo_root / 'models' / 'best_model.pkl'
# # avg_path = repo_root / 'models' / 'avg_premium.pkl'

# # predictor = None
# # try:
# #     if model_path.exists():
# #         log.info(f'Loading model from {model_path}')
# #         predictor = Predictor(str(model_path))
# #         log.info('Predictor loaded successfully')
# #     else:
# #         log.warning(f'Model file not found at {model_path}')
# #         predictor = None
# # except Exception as e:
# #     log.exception('Failed to load Predictor:')
# #     predictor = None

# # # Load avg_premium fallback if available
# # avg_premium = None
# # try:
# #     if avg_path.exists():
# #         avg_premium = float(joblib.load(str(avg_path)))
# #         log.info(f'Loaded avg_premium: {avg_premium}')
# #     else:
# #         log.info('No avg_premium file found; continuing without fallback')
# # except Exception:
# #     log.exception('Failed to load avg_premium')
# #     avg_premium = None

# # st.markdown("---")

# # # -------------------------
# # # INPUT
# # # -------------------------
# # with st.form(key='input_form'):
# #     age = st.slider("Age", 18, 70, 32)
# #     bmi = st.slider("BMI", 15, 40, 21)
# #     smoker = st.selectbox("Smoker", ["yes", "no"], index=1)
# #     gender = st.selectbox("Gender", ["male", "female", "other"], index=0)
# #     type_policy = st.selectbox("Policy type", ["I", "II", "III"], index=0)
# #     exposure_time = st.number_input("Exposure time (years)", min_value=0.0, max_value=100.0, value=1.0, step=0.5)
# #     submitted = st.form_submit_button('Predict')

# # input_df = pd.DataFrame([{
# #     "age": int(age),
# #     "bmi": float(bmi),
# #     "smoker": smoker
# #     ,"gender": gender,
# #     "type_policy": type_policy,
# #     "exposure_time": float(exposure_time)
# # }])

# # # Show model debug info to help understand poor predictions
# # if predictor is None:
# #     st.caption('Model not loaded; predictions will use fallback if available.')
# # else:
# #     try:
# #         feat_count = len(predictor.feature_cols) if predictor.feature_cols is not None else 'unknown'
# #         preproc = 'yes' if getattr(predictor, 'preprocessor', None) is not None else 'no'
# #         st.caption(f"Model loaded — features: {feat_count}, preprocessor: {preproc}")
# #     except Exception:
# #         pass

# # if submitted:
# #     premium = None
# #     if predictor is None:
# #         st.warning('Model not available or failed to load.')
# #         if avg_premium is not None:
# #             st.info('Using average-premium fallback.')
# #             premium = avg_premium
# #         else:
# #             st.error('No model or fallback available.')
# #     else:
# #         try:
# #             premium = predictor.predict(input_df)[0]
# #         except Exception as e:
# #             st.error('Model prediction failed: ' + str(e))
# #             if avg_premium is not None:
# #                 st.info('Using average-premium fallback.')
# #                 premium = avg_premium
# #             else:
# #                 premium = None

# #     # Results column
# #     col1, col2 = two_column_layout()
# #     with col1:
# #         if premium is not None:
# #             result_card('Estimated Premium', f'₹{round(premium,2)}')
# #         else:
# #             st.info('Average premium not available' if avg_premium is None else f'Avg premium: ₹{round(avg_premium,2)}')

# #     # Risk and compare
# #     with col2:
# #         st.write('Risk Level:', risk_level(premium))
# #         st.write(compare_with_avg(premium))

# #     # Suggestions
# #     st.subheader("💡 Suggestions")
# #     suggestions = get_recommendations(input_df.iloc[0], premium, predictor)
# #     if suggestions:
# #         for s in suggestions:
# #             st.write('✔', s)
# #     else:
# #         st.write('No suggestions available.')

# #     # Simulation
# #     st.subheader("🔁 What-if Simulation")
# #     new_bmi = st.slider("Try different BMI", 15, 40, int(bmi))
# #     modified_df = input_df.copy()
# #     modified_df["bmi"] = new_bmi

# #     sim = simulate(predictor, input_df, modified_df)

# #     # Guard None values to avoid TypeError when rounding
# #     orig = sim.get('original') if sim else None
# #     new = sim.get('new') if sim else None
# #     savings = sim.get('savings') if sim else None

# #     if orig is None:
# #         st.info('Original premium not available')
# #     else:
# #         st.write(f"Old Premium: ₹{round(orig,2)}")

# #     if new is None:
# #         st.info('New premium not available')
# #     else:
# #         st.write(f"New Premium: ₹{round(new,2)}")

# #     if savings is None:
# #         st.info('Savings not available')
# #     else:
# #         st.write(f"Savings: ₹{round(savings,2)} 🎉")

# #     # SHAP explanation (if available)
# #     # SHAP explanation (if available)
# #     shap_out = None
# #     try:
# #         from app.explanation import explain_with_shap_plot
# #         shap_out = explain_with_shap_plot(predictor, input_df)
# #     except Exception:
# #         shap_out = None

# #     if shap_out is None:
# #         st.info('SHAP not available or could not explain this model (install shap)')
# #     else:
# #         contrib_list, fig = shap_out
# #         st.subheader('Explanation (top contributors)')
# #         for e in contrib_list:
# #             st.write(f"{e['feature']}: {round(e['shap'],3)}")
# #         st.pyplot(fig)





# """
# app/app.py  —  Insurance Premium Predictor  (FIXED v2)
# """

# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib
# import os
# import matplotlib.pyplot as plt
# from pathlib import Path

# # ─────────────────────────────────────────────
# # Paths
# # ─────────────────────────────────────────────
# REPO_ROOT   = Path(__file__).resolve().parents[1]
# MODEL_PATH  = REPO_ROOT / "models" / "best_model.pkl"
# FEAT_PATH   = REPO_ROOT / "models" / "feature_columns.pkl"
# TRAIN_PATH  = REPO_ROOT / "data"   / "split" / "X_train.csv"

# # ─────────────────────────────────────────────
# # Load model + feature columns
# # ─────────────────────────────────────────────
# @st.cache_resource
# def load_model():
#     if not MODEL_PATH.exists():
#         return None, None, None
#     raw = joblib.load(str(MODEL_PATH))
#     # handle dict-wrapped or raw model
#     model = raw["model"] if isinstance(raw, dict) and "model" in raw else raw
#     feat_cols = None
#     if FEAT_PATH.exists():
#         feat_cols = joblib.load(str(FEAT_PATH))
#     # load training medians to fill missing columns
#     train_medians = {}
#     if TRAIN_PATH.exists():
#         df_tr = pd.read_csv(TRAIN_PATH)
#         train_medians = df_tr.median(numeric_only=True).to_dict()
#         if feat_cols is None:
#             feat_cols = list(df_tr.columns)
#     return model, feat_cols, train_medians

# model, feat_cols, train_medians = load_model()

# # ─────────────────────────────────────────────
# # Compute dataset average premium for comparison
# # ─────────────────────────────────────────────
# @st.cache_data
# def get_avg_premium():
#     avg_path = REPO_ROOT / "models" / "avg_premium.pkl"
#     if avg_path.exists():
#         return float(joblib.load(str(avg_path)))
#     # fallback: compute from y_test
#     y_path = REPO_ROOT / "data" / "split" / "y_test.csv"
#     if y_path.exists():
#         return float(pd.read_csv(y_path).values.ravel().mean())
#     return None

# AVG_PREMIUM = get_avg_premium()

# # ─────────────────────────────────────────────
# # Helper: build input row aligned to model features
# # ─────────────────────────────────────────────
# def build_input_row(inputs: dict) -> pd.DataFrame:
#     """
#     Takes the raw UI inputs dict and builds a single-row DataFrame
#     aligned exactly to feat_cols (same columns the model was trained on).
#     Missing columns are filled with training medians.
#     """
#     if feat_cols is None:
#         return pd.DataFrame([inputs])

#     # Start with all training medians as defaults
#     row = {c: float(train_medians.get(c, 0)) for c in feat_cols}

#     age            = float(inputs.get("age", 35))
#     exposure_time  = float(inputs.get("exposure_time", 1.0))
#     seniority      = float(inputs.get("seniority_insured", 5))
#     gender         = str(inputs.get("gender", "M"))
#     policy_type    = str(inputs.get("type_policy", "I"))
#     reimbursement  = str(inputs.get("reimbursement", "No"))
#     new_biz        = str(inputs.get("new_business", "No"))

#     # ── numeric features the model knows about ──
#     row["age"]              = age
#     row["age_squared"]      = age ** 2
#     row["age_cubed"]        = age ** 3
#     row["exposure_time"]    = exposure_time
#     row["seniority_insured"]= seniority
#     row["age_x_seniority"]  = age * seniority
#     row["age_x_exposure"]   = age * exposure_time
#     row["exposure_seniority"]= exposure_time * seniority

#     # ── one-hot columns — set the right dummy to 1 ──
#     # gender
#     for col in feat_cols:
#         if col.startswith("gender_"):
#             val = col.split("gender_", 1)[1]
#             row[col] = 1.0 if gender == val else 0.0

#     # type_policy
#     for col in feat_cols:
#         if col.startswith("type_policy_") and not col.startswith("type_policy_dg"):
#             val = col.split("type_policy_", 1)[1]
#             row[col] = 1.0 if policy_type == val else 0.0

#     # reimbursement_Yes
#     if "reimbursement_Yes" in row:
#         row["reimbursement_Yes"] = 1.0 if reimbursement == "Yes" else 0.0

#     # new_business_Yes
#     if "new_business_Yes" in row:
#         row["new_business_Yes"] = 1.0 if new_biz == "Yes" else 0.0

#     df = pd.DataFrame([row], columns=feat_cols)
#     df = df.fillna(0).astype("float32")
#     return df

# # ─────────────────────────────────────────────
# # Helper: predict
# # ─────────────────────────────────────────────
# def predict_premium(inputs: dict) -> float | None:
#     if model is None:
#         return None
#     try:
#         X = build_input_row(inputs)
#         pred_log = model.predict(X)
#         return float(np.expm1(pred_log)[0])
#     except Exception as e:
#         st.error(f"Prediction error: {e}")
#         return None

# # ─────────────────────────────────────────────
# # Helper: risk level  ← FIXED THRESHOLDS
# # ─────────────────────────────────────────────
# def risk_level(premium):
#     """
#     Thresholds based on ACTUAL data range (~800–4000 typical).
#     Adjust if your data has different scale.
#     """
#     if premium is None:
#         return "UNKNOWN ❓"
#     p = float(premium)
#     if p > 3000:
#         return "HIGH 🔴"
#     elif p > 1800:
#         return "MEDIUM 🟡"
#     else:
#         return "LOW 🟢"

# # ─────────────────────────────────────────────
# # Helper: compare with average
# # ─────────────────────────────────────────────
# def compare_with_avg(premium):
#     if premium is None or AVG_PREMIUM is None:
#         return "Average premium data not available"
#     diff_pct = ((float(premium) - AVG_PREMIUM) / AVG_PREMIUM) * 100
#     if diff_pct >= 0:
#         return f"📈 Your premium is **{diff_pct:.1f}% higher** than average (avg: ₹{AVG_PREMIUM:.0f})"
#     else:
#         return f"📉 Your premium is **{abs(diff_pct):.1f}% lower** than average (avg: ₹{AVG_PREMIUM:.0f})"

# # ─────────────────────────────────────────────
# # Helper: recommendations
# # ─────────────────────────────────────────────
# def get_recommendations(inputs: dict, current_premium: float) -> list[str]:
#     suggestions = []
#     if model is None or current_premium is None:
#         return ["Load model to get personalised suggestions."]

#     age           = float(inputs.get("age", 35))
#     exposure_time = float(inputs.get("exposure_time", 1.0))
#     seniority     = float(inputs.get("seniority_insured", 5))

#     # Suggestion 1: increase exposure time
#     if exposure_time < 1.0:
#         new_inputs = {**inputs, "exposure_time": 1.0}
#         new_p = predict_premium(new_inputs)
#         if new_p and new_p < current_premium:
#             saving = current_premium - new_p
#             suggestions.append(f"📅 Increase exposure time to full year → save ~₹{saving:.0f}")

#     # Suggestion 2: older policy seniority (loyalty discount)
#     if seniority < 10:
#         new_inputs = {**inputs, "seniority_insured": seniority + 5}
#         new_p = predict_premium(new_inputs)
#         if new_p and new_p < current_premium:
#             saving = current_premium - new_p
#             suggestions.append(f"📆 Longer policy tenure (5 more years) → save ~₹{saving:.0f}")

#     # Suggestion 3: switch policy type
#     current_type = inputs.get("type_policy", "I")
#     for alt_type in ["I", "II", "III"]:
#         if alt_type != current_type:
#             new_inputs = {**inputs, "type_policy": alt_type}
#             new_p = predict_premium(new_inputs)
#             if new_p and new_p < current_premium:
#                 saving = current_premium - new_p
#                 suggestions.append(f"📋 Switch to Policy Type {alt_type} → save ~₹{saving:.0f}")
#                 break

#     # Suggestion 4: high risk warning
#     risk = risk_level(current_premium)
#     if "HIGH" in risk:
#         suggestions.append("⚠️ Your risk profile is HIGH — consider reviewing coverage options with an advisor")

#     if not suggestions:
#         suggestions.append("✅ Your premium looks competitive. No major savings found for your profile.")

#     return suggestions

# # ─────────────────────────────────────────────
# # Helper: SHAP explanation
# # ─────────────────────────────────────────────
# def explain_prediction(inputs: dict):
#     if model is None:
#         return None
#     try:
#         import shap
#         X = build_input_row(inputs)
#         try:
#             explainer = shap.TreeExplainer(model)
#             shap_vals = explainer.shap_values(X)
#             vals = shap_vals[0] if isinstance(shap_vals, list) else shap_vals[0]
#         except Exception:
#             explainer = shap.Explainer(model)
#             sv = explainer(X)
#             vals = sv.values[0]

#         names = feat_cols if feat_cols else [f"f{i}" for i in range(len(vals))]
#         contrib = sorted(zip(names, vals), key=lambda x: -abs(x[1]))[:10]

#         feats      = [c[0] for c in contrib][::-1]
#         shap_vals2 = [c[1] for c in contrib][::-1]
#         colors     = ["#1f77b4" if v >= 0 else "#ff7f0e" for v in shap_vals2]

#         fig, ax = plt.subplots(figsize=(7, max(3, len(feats) * 0.5)))
#         ax.barh(feats, shap_vals2, color=colors)
#         ax.axvline(0, color="black", linewidth=0.8)
#         ax.set_xlabel("SHAP value (impact on premium)")
#         ax.set_title("Why this premium? — Top 10 factors")
#         plt.tight_layout()
#         return fig, contrib[::-1]   # highest impact first
#     except ImportError:
#         return None
#     except Exception as e:
#         st.warning(f"SHAP explanation failed: {e}")
#         return None

# # ═════════════════════════════════════════════
# # UI
# # ═════════════════════════════════════════════
# st.set_page_config(page_title="Insurance Premium Predictor", page_icon="🛡️", layout="wide")

# st.title("🛡️ Insurance Premium Predictor")
# st.caption("Fill in your details below and click **Predict** to get your estimated premium.")

# if model is None:
#     st.error("⚠️ Model not found. Run `05_model_training.ipynb` first, then make sure `models/best_model.pkl` exists.")
#     st.stop()

# st.markdown("---")

# # ─────────────────────────────────────────────
# # INPUT FORM
# # ─────────────────────────────────────────────
# with st.form("input_form"):
#     st.subheader("📋 Your Details")
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         age            = st.slider("Age", 18, 85, 45)
#         gender         = st.selectbox("Gender", ["M", "F"])
#         exposure_time  = st.slider("Exposure Time (years)", 0.1, 1.0, 1.0, step=0.1)

#     with col2:
#         seniority      = st.slider("Years as Insured (Seniority)", 0, 30, 10)
#         type_policy    = st.selectbox("Policy Type", ["I", "II", "III"])
#         reimbursement  = st.selectbox("Reimbursement", ["Yes", "No"])

#     with col3:
#         new_business   = st.selectbox("New Business", ["Yes", "No"])
#         n_insured_mun  = st.number_input("Insured in Municipality", 1, 10000, 500)
#         n_insured_prov = st.number_input("Insured in Province",     1, 10000, 3000)

#     submitted = st.form_submit_button("🔍 Predict Premium", use_container_width=True)

# # Collect inputs
# inputs = {
#     "age":              age,
#     "gender":           gender,
#     "exposure_time":    exposure_time,
#     "seniority_insured":seniority,
#     "seniority_policy": seniority,
#     "type_policy":      type_policy,
#     "reimbursement":    reimbursement,
#     "new_business":     new_business,
#     "n_insured_mun":    float(n_insured_mun),
#     "n_insured_prov":   float(n_insured_prov),
#     "n_insured_pc":     float(n_insured_mun),
# }

# # ─────────────────────────────────────────────
# # RESULTS
# # ─────────────────────────────────────────────
# if submitted:
#     with st.spinner("Calculating..."):
#         premium = predict_premium(inputs)

#     if premium is None:
#         st.error("Prediction failed. Check model and feature columns.")
#         st.stop()

#     st.markdown("---")
#     st.subheader("📊 Results")

#     # ── Metric cards ──
#     r1, r2, r3 = st.columns(3)
#     r1.metric("💰 Estimated Premium", f"₹{premium:,.2f}")
#     r2.metric("⚡ Risk Level", risk_level(premium))
#     r3.metric("📈 vs. Average", f"₹{AVG_PREMIUM:,.0f}" if AVG_PREMIUM else "N/A",
#               delta=f"{((premium - AVG_PREMIUM)/AVG_PREMIUM*100):.1f}%" if AVG_PREMIUM else None)

#     st.info(compare_with_avg(premium))

#     # ── Suggestions ──
#     st.markdown("---")
#     st.subheader("💡 How to Reduce Your Premium")
#     suggestions = get_recommendations(inputs, premium)
#     for s in suggestions:
#         st.write(s)

#     # ── What-if Simulation ──
#     st.markdown("---")
#     st.subheader("🔁 What-if Simulation")
#     st.caption("Adjust a parameter below to see how your premium changes.")

#     sim_col1, sim_col2 = st.columns(2)
#     with sim_col1:
#         sim_age        = st.slider("Simulate Age",      18, 85, age,       key="sim_age")
#         sim_seniority  = st.slider("Simulate Seniority", 0, 30, seniority, key="sim_sen")
#     with sim_col2:
#         sim_exposure   = st.slider("Simulate Exposure", 0.1, 1.0, exposure_time, 0.1, key="sim_exp")
#         sim_policy     = st.selectbox("Simulate Policy Type", ["I", "II", "III"],
#                                        index=["I","II","III"].index(type_policy), key="sim_pol")

#     sim_inputs  = {**inputs, "age": sim_age, "seniority_insured": sim_seniority,
#                    "exposure_time": sim_exposure, "type_policy": sim_policy}
#     sim_premium = predict_premium(sim_inputs)

#     if sim_premium is not None:
#         saving = premium - sim_premium
#         sc1, sc2, sc3 = st.columns(3)
#         sc1.metric("Original Premium", f"₹{premium:,.2f}")
#         sc2.metric("Simulated Premium", f"₹{sim_premium:,.2f}")
#         sc3.metric("Savings" if saving > 0 else "Extra Cost",
#                    f"₹{abs(saving):,.2f}",
#                    delta=f"{'−' if saving > 0 else '+'}{abs(saving):,.2f}",
#                    delta_color="normal" if saving > 0 else "inverse")

#         # bar chart comparison
#         fig_sim, ax_sim = plt.subplots(figsize=(4, 2.5))
#         ax_sim.bar(["Original", "Simulated"],
#                    [premium, sim_premium],
#                    color=["#4472C4", "#ED7D31"])
#         ax_sim.set_ylabel("Premium (₹)")
#         ax_sim.set_title("Premium Comparison")
#         for i, v in enumerate([premium, sim_premium]):
#             ax_sim.text(i, v + 10, f"₹{v:,.0f}", ha="center", fontsize=9)
#         plt.tight_layout()
#         st.pyplot(fig_sim)

#     # ── SHAP explanation ──
#     st.markdown("---")
#     st.subheader("🧠 Why This Premium? (Explanation)")
#     with st.spinner("Calculating SHAP values..."):
#         shap_out = explain_prediction(inputs)

#     if shap_out is None:
#         st.info("SHAP explanation not available. Run `pip install shap` in your environment.")
#     else:
#         fig_shap, contrib = shap_out
#         st.pyplot(fig_shap)
#         st.caption("Blue bars = factors that INCREASE your premium. Orange = factors that DECREASE it.")

#         with st.expander("See full contribution table"):
#             contrib_df = pd.DataFrame(contrib, columns=["Feature", "SHAP Value"])
#             contrib_df["Impact"] = contrib_df["SHAP Value"].apply(
#                 lambda v: f"⬆ +{v:.4f}" if v > 0 else f"⬇ {v:.4f}"
#             )
#             st.dataframe(contrib_df[["Feature", "Impact"]], use_container_width=True)

#     # ── Download report ──
#     st.markdown("---")
#     st.subheader("📄 Download Report")
#     report_lines = [
#         "INSURANCE PREMIUM PREDICTION REPORT",
#         "=" * 40,
#         f"Age:              {age}",
#         f"Gender:           {gender}",
#         f"Exposure Time:    {exposure_time} yrs",
#         f"Seniority:        {seniority} yrs",
#         f"Policy Type:      {type_policy}",
#         f"Reimbursement:    {reimbursement}",
#         "",
#         f"Estimated Premium:  ₹{premium:,.2f}",
#         f"Risk Level:         {risk_level(premium)}",
#         f"vs. Average:        {compare_with_avg(premium)}",
#         "",
#         "Suggestions:",
#         *[f"  - {s}" for s in suggestions],
#     ]
#     report_text = "\n".join(report_lines)
#     st.download_button(
#         label=" Download Report (.txt)",
#         data=report_text,
#         file_name="premium_report.txt",
#         mime="text/plain"
#     )


# ============================================================
# app/app.py  —  InsureIQ  (FULL FEATURED VERSION)
# ============================================================
# HOW TO RUN (from project root):
#   streamlit run app/app.py
# ============================================================


# ============================================================
# app/app.py  —  InsureIQ  (FIXED — categorical error resolved)
# ============================================================
# HOW TO RUN (from project root):
#   cd /home/richee/Downloads/Assesment
#   streamlit run app/app.py
# ============================================================

# ============================================================
# app/app.py  —  InsureIQ  (FINAL FIXED VERSION)
# ============================================================


#####@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
# from pathlib import Path
# from datetime import datetime
# import sys, os

# st.set_page_config(
#     page_title="InsureIQ — Premium Predictor",
#     page_icon="🛡️",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# REPO_ROOT = Path(__file__).resolve().parents[1]
# if str(REPO_ROOT) not in sys.path:
#     sys.path.insert(0, str(REPO_ROOT))

# from src.utils.predict import Predictor

# # ================= LOAD =================
# MODEL_PATH = REPO_ROOT / "models" / "best_model.pkl"

# @st.cache_resource
# def load_predictor():
#     try:
#         return Predictor(str(MODEL_PATH))
#     except:
#         return None

# predictor = load_predictor()

# # ================= INPUT BUILDER =================
# def build_input_df(inputs):
#     age = float(inputs["age"])
#     sen = float(inputs["seniority_insured"])
#     exp = float(inputs["exposure_time"])
#     ni_m = float(inputs["n_insured_mun"])
#     ni_p = float(inputs["n_insured_prov"])

#     row = {
#         "age": age,
#         "age_squared": age**2,
#         "age_cubed": age**3,
#         "exposure_time": exp,
#         "seniority_insured": sen,
#         "seniority_policy": sen,
#         "age_x_seniority": age*sen,
#         "age_x_exposure": age*exp,
#         "exposure_seniority": exp*sen,
#         "n_insured_mun": ni_m,
#         "n_insured_prov": ni_p,
#         "prov_mun_ratio": ni_p/(ni_m+1),

#         "gender": str(inputs["gender"]),
#         "type_policy": str(inputs["type_policy"]),
#         "reimbursement": str(inputs["reimbursement"]),
#         "new_business": str(inputs["new_business"]),
#         "distribution_channel": "A",
#         "type_product": "S",
#     }

#     return pd.DataFrame([row])

# # ================= PREDICT =================
# def predict_premium(inputs):
#     try:
#         df = build_input_df(inputs)
#         pred = predictor.predict(df)
#         return float(pred[0])
#     except Exception as e:
#         st.error(f"Prediction error: {e}")
#         return None

# # ================= UI =================
# st.title("🛡️ InsureIQ — Premium Predictor")

# if predictor is None:
#     st.error("Model not found. Train model first.")
#     st.stop()

# with st.form("form"):
#     c1, c2, c3 = st.columns(3)

#     with c1:
#         age = st.slider("Age", 18, 85, 40)
#         gender = st.selectbox("Gender", ["M","F"])
#         exposure_time = st.slider("Exposure", 0.1, 1.0, 1.0)

#     with c2:
#         seniority = st.slider("Seniority", 0, 30, 5)
#         type_policy = st.selectbox("Policy", ["I","II","III"])
#         reimbursement = st.selectbox("Reimbursement", ["Yes","No"])

#     with c3:
#         new_business = st.selectbox("New Business", ["Yes","No"])
#         n_insured_mun = st.number_input("Municipality", 100, 10000, 500)
#         n_insured_prov = st.number_input("Province", 100, 10000, 3000)

#     btn = st.form_submit_button("Predict")

# inputs = {
#     "age": age,
#     "gender": gender,
#     "exposure_time": exposure_time,
#     "seniority_insured": seniority,
#     "type_policy": type_policy,
#     "reimbursement": reimbursement,
#     "new_business": new_business,
#     "n_insured_mun": n_insured_mun,
#     "n_insured_prov": n_insured_prov,
# }

# if btn:
#     val = predict_premium(inputs)
#     if val:
#         st.success(f"💰 Premium: ₹{val:,.2f}")




#newwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww#
#33333333333333333333333333333333333333

# ============================================================
# FINAL app/app.py — FULLY WORKING (NO IMPORT ERRORS)
# ============================================================
# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from pathlib import Path
# import sys, os

# # ---------------- PATH FIX ----------------
# APP_DIR = os.path.dirname(os.path.abspath(__file__))
# ROOT_DIR = os.path.dirname(APP_DIR)

# if ROOT_DIR not in sys.path:
#     sys.path.append(ROOT_DIR)

# # ---------------- IMPORT MODEL ----------------
# from src.utils.predict import Predictor

# # ---------------- STREAMLIT CONFIG ----------------
# st.set_page_config(
#     page_title="InsureIQ — Premium Predictor",
#     page_icon="🛡️",
#     layout="wide"
# )

# # ---------------- LOAD MODEL ----------------
# MODEL_PATH = Path("models/best_model.pkl")

# @st.cache_resource
# def load_model():
#     if MODEL_PATH.exists():
#         return Predictor(str(MODEL_PATH))
#     return None

# predictor = load_model()

# # ---------------- BUILD INPUT ----------------
# def build_df(inputs):
#     # initialize all features with 0
#     row = {col: 0 for col in predictor.feature_cols}

#     age = inputs["age"]
#     sen = inputs["seniority"]
#     exp = inputs["exposure"]

#     # numeric features
#     row.update({
#         "age": age,
#         "age_squared": age**2,
#         "age_cubed": age**3,
#         "exposure_time": exp,
#         "seniority_insured": sen,
#         "seniority_policy": sen,
#         "age_x_seniority": age * sen,
#         "age_x_exposure": age * exp,
#         "exposure_seniority": exp * sen,
#         "n_insured_mun": inputs["mun"],
#         "n_insured_prov": inputs["prov"]
#     })

#     # categorical features (IMPORTANT)
#     row["gender"] = inputs["gender"]
#     row["type_policy"] = inputs["policy"]
#     row["reimbursement"] = inputs["reimb"]
#     row["new_business"] = inputs["new"]

#     return pd.DataFrame([row])

# # ---------------- PREDICT ----------------
# import requests

# def predict(inputs):
#     # Change from local predictor to API call
#     url = "http://127.0.0.1:8000/predict"
    
#     # Map the UI keys to match the model keys exactly
#     payload = {
#         "age": inputs["age"],
#         "gender": inputs["gender"],
#         "exposure_time": inputs["exposure"], 
#         "seniority_insured": inputs["seniority"],
#         "type_policy": inputs["policy"],
#         "reimbursement": "S" if inputs["reimb"] == "Yes" else "N",
#         "new_business": "S" if inputs["new"] == "Yes" else "N"
#     }
    
#     response = requests.post(url, json=payload)
#     if response.status_code == 200:
#         return response.json()["premium"]
#     else:
#         st.error("API Error")
#         return 0.0
# # ---------------- SHAP ----------------
# def get_shap(inputs):
#     try:
#         import shap
#         df = build_df(inputs)
#         X = predictor.preprocess(df)

#         explainer = shap.Explainer(predictor.model)
#         sv = explainer(X)

#         vals = sv.values[0]
#         names = predictor.feature_cols

#         return sorted(zip(names, vals), key=lambda x: -abs(x[1]))[:10]
#     except:
#         return None

# # ---------------- SUGGESTIONS ----------------
# def get_suggestions(inputs, premium):
#     sug = []

#     if inputs["seniority"] < 10:
#         sug.append("📅 Increase seniority → reduce premium")

#     if inputs["exposure"] < 1:
#         sug.append("📆 Full year coverage reduces cost")

#     if inputs["policy"] == "III":
#         sug.append("📋 Try Policy I or II")

#     if premium > 3000:
#         sug.append("⚠️ High risk — improve health profile")

#     if not sug:
#         sug.append("✅ Your premium looks optimal")

#     return sug

# # ---------------- UI ----------------
# st.title("🛡️ InsureIQ — Premium Predictor")

# if predictor is None:
#     st.error("❌ Model not found. Train model first.")
#     st.stop()

# col1, col2, col3 = st.columns(3)

# with col1:
#     age = st.slider("Age", 18, 80, 40)
#     gender = st.selectbox("Gender", ["M", "F"])
#     exposure = st.slider("Exposure", 0.1, 1.0, 1.0)

# with col2:
#     seniority = st.slider("Seniority", 0, 30, 5)
#     policy = st.selectbox("Policy", ["I", "II", "III"])
#     reimb = st.selectbox("Reimbursement", ["Yes", "No"])

# with col3:
#     new = st.selectbox("New Business", ["Yes", "No"])
#     mun = st.number_input("Municipality", 100, 10000, 500)
#     prov = st.number_input("Province", 100, 10000, 3000)

# if st.button("Predict"):

#     inputs = {
#         "age": age,
#         "gender": gender,
#         "exposure": exposure,
#         "seniority": seniority,
#         "policy": policy,
#         "reimb": reimb,
#         "new": new,
#         "mun": mun,
#         "prov": prov
#     }

#     premium = predict(inputs)

#     st.success(f"💰 Premium: ₹{premium:.2f}")

#     # -------- SHAP --------
#     st.subheader("🧠 Why this premium?")
#     shap_vals = get_shap(inputs)

#     if shap_vals:
#         df = pd.DataFrame(shap_vals, columns=["Feature", "Impact"])

#         fig, ax = plt.subplots()
#         ax.barh(df["Feature"], df["Impact"])
#         ax.axvline(0)
#         st.pyplot(fig)

#     # -------- SUGGESTIONS --------
#     st.subheader("💡 Suggestions")
#     for s in get_suggestions(inputs, premium):
#         st.write(s)

#     # -------- SIMULATION --------
#     st.subheader("🔁 Simulation")

#     new_inputs = inputs.copy()
#     new_inputs["seniority"] += 5

#     new_premium = predict(new_inputs)

#     st.write(f"New Premium: ₹{new_premium:.2f}")
#     st.write(f"Savings: ₹{premium - new_premium:.2f}")

#     # -------- REPORT --------
#     st.subheader("📄 Report")

#     report = f"""
#     Premium: ₹{premium:.2f}
#     Suggestions: {get_suggestions(inputs, premium)}
#     """

#     st.download_button("Download Report", report)

# ============================================================
# FINAL PRODUCTION app/app.py
# ============================================================
# app/app.py
# app.py
# app.py
# app/app.py  — InsureIQ Premium Predictor (FIXED: SHAP + compact graphs)
# app/app.py  — InsureIQ Premium Predictor  (Premium UI Redesign)
import os
from huggingface_hub import login

# This bypasses the need for Databricks Secret Scopes
os.environ["HF_TOKEN"] = "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"
login(token=os.environ["HF_TOKEN"])




import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import sys
import joblib
import requests

# ================= PATH FIX =================
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "src" / "utils"))
sys.path.append(str(ROOT / "src" / "explainability"))

from predict import Predictor
from shap_utils import get_explainer, explain_instance

# ================= PAGE CONFIG =================
st.set_page_config(
    layout="wide",
    page_title="InsureIQ — Premium Predictor",
    page_icon="🛡️",
    initial_sidebar_state="collapsed",
)

# ================= GLOBAL CSS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* ── Root palette ── */
:root {
  --bg:        #0a0e1a;
  --surface:   #111827;
  --surface2:  #1a2236;
  --border:    rgba(99,179,237,0.12);
  --gold:      #f5c842;
  --gold-soft: rgba(245,200,66,0.10);
  --teal:      #38bdf8;
  --teal-soft: rgba(56,189,248,0.08);
  --red:       #f87171;
  --green:     #34d399;
  --text:      #e2e8f0;
  --muted:     #64748b;
  --radius:    12px;
}

/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  font-family: 'Sora', sans-serif;
  color: var(--text);
}
[data-testid="stHeader"], [data-testid="stToolbar"] { display:none !important; }
[data-testid="stSidebar"] { display:none !important; }
.block-container { padding: 0 2rem 4rem 2rem !important; max-width: 1400px !important; }

/* ── Hero banner ── */
.iq-hero {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #0f2744 100%);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 2.5rem 3rem;
  margin: 1.5rem 0 2rem 0;
  position: relative;
  overflow: hidden;
}
.iq-hero::before {
  content:'';
  position:absolute; top:-60px; right:-60px;
  width:280px; height:280px;
  background: radial-gradient(circle, rgba(245,200,66,0.12) 0%, transparent 70%);
  pointer-events:none;
}
.iq-hero::after {
  content:'';
  position:absolute; bottom:-40px; left:30%;
  width:200px; height:200px;
  background: radial-gradient(circle, rgba(56,189,248,0.08) 0%, transparent 70%);
  pointer-events:none;
}
.iq-logo { font-size:2.4rem; font-weight:700; letter-spacing:-1px; margin:0; }
.iq-logo span { color: var(--gold); }
.iq-tagline { color: var(--muted); font-size:.95rem; margin:.35rem 0 0 0; letter-spacing:.5px; }
.iq-badge {
  display:inline-flex; align-items:center; gap:.4rem;
  background: var(--gold-soft); border:1px solid rgba(245,200,66,0.25);
  border-radius:20px; padding:.25rem .85rem;
  font-size:.75rem; color:var(--gold); font-weight:600; letter-spacing:.5px;
  margin-top:1rem;
}

/* ── Section headers ── */
.iq-section {
  display:flex; align-items:center; gap:.6rem;
  font-size:1rem; font-weight:600; letter-spacing:.5px;
  color: var(--teal); text-transform:uppercase;
  margin: 2rem 0 .75rem 0;
  padding-bottom:.5rem;
  border-bottom:1px solid var(--border);
}
.iq-section-icon { font-size:1.1rem; }

/* ── Input card ── */
.iq-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem;
  margin-bottom:1rem;
}
.iq-label {
  font-size:.7rem; font-weight:600; letter-spacing:1px;
  text-transform:uppercase; color:var(--muted);
  margin-bottom:.3rem;
}

/* ── Streamlit element overrides ── */
div[data-testid="stSlider"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
  font-size:.72rem !important; font-weight:600 !important;
  letter-spacing:.8px !important; text-transform:uppercase !important;
  color: var(--muted) !important;
}
div[data-testid="stSlider"] > div > div > div {
  background: var(--teal) !important;
}
div[data-testid="stSelectbox"] > div > div {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text) !important;
}
div[data-testid="stNumberInput"] > div > div > input {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text) !important;
}
/* Button */
div[data-testid="stButton"] > button {
  background: linear-gradient(135deg, #b7891a 0%, var(--gold) 100%) !important;
  color: #0a0e1a !important;
  font-family: 'Sora', sans-serif !important;
  font-weight: 700 !important;
  font-size: .9rem !important;
  letter-spacing: .5px !important;
  border: none !important;
  border-radius: 10px !important;
  padding: .75rem 2.5rem !important;
  width: 100% !important;
  transition: opacity .2s !important;
  box-shadow: 0 4px 20px rgba(245,200,66,0.25) !important;
}
div[data-testid="stButton"] > button:hover { opacity:.88 !important; }

/* ── Result card ── */
.iq-result {
  background: linear-gradient(135deg, #0f2744 0%, #1a3a5c 100%);
  border: 1px solid rgba(56,189,248,0.3);
  border-radius: var(--radius);
  padding: 1.8rem 2rem;
  margin: 1.5rem 0;
  display: flex; align-items:center; justify-content:space-between;
}
.iq-result-label { font-size:.72rem; font-weight:600; letter-spacing:1.2px; text-transform:uppercase; color:var(--teal); }
.iq-result-value { font-family:'Space Mono', monospace; font-size:2.8rem; font-weight:700; color:#fff; letter-spacing:-1px; margin:.3rem 0; }
.iq-result-sub { font-size:.8rem; color:var(--muted); }
.iq-result-icon { font-size:3.5rem; opacity:.7; }

/* ── KPI pills ── */
.iq-kpi-row { display:flex; gap:1rem; margin:1rem 0; flex-wrap:wrap; }
.iq-kpi {
  background: var(--surface2);
  border:1px solid var(--border);
  border-radius:10px;
  padding:.8rem 1.2rem;
  flex:1; min-width:140px;
}
.iq-kpi-label { font-size:.65rem; font-weight:600; letter-spacing:1px; text-transform:uppercase; color:var(--muted); }
.iq-kpi-value { font-family:'Space Mono',monospace; font-size:1.3rem; font-weight:700; color:var(--text); margin-top:.2rem; }
.iq-kpi-delta { font-size:.7rem; margin-top:.15rem; }
.delta-up { color:var(--red); }
.delta-down { color:var(--green); }
.delta-neutral { color:var(--muted); }

/* ── SHAP table ── */
div[data-testid="stDataFrame"] {
  border-radius: 10px !important;
  overflow: hidden !important;
  border: 1px solid var(--border) !important;
}

/* ── Suggestions ── */
.iq-suggestion {
  background: var(--surface2);
  border-left: 3px solid var(--gold);
  border-radius: 0 8px 8px 0;
  padding: .65rem 1rem;
  margin: .4rem 0;
  font-size:.87rem;
  color: var(--text);
}
.iq-suggestion.warn { border-left-color: var(--red); }
.iq-suggestion.ok   { border-left-color: var(--green); }

/* ── Simulation card ── */
.iq-sim-card {
  background: var(--surface);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:1.5rem;
  display:flex; gap:2rem; align-items:center; flex-wrap:wrap;
}
.iq-sim-item { flex:1; min-width:160px; }
.iq-sim-lbl { font-size:.65rem; font-weight:600; letter-spacing:1px; text-transform:uppercase; color:var(--muted); }
.iq-sim-val { font-family:'Space Mono',monospace; font-size:1.5rem; font-weight:700; color:var(--text); margin-top:.2rem; }
.iq-sim-savings { color:var(--green); }

/* ── Report textarea ── */
div[data-testid="stTextArea"] textarea {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  font-family: 'Space Mono', monospace !important;
  font-size:.75rem !important;
  color: var(--text) !important;
}

/* ── Download button ── */
div[data-testid="stDownloadButton"] > button {
  background: var(--surface2) !important;
  color: var(--teal) !important;
  border: 1px solid rgba(56,189,248,0.3) !important;
  border-radius: 8px !important;
  font-family: 'Sora', sans-serif !important;
  font-weight: 600 !important;
}

/* ── Success/Error ── */
div[data-testid="stAlert"] {
  border-radius: 10px !important;
}

/* ── Divider ── */
.iq-divider {
  height:1px; background:var(--border);
  margin:2rem 0;
}

/* ── Model badge row ── */
.iq-model-info {
  display:flex; gap:.75rem; flex-wrap:wrap; margin-top:1rem;
}
.iq-model-pill {
  background:var(--surface2); border:1px solid var(--border);
  border-radius:20px; padding:.25rem .9rem;
  font-size:.72rem; color:var(--muted);
}
.iq-model-pill b { color:var(--text); }

/* ── scrollbar ── */
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--surface2); border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ================= MODEL PATHS =================
MODEL_DIR  = ROOT / "models"
MODEL_PATH = MODEL_DIR / "best_model.pkl"

# ---------------- DOWNLOAD FUNCTION ----------------
def download_file_from_gdrive(file_id, destination):
    if not destination.exists():
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        url = f"https://drive.google.com/uc?id={file_id}"
        with st.spinner(f"📦 Downloading {destination.name} …"):
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                with open(destination, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                st.success(f"✅ {destination.name} downloaded!")
            except Exception as e:
                st.error(f"❌ Failed to download {destination.name}: {e}")
                st.stop()

MODEL_FILE_ID = "16wrwJWrg-XuZFsBWc6N0zIdJVVAbRPWE"
download_file_from_gdrive(MODEL_FILE_ID, MODEL_PATH)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_predictor():
    return Predictor(MODEL_PATH)

predictor = load_predictor()

# ================= HERO HEADER =================
st.markdown("""
<div class="iq-hero">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
    <div>
      <p class="iq-logo">🛡️ Insure<span>IQ</span></p>
      <p class="iq-tagline">Intelligent Health Insurance Premium Predictor · Powered by LightGBM</p>
      <div class="iq-badge">⚡ AI-Powered · Real-time Analysis</div>
    </div>
    <div style="text-align:right;">
      <div class="iq-model-info">
        <div class="iq-model-pill">Model <b>LightGBM</b></div>
        <div class="iq-model-pill">MAE <b>₹164</b></div>
        <div class="iq-model-pill">RMSE <b>₹377</b></div>
        <div class="iq-model-pill">R² <b>0.567</b></div>
        <div class="iq-model-pill">MAPE <b>18.15%</b></div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ================= INPUT SECTION =================
st.markdown('<div class="iq-section"><span class="iq-section-icon">📋</span>CUSTOMER PROFILE</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="iq-card">', unsafe_allow_html=True)
    age      = st.slider("Age", 18, 85, 40)
    gender   = st.selectbox("Gender", ["M", "F"])
    exposure = st.slider("Exposure Time (Years)", 0.1, 1.0, 1.0, step=0.05)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="iq-card">', unsafe_allow_html=True)
    seniority = st.slider("Seniority (Years)", 0, 30, 5)
    policy    = st.selectbox("Policy Type", ["I", "II", "III"])
    reimb     = st.selectbox("Reimbursement", ["Yes", "No"])
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="iq-card">', unsafe_allow_html=True)
    new    = st.selectbox("New Business", ["Yes", "No"])
    mun    = st.number_input("Municipality Insured", 100, 10000, 500, step=100)
    prov   = st.number_input("Province Insured", 100, 10000, 3000, step=100)
    claims = st.number_input("Annual Claims Cost (₹)", 0, 10000, 1000, step=100)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Predict button (centred) ──
_, btn_col, _ = st.columns([2, 3, 2])
with btn_col:
    predict_clicked = st.button("🔮  Predict My Premium")

# ================= BUILD DATAFRAME =================
def build_df():
    row = {col: 0 for col in predictor.feature_cols}
    row.update({
        "age":               age,
        "exposure_time":     exposure,
        "seniority_insured": seniority,
        "seniority_policy":  seniority,
        "n_insured_mun":     mun,
        "n_insured_prov":    prov,
        "n_insured_pc":      mun,
        "cost_claims_year":  claims,
        "gender":            gender,
        "type_policy":       policy,
        "reimbursement":     reimb,
        "new_business":      new,
    })
    return pd.DataFrame([row])

# ================= MATPLOTLIB DARK THEME =================
def set_dark_style():
    plt.rcParams.update({
        "figure.facecolor":  "#111827",
        "axes.facecolor":    "#1a2236",
        "axes.edgecolor":    "#1e3a5c",
        "axes.labelcolor":   "#94a3b8",
        "xtick.color":       "#64748b",
        "ytick.color":       "#64748b",
        "text.color":        "#e2e8f0",
        "grid.color":        "#1e293b",
        "grid.linewidth":    0.5,
        "font.family":       "monospace",
    })

# ================= RESULTS =================
if predict_clicked:
    df      = build_df()
    premium = predictor.predict(df)[0]

    avg_premium = 1800
    delta_pct   = ((premium - avg_premium) / avg_premium) * 100
    risk_label  = "LOW RISK" if premium < 1000 else ("MEDIUM RISK" if premium < 2500 else "HIGH RISK")
    risk_color  = "#34d399"  if premium < 1000 else ("#f5c842"     if premium < 2500 else "#f87171")

    # ── Result hero card ──
    st.markdown(f"""
    <div class="iq-result">
      <div>
        <div class="iq-result-label">Estimated Annual Premium</div>
        <div class="iq-result-value">₹{premium:,.2f}</div>
        <div class="iq-result-sub">
          {"▲" if delta_pct>0 else "▼"} {abs(delta_pct):.1f}% vs. market average of ₹{avg_premium:,}
          &nbsp;·&nbsp;
          <span style="color:{risk_color};font-weight:600;">{risk_label}</span>
        </div>
      </div>
      <div class="iq-result-icon">💰</div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI row ──
    monthly = premium / 12
    cover_ratio = max(0, (10000 - claims) / 10000 * 100)
    st.markdown(f"""
    <div class="iq-kpi-row">
      <div class="iq-kpi">
        <div class="iq-kpi-label">Monthly Premium</div>
        <div class="iq-kpi-value">₹{monthly:,.0f}</div>
        <div class="iq-kpi-delta delta-neutral">per month</div>
      </div>
      <div class="iq-kpi">
        <div class="iq-kpi-label">vs Market Avg</div>
        <div class="iq-kpi-value">{"+" if delta_pct>0 else ""}{delta_pct:.1f}%</div>
        <div class="iq-kpi-delta {'delta-up' if delta_pct>0 else 'delta-down'}">
          {"above" if delta_pct>0 else "below"} average
        </div>
      </div>
      <div class="iq-kpi">
        <div class="iq-kpi-label">Coverage Health</div>
        <div class="iq-kpi-value">{cover_ratio:.0f}%</div>
        <div class="iq-kpi-delta {'delta-up' if cover_ratio<70 else 'delta-down'}">
          remaining coverage
        </div>
      </div>
      <div class="iq-kpi">
        <div class="iq-kpi-label">Policy Seniority</div>
        <div class="iq-kpi-value">{seniority}y</div>
        <div class="iq-kpi-delta {'delta-down' if seniority>=10 else 'delta-neutral'}">
          {"mature" if seniority>=10 else "early stage"}
        </div>
      </div>
      <div class="iq-kpi">
        <div class="iq-kpi-label">Risk Profile</div>
        <div class="iq-kpi-value" style="color:{risk_color}">{risk_label.split()[0]}</div>
        <div class="iq-kpi-delta delta-neutral">assessment</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── VISUAL INSIGHTS ──
    st.markdown('<div class="iq-section"><span class="iq-section-icon">📊</span>VISUAL INSIGHTS</div>', unsafe_allow_html=True)
    set_dark_style()

    g1, g2, g3 = st.columns(3)

    with g1:
        fig, ax = plt.subplots(figsize=(3.8, 2.6))
        bars = ax.barh(["Market Avg", "Your Premium"], [avg_premium, premium],
                       color=["#334155", "#38bdf8"], height=0.5)
        ax.bar_label(bars, fmt="₹%.0f", padding=4, fontsize=8, color="#e2e8f0")
        ax.set_xlim(0, max(premium, avg_premium) * 1.3)
        ax.set_title("Premium vs Market", fontsize=9, color="#94a3b8", pad=8)
        ax.set_xlabel("Annual ₹", fontsize=7)
        ax.grid(axis="x", alpha=0.3)
        ax.spines[["top","right","left"]].set_visible(False)
        fig.tight_layout(pad=0.6)
        st.pyplot(fig, use_container_width=False)
        plt.close(fig)

    with g2:
        fig2, ax2 = plt.subplots(figsize=(3.0, 2.6))
        sizes  = [claims, max(1, 10000 - claims)]
        colors = ["#f87171", "#34d399"]
        wedges, texts, autotexts = ax2.pie(
            sizes, labels=["Claims","Coverage"],
            colors=colors, autopct="%1.0f%%",
            startangle=90,
            wedgeprops={"linewidth":0, "edgecolor":"#111827"},
            textprops={"fontsize":8},
        )
        for at in autotexts: at.set_fontsize(8)
        ax2.set_title("Claims vs Coverage", fontsize=9, color="#94a3b8", pad=8)
        fig2.tight_layout(pad=0.6)
        st.pyplot(fig2, use_container_width=False)
        plt.close(fig2)

    with g3:
        fig3, ax3 = plt.subplots(figsize=(3.8, 2.6))
        bars3 = ax3.bar(["Seniority (y)", "Exposure (y)"],
                        [seniority, exposure],
                        color=["#f5c842", "#818cf8"], width=0.45)
        ax3.bar_label(bars3, fmt="%.1f", padding=3, fontsize=8, color="#e2e8f0")
        ax3.set_title("Seniority & Exposure", fontsize=9, color="#94a3b8", pad=8)
        ax3.set_ylim(0, max(seniority, exposure, 1) * 1.35)
        ax3.grid(axis="y", alpha=0.3)
        ax3.spines[["top","right","left"]].set_visible(False)
        fig3.tight_layout(pad=0.6)
        st.pyplot(fig3, use_container_width=False)
        plt.close(fig3)

    # ── SHAP FEATURE CONTRIBUTIONS ──
    st.markdown('<div class="iq-section"><span class="iq-section-icon">🔍</span>FEATURE CONTRIBUTIONS (SHAP)</div>', unsafe_allow_html=True)

    try:
        X_proc = predictor.preprocess(df)
        X_bg   = pd.concat([X_proc] * 10, ignore_index=True)
        explainer = get_explainer(predictor.model, X_bg)

        if explainer is None:
            st.warning("⚠️ SHAP explainer could not be built for this model type.")
        else:
            shap_vals = explain_instance(explainer, X_proc)
            shap_df = (
                pd.DataFrame(list(shap_vals.items()), columns=["Feature", "Impact"])
                .sort_values(by="Impact", key=abs, ascending=False)
                .reset_index(drop=True)
            )
            top_df = shap_df.head(10)

            tc1, tc2 = st.columns([1, 1])

            with tc1:
                st.dataframe(
                    top_df.style
                        .format({"Impact": "{:+.4f}"})
                        .background_gradient(subset=["Impact"], cmap="RdYlGn", vmin=-300, vmax=300),
                    use_container_width=True,
                    height=340,
                )

            with tc2:
                set_dark_style()
                fig_s, ax_s = plt.subplots(figsize=(4.5, 3.2))
                vals_plot   = top_df["Impact"].values[::-1]
                feats_plot  = top_df["Feature"].values[::-1]
                bar_colors  = ["#34d399" if v >= 0 else "#f87171" for v in vals_plot]
                bars_s = ax_s.barh(range(len(feats_plot)), vals_plot, color=bar_colors, height=0.6)
                ax_s.set_yticks(range(len(feats_plot)))
                ax_s.set_yticklabels(feats_plot, fontsize=7.5)
                ax_s.axvline(0, color="#64748b", linewidth=0.8, linestyle="--")
                ax_s.set_xlabel("SHAP value", fontsize=7.5)
                ax_s.set_title("Top Feature Contributions", fontsize=9, color="#94a3b8", pad=8)
                ax_s.grid(axis="x", alpha=0.3)
                ax_s.spines[["top","right"]].set_visible(False)
                pos_patch = mpatches.Patch(color="#34d399", label="Increases premium")
                neg_patch = mpatches.Patch(color="#f87171", label="Reduces premium")
                ax_s.legend(handles=[pos_patch, neg_patch], fontsize=7,
                            loc="lower right", framealpha=0.2)
                fig_s.tight_layout(pad=0.6)
                st.pyplot(fig_s, use_container_width=False)
                plt.close(fig_s)

    except Exception as e:
        st.error(f"SHAP analysis failed: {e}")

    # ── PERSONALIZED SUGGESTIONS ──
    st.markdown('<div class="iq-section"><span class="iq-section-icon">💡</span>PERSONALIZED SUGGESTIONS</div>', unsafe_allow_html=True)

    suggestions = []
    if claims > 3000:
        suggestions.append(("warn", "⚠️ High claims cost — consider preventive health measures to lower future premiums."))
    if seniority < 10:
        suggestions.append(("tip", "📈 Increase policy seniority for better coverage benefits and loyalty discounts."))
    if policy == "III":
        suggestions.append(("tip", "💼 Consider switching to Policy I or II for more competitive premium rates."))
    if premium > 3000:
        suggestions.append(("warn", "📊 High premium detected — review claims history and age risk factors."))
    if not suggestions:
        suggestions.append(("ok", "✅ Your profile looks optimal. Maintain healthy habits to keep premiums low!"))

    s_cols = st.columns(min(len(suggestions), 2))
    for i, (stype, stxt) in enumerate(suggestions):
        cls = "warn" if stype == "warn" else ("ok" if stype == "ok" else "")
        with s_cols[i % len(s_cols)]:
            st.markdown(f'<div class="iq-suggestion {cls}">{stxt}</div>', unsafe_allow_html=True)

    # ── SCENARIO SIMULATION ──
    st.markdown('<div class="iq-section"><span class="iq-section-icon">🔁</span>SCENARIO SIMULATION</div>', unsafe_allow_html=True)

    sim_df = df.copy()
    sim_df["seniority_insured"] += 5
    new_premium = predictor.predict(sim_df)[0]
    savings     = premium - new_premium

    st.markdown(f"""
    <div class="iq-sim-card">
      <div class="iq-sim-item">
        <div class="iq-sim-lbl">Current Premium</div>
        <div class="iq-sim-val">₹{premium:,.2f}</div>
      </div>
      <div style="color:#334155;font-size:1.5rem;">→</div>
      <div class="iq-sim-item">
        <div class="iq-sim-lbl">After +5 Years Seniority</div>
        <div class="iq-sim-val">₹{new_premium:,.2f}</div>
      </div>
      <div style="color:#334155;font-size:1.5rem;">=</div>
      <div class="iq-sim-item">
        <div class="iq-sim-lbl">Potential Savings</div>
        <div class="iq-sim-val iq-sim-savings">{"+" if savings > 0 else ""}₹{savings:,.2f}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── DETAILED REPORT ──
    st.markdown('<div class="iq-section"><span class="iq-section-icon">📄</span>DETAILED INSURANCE REPORT</div>', unsafe_allow_html=True)

    sugg_text = "\n".join(f"  • {t}" for _, t in suggestions)
    report = f"""
╔══════════════════════════════════════════════════╗
║           InsureIQ — INSURANCE REPORT            ║
╚══════════════════════════════════════════════════╝

Policy Holder : ID-{df.index[0]+1000}
Date          : {pd.Timestamp.now().strftime('%d %b %Y')}

── PERSONAL DETAILS ─────────────────────────────
  Age           : {age} years
  Gender        : {gender}
  Policy Type   : {policy}
  Seniority     : {seniority} years
  Exposure Time : {exposure:.2f} years
  Reimbursement : {reimb}
  New Business  : {new}

── FINANCIAL DETAILS ────────────────────────────
  Municipality Insured : {mun:,}
  Province Insured     : {prov:,}
  Annual Claims Cost   : ₹{claims:,.2f}

── PREMIUM ESTIMATE ─────────────────────────────
  Estimated Annual Premium : ₹{premium:,.2f}
  Monthly Equivalent       : ₹{monthly:,.2f}
  Risk Classification      : {risk_label}
  vs Market Average        : {"+" if delta_pct>0 else ""}{delta_pct:.1f}%

── RECOMMENDATIONS ──────────────────────────────
{sugg_text}

── SIMULATION ───────────────────────────────────
  Seniority +5 yrs  →  New Premium : ₹{new_premium:,.2f}
  Potential Annual Savings         : ₹{savings:,.2f}

════════════════════════════════════════════════════
  This report is generated by InsureIQ AI system.
  For informational purposes only.
════════════════════════════════════════════════════
"""
    rc1, rc2 = st.columns([1, 2])
    with rc1:
        st.download_button(
            "📥  Download Insurance Report",
            report,
            file_name=f"insureiq_report_ID{df.index[0]+1000}.txt",
            mime="text/plain",
        )
    st.text_area("📄 Report Preview", report, height=380)

# ── Footer ──
st.markdown("""
<div style="text-align:center;padding:2.5rem 0 1rem 0;color:#334155;font-size:.75rem;letter-spacing:.5px;">
  InsureIQ · Health Insurance Premium Intelligence · Built with LightGBM + SHAP + Streamlit
</div>
""", unsafe_allow_html=True)