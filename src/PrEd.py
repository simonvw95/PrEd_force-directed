# PrEd algorithm
import numpy as np
import networkx as nx
import math
import matplotlib.pyplot as plt
import os
import imageio
import time

from datetime import datetime
from scipy.spatial import Delaunay

def pred(G, pos, delta, gamma, iterations):
    
    folder_name = datetime.now()
    folder_name = folder_name.strftime('test_%d-%m_%H-%M')
    # hardcoded location of where to save images
    location = './ImPrEd/Results/' + folder_name + '/'
    
    counter = 0
    n = G.number_of_nodes()
    m = G.number_of_edges()
    nodes = list(G.nodes())
    edges = list(G.edges())
    
    # initialize the degrees of the zones
    zone_dicts = {0 : [0, 45], 1 : [45, 90], 2 : [90, 135], 3 : [135, 180], 4 : [180, 225], 5 : [225, 270], 6 : [270, 315], 7 : [315, 360]}
    
    start_time = time.time()
    
    while counter < iterations:
    
        if (counter > 0) and (counter % 20 == 0):
            curr_time = time.time()
            print(str(counter) + ' iterations took ' + str(round(curr_time - start_time, 2)) + ' seconds.')
        for i in range(n):
            R = {}
            # initialize the force results
            fr_vx = []
            fr_vy = []
            fa_vx = []
            fa_vy = []
            fe_vx = []
            fe_vy = []
            for j in range(n):
                if i != j:
                    # compute the node to node repulsion, all nodes to all other nodes
                    temp1, temp2 = node_node_repulsion(delta, pos[nodes[i]], pos[nodes[j]])
                    fr_vx.append(temp1)
                    fr_vy.append(temp2)
                    # compute the edge attraction, all nodes to nodes that it is connected to with an edge
                    if G.has_edge(nodes[i], nodes[j]):
                         temp1, temp2 = edge_attraction(delta, pos[nodes[i]], pos[nodes[j]])
                         fa_vx.append(temp1)
                         fa_vy.append(temp2)
                     
            for j in range(m):
                if nodes[i] != edges[j][0] and nodes[i] != edges[j][1]:
                    temp1, temp2 = node_edge_repulsion(gamma, pos[nodes[i]], pos[edges[j][0]], pos[edges[j][1]])
                    
                    fe_vx.append(temp1)
                    fe_vy.append(temp2)
                    
                    # initialize the radii if they do not have a value yet
                    if nodes[i] not in R:
                        R[nodes[i]] = [np.inf] * 8
                    if edges[j][0] not in R:
                        R[edges[j][0]] = [np.inf] * 8
                    if edges[j][1] not in R:
                        R[edges[j][1]] = [np.inf] * 8
                    
                    R = radii(v_dict = {nodes[i] : pos[nodes[i]]}, a_dict = {edges[j][0] : pos[edges[j][0]]}, b_dict = {edges[j][1] : pos[edges[j][1]]}, R = R, zone_dicts = zone_dicts)
                    
            # movement of the node in x and y direction   
            F_vx = sum(fr_vx) + sum(fa_vx) + sum(fe_vx)
            F_vy = sum(fr_vy) + sum(fa_vy) + sum(fe_vy)
            
            # get the length of the force vector
            F = eucl_distance(u = pos[nodes[i]], v = [pos[nodes[i]][0] + F_vx, pos[nodes[i]][1] + F_vy])
            
            # find the angle of the direction and its subsequent zone
            deg_F = np.rad2deg(np.arctan2(F_vy, F_vx))
            if deg_F < 0:
                deg_F += 360
            
            # find the specific zone of the force vector
            for zone in zone_dicts:
                if zone_dicts[zone][0] < deg_F < zone_dicts[zone][1]:
                    s = zone
                    
            # clamp the force vector to the maximal movement if the Force is bigger than the maximal movement
            max_move = R[nodes[i]][s]
            actual_move = F
            if F > max_move:
                actual_move = max_move
                
            # now we have the length of the force vector (the same or limited by the maximal movement)
            # compute x and y increases
            x_increase = np.cos(np.deg2rad(deg_F)) * actual_move
            y_increase = np.sin(np.deg2rad(deg_F)) * actual_move
            
            pos[nodes[i]][0] += x_increase
            pos[nodes[i]][1] += y_increase
            
            create_img(G, pos, location, img_name = 'cnt' + str(counter) + '_v' + str(nodes[i]))
            
        counter += 1
    # create a gif of all the produced images
    create_gif(location)
    
    
def single_pred_gui(G, pos, delta, gamma, i):
    
    n = G.number_of_nodes()
    m = G.number_of_edges()
    nodes = list(G.nodes())
    edges = list(G.edges())
    
    # initialize the degrees of the zones
    zone_dicts = {0 : [0, 45], 1 : [45, 90], 2 : [90, 135], 3 : [135, 180], 4 : [180, 225], 5 : [225, 270], 6 : [270, 315], 7 : [315, 360]}

    R = {}
    # initialize the force results
    fr_vx = []
    fr_vy = []
    fa_vx = []
    fa_vy = []
    fe_vx = []
    fe_vy = []
    for j in range(n):
        if i != j:
            # compute the node to node repulsion, all nodes to all other nodes
            temp1, temp2 = node_node_repulsion(delta, pos[nodes[i]], pos[nodes[j]])
            fr_vx.append(temp1)
            fr_vy.append(temp2)
            # compute the edge attraction, all nodes to nodes that it is connected to with an edge
            if G.has_edge(nodes[i], nodes[j]):
                 temp1, temp2 = edge_attraction(delta, pos[nodes[i]], pos[nodes[j]])
                 fa_vx.append(temp1)
                 fa_vy.append(temp2)
             
    for j in range(m):
        if nodes[i] != edges[j][0] and nodes[i] != edges[j][1]:
            temp1, temp2 = node_edge_repulsion(gamma, pos[nodes[i]], pos[edges[j][0]], pos[edges[j][1]])
            
            fe_vx.append(temp1)
            fe_vy.append(temp2)
            
            # initialize the radii if they do not have a value yet
            if nodes[i] not in R:
                R[nodes[i]] = [np.inf] * 8
            if edges[j][0] not in R:
                R[edges[j][0]] = [np.inf] * 8
            if edges[j][1] not in R:
                R[edges[j][1]] = [np.inf] * 8
            
            R = radii(v_dict = {nodes[i] : pos[nodes[i]]}, a_dict = {edges[j][0] : pos[edges[j][0]]}, b_dict = {edges[j][1] : pos[edges[j][1]]}, R = R, zone_dicts = zone_dicts)
            
    # movement of the node in x and y direction   
    F_vx = sum(fr_vx) + sum(fa_vx) + sum(fe_vx)
    F_vy = sum(fr_vy) + sum(fa_vy) + sum(fe_vy)
    
    # get the length of the force vector
    F = eucl_distance(u = pos[nodes[i]], v = [pos[nodes[i]][0] + F_vx, pos[nodes[i]][1] + F_vy])
    
    # find the angle of the direction and its subsequent zone
    deg_F = np.rad2deg(np.arctan2(F_vy, F_vx))
    if deg_F < 0:
        deg_F += 360
    
    # find the specific zone of the force vector
    for zone in zone_dicts:
        if zone_dicts[zone][0] < deg_F < zone_dicts[zone][1]:
            s = zone
            
    # clamp the force vector to the maximal movement if the Force is bigger than the maximal movement
    max_move = R[nodes[i]][s]
    actual_move = F
    if F > max_move:
        actual_move = max_move
        
    # now we have the length of the force vector (the same or limited by the maximal movement)
    # compute x and y increases
    x_increase = np.cos(np.deg2rad(deg_F)) * actual_move
    y_increase = np.sin(np.deg2rad(deg_F)) * actual_move
    
    new_pos = [pos[nodes[i]][0] + x_increase, pos[nodes[i]][1] + y_increase]

    return new_pos, pos[nodes[i]]
            
def node_node_repulsion(delta, u, v):

    p1 = (delta / eucl_distance(u, v)) ** 2 
    
    return [p1 * (u[0] - v[0]), p1 * (u[1] - v[1])]
    
def edge_attraction(delta, u, v):
    
    p1 = eucl_distance(u, v) / delta
    
    return [p1 * (v[0] - u[0]), p1 * (v[1] - u[1])]
    
def node_edge_repulsion(gamma, v, a, b):

    x_cross, slope_perp, b_perp = node_projection(v, a, b)
    
    # if x_cross is inbetween the x values of the edge then the projection is ON the edge, else not
    if (min(a[0], b[0]) < x_cross < max(a[0], b[0])) == False:
        return [0, 0]
    
    # get the y coordinate of the virtual node
    y_cross = (slope_perp * x_cross) + b_perp
    
    v_e = [x_cross, y_cross]
    
    # get the distance to the virtual node
    dist = eucl_distance(v, v_e)
    
    if dist >= gamma:
    
        p1 = ((gamma - dist) ** 2 / dist)
    
        return [p1 * (v[0] - v_e[0]), p1 * (v[1] - v_e[1])]
    else:
        return [0, 0]
        
def node_projection(v, a, b):
    
    # get the slope and starting point of the edge
    slope_ab = (b[1] - a[1]) / (b[0] - a[0])
    b_ab = b[1] - (slope_ab * b[0])
    
    # get the slope and starting point of the line perpendicular, that goes through v, to the edge
    slope_perp = (1 / slope_ab) * -1
    b_perp = v[1] - (slope_perp * v[0])
    
    # get the x coordinate where the perpendicular line crosses the edge line
    x_cross = (b_perp - b_ab) / (slope_ab - slope_perp)
    
    return x_cross, slope_perp, b_perp
    
def radii(v_dict, a_dict, b_dict, R, zone_dicts):

    v = list(v_dict.keys())[0]
    a = list(a_dict.keys())[0]
    b = list(b_dict.keys())[0]

    x_cross, slope_perp, b_perp = node_projection(v_dict[v], a_dict[a], b_dict[b])
    y_cross = (slope_perp * x_cross) + b_perp

    v_e = [x_cross, y_cross]
    
    # if the x coordinate of the virtual node is not inbetween the x values of the edge, then it is not on that edge
    if (min(a_dict[a][0], b_dict[b][0]) < x_cross < max(a_dict[a][0], b_dict[b][0])) == False:
     for j in range(8):
        R[v][j] = min(R[v][j], min(eucl_distance(a_dict[a], v_dict[v]), eucl_distance(b_dict[b], v_dict[v])) / 3)
        R[a][j] = min(R[a][j], eucl_distance(a_dict[a], v_dict[v]) / 3)
        R[b][j] = min(R[b][j], eucl_distance(b_dict[b], v_dict[v]) / 3)
    
    else:
        # find out in which direction the orthogonal line is
        deg_orth = np.rad2deg(np.arctan2(y_cross - v_dict[v][1], x_cross - v_dict[v][0]))
        if deg_orth < 0:
            deg_orth += 360
        
        # find which zone the orthogonal line is in
        for zone in zone_dicts:
            if zone_dicts[zone][0] < deg_orth < zone_dicts[zone][1]:
                s = zone
        
        js_v = list(range(-2, 3))
        js_ab = list(range(2, 7))
        
        # update the maximal movements of each zone
        for i in range(5):
            v_idx = (s - js_v[i]) % 8
            ab_idx = (s + js_ab[i]) % 8
            R[v][v_idx] = min(R[v][v_idx], eucl_distance(v_dict[v], v_e) / 3)
            R[a][ab_idx] = min(R[a][ab_idx], eucl_distance(v_dict[v], v_e) / 3)
            R[b][ab_idx] = min(R[b][ab_idx], eucl_distance(v_dict[v], v_e) / 3)
       
    return R
    

def eucl_distance(u, v):
        
    return np.sqrt((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2)
    
    
def create_img(G, pos, location, img_name):
    
    # if the directory doesn't exist yet then make it
    if not os.path.exists(location):
        os.mkdir(location)
        
        
    dpi = 96
    # draw then save the image
    plt.figure(figsize = (1000 / dpi, 1000 / dpi), dpi = dpi)
    nx.draw(G, pos = pos, with_labels = True)
    plt.savefig(location + img_name + '.png')
    plt.clf()
    plt.close('all')
    
    
def create_gif(location):
    
    files = os.listdir(location)
    
    start_time = time.time()
    images = []
    for i in files:
        if i[-4:] == '.png':
            images.append(imageio.imread(location + i))
            
    imageio.mimsave(location + 'progression.gif', images, format = 'GIF', fps = 2)
    
    curr_time = time.time()
    print('Making the gif took: ' + str(round(curr_time - start_time, 2)) + ' seconds')
    
    #for i in files:
        #if i[-4:] == '.png':
            #os.remove(location + i)
            
            
            
            
"""    
Function for generating a single planar graph using delaunay triangulation

Input
n:  number of nodes the planar graph will have

Output
graph dictionary: 
    nodes:  list of nodes
    nodes_coords:   dictionary of nodes and their x and y coordinates
    edges:  list of edges
    id_no:  unique identifier of the generated graph
"""
def generate_single_delaunay(n):
    
    # generate random x and y coordinates for a canvas of size 1000x1000
    random_coords = np.random.uniform((0, 0), (1000, 1000), (n, 2))
    
    # get the Delaunay triangulation
    # https://en.wikipedia.org/wiki/Delaunay_triangulation
    tri = Delaunay(random_coords)
    
    # initialize the edge list and get the created triangles
    edges = []
    triangles = tri.simplices
    
    for i in range(len(triangles)):
        
        # get all three edges from the triangles
        new_edge1 = [triangles[i][0], triangles[i][1]]
        new_edge2 = [triangles[i][1], triangles[i][2]]
        new_edge3 = [triangles[i][0], triangles[i][2]]
        
        # add the edges to the edge list (if isn't already in there due to the other triangles)
        if new_edge1 not in edges and list(reversed(new_edge1)) not in edges:
            edges.append(new_edge1)
        if new_edge2 not in edges and list(reversed(new_edge2)) not in edges:
            edges.append(new_edge2)
        if new_edge3 not in edges and list(reversed(new_edge3)) not in edges:
            edges.append(new_edge3)
    
    nodes = list(range(n))
    
    nodes_coords = {}
    for i in range(n):
        nodes_coords[nodes[i]] = [random_coords[i][0], random_coords[i][1]]
        
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    return {'G' : G, 'pos' : nodes_coords}
    