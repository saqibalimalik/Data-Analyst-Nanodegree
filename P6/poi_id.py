#!/usr/bin/python

import sys
import pickle
import matplotlib
from matplotlib import pyplot
sys.path.append("../tools/")
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn import tree
from sklearn.grid_search import GridSearchCV
from numpy import mean
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
target_feature = 'poi' # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

#Total Number of Data points
num_data_points = len(data_dict)
print "Total Data Points: ", num_data_points

#Total number of features in data points
num_data_features = len(data_dict[data_dict.keys()[0]])
print "Number of Features: ", num_data_features

#Let us find out total number of POI in dat
num_poi = 0
for dic in data_dict.values():
  if dic['poi'] == 1: num_poi += 1
print "Total POIs: ", num_poi


### Task 2: Remove outliers

#for dic in data_dict.values():
#    matplotlib.pyplot.scatter( dic['salary'] , dic['bonus']  )
#matplotlib.pyplot.show()

#Find outlier in the plot
for k, v in data_dict.items():
     if v['salary'] != 'NaN' and v['salary'] > 10000000: print k

def remove_keys(dict_object, keys):
    """ removes a list of keys from a dict object """
    for key in keys:
        dict_object.pop(key, 0)
outlier_keys = ['TOTAL', 'THE TRAVEL AGENCY IN THE PARK', 'LOCKHART EUGENE E']
remove_keys(data_dict,outlier_keys)

def count_valid_values(data_dict):
    """ counts the number of non-NaN values for each feature """
    counts = dict.fromkeys(data_dict.itervalues().next().keys(), 0)
    for record in data_dict:
        person = data_dict[record]
        for field in person:
            if person[field] != 'NaN':
                counts[field] += 1
    return counts
### Task 3: Create new feature(s)


### Store to my_dataset for easy export below.
my_dataset = data_dict


for item in my_dataset:
    person = my_dataset[item]
    if (all([person['from_poi_to_this_person'] != 'NaN',
        person['from_this_person_to_poi'] != 'NaN',
        person['to_messages'] != 'NaN',
        person['from_messages'] != 'NaN'
      ])):
      fraction_from_poi = float(person["from_poi_to_this_person"]) / float(person["to_messages"])
      person["fraction_from_poi"] = fraction_from_poi
      fraction_to_poi = float(person["from_this_person_to_poi"]) / float(person["from_messages"])
      person["fraction_to_poi"] = fraction_to_poi
    else:
        person["fraction_from_poi"] = person["fraction_to_poi"] = 0

## Financial:
for item in my_dataset:
  person = my_dataset[item]
  if (all([ person['salary'] != 'NaN',
        person['total_stock_value'] != 'NaN',
        person['exercised_stock_options'] != 'NaN',
        person['bonus'] != 'NaN'
      ])):
    person['wealth'] = sum([person[field] for field in ['salary','total_stock_value','exercised_stock_options','bonus']])
  else:
      person['wealth'] = 'NaN'

## Print non NaN values count
# print count_valid_values(data_dict);

my_features = [target_feature] + ['from_messages',
                                  'from_poi_to_this_person',
                                  'from_this_person_to_poi',
                                  'shared_receipt_with_poi',
                                  'to_messages', 'fraction_from_poi',
                                  'fraction_to_poi',
                                  'shared_receipt_with_poi',
                                  'expenses',
                                  'loan_advances',
                                  'long_term_incentive',
                                  'other',
                                  'restricted_stock',
                                  'restricted_stock_deferred',
                                  'deferral_payments',
                                  'deferred_income',
                                  'salary',
                                  'total_stock_value',
                                  'exercised_stock_options',
                                  'total_payments',
                                  'bonus',
                                  'wealth']
### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, my_features, sort_keys = True)
labels, features = targetFeatureSplit(data)

print "Intuitive features:", my_features

# Scale features
scaler = MinMaxScaler()
features = scaler.fit_transform(features)

# K-best features

def get_k_best(data_dict, features_list, k):
    """ runs scikit-learn's SelectKBest feature selection
        returns dict where keys=features, values=scores
    """
    data = featureFormat(data_dict, features_list)
    labels, features = targetFeatureSplit(data)

    k_best = SelectKBest(k=k)
    k_best.fit(features, labels)
    scores = k_best.scores_
    unsorted_pairs = zip(features_list[1:], scores)
    sorted_pairs = list(reversed(sorted(unsorted_pairs, key=lambda x: x[1])))
    k_best_features = dict(sorted_pairs[:k])
    print "{0} best features: {1}\n".format(k, k_best_features.keys())
    return k_best_features

best_features = get_k_best(my_dataset, my_features, 10)
print "K-best features:", best_features
my_features = [target_feature]+best_features.keys()


print "My Features:", my_features
data = featureFormat(my_dataset, my_features, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
def test_clf(grid_search, features, labels, parameters, iterations=100):
  precision, recall = [], []
  for iteration in range(iterations):
    features_train, features_test, labels_train, labels_test = train_test_split(features, labels, random_state=iteration)
    grid_search.fit(features_train, labels_train)
    predictions = grid_search.predict(features_test)
    precision = precision + [precision_score(labels_test, predictions)]
    recall = recall + [recall_score(labels_test, predictions)]
    if iteration % 10 == 0:
      sys.stdout.write('.')
  print '\nPrecision:', mean(precision)
  print 'Recall:', mean(recall)
  best_params = grid_search.best_estimator_.get_params()
  for param_name in sorted(parameters.keys()):
    print '%s=%r, ' % (param_name, best_params[param_name])

### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
parameters = {}
grid_search = GridSearchCV(clf, parameters)
print '\nGaussianNB:'
test_clf(grid_search, features, labels, parameters)

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# # Decision Tree
# from sklearn import tree
# clf = tree.DecisionTreeClassifier()
# #param grid from http://chrisstrelioff.ws/sandbox/2015/06/25/decision_trees_in_python_again_cross_validation.html
# parameters = {'criterion': ['gini', 'entropy'],'min_samples_split': [2, 10, 20],'max_depth': [None, 2, 5, 10],'min_samples_leaf': [1, 5, 10],'max_leaf_nodes': [None, 5, 10, 20]}
# grid_search = GridSearchCV(clf, parameters)
# print '\nDecisionTree:'
# test_clf(grid_search, features, labels, parameters)
#
# from sklearn.ensemble import AdaBoostClassifier
# clf = AdaBoostClassifier()
# parameters = {'n_estimators': [10, 20, 30, 40, 50],
#               'algorithm': ['SAMME', 'SAMME.R'],
#               'learning_rate': [.5,.8, 1, 1.2, 1.5]}
# grid_search = GridSearchCV(clf, parameters)
# print '\nAdaBoost:'
# test_clf(grid_search, features, labels, parameters)

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)




### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, my_features)