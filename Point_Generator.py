#Author : SAI BALACHANDAR V

import numpy as np
import random
import csv
import itertools
def point_generator(*args):
    """
    Generates random points within a closed polygon defined by the given vertices.
    Usage:
        point_generator([0, 0],[2, 0],[1, 1.25],[0, 2],[2, 3])
        
    Parameters:
        1) *args : list of list or tuple
        2) Coordinates of the polygon vertices. A minimum of three points is required to form a closed shape.
        3) verticesmus be 2 dimentional
    Returns:
        A csv of containging points located inside the polygon.
    """

    temp_list = [np.array(i) for i in args]
    triangles = []
    for combos in itertools.combinations(temp_list,3):
        Var_x,Var_y,Var_z = combos
        # Check orientation
        AB = Var_y - Var_x
        BC = Var_z - Var_y
        cross_z = AB[0]*BC[1] - AB[1]*BC[0]
        if cross_z > 0:
            triangles.append([Var_x ,Var_y ,Var_z ])  # --- > Check if the selected set forms a concave shape; if so, append it to 'triangles'.
                                                      # --- >  If not, skip to the next iteration.
                                                      # --- >  Eventually, convex triangles will be separated and sent to the point generation code.

        else :
            continue
    while True:
        # Generate point inside triangle
        tris = random.choice(triangles)
        alpha = random.random()
        beta = random.random()
        if alpha + beta > 1:
            alpha = 1 - alpha
            beta = 1 - beta
        gamma = 1 - alpha - beta
        Var_x,Var_y,Var_z = tris
        generated_point = Var_x*alpha + Var_y*beta + Var_z*gamma
        yield generated_point

points  =  point_generator([0, 0],[2, 0],[1, 1.25],[0, 2],[2, 3]) # input vertices

'''
below code snippet will call  the above function 10K times and generate points inside the given vertices randomly each time
and write the generated points as CSV file.
'''
file_name = "Generated_points.csv"
with open(file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    for _ in range(10000):
        tmp = next(points)
        tmp = [tmp.tolist()]
        writer.writerows(tmp)
        del tmp       
print("Data has been written") 



