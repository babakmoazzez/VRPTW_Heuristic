from Stop import *
from main import dist_coord,dist

class Car:
    '''Class Car: has a route and a cap. 
    Methods are: add_to_route, add_to_route_util and shift'''
    def __init__(self, num , cap):
        self.cap = cap
        self.route = [] 
        
    def get_route_len(self):
        return len(self.route)
    
    def add_to_route(self,ticket):
        pickup = ticket[0] #pickup
        dropoff = ticket[1] #dropoff

        #the case when the route is []
        if (self.get_route_len()==0):
            if (self.add_to_route_util(pickup,0)):
                if (self.add_to_route_util(dropoff,1)):
                    return True
            if self.get_route_len()!=0:
                return False
        
        #Find the first idx in self.route where we can insert pickup
        passenger_count = 0
        for i in range(self.get_route_len()):
            previous_stop = None
            if (i != 0):
                s1 = self.route[i - 1]
                #How many passengers in car?
                if (s1.pd == 'p'):
                    passenger_count+=1
                else:
                    passenger_count-=1
                    
            if (passenger_count >= self.cap):
                continue;

            s2 = None
            if (i < len(self.route)):
                s2 = self.route[i]
                if (pickup.et > s2.lt):
                    continue;


            #Just found a candidate idx, backup accumulative times and passenger count in case we have to revert
            backup_times = []
            for s in self.route:
                backup_times.append(s.accum_time);
            backup_passenger_count = passenger_count

            #Insert pickup into self.route at index idx
            idx = self.get_route_len()
            if (i < self.get_route_len()):
                idx = self.route.index(s2)
            flag = self.add_to_route_util(pickup,idx)
            if (not flag):#not successful, revert
                c=0
                for s in self.route:
                    s.accum_time = backup_times[c]
                    c+=1
                passenger_count = backup_passenger_count
                continue

            #Find the first idx in self.route we can insert dropoff
            s2 = None
            s1 = pickup
            car_full = False
            for k in range(idx + 1, len(self.route)):  
                
                s2 = self.route[k]
                if (s1.pd == 'p'):
                    passenger_count+=1
                else:
                    passenger_count-=1

                if (passenger_count > self.cap):
                    #not successful, overload, revert
                    self.route.remove(pickup)
                    c=0
                    for s in self.route:
                        s.accum_time = backup_times[c]
                        c+=1
                    passenger_count = backup_passenger_count

                    car_full = True
                    break
                
                #Just found a candidate idx to insert dropoff
                flag = self.add_to_route_util(dropoff, self.route.index(s2))
                if (not flag):
                    s1 = s2
                    continue
                return True

            if (not car_full):

                #Inserting dropoff in the last idx
                flag = self.add_to_route_util(dropoff,self.get_route_len())
                if (flag):
                    return True
                else:
                    if pickup in self.route:
                        self.route.remove(pickup)
                    if dropoff in self.route:
                        self.route.remove(dropoff)
                    c=0
                    for s in self.route:
                        s.accum_time = backup_times[c]
                        c+=1
                    passenger_count = backup_passenger_count
        
        return False
        
    def add_to_route_util(self, stop, idx):
        '''Is it possible to insert stop to the route at idx?'''
        
        assert(0 <= idx <= len(self.route))
        
        #Try idx = 0
        if (idx == 0):
            #Can we get to the stop location before its latest time lt?
            if (dist_coord((0,0), (stop.x,stop.y)) > stop.lt):
                return False
            
            stop.accum_time = dist_coord((0,0), (stop.x,stop.y))
            if (stop.accum_time < stop.et):
                stop.accum_time = stop.et

            #Can we shift everything after?
            if (self.get_route_len()>0):
                s = self.route[idx]
                if (stop.accum_time + dist(stop, s) > s.accum_time):
                    flag = self.shift(s, stop)
                    if (not flag):
                        return False
        
        #Inserting to the middle of route between s1 and s2
        elif 0 < idx < self.get_route_len():
        
            s1 = self.route[idx - 1]
            s2 = self.route[idx]


            if (s1.accum_time > stop.lt):
                return False
            
            #no empty time interval
            if (s1.x == s2.x and s1.y == s2.y and s1.accum_time == s2.accum_time):
                return False
            
            #Can we make it on time?
            if (s1.accum_time + dist(s1, stop) > stop.lt):
                return False

            stop.accum_time = s1.accum_time + dist(s1, stop)
            if (stop.accum_time < stop.et):
                stop.accum_time = stop.et

            #Can we make it to s2?
            if (stop.accum_time + dist(stop, s2) > s2.lt):
                return False

            #Shift
            if (s2.accum_time < stop.accum_time + dist(stop, s2)):
                flag = self.shift(s2, stop)
                if (not flag):
                    return False
                
        #Try inserting stop in the last place
        else:   
            s = self.route[self.get_route_len()-1] 
            
            if (s.accum_time > stop.lt):
                return False

            if (s.accum_time + dist(s, stop) > stop.lt):
                return False

            stop.accum_time = s.accum_time + dist(s, stop)
            if (stop.accum_time < stop.et):
                stop.accum_time = stop.et
                    
        self.route.insert(idx, stop)
        return True
        

    
    def shift(self, stop, current_stop):
        '''Shift all stops after inserting "current_stop" before "stop" '''
        
        to_be_inserted = current_stop;
        to_be_inserted_accum_time = current_stop.accum_time;
        total=to_be_inserted_accum_time
        for i in range(self.route.index(stop), len(self.route)):
            to_be_shifted = self.route[i]
            to_be_shifted_accum_time = total + dist(to_be_inserted, to_be_shifted)
            if (to_be_inserted_accum_time > to_be_shifted.lt):
                return False
            if (to_be_shifted_accum_time < to_be_shifted.et):
                to_be_shifted_accum_time = to_be_shifted.et
            to_be_inserted = to_be_shifted
            total = to_be_shifted_accum_time
        
        for i in range(self.route.index(stop),len(self.route)):
            to_be_shifted = self.route[i]
            to_be_shifted.accum_time = current_stop.accum_time + dist(current_stop, to_be_shifted)
            if (to_be_shifted.accum_time < to_be_shifted.et):
                to_be_shifted.accum_time = to_be_shifted.et
            current_stop = to_be_shifted
        return True
    
