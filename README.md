# cluster_every_combo
Runs through a database of features, and clusters every single combination. amount_of_combinations parameter gives you the option to tell the algorithm how many features you want to cluster at a time. I used this algo for I job I was working on where the data had labels, but the labels were wrong a lot of the time. I clustered every single combination, then calculated the probaility of a cluster having a the deisred label I was looking for. I then reenginered the labels where if a cluster had above a 70% chance of being the desired label I was looking for, every single trainig example within that cluster would now have that specific label. This is just one application of how this algo can be useful. 

PARAMETERS:
1. required parameter - db: A pandas dataframe. Must only consist of features. If there is a y_lables column, see y_lables parameter
2. optional parameter - amount_of_combinations: number of combinations to combine at one time. READ DOCUMENTATIONN FOR FURTHER CLARIFICATION
3. optional parameter - clustering_algo: the clustering algotihm to use. Default ia DBSCAN. The other option is 'kmeans'.
4. optional parameter - y_labels: Whether or not the database has a y_labels column or not. Default set to False

Objects that algorith returns:
1. self.db - the original database that was used for the algorithm

2. self.x - the original database that was used for the algorithm with the features reegnineered into a standard normal distributon

3. self.matrix_of_cooresponding_labels - returns the combinations of features in a list of list. EX: [['feature 1', 'feature 2'], ['feature 1', 'feature 3'], ['feature 2', 'feature 3'] ]

4. self.reengineered_labels_matrix - A matrix of shape 2. Example shape:[3, 100], where the first indice, 3 represents the specific cluster, and the second indice, 100, represents the training example. So for instance, value one for the first indice would corelate to the first cluster in our self.matrix_of_cooresponding_labels object, which is ['feature 1', 'feature 2'], and a value of 1 in the second indice would mean its the 1st training example, so it would map to the 1st  trainig examples in self.db and self.x

These are really the only important objects that you would need to call for this algorithm. You can read through the code, which is well documented if you'd like to see the other objects that are created for this algo, or to get a better feel for how the algo works. Also, to see how the algorithm counts through the indice's, creating an array of features with every possible combination, which is saved as the self.matrix_of_combinations object, check out this image, ![input](https://github.com/bnicholl/cluster_every_combo/blob/master/how_algo_counts.jpeg)
