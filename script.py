import json
import os
from teams import Player, Team
import random
from datetime import datetime as dt
import jsonpickle

masterplayerpool = []  # this is all players
playerpool = []  # these are players who may be popped
playerpool2 = []
# this is left over players, append this to player pool after a team has been created
rejects = []  # players who could not be fit into the game with criteria
maxteams = 0  # these are how many teams you want to split the player pool into
masterdictionary =None
teams = []
team1 = ""  # fix this to be dynamic later
team2 = ""
index =0
save = []
runtime = 0 #how many time program was created

def getfileindex():
    try:
        file=open("teams.json", "r+")
        json_data = json.load(file)
    except:
        return 0
    return len(json_data["Items"])

data = {
    "Time": f"{dt.now().isoformat()}",
    "Index": f"{getfileindex()}",
    "PlayerPool": [],
    "Teams": [],
    "Rejects": []
}

def add_to_playerpool(*arg):  # make this take a group in and then enumerate by a list
    global playerpool, data
    for players in arg:
        if isinstance(players, Player):  # make sure the argument is a player
            # print(players)
            # print("is a player")
            playerpool.append(players)
            masterplayerpool.append(players)
    data["PlayerPool"]=masterplayerpool #saves initial player pool


def choose_random_player():  # maybe make a clause, if number has already been chosen, dont choose it again for this instance? theres w ayt od ot his
    max = len(playerpool)-1  # this gives an error sometims, invesitage
    if max < 1:
        max = 0
    number = random.randint(0, max)
    return playerpool.pop(number)

def create_team(teamid, size=5, roleblock=True):  # you have to put a team id in!
    global playerpool, data
    team = Team(teamid, size, roleblock)
    for numbers in range(size):
        if len(playerpool) == 0:  # if there's not enough players in player pool, stop
            break

        player = choose_random_player()  # save random player (because they are removed now)
        outcome = team.addplayer(player)
        while outcome == None:
            if not outcome == None:  # if the outcome wasnt none to begin with, break out of this loop
                break

            # if there's not enough players in player pool, stop. This means some teams may not produce 5
            if len(playerpool) == 0:
                break

            # if outcome was none, put player into player pool 2 so they are not removed from game
            if outcome == None:
                # saves player back into player pool just in case
                playerpool2.append(player)
            player = choose_random_player()  # get new player
            # otherwise, keep trying to add a player
            outcome = team.addplayer(player)

    # return the reject players back into player pool. (What if they get rejected twice?)
    playerpool = playerpool + playerpool2
    # if player.rejectionamount == self.teamid (depending on how many teams there is, if its team 3 and rejection 3, or team 2 and rejection 2)
    # or simply, if this is the last iteration of team creation and the player is still in pool...save to rejects list
    global maxteams
    global rejects
    global teams
    if teamid == maxteams:  # if this is the last team to be created
        checkplayerrejects()  # save rejected players to list called rejects and show to user
        # we want to save rejects even if its null, to stay concurrent with the teams
    teams.append(team)  #saves team
    return team


def checkplayerrejects():
    global playerpool, rejects
    rejects = playerpool
    print("Rejects:")
    for players in rejects:
        print(players)
    return rejects  # (print this out?)


def printteam(team):  # make a function that returns a team based off id
    for players in team.players:
        print(f"{players}, {players.queuedroles}") #, {players.rank}
    #print(team.rank)    


def createteams(teamamount, size=5, roleblock=True):
    global maxteams, teams, team1, team2, data
    maxteams = teamamount  # set max teams
    for teamid in range(teamamount):  # create team with id until id = maxteams
        # save team into a variable such as team 1, team 2, etc. -> can you automate variable names?
        
        team1 = create_team(teamid, size, roleblock)
        printteam(team1)
        print()
    checkplayerrejects()
    data["Teams"]=teams
    data["Rejects"]=rejects #save rejects (should be same date/time or index as save team) 
    #writetojson(teamsavedict, "teams.json")
    return None


def get_saved_playerpool(date=None,id=None): #can call with no values, will get latest. we will use this to rebuild player pool, date is used for when looking at list, may not need if i can see id
    file = open("playerpoolspickle.json", 'r')
    json_data = json.load(file)
    list = []
    
    if not date == None: #if date has a value
        id = 0 #setid to 0
        x = 0
        for items in json_data["PlayerPool"]:
            if items[0] == date:
                id=x
            x=x+1
    elif id == None: #if id does not has a value
        id=len(json_data["PlayerPool"])-1 #set to latest entry
    
    for player in json_data["PlayerPool"][id][1]:
        p = jsonpickle.decode(player)
        list.append(p) 
        #print(player)
    return list #not needed, channges global value; instead, let it return a list so i can say playerpool=list as neeeded

#ill only need this if i'll save player pools and team creations separate? here's the player pool, here's the teams built from it?
def check_if_playerpool_saved(pool=playerpool): #re-write for teams
    file = open("playerpoolspickle.json", 'r')
    json_data = json.load(file)
    list = []
    id = 0
    id2=0
    true = 0 #how many of these matches are true
    for items in json_data["PlayerPool"]:
        global playerpool
        for player in json_data["PlayerPool"][id][1]: #create list from json
            p = jsonpickle.decode(player)
            list.append(p) 
            #print(player)
        
        
        #probably a quicker and easier way to do this
        for player in list: #hash the current player pool and the list, compare the hash values.
            if hash(player.name) == hash(playerpool[id2].name): # we have to compare the names because we created new objects when we read in a json file 
                true = true+1 #for every true match, count
            
            if true == len(playerpool) and len(list): #if the length of args = the amount checked to be ture, they are equal to true
                return True   
            
            id2=id2+1
        
        if playerpool == list:
            return True
        id=id+1
    return False #if it reache shere, its not in the list

        
#or save the entire dict so we can save the team/pool and run i
def save_playerpool_to_favorites(): #OR save the date
    #save_current_playerpool() #save to dict
    #writetojson(playerpooldict,"favorites_playerpool.json")
    return None

#retrieve player pool so we can rerun it? i think ill save these for later
def get_playerpool_favorites(date=None, id=None):
    file = open("favorites_playerpool.json", 'r')
    json_data = json.load(file)
    list = []
    
    if not date == None: #if date has a value
        id = 0 #setid to 0
        x = 0
        for items in json_data["PlayerPool"]:
            if items[0] == date:
                id=x
            x=x+1
    elif id == None: #if id does not has a value
        id=len(json_data["PlayerPool"])-1 #set to latest entry
    
    for player in json_data["PlayerPool"][id][1]:
        p = jsonpickle.decode(player)
        list.append(p) 
        #print(player)
    return list 

def remove_from_playerpool(player): #i havent tested this function but im concerned how it will work with automatic saves?
    i = playerpool.index(player)
    playerpool.pop(i)
    i = masterplayerpool.index(player)
    masterplayerpool.pop(i)
    data["PlayerPool"]=masterplayerpool #save to new masterplayer pool?
    return None

def filesave(): #save to file
    global data, masterdictionary
    try: #appending to file
        file=open("teams.json", "r+")
        json_data = json.load(file)
        json_data["Items"].append(data)
        file.seek(0)
        json.dump(json_data, file, indent = 4, default=jsonpickle.encode)
        #masterdictionary["Items"].append(data)
    except: #write brand new file
        masterdictionary = {
            "Items": [ data ]
        }
        file=open("teams.json", "w+")
        json.dump(masterdictionary, file, indent=4, default=jsonpickle.encode)
        file.close()


#there may be instances where i dont want to run save file, such as if we're getting from an old team instance.

#1,2,3, 3=best, 1=not so best
p1 = Player("Ejay", ["Tank","DPS", "Support"], 2)  # i could use numbers for roles
p2 = Player("Jade", ["Support"], 3)  # i could use numbers for roles
p3 = Player("Shane", ["Tank", "DPS", "Support"], 3)  # i could use numbers for roles
# i could use numbers for roles
p4 = Player("Meredith", ["Tank", "DPS", "Support"], 2)
p5 = Player("Squilly", ["Tank","DPS"], 1)  # i could use numbers for roles
p6 = Player("Luke", ["Tank","DPS","Support"], 3)  # i could use numbers for roles
p7 = Player("Nick", ["Tank","DPS","Support"], 3)  # i could use numbers for roles
p8 = Player("Baj", ["DPS","Support"], 2)  # i could use numbers for roles
p9 = Player("Wanda", ["Support"],1)  # i could use numbers for roles
# i could use numbers for roles
p10 = Player("Mike", ["Tank", "DPS"], 2)
p11 = Player("Kyle", ["Tank","Support"], 3)  # i could use numbers for roles
p12 = Player("Moses", ["DPS","Support"], 3)  # i could use numbers for roles

#playerpool=get_saved_playerpool() #replaces 
add_to_playerpool(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12)

createteams(2,6)



#Next:
#(who plays what), put in teams.py? #make a possible button, and save makeups to list/history?
def assignroles():
    # this will create assign roles to each player if they have more than one role, to make up the 5v5 or traditional 6v6
    # this can be run on its own several times with the last, saved team makeup. Or you can name a team makeup (if you dont it will default to last)
    # make teams saved seeable (return the values i guess)
    return None
#maybe not completely necessary

#after this, create flask/django app
#create login function so when you login, no email/password needed. create this with django? or flask to start to be quick and then django





#others todos for later:
# save to favorites, custom lists/names
# create new teams from old player pools? how to display this? player pool and teams together? and save a list of teams made from that player pool? draw this out

#other ideas:
#maybe we can make it to where players can login to their player role and join multiple existing tourneys



filesave()



    