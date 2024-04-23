import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('./ML_Algos/training.csv')

label_encoder = LabelEncoder()
df['prognosis_encoded'] = label_encoder.fit_transform(df['prognosis'])

X = df.drop(['prognosis', 'prognosis_encoded'], axis=1)
y = df['prognosis_encoded']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

svc_model = SVC()

svc_model.fit(x_train, y_train)

y_test_pred_svc = svc_model.predict(x_test)

print("Testing Accuracy:", accuracy_score(y_test, y_test_pred_svc))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_test_pred_svc))
print("\nClassification Report:")
print(classification_report(y_test, y_test_pred_svc))

with open('./ML_Models/disease_predictor_model.pkl', 'wb') as file:
    pickle.dump(svc_model, file)

print("Disease predictor model saved successfully.")