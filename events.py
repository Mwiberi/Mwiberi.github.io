class event(object):

    def __init__(self,name, eventID,location,date):
        
        self.name = name
        self.eventID =eventID
        self.location =location
        self.date =date
        

        EventDetails={}
        

    def add_event(self,name, eventID,location,date):
        self.name = name
        self.eventID =eventID
        self.location =location
        self.date =date
        
        if type(name) or type(location) !=str:
            return "Invalid input. Enter character elements"
        if name and eventID and location and date:
            #store details in a dictionary
            self.eventDetails={'Event Name':name,'Event ID':eventID,'Location':location,'Date':date}