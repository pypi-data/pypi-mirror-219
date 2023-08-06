# Binary Classification Utilities

This packages provides a simple convenience wrapper around some basic sklearn and scikit-plot utilities for binary classification. The only function available is `eval_classification()`.

### Available Parameters

**For cross-validation on full dataset**

`untrained_model`: classifier object (untrained); this is used for cross-validation

`X`: Pandas DataFrame containing preprocessed, normalized, complete dataset

`y`: Pandas Series containing encoded labels for `X`

**For single run evaluation**

`y_test`: ground-truth encoded labels of test set

`y_pred`: binary predicted labels for test set

`y_pred_proba`: probabilist predictions per class for test set

**For plotting**

`class_names`: list of unique classes

`RESULTS_DIR`: location to store results; directory will be created if it does not exist

`save`: set True if you want to save all results in RESULTS_DIR; defaults to False

`show`: display all results; useful in notebooks; defaults to False

### Example Usage
```python
'''
X:               Pandas DataFrame containing preprocessed,normalized data matrix
y:               Pandas Series containing encoded labels
class_names:     Set of unique class names.
'''

from sklearn.datasets import load_breast_cancer

data = load_breast_cancer()

X = pd.DataFrame(data.data)
y = pd.Series(data.target)

class_names = data.target_names

from sklearn.model_selection import train_test_split
import pandas as pd

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=42)

from sklearn.tree import DecisionTreeClassifier
clf_dt = DecisionTreeClassifier()
clf_dt.fit(X_train, y_train)

y_pred = clf_dt.predict(X_test)
y_pred_proba = clf_dt.predict_proba(X_test)

from bcutils4r.eval_classification import eval_classification
eval_classification( untrained_model=DecisionTreeClassifier(), n_splits=5,
                    class_names=class_names, 
                    X=X, y=y, 
                    y_test=y_test, y_pred=y_pred, y_pred_proba=y_pred_proba, 
                    save=False, RESULTS_DIR=None,
                    show=True)

```
<!-- ### Confusion Matrix -->
![cm](tests/example_classification/results/confusion_matrix.png)
<!-- ![cm](https://github.com/rutujagurav/bcutils4r/blob/master/tests/example_classification/results/confusion_matrix.png) -->

<!-- ### Class-wise ROC curve -->
![roc](tests/example_classification/results/classwise_roc_curve.png)
<!-- ![roc](https://github.com/rutujagurav/bcutils4r/blob/master/tests/example_classification/results/classwise_roc_curve.png) -->

<!-- ### Class-wise PR curve -->
![pr](tests/example_classification/results/classwise_pr_curve.png)
<!-- ![pr](https://github.com/rutujagurav/bcutils4r/blob/master/tests/example_classification/results/classwise_pr_curve.png) -->

<!-- ### KS statistic  -->
![ks_stat](tests/example_classification/results/ks_stat.png)
<!-- ![ks_stat](https://github.com/rutujagurav/bcutils4r/blob/master/tests/example_classification/results/ks_stat.png) -->

<!-- ### Lift Curve  -->
![lift](tests/example_classification/results/lift_curve.png)
<!-- ![lift](https://github.com/rutujagurav/bcutils4r/blob/master/tests/example_classification/results/lift_curve.png) -->

<!-- ### Cross-validated ROC curves -->
![cv_roc](tests/example_classification/results/crossvalidation_roc_curve.png)
<!-- ![cv_roc](https://github.com/rutujagurav/bcutils4r/blob/master/tests/example_classification/results/crossvalidation_roc_curve.png) -->

<!-- ### Cross-validated PR curves -->
![cv_pr](tests/example_classification/results/crossvalidation_pr_curve.png)
<!-- ![cv_pr](https://github.com/rutujagurav/bcutils4r/blob/master/tests/example_classification/results/crossvalidation_pr_curve.png) -->