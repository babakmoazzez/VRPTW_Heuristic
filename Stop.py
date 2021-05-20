class Stop:
    '''Class Stop: Coordinates are x,y. [et,lt] is availability window. Either a pickup (p) or a dropoff (d). accum_time is the accumulated time when inserted to a route. '''
    def __init__(self,x,y , et, lt, ticket_num, pd):
        self.x=x
        self.y=y
        self.et=et
        self.lt=lt
        self.ticket_num=ticket_num
        self.pd=pd
        self.accum_time = 0