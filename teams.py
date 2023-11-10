import json
import random
class Team:
    def __init__(self, teamid=1, maxplayers=5, rolelock=True):
      if maxplayers < 5: #if not enough players for min classic role lock play, turn it off
        rolelock=False
      
      self.teamid= teamid
      self.maxplayers = maxplayers
      self.filledroles= [] #lists what roles are filled in this team, if role lock is on
      self.achievedroles = [] #lists how many spots for each role we have
      self.rank = 0 #adds the players of all the ranks together
      self.players = []
      self.playercount = 0 #how many players are in
      self.support = 0
      self.tank = 0
      self.dps = 0
      self.rolelock = rolelock #if true, then players will not be added to teams where their specified role is already fulfilled in a team. Set on by default

    def __str__(self):
        return f"Team: {self.teamid}"
    
    def addplayer(self, PlayerName): #when it returns none, algo should try to add a different player- maybe with the needs of the team?
      self.playercount=self.playercount+1
      if self.isteamfull(): #if the team is full, ERROR
        print("ERROR: Max players reached!")
        return None
  
      addedrole=0#keep track of roles for each player added
      #perform role queue for role locks. if someone chooses only one role, it will lock the role
      if self.rolelock == True and len(PlayerName.role) == 1: #if role lock is on and team not filled yet, allow add players
        for roles in PlayerName.role: #check if there is no role space for this
          if roles == "Tank": #add tank
            if self.maxplayers == 6 and self.tank<2 and not self.filledroles.count("Tank"): #if its a 6v6 and we dont have 2 tanks, allow an add of a tank
              self.tank=self.tank+1
              addedrole=addedrole+1
              self.achievedroles.append("Tank") #takes note we have an extra player of this type available
              PlayerName.queuedroles.append(roles)#make this a role that they can queue for
              if self.tank ==2: #role lock. //and self.maxplayers == 6
                  self.filledroles.append("Tank")  
            elif self.maxplayers <= 5 and self.tank == 0:
              self.tank=self.tank+1
              addedrole=addedrole+1
              self.filledroles.append("Tank") #set tank role to filled! we can only have 1 tank in a 5v5!
              self.achievedroles.append("Tank") #takes note we have an extra player of this type available
              PlayerName.queuedroles.append(roles)#make this a role that they can queue for
          if roles == "DPS" and self.dps <=2 and not self.filledroles.count("DPS"): #add dps
            self.dps=self.dps+1
            addedrole=addedrole+1
            self.achievedroles.append("DPS") #takes note we have an extra player of this type available
            PlayerName.queuedroles.append(roles)#make this a role that they can queue for
            if self.dps ==2: #check if this role is filled, mark it. can only happen with role lock
              self.filledroles.append("DPS") 
        
          if roles == "Support" and self.support <=2 and not self.filledroles.count("Support"):
            self.support=self.support+1
            addedrole=addedrole+1
            self.achievedroles.append("Support") #takes note we have an extra player of this type available
            PlayerName.queuedroles.append(roles)#make this a role that they can queue for
            if self.support ==2: #check if these roles are filled; can only have this with role lock on
              self.filledroles.append("Support") 
        
        if addedrole==0: #if it gets to the end of this for loop and no roles have been added
          print("ERROR: Cannot add player! Role Filled (Role lock on)")
          return None
        else:
            self.players.append(PlayerName)
            self.rank= self.rank+ PlayerName.rank #add rank to team total
            
            if self.addplayercheck() or self.addplayercheck()==None: #make sure every role is accounted for
              return True
            else:
              return False
    
      elif self.rolelock==True: #only add player if they can fill a role not already filled, meaning they didnt just queue for one role
        deniedroles=0 #the amount of roles locked to this player
        i = 0
        while i < len(PlayerName.role) or len(self.filledroles) !=0: #go through the full list of roles queued by player; or not at all if there are no filled roles
          if i == len(PlayerName.role): #if we start with i<len(playername). break out of loop
            break
          if self.filledroles.count(PlayerName.role[i]): #if player has queued for a role already filled, note that this is a locked role
              deniedroles=deniedroles+1
          else:
              self.achievedroles.append(PlayerName.role[i])
              PlayerName.queuedroles.append(PlayerName.role[i])#make this a role that they can queue for
          i=i+1
        
        if deniedroles==len(PlayerName.role): 
          print("player queued for roles already filled!")
          return None
        else: #if roles for player not already filled, then add player to the team!
          self.players.append(PlayerName)
          self.rank= self.rank+ PlayerName.rank
          
          if self.addplayercheck() or self.addplayercheck()==None: #make sure every role is accounted for if team is full #if true or None (meaning team not full)
            return True
          else:
            return False
      
      #if role lock is off, add player regardless
      if self.rolelock == False: #if role lock is off,quickplay open queue: just check that the team isnt at max capacity yet
        self.players.append(PlayerName)
        self.rank= self.rank+ PlayerName.rank
        
        for roles in PlayerName.role:
          if roles == "Tank":
            self.tank=self.tank+1
            self.achievedroles.append("Tank") #takes note we have an extra player of this type available
            
          if roles == "DPS":
            self.dps=self.dps+1
            self.achievedroles.append("DPS") #takes note we have an extra player of this type available
        
          if roles == "Support":
            self.support=self.support+1 
            self.achievedroles.append("Support") #takes note we have an extra player of this type available
        return True
        
    def isteamfull(self):
      if self.maxplayers==len(self.players): #we hav to add +1 because it doesnt count 0
        return True
      return False
    
    def addplayercheck(self):
      if self.isteamfull()==True:
          result = self.checkteamroles() #make sure every role is accounted for
          if result==True: #every role is accounted for
            print("Team is good to go!") #call create team function?
            self.balanceroles() #we need to reach here
            return True
          else: #if every role is not accounted for, return None
            print(f"we are missing a {result[1]}!")
            return False
      return None
      #print("team not full")

    def checkteamroles(self): #i believe i will kep this simple, because the addplayers method already accounts for filled roles
      #Do we have all roles accounted for? 
      
      # 6v6. Returns missing role
      if self.maxplayers==6:
        if self.achievedroles.count("Tank")<2:
          return (False, "Tank")
        elif self.achievedroles.count("DPS")<2:
          return (False, "DPS")
        elif self.achievedroles.count("Support")<2:
          return (False, "Support")
        elif self.achievedroles.count("Tank")==2: #this doesnt work and can be deleted
          return True #make algo to accept this value
        return True
      
      #smae thing but for a 5v5
      if self.maxplayers==5:
        if self.achievedroles.count("Tank")==0:
          return (False, "Tank")
        elif self.achievedroles.count("DPS")<2:
          return (False, "DPS")
        elif self.achievedroles.count("Support")<2:
          return (False, "Support")
        elif self.achievedroles.count("Tank")==1: #this doesnt work and can be deleted
          return True #make algo to accept this value
        return True

    def balanceroles(self): #removes a player's queued roles if already filled
      if self.filledroles:
        for filledrole in self.filledroles: #for all the filled roles
          for player in self.players: #scroll through all the players
            if len(player.role)>1: #check if a player has more than one role...
              for roles in player.queuedroles: #check through all the roles the player has
                if roles == filledrole: #if they have a role that is already filled
                  player.queuedroles.remove(roles) #remove it from their queue-able roles
  
    def getplayers(self):
      return self.players
    
    def removeplayer(self):
      return self.players
    
    def getteamid(self):
      return self.teamid
    
class Player:
  def __init__(self, name, role=["Tank", "DPS", "Support"], rank=0):
    super().__init__()
    self.name = name
    self.role = role
    self.rank = rank #i can get this from overwatch?
    self.queuedroles = [] #these are the roles that the player can queue as for the team
  
  def __str__(self):
    return f"{self.name}"
