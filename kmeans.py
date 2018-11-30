'''
K-Means cluster with seeds dataset

choose k data points to act as centroid
until the changes for centroids is small:
    calculate distance between a datapoint and centroid
    assign the datapoint to cluster with smallest distance

    check to see that each cluster has at least one datapoint
for each cluster, calculate a new mean to get new centroid
if there is a new centroid, do above steps

'''

from random import randint
from copy import deepcopy
from math import sqrt
from operator import itemgetter
from functools import partial

##### HELPER FUNCTIONS #####
#calcuate distance between A(x1, y1, z1) and B(x1, y1, z1) using Pythagorean theorem
def get_distance(point1, point2):
    x = (point1[0] - point2[0])*(point1[0] - point2[0])
    y = (point1[1] - point2[1])*(point1[1] - point2[1])
    z = (point1[2] - point2[2])*(point1[2] - point2[2])
    return sqrt(x+y+z) #distance


#given a cluster, find the new centroid, by finding the average in cluster
def get_centroid_avg(data):
    #avg = sum(data)/len(data)
    #return min(data, key=lambda x:abs(x-avg))
    sum_of_points = [sum(x) for x in zip(*data)]
    return [x/len(data) for x in sum_of_points] #average


#given two lists of centroids, return whether they are the same
def are_equal(current, new):
    if current == new:
        return True
    return False


#measure Euclidean distance between two points
def distance_squared(x, y):
    return (x[0] - y[0])**2 + (x[1] - y[1])**2 + (x[2] - y[2])**2


#given the average of a cluster, find the closest data point to that average
def get_new_centroid(avg):
    return min(data_points, key=partial(distance_squared, avg))


#if a cluster doesn't have any points, give it one from each other cluster
def check_cluster_population(clusters, centroid_points):
    print("Length of cluster 0: ", len(clusters[0]))
    print("Length of cluster 1: ", len(clusters[1]))
    print("Length of cluster 2: ", len(clusters[2]))
    if len(clusters[0]) == 0:
        if len(clusters[1]) != 0:
            random_point = randint(0, len(clusters[1]))
            clusters[0].append(clusters[0].pop(random_point))
        if len(clusters[2]) != 0:
            random_point = randint(0, len(clusters[2]))
            clusters[0].append(clusters[2].pop(random_point))
    elif len(clusters[1]) == 0:
        if len(clusters[2]) != 0:
            random_point = randint(0, len(clusters[2]))
            clusters[1].append(clusters[2].pop(random_point))
        if len(clusters[0]) != 0:
            random_point = randint(0, len(clusters[0]))
            clusters[1].append(clusters[0].pop(random_point))
    elif len(clusters[2]) == 0:
        if len(clusters[0]) != 0:
            random_point = randint(0, len(clusters[0]))
            clusters[2].append(clusters[0].pop(random_point))
        if len(clusters[1]) != 0:
            random_point = randint(0, len(clusters[1]))
            clusters[2].append(clusters[1].pop(random_point))


#given centroids, compute the clusters and return them
def create_clusters(centroids):
    centroid_points = [[], [], []]  # array of points per cluster
    for p in data_points:
        distances = []
        for c in centroids:
            distances.append(get_distance(p, c)) #distance to centroids
        idx = min(enumerate(distances), key=itemgetter(1))[0]
        centroid_points[idx].append(p)
    return centroid_points
##### END HELPER FUNCTIONS #####


##### MAIN PROGRAM ######


#read in dataset
data_points = []
with open("seeds_dataset.txt") as file:
    for line in file:
        values = [float(n) for n in line.split()] #array of attributes for each point
        points = values[2:5] #only want 3rd, 4th, 5th attribute
        data_points.append(points) #array of data points

#randomly pick three datapoints to be centroids and take them out of dataset
centroids = []
for k in range(3):
    num = randint(0, 209) #210 datapoints
    print("Centroid: ", num, data_points[num])
    centroids.append(data_points[num])
print()

#main loop of k-means:
#while new centroids are being found, keep assigning points to clusters
#and keep finding new centroids
#stopping condition: new centroids are same as last centroids


#for each point, calculate the distance into a list
#find the min distance, and put that datapoint into the centroid's list
convergence = False
i = 0
while convergence != True:
    print()
    print("ITERATION ", i)
    print("Centroids are: ")
    for c in centroids:
        print(c)
    print("Creating clusters")
    clusters = create_clusters(centroids) #create initial centroid and clusters
    check_cluster_population(clusters, centroids)

    #for every point in every cluster, find the average of the cluster
    #find the datapoint closest to the average. that will be the new centroid
    new_centroids = []
    for c in clusters:
        centroid_avg = get_centroid_avg(c)
        new_centroid = get_new_centroid(centroid_avg)
        new_centroids.append(new_centroid)

    print("New centroids are: ")
    for n in new_centroids:
        print(n)

    convergence = are_equal(centroids, new_centroids) #check for convergence
    if convergence == True:
        print("Convergence found")
        print("Old centroids are: ", centroids)
        print("New centroids are ", new_centroids)
        print("Number of iterations: ", i)
        break

    i+=1
    centroids = new_centroids
    create_clusters(centroids)
