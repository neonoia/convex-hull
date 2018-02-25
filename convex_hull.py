# Implementing Quick Hull algorithm to find convex hull
# Hafizh Budiman, February 22nd 2018
# Informatics Engineering, Bandung Institute of Technology, 2018

import numpy as np 
import matplotlib.pyplot as plt

def divide_conquer(points):
    
    # initialize hull with leftmost and rightmost point
    # get the x min, and x max from the randomly generated points
    min_x = float('inf')
    max_x = 0
    min_y = 0
    max_y = 0

    for x,y in points:
        if x < min_x:
            min_x = x
            min_y = y
        if x > max_x:
            max_x = x
            max_y = y

    min, max = [min_x,min_y], [max_x,max_y]

    # initial division
    hullpts = quickhull(points, min, max)
    hullpts = hullpts + quickhull(points, max, min)

    return hullpts 

'''
    Does the sorting for the quick hull sorting algorithm
'''
def quickhull(points, min, max):
    
    # get all points which situated in the 
    # left part of the newly formed triangle
    left_points = get_left_points(min, max, points)

    # set the furthest point from the line as a new hull point
    hull_point = max_distance_point(min, max, left_points)

    if len(hull_point) < 1: # return the point max as hull points
        return [max]

    # divide recursively
    hullPts = quickhull(left_points, min, hull_point)
    hullPts = hullPts + quickhull(left_points, hull_point, max)

    return hullPts

'''
    Returns all points that a LEFT of a line
    that joins the point p1 and p2.
'''
def get_left_points(p1, p2, points):
    pts = []

    for pt in points:
        val = ((p2[1]-p1[1])*(pt[0]-p2[0]) - (p2[0]-p1[0])*(pt[1]-p2[1]))
        if (val != 0) and (val < 0):
            pts.append(pt)

    return pts

'''
    Returns the furthest point from 
    a line joining the p1 and p2.
'''
def max_distance_point(p1, p2, points):
    max_dist = 0
    max_point = []

    for point in points:
        if (point[0]!=p1[0] or point[1]!=p1[1]) and (point[1]!=p2[1] or point[0]!=p2[0]):
            dist = line_distance(p1, p2, point)
            if dist > max_dist:
                max_dist = dist
                max_point = point

    return max_point

'''
    Returns a value proportional to the distance
    between the point pt and the line joining p1 and p2.
'''
def line_distance(p1, p2, pts): # pt is the point
    x1, y1 = p1
    x2, y2 = p2
    x0, y0 = pts
    top = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    bottom = ((y2 - y1)**2 + (x2 - x1) ** 2) ** 0.5
    result = top / bottom
    return result

'''
    Prints the hull results and draw it
'''
def draw(points):

    if (len(points) < 3):
        return

    quick_hull = divide_conquer(points)

    # print convex hull points result
    print "\nQuick hull result:"
    for x in quick_hull: print x

    # draw convex hull result using matplotlib.pyplot
    n = len(quick_hull)
    for i in range(n):
        plt.plot([quick_hull[i][0], quick_hull[(i+1)%n][0]], [quick_hull[i][1],quick_hull[(i+1)%n][1]],'k-',lw=2)
        plt.pause(0.08)

    return

def main():
    # Entering number of points
    n = input("Enter the value for n: ")

    points = np.random.randint(100,size=(n,2))
    points[points[:0].argsort()] # sorting points

    print ("Randomly Generated Points: \n")
    for x in points:
        print x
        plt.scatter(x[0],x[1])
    
    draw(points.tolist())

    plt.show()

if __name__=="__main__":
    main()