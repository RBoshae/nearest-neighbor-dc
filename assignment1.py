import sys
from math import sqrt
import math
import re
import timeit

pointRE=re.compile("(-?\\d+.?\\d*)\\s(-?\\d+.?\\d*)")

# Perfect
def dist(p1, p2):
    return sqrt(pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2))

# Run the divide-and-conquor nearest neighbor
# Perfect
def nearest_neighbor(points):

    # Sort the points by x-values.
    points.sort(key=lambda points:points[0])

    return nearest_neighbor_recursion(points)

# Perfect
# Brute force version of the nearest neighbor algorithm, O(n**2)
def brute_force_nearest_neighbor(points):
    min_distance = 0
    distance = 0

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
    window_distance=0
    R_New = []
    L_New = []

    # If points is contains more than three points we want to use recurstion to divide-and-conquor again
    if len(points) > 3:
        # Find the midpoint along the x-axis
        x_midpoint = math.ceil(len(points)/2)

        # Divide points into to regions, L and R
        L = points[:x_midpoint]
        R = points[x_midpoint:]

        L_min_distance = nearest_neighbor_recursion(L)
        R_min_distance = nearest_neighbor_recursion(R)

        if L_min_distance > R_min_distance:
            min_distance = R_min_distance
        else:
            min_distance = L_min_distance
    # else if the number of points is less than three calc the distance
    else:
       min_distance =  brute_force_nearest_neighbor(points)
       return min_distance

   # Sliding Window
   # Calculate left and right boundaries
    L_boundary = (x_midpoint - min_distance)
    R_boundary = (x_midpoint + min_distance)

    # Create a new R and L with only points within the window
    for i in range(len(L)-1,0,-1):
        if L[i][0] >= L_boundary:
            L_New.append(L[i])
        else:
            break

    for i in range(len(R)):
        if R[i][0] <= R_boundary:
            R_New.append(R[i])
        else:
            break

    # Sort R_New and L_New by y values
    L_New.sort(key=lambda L_New:L_New[1])
    R_New.sort(key=lambda R_New:R_New[1])


    # The hard part
    k_init = 0
    window_boundary = min_distance
    for h in range(len(L_New)):
        #print("h value", h)
        k = k_init
        while (k < len(R_New)):
            #print("k ",k, "L", L_New[h][1], "lb", (L_New[h][1] - window_boundary),"R Value", R_New[k][1], "ub", (L_New[h][1] + window_boundary))
            if(float(L_New[h][1] - window_boundary) <= R_New[k][1] and R_New[k][1] <= float(L_New[h][1] + window_boundary)):
                window_distance = dist(L_New[h], R_New[k])
                #print("Window Distance", window_distance)
                if window_distance < min_distance:
                    min_distance = window_distance
            elif R_New[k][1] > (L_New[h][1] + window_boundary) and k > 0:
            #    print("A")
                k_init = k - 1
                break
            k = k + 1
            #print(k)



    '''
    window_points = L_New + R_New:
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
    return min_distance

# Perfect
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

# Perfect
def main(filename,algorithm):
    algorithm=algorithm[1:]
    points=read_file(filename)
    if algorithm =='dc':
        start=timeit.default_timer()
        nn = nearest_neighbor(points)
        print("Divide and Conquer: ", nn)
        stop=timeit.default_timer()
        print (stop - start)

        # Print to file
        output_filename = re.sub('.txt', '_distance.txt', filename)
        f = open(output_filename, 'w')
        f.write(str(nn))  # or f.write('...\n')
        f.close()
    if algorithm == 'bf':
        start=timeit.default_timer()
        print("Brute Force: ", brute_force_nearest_neighbor(points))
        stop=timeit.default_timer()
        print (stop - start)
    if algorithm == 'both':
        start=timeit.default_timer()
        nn = nearest_neighbor(points)
        print("Divide and Conquer: ", nn)
        stop=timeit.default_timer()
        print ("DC Time:", (stop - start))
        # Print to file
        output_filename = re.sub('.txt', '_distance.txt', filename)
        f = open(output_filename, 'w')
        f.write(str(nn))  # or f.write('...\n')
        f.close()
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
