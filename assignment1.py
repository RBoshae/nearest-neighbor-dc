import sys
from math import sqrt
import math
import re
import timeit

pointRE=re.compile("(-?\\d+.?\\d*)\\s(-?\\d+.?\\d*)")

def dist(p1, p2):
    return sqrt(pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2))

# Run the divide-and-conquor nearest neighbor
def nearest_neighbor(points):

    # points.sort will implicitly assign sorted version of points.
    points.sort(key=lambda points:points[0])

    return nearest_neighbor_recursion(points)

# Brute force version of the nearest neighbor algorithm, O(n**2)
def brute_force_nearest_neighbor(points):
    min_distance = 0
    distance = 0

    # Select a point
    # Get the minimum distance of the selected point from all other points
    # Select the next point...do the same thing
    # return the minimum distance

    for selected_point in range(len(points)):
        other_point = selected_point +1
        while (other_point < len(points)):
            distance = dist(points[selected_point], points[other_point])

            if min_distance == 0:
                min_distance = distance;
            elif distance < min_distance:
                min_distance = distance

            other_point+=1
    return min_distance

def nearest_neighbor_recursion(points):
    min_distance=0
    left_distance=0
    right_distance=0
    window_distance=0
    x_midpoint = int(len(points)/2)
    L = points[:x_midpoint]
    R = points[x_midpoint:]
    R_New = []
    L_New = []


    if len(points) <= 3:              # divide and conquer until we reach out base case of just three points
       min_distance =  brute_force_nearest_neighbor(points)
       return min_distance
    else:
        left_distance = nearest_neighbor_recursion(L)
        right_distance = nearest_neighbor_recursion(R)

        if left_distance > right_distance:
            min_distance = right_distance
        else:
            min_distance = left_distance

   # This is where sliding window happens
   # Calculate left and right boundaries
    left_boundary = (x_midpoint - min_distance)
    right_boundary = (x_midpoint + min_distance)

    # Remove values outside of boundaries
    for i in range(len(L)):
        #if  i[0] < left_boundary:
        #    L.remove(i)
        if L[i][0] > left_boundary:
            L_New.append(L[i])
        # else:
        #    break
    for i in range(len(R)):
      #  if i[0] > right_boundary:
      #      R.remove(i) #Possible: create new list and append
        if R[i][0] < right_boundary:
            R_New.append(R[i])
        else:
            break
    window_points = L_New + R_New
    window_points.sort(key=lambda window_points:window_points[1])

    # Sliding Window Time
    window_distance = min_distance
    #print("Window Distance", window_distance)
    i = 0
    while (i < len(window_points)):
        if ((i + 7) < len(window_points)):
            window_distance = brute_force_nearest_neighbor(window_points[i:(i+7)])
        else:
            window_distance = brute_force_nearest_neighbor(window_points[i:])

        if window_distance < min_distance and window_distance != 0:
             min_distance = window_distance
        i= i+1

    '''
    # NEW CODE
    print("Sliding Window Starts Now")
    print("Current min: ", min_distance)
    tracker = 0
    window_boundary = (x_midpoint - left_boundary)
    print("wind_boundary: ", window_boundary)
    for i in range(len(L)):
    #    eye = i[1]

        for k in range(len(R)):
    #        kay = k[1]
    #        k = tracker
            # if R's y value is within the L's y boundary then check the distance
            if (R[k][1] <= (L[i][1] + window_boundary)) and (R[k][1] >= (L[i][1] - window_boundary)):
                window_distance = dist(R[k],L[i])
                # compare the distance of L y and R y
                if window_distance < min_distance:
                    min_distance = window_distance
            # if the R y valyes is above the boundary break
            elif R[k][1] > (L[i][1] + window_boundary) and k >0:
     #           tracker = k - 2
                break
            else:
                continue
    '''
    return min_distance

def read_file(filename):
    points=[]
    # File format
    # x1 y1
    # x2 y2
    # ...
    in_file=open(filename,'r')
    for line in in_file.readlines():
        line = line.strip()
        point_match=pointRE.match(line)
        if point_match:
            x = float(point_match.group(1))
            y = float(point_match.group(2))
            points.append((x,y))
   # print(points)
    return points

def main(filename,algorithm):
    algorithm=algorithm[1:]
    points=read_file(filename)
    if algorithm =='dc':
        start=timeit.default_timer()
        print("Divide and Conquer: ", nearest_neighbor(points))
        stop=timeit.default_timer()
        print (stop - start)
    if algorithm == 'bf':
        start=timeit.default_timer()
        print("Brute Force: ", brute_force_nearest_neighbor(points))
        stop=timeit.default_timer()
        print (stop - start)
    if algorithm == 'both':
        start=timeit.default_timer()
        print("Divide and Conquer: ", nearest_neighbor(points))
        stop=timeit.default_timer()
        print ("DC Time:", (stop - start))
        start=timeit.default_timer()
        print("Brute Force: ", brute_force_nearest_neighbor(points))
        stop=timeit.default_timer()
        print ("BF Time", (stop - start))
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python assignment1.py -<dc|bf|both> <input_file>")
        quit(1)
    if len(sys.argv[1]) < 2:
        print("python assignment1.py -<dc|bf|both> <input_file>")
        quit(1)
    main(sys.argv[2],sys.argv[1])
