#!/usr/bin/env python3 

'''
Search Problem:

The search problem can be thought of as a dense graph where  we are looking to find a path between two nodes. There could 
be multiple paths from our root node to our goal state. We need to choose the best possible path based on various edge 
constraints. The challenge for the task is goes beyond finding a path to the goal state. The challenge would be to design an
algorithm that could give us an optimal solution(if it exists) for wide variety of inputs.

State Space: 
The State Space S is the set of all possible routes in our data set. The state space is stored in a dictionary segments.

Edge Weights: 
There can be three types of edge weights
1) The distance between two states.
2) Time taken to travel from current node to another node.
3) The count of the edge betwwen two cities

Heuristic : 
For the astar algorithm we have designed a heuristic that calculates the great circle distance
(reference : "https://en.wikipedia.org/wiki/Great-circle_distance") between the current state and goal state. The heuristic 
will be admissible because the great circle distance will be the distance that can be taken to reach the goal state. Any path
we take will be equal or more than our heuristic. For the intersection with no latitude and longitude, we calculate them by 
taking the mean of all the adjacent cities that have latitudes and longitudes. We leave out those intersections that do not 
have any cities adjacent to them. This might slightly affect the algorithm. A slightly better heuristic would be to calculate 
the goal state by taking the weighted average of all the adjacent latitude longitude based on distance from the intersection.

Working: 

Bfs:  
The bfs is implemented using a queue where we implement FIFO. The bfs will always parse through the states at the same 
level of the search space before moving to the next level. As soon as we reach the goal state. We return the path taken to 
reach the goal state and stop the algorithm. The algorithm is far from optimal as we do not check for better paths.

Dfs: 
Dfs will be implemented using a stack where we implement LIFO. The dfs will go deeper in the search space while ignoring most of 
the states. Again, the algorithm would be far from optimal.

Uniform: 
We follow a greedy approach for this algorithm by implementing a priority queque where we try to explore the more promising states 
first. The algorithm ensures that we get an optimal solution for our problem. Although, the algorithm may ensure an optimal solution 
we do not make use of the details that are specific to our problem ,that we can exploit and reduce the time to reach our optimal 
solution. 

Astar: 
The drawback of the previous approach can be overcame by designing a heuristic that acts as a guide of the section of the map we 
should search first. At each instant we try to estimate the minimum distance that we would have to take to reach the goal state.
The heuristic cannot overstimate the distance. We have implemented the great circle distance as our heuristic which would try to 
estimate the distance of successor from the goal state. At each state we choose the path that would minimise the sum of the cost 
to reach that state and our great circle distance to goal.    

Problems faced: 
There  were a few missing values for speed limits in our data. We decided to ignore such rows. 

The astar algorithm seems to work best for various outputs.For cities that are close to each other we do not see much differnce in 
the algorithms other than dfs.The astar algorithm would give us the fatest solution in terms of both time and memory. The 
heuristic of great circle can be improved if we can get the latitude and longitude of the junctions to get a more accurate 
representation. 
''' 

import os 
import sys
import queue
from collections import defaultdict
import heapq
from math import *

#Check the occurence of city in our state space and return the adjacent city or junction with the 
#distance time and the highway to that city/junction
def lookup(city):
    adj_route = [[]]
    for row in segments[city]:
        if row[2] > 0:
            adj_route.append([row[0], row[1], row[1] / row[2], row[3]])

    return adj_route[1:]

#Check the successors to the city while storing the path only if it is to a city/junction that was not in our path 
#or if we find a shorter path to a visited state. 
def successors(city, path):
    r = []
    for route in lookup(city):
        dest, dist, time, highway = route
        if dest in path:
            if dist + path[city][0] < path[dest][0]:
                path[dest] = [dist + path[city][0], time + path[city][1], 1 + path[city][2], highway]
                path[dest][3:] = path[city][3:]
                path[dest].append(city)
                path[dest].append(highway)
                r.append(dest)

        elif dest not in path:
            if city != start_city:
                path[dest] = [dist + path[city][0], time + path[city][1], 1 + path[city][2]]
                for v in path[city][3:]:
                    path[dest].append(v)
                path[dest].append(city)
                path[dest].append(highway)
                r.append(dest)

            else:
                path[dest] = [dist, time, 1, city, highway]
                r.append(dest)
    return r, path



#Implement the  breadth first algorithm using a queue and return the path when we reach the goal state 
def bfs(initial_path):
    result = []
    fringe = [start_city]
    path = initial_path
    while fringe:
        sublist, p = successors(fringe.pop(0), path)

        for s1 in sublist:
            path = p
            fringe.append(s1)
        if end_city in path:
            path[end_city].append(end_city)
            result.append(path[end_city][0])
            result.append(path[end_city][1])
            result.append(start_city)
            print("Total Distance from " + start_city + " to " + end_city + " is " + str(
                path[end_city][0]) + " miles" + "\n")
            print("Expected time to " + end_city + " is " + str(path[end_city][1]) + " hours " + "\n")
            print("Start from " + start_city, end=" ")
            for idx, city in enumerate(path[end_city]):
                if idx > 3:
                    if idx % 2 == 0:
                        print("Then take the highway " + path[end_city][idx] + " to ", end="")
                    else:
                        print(path[end_city][idx] + "\n")
                        result.append(path[end_city][idx])

            return result
    return False

#Implement the depth first algorithm using a stack and return the path when we reach the goal state. 
def dfs(initial_path):
    result = []
    fringe = [start_city]
    path = initial_path
    while fringe:
        sublist, p = successors(fringe.pop(), path)
        for s1 in sublist:
            path = p
            fringe.append(s1)
            if end_city in path:
                path[end_city].append(end_city)
                result.append(path[end_city][0])
                result.append(path[end_city][1])
                result.append(start_city)
                print("Total Distance from " + start_city + " to " + end_city + " is " + str(
                    path[end_city][0]) + " miles" + "\n")
                print("Expected time to " + end_city + " is " + str(path[end_city][1]) + " hours " + "\n")
                print("Start from " + start_city, end=" ")
                for idx, city in enumerate(path[end_city]):
                    if idx > 3:
                        if idx % 2 == 0:
                            print("Then take the highway " + path[end_city][idx] + " to ", end="")
                        else:
                            print(path[end_city][idx] + "\n")
                            result.append(path[end_city][idx])

                return result
    return False


 
def successors_ucs(tup, path, cost):
    r = []
    city = tup[1]
    for route in lookup(city):
        dest, dist, time, highway = route

        if cost == "distance":
            measure = dist
            c,p = 0,1
        if cost == "time": 
            measure = time
            c,p = 1,1
        if cost == "segments":
            measure = 1
            c,p = 2,1
       	if cost =="longtour":
       		measure = dist
       		c,p = 0,-1

        if dest in path:
            if measure + path[city][c] < path[dest][c]:
                path[dest] = [dist + path[city][0], time + path[city][1], 1 + path[city][2], highway]
                path[dest][3:] = path[city][3:]
                path[dest].append(city)
                path[dest].append(highway)
                r.append([p*(measure + path[city][c]), dest])

        elif dest not in path:
            if city != start_city:

                path[dest] = [dist + path[city][0], time + path[city][1], 1 + path[city][2]]
                for v in path[city][3:]:
                    path[dest].append(v)
                path[dest].append(city)
                path[dest].append(highway)
                r.append([p*(measure + path[city][c]), dest])

            else:
                path[dest] = [dist, time, measure, city, highway]
                r.append([p*(measure + path[city][c]), dest])

    return r, path


def ucs(initial_path, cost):
    result = []
    fringe = [[0, start_city]]
    path = initial_path
    while fringe:
        sublist, p = successors_ucs(heapq.heappop(fringe), path, cost)
        for s1 in sublist:
            path = p
            heapq.heappush(fringe, s1)

            if end_city in path:

                path[end_city].append(end_city)
                result.append(path[end_city][0])
                result.append(path[end_city][1])
                result.append(start_city)
                print("Total Distance from " + start_city + " to " + end_city + " is " + str(
                    path[end_city][0]) + " miles" + "\n")
                print("Expected time to " + end_city + " is " + str(path[end_city][1]) + " hours " + "\n")
                print("Start from " + start_city, end=" ")
                for idx, city in enumerate(path[end_city]):
                    if idx > 3:
                        if idx % 2 == 0:
                            print("then take the highway " + path[end_city][idx] + " to ", end="")
                        else:

                            print(path[end_city][idx] + "\n")
                            result.append(path[end_city][idx])

                return result
    return False


#
def circledistance(city):
    lat1, long1 = 0, 0

    if len(location[city]) == 2:
        lat1, long1 = location[city][0] * pi / 180, location[city][1] * pi / 180



    else:
        i = 0
        for adj_segments in segments[city]:
            adj_city = adj_segments[0]
            if len(location[adj_city]) == 2:
                lat1 += location[adj_city][0]
                long1 += location[adj_city][1]
                i += 1
        if i > 0:
            lat1, long1 = (lat1 * pi)/ (180 * i), (long1 * pi) / (180 * i)
        else:
            return 99999999
    lat2, long2 = location[end_city][0] * pi / 180, location[end_city][1] * pi / 180
    delta = lat1 - lat2
    lamda = long1 - long2
    return 3959 * 2 * asin(((sin(delta / 2) ** 2) + cos(lat1) * cos(lat2) * (sin(lamda / 2) ** 2)) ** 0.5)


def lookup_astar(city):
    adj_route = [[]]
    for row in segments[city]:
        if row[2] > 0:
            heuristic = circledistance(row[0])
            if cost == "time":
            	heuristic = heuristic/100
            if cost == "segments":
            	heuristic = heuristic/730
            if cost == "longtour":
            	heuristic = heuristic
            adj_route.append([row[0], row[1], row[1] / row[2], row[3], heuristic])
    return adj_route[1:]


def successors_astar(tup, path, cost):
    r = []
    city = tup[1]
    for route in lookup_astar(city):
        dest, dist, time, highway, heuristic = route

        if heuristic == 99999999:
            continue
        if cost == "distance":
            measure = dist
            c,p = 0,1
        if cost == "time":
            measure = time
            c,p = 1,1
        if cost == "segments":
            measure = 1
            c,p = 2,1
        if cost  == "longtour":
        	measure =dist
        	c,p = 0,-1 
        if dest in path:
            if measure + path[city][c] < path[dest][c]:
                path[dest] = [dist + path[city][0], time + path[city][1], 1 + path[city][2], highway]
                path[dest][3:] = path[city][3:]
                path[dest].append(city)
                path[dest].append(highway)

                r.append([p*(path[dest][c] + heuristic), dest])

        elif dest not in path:
            if city != start_city:
                if dest == end_city:
                    print(1)

                path[dest] = [dist + path[city][0], time + path[city][1], 1 + path[city][2]]
                for v in path[city][3:]:
                    path[dest].append(v)
                path[dest].append(city)
                path[dest].append(highway)

                r.append([p*(path[dest][c] + heuristic), dest])

            else:
                path[dest] = [dist, time, measure, city, highway]
                r.append([p*(path[dest][c] + heuristic), dest])
    return r, path


def astar(intial_path, cost):
    initial_heuristic = circledistance(start_city)
    result = []
    fringe = [[initial_heuristic, start_city]]
    path = initial_path
    while fringe:
 
        sublist, p = successors_astar(heapq.heappop(fringe), path, cost)
       
        for s1 in sublist:
            path = p
            heapq.heappush(fringe, s1)

            if end_city in path :#and state_count == 48:

                path[end_city].append(end_city)
                result.append(path[end_city][0])
                result.append(path[end_city][1])
                result.append(start_city)
                print("Total Distance from " + start_city + " to " + end_city + " is " + str(path[end_city][0]) + " miles" + "\n")
                print("Expected time to " + end_city + " is " + str(path[end_city][1]) + " hours " + "\n")
                print("Start from " + start_city, end=" ")
                for idx, city in enumerate(path[end_city]):
                    if idx > 3:
                        if idx % 2 == 0:
                            print("then take the highway " + path[end_city][idx] + " to ", end="")
                        else:

                            print(path[end_city][idx] + "\n")
                            result.append(path[end_city][idx])

                return result
    return False


'''
load all the edges into a dictionary with the city as the key and the other city, distance, speed and 
highway as the key. We consider only those segments that have no missing information. 
'''
segments = defaultdict(list)
with open('road-segments.txt', 'r') as f:
    for line in f:
        splitLine = line.split()
        if len(splitLine) == 5:
            if splitLine[0] in segments:
            
            	segments[splitLine[0]].append([splitLine[1], int(splitLine[2]), int(splitLine[3]), splitLine[4]])
            else:
            	segments[splitLine[0]] = [[splitLine[1], int(splitLine[2]), int(splitLine[3]), splitLine[4]]]
            
            if splitLine[1] in segments:
            	
            	segments[splitLine[1]].append([splitLine[0], int(splitLine[2]), int(splitLine[3]), splitLine[4]])
            
            else:

            	segments[splitLine[1]] = [[splitLine[0], int(splitLine[2]), int(splitLine[3]), splitLine[4]]]

# create a dictionary for location which would hold the latitude and longitude coordinates of a city.
states = [] 
location = defaultdict(list)
with open('city-gps.txt', 'r') as t:
    for line in t:
        splitLine = line.split()
        if len(splitLine) > 1:
            location[splitLine[0]] = [float(splitLine[1]), float(splitLine[2])]
            
            r =splitLine[0].split(",_")
            states.append(r[1])
        else:
            location[splitLine] = []

cost = sys.argv[4]
algo = sys.argv[3]
end_city = sys.argv[2]
start_city = sys.argv[1]

initial_path = defaultdict(list)
initial_path[start_city] = [0, 0, 0, 0]

states = ["Alabama","Arizona","Arkansas","California","Colorado","Connecticut","Delaware"
,"Florida","Georgia","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana",
"Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
"Nebraska","Nevada","New_Hampshire","New_Jersey","New_Mexico","New_York","North Carolina",
"North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina",
"South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia",
"Wisconsin","Wyoming"]



if algo == "bfs":
    print(" ".join([str(element) for element in bfs(initial_path)]))
elif algo == "dfs":
    print(" ".join([str(element) for element in dfs(initial_path)]))
elif algo == "uniform":
    print(" ".join([str(element) for element in ucs(initial_path, cost)]))
elif algo == "astar":
    print(" ".join([str(element) for element in astar(initial_path, cost)]))
else:
    print("Please check the algorithm")




