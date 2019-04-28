"""
CS 6170 - Spring 2019
Nithin Chalapathi
"""
import numpy as np
from os import listdir
from os.path import isfile, join
import sys
import subprocess as sp
import re
import pickle
from matplotlib import pyplot as plt
from sklearn import manifold
PH_PKL_FILE="./dgms_conv2d1.pkl"

def run_hera(dgms, distance="geom_bottleneck", dim=0):
    try:
        distance_matrix = np.load("./data/hera_output/" + distance + "-" + str(dim) + ".npy")
        print("Found saved matrix for " + distance + " " + str(dim))
        return distance_matrix
    except IOError:
        print("Couldn't find matrix for " + distance + " " + str(dim) + ". Generating...")
    num = len(dgms)
    distance_matrix = np.zeros((num,num), dtype=np.float64)
    if distance == "geom_bottleneck":
        executable = distance + "/build/" + "bottleneck_dist"
    else:
        executable = "geom_matching/wasserstein/build/wasserstein_dist"
    hera_loc = "./hera/" + executable
    f1 = "tmp1.txt"
    f2 = "tmp2.txt"
    for counter1, b1 in enumerate(dgms):
        dgm1 = b1[dim]
        life_times = dgm1[:, 1] - dgm1[:, 0]
        idx_top_200 = np.argpartition(life_times, -200)[-200:] 
        np.savetxt(f1, dgm1[idx_top_200, :], delimiter=' ')
        print("Computing distance for %d dgm in dim %d" % (counter1, dim))
        for y in range(num-counter1):
            print(y)
            dgm2 = dgms[y][dim]
            life_times = dgm2[:, 1] - dgm2[:, 0]
            idx_top_200 = np.argpartition(life_times, -200)[-200:] 
            np.savetxt(f2, dgm2[idx_top_200, :], delimiter=' ')
            hera_cmd = [hera_loc, f1, f2]
            finished_hera = sp.run(hera_cmd, stdout=sp.PIPE, check=True,  encoding="utf-8")
            distance_matrix[counter1, y] = float(finished_hera.stdout.strip())
#Correcting float precision errors
    tmp = distance_matrix.T + distance_matrix 
    ind = np.arange(distance_matrix.shape[0])
    tmp[ind, ind] = distance_matrix[ind, ind]
    distance_matrix = tmp
    np.save("./data/hera_output/" + distance + "-" + str(dim), distance_matrix)
    return distance_matrix

def plot_mds(distance_matrix, description, fig, pos):
    fig.add_subplot(pos)
    embedding = manifold.MDS(n_components=2, dissimilarity='precomputed')
    transformed = embedding.fit_transform(distance_matrix)
    plt.scatter(transformed[:, 0], transformed[:, 1])
    plt.title(description)

def plot_tsne(distance_matrix, description, fig, pos):
    fig.add_subplot(pos)
    embedding = manifold.TSNE(n_components=2, metric='precomputed')
    transformed = embedding.fit_transform(distance_matrix)
    plt.scatter(transformed[:, 0], transformed[:, 1])
    plt.title(description)

def main():
    with open(PH_PKL_FILE, "rb") as d_file:
        dgms = pickle.load(d_file)
    fig_was = plt.figure(1)
    fig_was.suptitle("mixed4a_pre_relu Graphs Wasserstein")
    distance_matrix = run_hera(dgms, distance="wasserstein", dim=0)
    plot_mds(distance_matrix, "Wasserstein Distance in Dim 0 (MDS)", fig_was, 221)
    plot_tsne(distance_matrix, "Wasserstein Distance in Dim 0 (t-SNE)", fig_was, 222)

    distance_matrix = run_hera(dgms, distance="wasserstein", dim=1)
    plot_mds(distance_matrix, "Wasserstein Distance in Dim 1 (MDS)", fig_was, 223)
    plot_tsne(distance_matrix, "Wasserstein Distance in Dim 1 (t-SNE)", fig_was, 224)
#    plt.show()

    plt.close(fig_was)
    fig_bottle = plt.figure(2)
    fig_bottle.suptitle("Bottleneck Graphs")
    distance_matrix = run_hera(dgms, distance="geom_bottleneck", dim=0)
    plot_mds(distance_matrix, "Bottleneck Distance in Dim 0 (MDS)", fig_bottle, 221)
    plot_tsne(distance_matrix, "Bottleneck Distance in Dim 0 (t-SNE)", fig_bottle, 222)

    distance_matrix = run_hera(dgms, distance="geom_bottleneck", dim=1)
    plot_mds(distance_matrix, "Bottleneck Distance in Dim 1 (MDS)", fig_bottle, 223)
    plot_tsne(distance_matrix, "Bottleneck Distance in Dim 1 (t-SNE)", fig_bottle, 224)
    plt.show()

if __name__ == '__main__':
    main()
