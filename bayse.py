# -*- coding: utf-8 -*-  
import numpy as np   
from sklearn.cross_validation import train_test_split  
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_recall_curve  
from sklearn.metrics import classification_report
  
#读取
data = np.loadtxt('../data/data.txt',dtype=np.int, delimiter='\t')
target = np.loadtxt("../data/comment.txt", dtype=np.int,delimiter='\n')
x = data
y = target
  
  
#加载数据集，切分数据集80%训练，20%测试  
x_train, x_test, y_train, y_test = train_test_split(data, target, test_size = 0.2) 
  
  
#调用MultinomialNB分类器  
clf = MultinomialNB().fit(x_train, y_train)
doc_class_predicted = clf.predict(x_test)  
      
#print(doc_class_predicted)  
#print(y)  
print(np.mean(doc_class_predicted == y_test))  
  
#准确率与召回率  
precision, recall, thresholds = precision_recall_curve(y_test, clf.predict(x_test))  
answer = clf.predict_proba(x_test)[:,1]  
report = answer > 0.5  
print(classification_report(y_test, report, target_names = ['neg', 'pos']))  
