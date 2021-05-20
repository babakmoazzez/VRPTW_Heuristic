# Dial_A_Ride_Heuristic

On a single day, there are five costumers who want to travel: Walt, Skyler, Jessie, Gus, and Saul.  Each have a number of trips at various times of the day.
The goal is to create a schedule for cars to fulfill all of their trips, using min number of cars.  All trips can be shared rides and cars have a certain capacity. 

# Data

The file “Tickets.txt” includes the data. The first line is the number of tickets, followed by tickets:

costumer	Trip#	earliest_time	latest_time	X1	Y1	X2	Y2
Walt	1	9:00	11:03	115	391	511	283

# Details

Origin and destination are specified as coordinates (X1, Y1) and (X2, Y2) respectively. 

Pixels per mile = 5

Average speed = 60 mph

Max capacity for all cars = 3 passengers

The heuristic is very simple: we pick a ticket and try to insert it into the route of a car that has already been used. If it is not possible, then we will use a  new car and insert the ticket into the route of that car.
