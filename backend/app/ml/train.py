from pathlib import Path #Library for hadnling files in python

import joblib # Used to save and load machine learning model
from sklearn.datasets import load_breast_cancer # Loading existing dataset
from sklearn.linear_model import LogisticRegression # Classification algorithm to predict data wisely
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split # To split data into Training data and Testing data
from sklearn.pipeline import make_pipeline # To combine multiple ml steps in single pipeline
from sklearn.preprocessing import StandardScaler # To Standarized data

#Input fields
FEATURES = ["mean radius", "mean texture", "mean perimeter", "mean area"]
MODEL_PATH = Path(__file__).parent / "model.joblib"
# __file__ means path of current file and it creates model.joblib in the same folder

data = load_breast_cancer(as_frame=True) # as_frame means loads data in Pandas Data Format
x = data.data[FEATURES]
y = data.target  # 0 = malignant  1 = benign

# data.data -> input features
# data.target -> Output labels
# data.feature_name -> Features names
# data.target_names -> Class names

X_train, X_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y # to maintain class properties to testing and training set ratio
)

#here we start classification in ml
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
model.fit(X_train, y_train) # we let model to learn

acc = accuracy_score(y_test, model.predict(X_test))
print(f"Test accuracy: {acc:.3f}")

#it will serialize and store the object
joblib.dump(
    {
        "model": model,
        "features": FEATURES,
        "classes": {0: "malignant", 1: "benign"}
    },
    MODEL_PATH
)

print(f"Saved to {MODEL_PATH}")