def kmeans(dataset, k, epsilon=0):
    
    history_centroids = []
 
    num_instances, num_features = dataset.shape
    centroids = dataset[np.random.randint(0, num_instances - 1, size=k)]
    history_centroids.append(centroids)
    centroids_old = np.zeros(centroids.shape)
    belongs_to = np.zeros((num_instances, 1))
    norm = euclidian(centroids, centroids_old)
    iteration = 0

    while norm > epsilon:
        iteration += 1
        norm = euclidian(centroids, centroids_old)
        centroids_old = centroids
        for index_instance, instance in enumerate(dataset):
            dist_vec = np.zeros((k, 1))
            for index_centroid, centroid in enumerate(centroids):
                dist_vec[index_centroid] = euclidian(centroid,
                                                        instance)

            belongs_to[index_instance, 0] = np.argmin(dist_vec)

        tmp_centroids = np.zeros((k, num_features))

        for index in range(len(centroids)):
            instances_close = [i for i in range(len(belongs_to)) if belongs_to[i] == index]
            centroid = np.mean(dataset[instances_close], axis=0)
            # prototype = dataset[np.random.randint(0, num_instances, size=1)[0]]
            tmp_centroids[index, :] = centroid

        centroids = tmp_centroids

        history_centroids.append(tmp_centroids)

    return centroids, history_centroids, belongs_to

def euclidian(a, b):
    return math.sqrt(np.power(a, b).sum())