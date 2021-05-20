from Car import *
from Stop import *
import matplotlib.pyplot as plt

#It is assumed that all cars are initially at a depot at coordinbates (0,0).

#Pixels per mile
ppm=5

#average car speed (mph)
avg_speed = 60

#Maximum number of cars available
max_avail=10

#Capacity of each cars (homogeneous)
cap=3

'''distance of two Stop objects'''
def dist(s1,s2): 
    return (avg_speed/60)*(((s1.x - s2.x)**2 + (s1.y - s2.y)**2)**0.5)/ppm

'''Returns distance between two pair of points'''
def dist_coord(s,t): 
    return (avg_speed/60)*(((s[0] - t[0])**2 + (s[1] - t[1])**2)**0.5)/ppm

'''from format 00:00 to minutes 0-1440'''
def time_to_min(t): 
    idx=t.index(':')
    return int(t[0:idx])*60+int(t[idx+1:])

'''from minute to 00:00 format'''
def min_to_time(t): 
    h = int(t//60)
    temp = int(t-60*h//1)
    if temp <10:
        m='0'+str(temp)
    else:
        m=str(temp)
    if h<10:
        h='0'+str(h)
    else:
        h=str(h)
    return h+':'+m


if __name__ == '__main__':
    #Read file Tickets.txt and get requests
    with open('Tickets.txt', 'r') as f:
        temp=f.readline().split()
        n=int(temp[0]) #n is the number of tickets
        tickets_raw=[] #list of tickets
        for i in range(n):
            temp=f.readline().split()
            tickets_raw.append([temp[0],int(temp[1]), time_to_min(temp[2]) , time_to_min(temp[3]) , int(temp[4]), int(temp[5]), int(temp[6]), int(temp[7])])

    #create object based on info read from file
    tickets=[]
    unserved_tickets=[]

    for i in range(n):
        sourcexy = [tickets_raw[i][4],tickets_raw[i][5]]
        destxy = [tickets_raw[i][6],tickets_raw[i][7]]
        lt=tickets_raw[i][3]-dist_coord(sourcexy, destxy) 
        source_stop = Stop(sourcexy[0],sourcexy[1],tickets_raw[i][2],lt,tickets_raw[i][1],'p')
        et=tickets_raw[i][2]+dist_coord(sourcexy, destxy)
        dest_stop = Stop(destxy[0],destxy[1],et,tickets_raw[i][3],tickets_raw[i][1],'d')

        tickets.append((source_stop ,dest_stop))
        unserved_tickets.append((source_stop ,dest_stop))
    
    #main: pick a new car, insert requests in its route until it is impossible to insert more. Then pick a new car. Stop when all requests are serviced
    c=0
    cars=[Car(c,cap)]
    c+=1
    for ticket in tickets:
        scheduled = False
        for car in cars:
            if car.add_to_route(ticket):
                unserved_tickets.remove(ticket)
                scheduled = True
                break
        if scheduled == False:        
            temp = Car(c,cap)
            flag = temp.add_to_route(ticket)
            
            if not flag: #we cannot get to this on time
                temp = None
                print(unserved_tickets)
            else: 
                cars.append(temp)
                c+=1
                unserved_tickets.remove(ticket)
    
    #Printing Solution
    if len(unserved_tickets) == 0:
        print('Successfully scheduled all requests using ' , len(cars) , ' cars.')
        
    else:
        print('The algorithm couldn\'t find a feasible solution. The best possible solution was able to meet ', n-len(unserved_tickets), ' tickets and ',len(unserved_tickets), ' tickets were not served.')
    
    #Itinerary:
    print('Itinerary\n')
    for i in cars:
        print('\nCar ',cars.index(i)+1,'\n')
        for j in i.route:
            if j.pd=='p':
                print('Pickup ', tickets_raw[j.ticket_num-1][0] ,' from (' ,j.x,',',j.y,') at ', min_to_time(j.accum_time) ,' (Ticket ', tickets_raw[j.ticket_num-1][1],')')
            else:
                print('Dropoff ', tickets_raw[j.ticket_num-1][0] ,' at (' ,j.x,',',j.y,') at ',min_to_time(j.accum_time) ,' (Ticket ', tickets_raw[j.ticket_num-1][1],')')

    #Plot each car's route
    fig, ax = plt.subplots()
    colors=['r','g','b', 'c','y','m','k']
    c=0
    for car in cars:
        x=[0]
        for i in car.route:
            x+=[i.x]
        y=[0]
        for i in car.route:
            y+=[i.y]
        x+=[0]
        y+=[0]

        c=cars.index(car)
        plt.plot(x, y,'-bo',label='$car : {num}$'.format(num=c+1),color =colors[c%7],alpha=0.5)
        for X, Y in zip(x, y):
            ax.annotate('{}'.format([X,Y]), xy=(X,Y), xytext=(-5, 5), ha='right',
                        textcoords='offset points',size=7)
        c+=1
    plt.legend(loc='best')
    plt.show()



