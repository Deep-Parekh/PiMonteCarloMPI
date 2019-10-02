#!/usr/bin/python3

from mpi4py import MPI
import math
import random

world = MPI.COMM_WORLD
numprocs = world.size
myid = world.rank
procname = MPI.Get_processor_name()

print('Process %d on %s' %(myid, procname))

POINTS = 50000000         
total_circle_points = 0
totalTime = 0
pi = 0

if myid == 0:
    start_time = MPI.Wtime()

circle_points = 0
    
random.seed(myid)

for i in range(0,POINTS):
    x = random.uniform(0,1) 
    y = random.uniform(0,1)

    r = math.sqrt((x*x)+(y*y))
    if (r <= 1):
        circle_points += 1

total_circle_points = world.reduce(circle_points, op=MPI.SUM,root=0)

if myid == 0:
    end_time = MPI.Wtime()
    totalTime = end_time-start_time
    pi = (float(total_circle_points)/(POINTS*numprocs)) * 4

world.barrier()

if myid == 0:
    print('Execution time (sec) = %f, pi = %f' %(totalTime, pi))
