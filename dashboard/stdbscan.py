import numpy as np
import math

def st_dbscan(dataset, spatial_threshold, temporal_threshold, minPts, de):
    """
    Python st-dbscan implementation.
    INPUTS:
        df={o1,o2,...,on} Set of objects
        spatial_threshold = Maximum geographical coordinate (spatial) distance
        value
        temporal_threshold = Maximum non-spatial distance value
        minPts = Minimun number of points within Eps1 and Eps2 distance
        de = threshold value to be included in a cluster
    OUTPUT:
        C = {c1,c2,...,ck} Set of clusters
    """
    cluster_label = 0
    noise = -1
    unmarked = 7777
    stack = []
    
    # initialize each point with unmarked in 4th index column    
    cluster_column = []
    for i in range(dataset.shape[0]):
        cluster_column.append(unmarked)

    cluster_vector = np.array([cluster_column]).T
    dataset = np.concatenate((dataset, cluster_vector), axis=1)
    
    # for each point in dataset
    for index in range(dataset.shape[0]):
        # <Debugging>
        # print('--------------------------------indeksfloat {} --------------------------------'.format(index))
        if dataset[index][4] == unmarked:
            neighborhood = retrieveNeighbors(index, dataset, spatial_threshold, temporal_threshold)
            
            # <Debugging>
            # print("jumlah tetangga di indeks ke-{} adalah: {}".format(index, len(neighborhood)))
            # print("tetangganya yaitu, {}".format(neighborhood))
            
            if len(neighborhood) < minPts:
                # mark point[index] as noise
                dataset[index][4] = noise
                # print("indeks ke-{} adalah noise".format(index))
                
            else:
                # find a core point (construct a new cluster)
                # print('masuk pemberian cluster..........................')
                
                cluster_label += 1
                # print('>>>> cluster {} telah dibuat'.format(cluster_label))
                
                dataset[index][4] = cluster_label
                # print("Indeks {} adalah core point".format(index))
                
                # centre_cluster.append(index)
                
                # assign core's label to its neighborhood
                for neigh_index in neighborhood:
                    dataset[neigh_index][4] = cluster_label
                    # print("tetangga indeks ke-{} adalah cluster ke-{} dan segera masuk ke stack".format(neigh_index ,cluster_label))
                
                    # append all neighborhood to stack
                    stack.append(neigh_index)
                    
                
                # print('stack: {}'.format(stack))
                
                # find new neighbors from core point neighborhood
                while len(stack) > 0:
                    # print("Mencari tetangga baru dari tetangga core point ke-{}".format(index))
                    
                    current_point_index = stack.pop() # popping the last order stack
                    
                    # print("mengeluarkan indeks {} dari stack".format(current_point_index))
                    new_neighborhood = retrieveNeighbors(current_point_index,
                                                         dataset,
                                                         spatial_threshold,
                                                         temporal_threshold)
                    
                    # print('Jumlah tetangga baru ada {}, yaitu {}'.format(len(new_neighborhood), new_neighborhood))
                    
                    # current_point is a new core
                    if len(new_neighborhood) >= minPts:
                        # print("mencari core point baru...............")
                        
                        for neigh_index in new_neighborhood:
                            # print("-----Indeks {}-----".format(neigh_index))
                            
                            neigh_cluster = dataset[neigh_index][4]
                            # print("nilai cluster: {}".format(neigh_cluster))
                            
                            neigh_ipm = dataset[neigh_index][3]
                            # print('neigh_ipm : {}'.format(neigh_ipm))
                            
                            ipm_cluster = dataset[np.where(dataset[:,4] == cluster_label) ,3]
                            # alternative >> np.sum(ipm_cluster)/ipm_cluster.shape[0]
                            
                            # print('ipm_cluster: {}'.format(len(ipm_cluster)))
                            # print('actual neig_cluster: {}'.format(neig_cluster))
                            
                            #print('ipm_cluster mean: {}'.format(ipm_cluster.mean()))
                            #print('ipm_cluster std: {}'.format(ipm_cluster.std()))
                            #print('standardizing difference (absolute): {}'.format(abs(standardizing(neigh_ipm, ipm_cluster))))
                            
                            # if object not marked as noise or it's not in a cluster
                            if all([neigh_cluster!= noise , neigh_cluster == unmarked]) and \
                                abs(standardizing(neigh_ipm, ipm_cluster)) <= de:
                                # abs((neigh_ipm - ipm_cluster.mean())) <= de:
                                
                                dataset[neigh_index][4] = cluster_label
                                #print("Indeks {} adalah core point baru".format(neigh_index))
                                
#                                 centre_cluster.pop()
#                                 centre_cluster.append(neigh_index)
                                
                                #if new_neigh_index not in stack:
                                stack.append(neigh_index)
#                             else:
#                                 #print("Indeks {} bukan core point baru".format(neigh_index))
#                                 # print("")
#                     else:
#                         # <Debugging>
#                         #print("Tidak menemukan jumlah tetangga yang melebihi minPts")
                                
#         else:
#             #print("indeks {} berada di cluster {}".format(index, cluster_label))
           
    #print('centre cluster: {}'.format(centre_cluster))
    return dataset

def retrieveNeighbors(index_center, dataset, spatial_threshold, temporal_threshold):
    
    neighborhood = []
    
    spatial_data = dataset[:,0:2]
    temporal_data = dataset[:,2]
    
    spatialNeigh = FindNeighborhood(index_center, spatial_data, spatial_threshold)
    temporalNeigh = FindNeighborhood(index_center, temporal_data, temporal_threshold)
    
    # find intersaction between spatial neighborhood and temporal neighborhood
    neighborhood = list(set(spatialNeigh) & set(temporalNeigh))
    
    return neighborhood


def FindNeighborhood(index_center, candidates, threshold):
    neigh_dist = []
    distance = 0
    for index_candidate in range(candidates.shape[0]):
        if index_candidate == index_center:
            continue
        else:
            x1 = candidates[index_center]
            x2 = candidates[index_candidate]
            # calculate euclidean distance for each row
            distance = math.sqrt(np.power(x1-x2,2).sum())#math.sqrt(np.sum((test1 - test2) ** 2))
            if distance <= threshold:
                neigh_dist.append(index_candidate)
        
    return neigh_dist


def standardizing(neigh_ipm, ipm_cluster):
    return (neigh_ipm - ipm_cluster.mean()) / ipm_cluster.std(ddof=0)