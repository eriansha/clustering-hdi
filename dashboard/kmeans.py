import numpy as np
import math

def kmeans(dataset, k, epsilon=0):
 
    # mengambil jumlah baris dan kolom di data
    num_instances, num_features = dataset.shape
 
    # inisiasi centroid sejumlah k secara acak
    centroids = dataset[np.random.randint(0, num_instances - 1, size=k)]
    centroids_old = np.zeros(centroids.shape)
    # array untuk menampung label dari hasil clustering
    cluster_label = np.zeros((num_instances, 1))

    norm = euclidian(centroids, centroids_old)
    # iteration = 0
    while norm > epsilon:
        # iteration += 1
        norm = euclidian(centroids, centroids_old)
        centroids_old = centroids
        # untuk setiap record di dataset
        for index_instance, instance in enumerate(dataset):
            # mendefinisikan jarak vektor sejumlah k
            dist_vec = np.zeros((k, 1))
            # untuk setiap centroid
            for index_centroid, centroid in enumerate(centroids):
                # hitung jarak antara record dan centroid
                dist_vec[index_centroid] = euclidian(centroid,
                                                        instance)

            # mencari jarak yang terdekat dari k-centroid
            # nyatakan sebagai cluster dari centroid tersebut
            cluster_label[index_instance, 0] = np.argmin(dist_vec)

        tmp_centroids = np.zeros((k, num_features))

        # untuk setiap cluster dari centroids
        for index in range(len(centroids)):
            # mengambil semua point yang dinyatakan sebagai cluster
            instances_close = [i for i in range(len(cluster_label)) if cluster_label[i] == index]
            # mencari nilai rata-rata dari poin tersebut untuk membuat centroid baru
            centroid = np.mean(dataset[instances_close], axis=0)
            # tampungan untuk centroid baru
            tmp_centroids[index, :] = centroid

        # tampungan menjadi centroid-centroid baru
        centroids = tmp_centroids

    return cluster_label

def euclidian(a, b):
    return math.sqrt(np.power(a-b, 2).sum())
