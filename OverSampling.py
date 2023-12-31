
import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
import pickle
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Read train data
df1 = pd.read_csv('airline_sentiment_analysis.csv', header=None, names=['S.No','AirLine_Sentiment', 'Text'])
df=df1.iloc[1:]
df.drop(df.columns[0], axis=1,inplace=True) 
for i in range(1,len(df['Text'])+1):
  if(df['AirLine_Sentiment'][i]=='positive'):
    df['AirLine_Sentiment'][i]=1
  else:
    df['AirLine_Sentiment'][i]=0

# Cleaning the texts
import re
corpus = []
for i in range(1,len(df['Text'])+1):
    review = re.sub('[^a-zA-Z\ ]', '', df['Text'][i])
    review = review.lower()
    review = review.split()
    review = ' '.join(review)
    corpus.append(review)

# Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1500)
X = cv.fit_transform(corpus).toarray()
y = df.iloc[:, 0].values
y=y.astype('int')

from sklearn.feature_extraction.text import TfidfTransformer
tfidfconverter = TfidfTransformer()
X = tfidfconverter.fit_transform(X).toarray()

# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 0)

unique, count = np.unique(y_train, return_counts=True)
Y_train_dict_value_count = { k:v for (k,v) in zip(unique, count)}
sm = SMOTE(random_state=12,sampling_strategy=0.5)
x_train_res, y_train_res = sm.fit_sample(X_train, y_train)
unique, count = np.unique(y_train_res, return_counts=True)
y_train_smote_value_count = { k:v for (k,v) in zip(unique, count)}

from sklearn.svm import SVC
classifier1 = SVC(kernel = 'rbf', random_state = 0)
classifier1.fit(x_train_res, y_train_res)

'''
# Fitting SVM to the Training set
from sklearn.svm import SVC
classifier1 = SVC(kernel = 'linear', random_state = 0)
classifier1.fit(x_train_res, y_train_res)

# Fitting Logistic Regression to the Training set
from sklearn.linear_model import LogisticRegression
classifier1 = LogisticRegression(random_state = 0)
classifier1.fit(x_train_res, y_train_res)

# Fitting XGBoost to the Training set
from xgboost import XGBClassifier
classifier1 = XGBClassifier()
classifier1.fit(x_train_res, y_train_res)

# Fitting K-NN to the Training set
from sklearn.neighbors import KNeighborsClassifier
classifier1 = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
classifier1.fit(x_train_res, y_train_res)

# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier1 = GaussianNB()
classifier1.fit(x_train_res, y_train_res)

# Fitting Decision Tree Classification to the Training set
from sklearn.tree import DecisionTreeClassifier
classifier1 = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
classifier1.fit(x_train_res, y_train_res)

# Fitting Random Forest Classification to the Training set
from sklearn.ensemble import RandomForestClassifier
classifier1 = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier1.fit(x_train_res, y_train_res)
'''

filename = 'finalized_model.sav'
pickle.dump(classifier1, open(filename, 'wb'))
classifier = pickle.load(open(filename, 'rb'))

# Predicting the Test set results
y_pred = classifier.predict(X_test)

print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))
print(accuracy_score(y_test, y_pred))

text = 'Congrats #SportStar on your 7th best goal from last season winning goal of the year :) #Baller #Topbin #oneofmanyworldies'
print(text)
text = re.sub('[^a-zA-Z\ ]', '', text)
text = text.lower()
text = text.split()
text = ' '.join(text)
text = cv.transform([text]).toarray()
text = tfidfconverter.transform(text).toarray()
label = classifier.predict(text)[0]

if(label==0):
        print('Negative')
else:
        print('Positive')
        
pickle.dump(cv, open("vectorizer.pickle", "wb")) 
pickle.dump(tfidfconverter, open("tfidfconverter.pickle", "wb"))
