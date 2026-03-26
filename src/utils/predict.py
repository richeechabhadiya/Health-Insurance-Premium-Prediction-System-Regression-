# import joblib
# import pandas as pd
# import numpy as np

# class Predictor:
#     def __init__(self, model_path):
#         bundle = joblib.load(model_path)

#         self.model = bundle["model"]
#         self.feature_cols = bundle["feature_cols"]
#         self.cat_cols = bundle.get("cat_cols", [])
#         self.cat_values = bundle.get("cat_values", {})

#     def preprocess(self, df):
#         X = df.copy()

#         # ensure all columns exist
#         for col in self.feature_cols:
#             if col not in X.columns:
#                 X[col] = 0

#         # correct order
#         X = X[self.feature_cols]

#         # categorical handling
#         for col in self.cat_cols:
#             if col in X.columns:
#                 X[col] = X[col].astype("category")
#                 if col in self.cat_values:
#                     X[col] = X[col].cat.set_categories(self.cat_values[col])

#         return X

#     def predict(self, df):
#         X = self.preprocess(df)
#         preds = self.model.predict(X)
#         return preds



import joblib
import pandas as pd
import numpy as np

class Predictor:
    def __init__(self, model_path):
        bundle = joblib.load(model_path)

        self.model = bundle["model"]
        self.feature_cols = bundle["feature_cols"]
        self.cat_cols = bundle.get("cat_cols", [])
        self.cat_values = bundle.get("cat_values", {})

    def preprocess(self, df):
        X = df.copy()

        # ensure all columns exist
        for col in self.feature_cols:
            if col not in X.columns:
                X[col] = 0

        # correct order
        X = X[self.feature_cols]

        # categorical handling
        for col in self.cat_cols:
            if col in X.columns:
                X[col] = X[col].astype("category")
                if col in self.cat_values:
                    X[col] = X[col].cat.set_categories(self.cat_values[col])

        return X

    def predict(self, df):
        X = self.preprocess(df)
        preds = self.model.predict(X)
        return preds