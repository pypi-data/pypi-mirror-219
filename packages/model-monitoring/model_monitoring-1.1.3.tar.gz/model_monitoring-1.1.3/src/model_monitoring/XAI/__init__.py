import warnings
import re
import pandas as pd
import numpy as np
import shap
from functools import reduce

from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold, GroupKFold
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.inspection import permutation_importance

from model_monitoring.utils import check_size, get_categorical_features


class XAI:
    """XAI (Explainable artificial intelligence) Class."""

    def __init__(
        self,
        model,
        use_cv=False,
        grid=None,
        cv_funct=RandomizedSearchCV,
        cv_scoring="auto",
        n_iter=20,
        cv_type=StratifiedKFold(5, random_state=42, shuffle=True),
        algo_type="classification",
    ):
        """XAI (Explainable artificial intelligence) Class.

        Args:
            model : classifier or regressor in sklearn API class.
            use_cv (bool, optional): determines if using hyperparameters tuning with CV logic. Defaults to False.
            grid (dict, optional): hyperparameters grid. Defaults to None.
            cv_funct: function or class for the Cross Validation. Defaults to None.
            cv_scoring: scoring argument of the cv_funct. Defaults to "auto" selects "roc_auc" fo classification, "r2" for regression
                and "balanced accuracy" for multiclass.
            n_iter (int, optional): number of iteration, i.e. set of hyperparams tested in Cross Validation. Defaults to 20.
            cv_type : function or class for defining the CV sets. Defaults to StratifiedKFold(5, random_state=42, shuffle=True).
            algo_type (str, optional): "classification", "multiclass", "regression", describes the problem type.
                "classification" has to be used only for binary classification. Defaults to "classification".
        """
        # If using a CV strategy, define the model as the SearchCV, otherwise initialize the model provided in input as attribute
        if use_cv:
            if grid is None:
                grid = {}
            if cv_scoring == "auto":
                if algo_type not in ["classification", "regression", "multiclass"]:
                    raise ValueError("algo_type argument must be one of ['classification', 'regression', 'multiclass']")
                else:
                    if algo_type == "classification":
                        cv_scoring = "roc_auc"
                    elif algo_type == "regression":
                        cv_scoring = "r2"
                    else:
                        cv_scoring = "balanced_accuracy"
            if (algo_type == "regression") and (
                str(cv_type.__class__()).startswith(("StratifiedKFold", "StratifiedGroupKFold"))
            ):
                raise ValueError(
                    "Fold Cross Validation uncorrect for regression algorithm, use KFold() or GroupKFold()"
                )
            try:
                CVSel_algo = cv_funct(model, grid, n_iter=n_iter, cv=cv_type, scoring=cv_scoring)
            except Exception:
                CVSel_algo = cv_funct(model, grid, cv=cv_type, scoring=cv_scoring)  # for GridSearchCV
            self.model = CVSel_algo
        else:
            self.model = model

        # Attributes
        self.use_cv = use_cv
        self.grid = grid
        self.cv_funct = cv_funct
        self.cv_scoring = cv_scoring
        self.n_iter = n_iter
        self.cv_type = cv_type
        self.algo_type = algo_type
        self._fitted = False
        self.report_feat_imp = None

    def fit(self, db, output_model, manage_groups=False, groups=None):
        """Fit data given in input with the model provided in input in the class.

        Args:
            db (pd.Series/pd.DataFrame): Features used from the model to explain.
            output_model (pd.Series/np.array): output of the model to explain.
            manage_groups (bool, optional): determines if there is a feature whose groups have to be kept joined in CV. Defaults to False.
            groups (pd.Series, optional): feature whose groups have to be kept joined in CV. Defaults to None.
        """
        # Check size of the output of the model and dataset in input
        check_size(db, output_model)

        self.db = db
        self.output_model = output_model

        # Groups check
        if manage_groups:
            if groups is None:
                warnings.warn("no group defined")
                manage_groups = False
            if not groups.index.equals(self.db.index):
                raise ValueError("Groups Series index do not match with DataFrame index in input!")
        else:
            groups = None

        self.manage_groups = manage_groups
        self.groups = groups

        self.categorical_ohe = False
        db_tsf = self.db.copy()
        cats_feat = get_categorical_features(self.db)
        self.cats_feat = cats_feat

        # One-Hot-Encoding Categorical features
        if len(cats_feat) > 0:
            preprocessor = ColumnTransformer(
                transformers=[
                    ("cat", OneHotEncoder(handle_unknown="ignore", sparse=False), cats_feat),
                ],
                remainder="passthrough",
            )
            preprocessor.fit(db_tsf)
            feat_names = preprocessor.get_feature_names_out()
            feat_names = [re.sub(r"((remainder)|(cat))__", "", x) for x in feat_names]
            db_tsf = pd.DataFrame(preprocessor.transform(db_tsf), columns=feat_names)
            self.categorical_ohe = True

        self.db_tsf = db_tsf

        if self.use_cv:
            # Redifine KFold strategy if there are groups to consider
            if self.manage_groups:
                if len(self.groups) != len(db_tsf):
                    raise ValueError(
                        "dataset to be performed shap and groups-Series don't have the same number of rows ({0},{1})".format(
                            len(db_tsf), len(self.groups)
                        )
                    )
                number_splits = self.cv_type.n_splits
                if not (str(self.cv_type.__class__()).startswith(("StratifiedKFold", "StratifiedGroupKFold"))):
                    self.model.cv = GroupKFold(number_splits).split(db_tsf, self.output_model, groups)

        # Fit
        self.model_fitted = self.model.fit(db_tsf, output_model)
        if self.use_cv:
            self.model_fitted = self.model_fitted.best_estimator_
        self._fitted = True

    def get_report_feature_importance(
        self,
        feat_imp_mode="gini",
        shap_type="tree",
        n_weighted_kmeans=10,
        n_samples_deep=1000,
        n_repeats_permutation=5,
        perm_crit="mean",
    ):
        """Retrieve the features importance report.

        Args:
            feat_imp_mode (str, optional): "coef","shap","permutation","gini" describes the type of retrieving features importance:
                - "coef" retrieves the coefficient for linear models (e.g. LogisticRegression, LinearRegression, SVM with linear kernel);
                - "shap" retrieves the features' Shapley Value;
                - "permutation" retrieves features importance by permutation algorithm;
                - "gini" retrieves features importance by impurity decrease algorithm.
                Defaults to "gini".
            shap_type (str, optional): "tree","kernel","deep" describes the type of Explainer for features' Shapley Value:
                - "tree" to explain the output of ensemble tree models;
                - "kernel" to explain the output of any models using a special weighted linear regression;
                - "deep" to approximate the output of deep learning models.
                It is set only if feat_impo_mode is "shap". Defaults to 'tree'.
            n_weighted_kmeans (int, optional): number of weighted centroids for summarizing the dataset used as background dataset for integrating out features.
                It is set only if feat_impo_mode is "shap" and shap_type is "kernel". Defaults to 10.
            n_samples_deep (int, optional): number of random background samples used for integrating out features.
                It is set only if feat_impo_mode is "shap" and shap_type is "deep". Defaults to 1000.
            n_repeats_permutation (int, optional): number of times to permute a feature.
                It is set only if feat_impo_mode is "permutation". Defaults to 5.
            perm_crit (str, optional): "mean","max","min" describes the mode of aggregating the permutation importances of samples for each feature. Defaults to 'mean'.

        Returns:
            pd.DataFrame: features importance report
        """
        # Check the type fo retrieving features importance
        if feat_imp_mode not in ["coef", "shap", "permutation", "gini"]:
            raise ValueError("feat_imp_mode argument must be one of ['coef', 'shap', 'permutation','gini']")
        self.feat_imp_mode = feat_imp_mode

        if self._fitted:
            feature_names = self.db_tsf.columns
            # Gini algorithm
            if self.feat_imp_mode == "gini":
                try:
                    feature_importances = np.abs(self.model_fitted.feature_importances_)
                except Exception:
                    raise ValueError(
                        f"{self.feat_imp_mode} not valid logic for retrieve feature importances with {self.model_fitted} model"
                    )
            # Permutation algorithm
            elif self.feat_imp_mode == "permutation":
                if perm_crit not in ["mean", "max", "min"]:
                    raise ValueError("perm_crit argument must be one of ['mean','max','min']")
                self.perm_crit = perm_crit
                try:
                    self.n_repeats_permutation = n_repeats_permutation
                    perm_importance = permutation_importance(
                        self.model_fitted, self.db_tsf, self.output_model, n_repeats=n_repeats_permutation
                    )
                    # Aggregating permutation importance scores by mean
                    if self.perm_crit == "mean":
                        feature_importances = np.abs(perm_importance.importances).mean(axis=1)
                    # Aggregating permutation importance scores by max
                    elif self.perm_crit == "max":
                        feature_importances = np.abs(perm_importance.importances).max(axis=1)
                    # Aggregating permutation importance scores by min
                    elif self.perm_crit == "min":
                        feature_importances = np.abs(perm_importance.importances).min(axis=1)
                except Exception:
                    raise ValueError(
                        f"{self.feat_imp_mode} not valid logic for retrieve feature importances with {self.model_fitted} model"
                    )
            # For Linear Models, retrieves absolute values of coefficients
            elif self.feat_imp_mode == "coef":
                try:
                    feature_importances = np.abs(self.model_fitted.coef_[0])
                except Exception:
                    raise ValueError(
                        f"{self.feat_imp_mode} not valid logic for retrieve feature importances with {self.model_fitted} model"
                    )
            # Features' Shapley Values algorithm
            elif self.feat_imp_mode == "shap":
                if shap_type not in ["tree", "kernel", "deep"]:
                    raise ValueError("shap_type argument must be one of ['tree','kernel','depp']")
                self.shap_type = shap_type
                # For tree models
                if self.shap_type == "tree":
                    try:
                        feature_importances = shap.TreeExplainer(self.model_fitted).shap_values(self.db_tsf)
                    except Exception:
                        raise ValueError(
                            f"{self.shap_type}-{self.feat_imp_mode} not valid logic for retrieve feature importances with {self.model_fitted} model"
                        )
                # For any models. ATTENTION: very slow, it depends on size of background dataset (second parameter of KernelExplainer)
                if self.shap_type == "kernel":
                    self.n_weighted_kmeans = n_weighted_kmeans
                    try:
                        feature_importances = shap.KernelExplainer(
                            self.model_fitted.predict, shap.kmeans(self.db_tsf, self.n_weighted_kmeans)
                        ).shap_values(self.db_tsf)
                    except Exception:
                        raise ValueError(
                            f"{self.shap_type}-{self.feat_imp_mode} not valid logic for retrieve feature importances with {self.model_fitted} model"
                        )
                # For deep learning models. ATTENTION: speed depends on size of background dataset (second parameter of DeepExplainer)
                if self.shap_type == "deep":
                    self.n_samples_deep = n_samples_deep
                    try:
                        feature_importances = shap.DeepExplainer(
                            self.model_fitted, self.db_tsf.sample(n=self.n_samples_deep)
                        ).shap_values(self.db_tsf.values)[0]
                    # DeepExplainer is not compatible for tensorflow models with version upper than 2.4.0
                    except AttributeError:
                        raise ValueError(
                            "model type not currently supported! If used a tensorflow model try using the following code in importing packages phase\n\nimport tensorflow as tf\ntf.compat.v1.disable_v2_behavior()"
                        )
                    except Exception:
                        raise ValueError(
                            f"{self.shap_type}-{self.feat_imp_mode} not valid logic for retrieve feature importances with {self.model_fitted} model"
                        )
                # For (multi) classification
                if isinstance(feature_importances, list):
                    db_list = list()
                    for i in range(len(feature_importances)):
                        db_list.append(
                            pd.DataFrame(
                                {
                                    "feature": feature_names,
                                    "shap_importance_" + str(i): np.abs(feature_importances[i]).mean(axis=0),
                                }
                            )
                        )
                    shap_importance = (
                        reduce(lambda left, right: pd.merge(left, right, how="outer", on="feature"), db_list)
                        .set_index("feature")
                        .assign(shap_importance=lambda x: x.sum(axis=1))
                        .loc[:, "shap_importance"]
                        .reset_index()
                    )
                    feature_importances = shap_importance.shap_importance.values
                # For regression and (some - depending on the classifier) binary classification
                elif isinstance(feature_importances, np.ndarray):
                    feature_importances = np.abs(feature_importances).mean(axis=0)
            # initialize the report of feature importances
            report_feat_imp = pd.DataFrame({"feature": feature_names, "feat_importance": feature_importances})
            # sum feature importance scores for variables auto-encoded
            if self.categorical_ohe:
                for i in self.cats_feat:
                    report_feat_imp.loc[report_feat_imp.feature.str.startswith(i)] = report_feat_imp.loc[
                        report_feat_imp.feature.str.startswith(i)
                    ].assign(
                        feature=i,
                        feat_importance=report_feat_imp.loc[
                            report_feat_imp.feature.str.startswith(i), "feat_importance"
                        ].sum(),
                    )
                report_feat_imp = report_feat_imp.drop_duplicates().dropna().reset_index(drop=True)

            # normalize with sum to 1 feature importance scores
            report_feat_imp.feat_importance = report_feat_imp.feat_importance / report_feat_imp.feat_importance.sum()

            self.report_feat_imp = report_feat_imp.sort_values(by=["feat_importance"], ascending=True)

        else:
            raise ValueError(
                f"no model fitted yet. Call {self.__name__}.{self.fit.__name__}() with appropriate arguments before using this method."
            )
        return self.report_feat_imp

    def plot(self):
        """Plot the report on features importance."""
        if self.report_feat_imp is not None:
            self.report_feat_imp.plot(x="feature", y="feat_importance", kind="barh", title="Features Importance")
        else:
            raise ValueError("Missing report, run .get_report_feature_importance() first")
