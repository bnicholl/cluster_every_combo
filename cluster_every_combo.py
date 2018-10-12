import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler
import pandas as pd

"""required parameter - db: A pandas dataframe. Must only consist of features. If there is a y_lables column, see y_lables parameter"""
"""optional parameter - amount_of_combinations: number of combinations to combine at one time. READ DOCUMENTATIONN FOR FURTHER CLARIFICATION"""
"""optional parameter - clustering_algo: the clustering algotihm to use. Default ia DBSCAN. The other option is 'kmeans'.""" 
"""optional parameter - y_labels: Whether or not the database has a y_labels column or not. Default set to False""" 

class run_cluster_of_every_combo():
    
    def __init__(self, db, amount_of_combinations = 1, clustering_algo = 'DBSCAN', y_labels = False):
        self.db = db
        self.amount_of_combinations = amount_of_combinations
        self.clustering_algo = clustering_algo
        self.y_labels = y_labels
        
        self.seperate_x_and_y()
           
  
    """this seperates our x variables and y labels from our pandas database, and puts our x features into a standard normal distribution"""
    def seperate_x_and_y(self):
        
        """shuffles the entire database"""
        self.db = shuffle(self.db)
        
        """save the feature names """
        self.feature_names = [i for i in self.db]
        
        self.db = np.array(self.db)
        
        if self.y_labels == True:
            """get the labels from our array"""
            self.y = self.db.T[-1]
            """delete the last column in the array, which are the labels"""
            self.db = np.delete(self.db, -1, axis=1)
            """remove the last column name, which is 'labels' """
            self.feature_names = self.feature_names[:-1]
               
        standard_scale = StandardScaler(with_mean = False)
        self.x = standard_scale.fit_transform(self.db)
    
        self.break_down_by_features() 
        
        
    def break_down_by_features(self):
        """hold the values of every possible combinations. Takes example shape [1326  3198  2], where 1326 represent every possible combination,
        3198 represents every training example, and 2 represents number of feature in the combinations(amount_of_combinations = 2) """
        self.matrix_of_combinations = []
        """holds the cooresponding combinations of labels(1st index in self.matrix_of_combinations) """
        self.matrix_of_cooresponding_labels = []
        
        indice_to_change = -1
        add_one = 0
        combinations = self.x.shape[1]  
        
        """EX for 3 features at a time: [0 0 0]"""
        dimensions_indice_vector = [0] *  self.amount_of_combinations
        
        """EX: turns dimensions_indice_vector from [0 0 0] to [0 1 2]"""
        for e,i in enumerate(dimensions_indice_vector):
            dimensions_indice_vector[e] = add_one
            add_one += 1
        
        while True:
            individual_combination = []
            cooresponding_labels = []
            """this loop appends each individual dimension to the above list. EX. if theres 3 dimensions per cluster,
            this loop appends the three dimensions that are in the 3 element vector dimensions_indice_vector """
            for i in dimensions_indice_vector:
                #print(i)
                """appends an entire feature vector one at a time"""
                individual_combination.append(self.x.T[i].tolist())
                """appends the cooresponding feature name"""
                cooresponding_labels.append(self.feature_names[i])
            
            
            self.matrix_of_cooresponding_labels.append(cooresponding_labels)
            """append our individual combonations to our list that will hold every single combination"""    
            self.matrix_of_combinations.append(individual_combination)  
            
            """add one to the last element in dimensions_indice_vector"""
            dimensions_indice_vector[-1] += 1
            
            
            """if the last dimension_indice_vector is equal to our to our total amount of features(AKA combinations)"""
            if dimensions_indice_vector[-1] == combinations:
                """subtract one from the last element so our statements below work correctly"""
                dimensions_indice_vector[-1] -= 1
                
                enter = True
                index = indice_to_change * 1
                while index < -1:

                    if dimensions_indice_vector[index] - dimensions_indice_vector[index + 1] == -1:
                        index += 1    
                    
                    elif dimensions_indice_vector[index] - dimensions_indice_vector[index + 1] != -1:
                        loop_in_reverse = -1
                        
                        """EX: of loop when it hits else statement:  V[0 2 3 6 7] would turn into V[0 2 4 5 6]"""
                        while True:
                            if dimensions_indice_vector[loop_in_reverse] - dimensions_indice_vector[loop_in_reverse - 1] == 1:
                                loop_in_reverse -= 1
                            else:
                                 """EX: V[0 2 3 6 7] would turn into V[0 2 4 6 7]"""
                                 dimensions_indice_vector[loop_in_reverse - 1] += 1
                                 """EX: of loop when it hits else statement:  V[0 2 4 6 7] would turn into V[0 2 4 5 6]. We add one because
                                 the first iteration, the value of e is 0"""
                                 for e,i in enumerate(dimensions_indice_vector[loop_in_reverse:]):
                                     dimensions_indice_vector[loop_in_reverse + e] = dimensions_indice_vector[loop_in_reverse- 1] + 1 + e
                                 
                                 break
                        
                        enter = False
                        break                            
                
                """this below code is when we change actual indices (look at paper)"""    
                if enter == True:
                    """move the indice to change one spot left"""
                    print(dimensions_indice_vector)
                    print(indice_to_change)
                    indice_to_change -= 1
                    """checks if the indice that we just changed actually exist. If it doesn't, we go to the next function"""
                    if abs(indice_to_change) > len(dimensions_indice_vector):
                        self.matrix_of_combinations = np.array(self.matrix_of_combinations)
                        self.matrix_of_combinations = self.matrix_of_combinations.transpose((0,2,1))
                        self.cluster_label()
                        return self.matrix_of_combinations
                    
                    """add one to the specific indice to change. EX for chainge 3rd indice: V[0 1 2 6 7] now equals [0 1 3 6 7]"""
                    dimensions_indice_vector[indice_to_change] += 1
                    """loops through and changes vector. EX:  V[0 1 3 6 7]  now equals  [0 1 3 4 5]. We add one because
                    the first iteration, the value of e is 0"""
                    for e,i in enumerate(dimensions_indice_vector[indice_to_change:]):
                        dimensions_indice_vector[indice_to_change + e] = dimensions_indice_vector[indice_to_change] + 1 + e
                    
                   
                                                        
    """this runs our broken up features created in break_down_by_features function, and obtains
    labels for all of them via a clustering algorithm. An outoput shape EX: [14675, 3198], where 14675 is possible combiination
    of the features, and 3198 are the individual training examples. """
    def cluster_label(self, number_of_clusters = 8):
        self.number_of_clusters = number_of_clusters
        self.reengineered_labels_matrix = []
        
        for cluster_plot in self.matrix_of_combinations:
            if self.clustering_algo == 'DBSCAN':
                clustering_algo = DBSCAN(eps = 0.1, min_samples = 4).fit(cluster_plot)
            elif self.clustering_algo == 'kmeans':
                clustering_algo = KMeans(n_clusters = self.number_of_clusters, random_state=0).fit(cluster_plot)
            reengineered_labels = clustering_algo.labels_.tolist()
            self.reengineered_labels_matrix.append(reengineered_labels)
        
        self.reengineered_labels_matrix = np.array(self.reengineered_labels_matrix)
        
        
a = run_cluster_of_every_combo(db)
