# cluster_every_combo
Runs through a database of features, and clusters every single combination. amount_of_combinations parameter gives you the option to tell the algorithm how many features you want to cluster at a time.

PARAMETERS:
1. required parameter - db: A pandas dataframe. Must only consist of features. If there is a y_lables column, see y_lables parameter
2. optional parameter - amount_of_combinations: number of combinations to combine at one time. READ DOCUMENTATIONN FOR FURTHER CLARIFICATION
3. optional parameter - clustering_algo: the clustering algotihm to use. Default ia DBSCAN. The other option is 'kmeans'.
4. optional parameter - y_labels: Whether or not the database has a y_labels column or not. Default set to False

Objects that algorith returns:
1. self.matrix_of_cooresponding_labels - returns the combinations of features in a list of list. EX:[['running_status', 'drive_current_monitor'],
 ['running_status', 'gas_lock_maximum_cycles'],
 ['running_status', 'fluid_over_pump_monitor'] ]
