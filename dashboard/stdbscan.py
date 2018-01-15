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
    cluster_list = []
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
        
        # Jika objek belum bagian dari cluster
        if dataset[index][4] == unmarked:
            # mencari tetangga yang directly density reachable dari objek
            neighborhood = retrieveNeighbors(index, dataset, spatial_threshold, temporal_threshold)
            
            if len(neighborhood) < minPts:
                # tandai sebagai noise
                dataset[index][4] = noise
                
            else:
                # menemukan core object (construct a new cluster)
                cluster_label += 1
                
                cluster_list.append(cluster_label)

                # nyatakan objek sebagai bagian dari cluster
                dataset[index][4] = cluster_label
                
                # nyatakan semua tetangga dari core objek sebagai bagian dari cluster
                for neigh_index in neighborhood:
                    dataset[neigh_index][4] = cluster_label
                    
                
                    # masukan seluruh tetangga ke dalam Stack
                    # Stack digunakan untuk mencari tetangga yang density-reachable
                    stack.append(neigh_index)
                    
                
                # Mencari tetangga baru (density-reachable) dari tetangga (directly density reachable) objek
                while len(stack) > 0:
                    
                    current_point_index = stack.pop() # popping the last order stack
                    
                    # mencari tetangga yang density-reachable
                    new_neighborhood = retrieveNeighbors(current_point_index,
                                                         dataset,
                                                         spatial_threshold,
                                                         temporal_threshold)
                    
                    # jika jumlah tetangga baru tetangga (directly density reachable) objek lebih
                    # lebih besar dari MinPts
                    if len(new_neighborhood) >= minPts:

                        
                        for neigh_index in new_neighborhood:
                            
                            neigh_cluster = dataset[neigh_index][4]
                            if neigh_cluster not in cluster_list:
                                neigh_ipm = dataset[neigh_index][3]
                                
                                ipm_cluster = dataset[np.where(dataset[:,4] == cluster_label) ,3]
                                
                                # Jika objek dari tetangga baru bukan noise atau
                                # belum bagian dari cluster
                                if (neigh_cluster != noise or \
                                    neigh_cluster == unmarked) and \
                                    abs(standardizing(neigh_ipm, ipm_cluster)) <= de:
                                    
                                    # menemukan density-reachable

                                    # nyatakan sebagai bagian dari cluster_label
                                    dataset[neigh_index][4] = cluster_label

                                    # masukan objek ke dalam stack 
                                    # untuk mencari density-reachbale lagi
                                    stack.append(neigh_index)

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