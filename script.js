//search for len(), count(), && remove() functions for arrays
class Team {
  constructor(teamid=1, maxplayers=5, rolelock=true) {
      if (maxplayers < 5){ //if not enough players for min classic role lock play, turn it off
          rolelock=false }
      this.teamid= teamid
      this.maxplayers = maxplayers
      this.filledroles= [] //lists what roles are filled in this team, if role lock is on
      this.achievedroles = [] // lists how many spots for each role we have
      this.rank = 0 // adds the players of all the ranks together
      this.players = []
      this.playercount = 0 // how many players are in
      this.support = 0
      this.tank = 0
      this.dps = 0
      this.rolelock = rolelock; // if true, then players will not be added to teams where their specified role is already fulfilled in a team. Set on by default
      
  }

  toString() {
      return "Team" + this.teamid; // toString has to return the string representation
  }
//this  is not done yet
  addplayer(PlayerName) { //when it returns none, algo should try to add a different player- maybe with the needs of the team?
    this.playercount=this.playercount+1
    if (this.isteamfull()){ //if the team is full, ERROR
        console.log("ERROR: Max players reached!")  
        return null
    }
    addedrole=0//keep track of roles for each player added
      //perform role queue for role locks. if someone chooses only one role, it will lock the role
    if (this.rolelock == true && PlayerName.role.length == 1){ //if role lock is on && team not filled yet, allow add players
      for (let i = 0; i < PlayerName.role.length; i++){ //check if there is no role space for this
        roles=PlayerName.role[i]
        if (roles == "Tank"){ //add tank
          if (this.maxplayers == 6 && this.tank<2 && this.filledroles.filter(x => x === "Tank").length == 0){ //if its a 6v6 && we dont have 2 tanks, allow an add of a tank
            this.tank=this.tank+1
            addedrole=addedrole+1
            this.achievedroles.push("Tank") //takes note we have an extra player of this type available
            PlayerName.queuedroles.push(roles)//make this a role that they can queue for
            if (this.tank ==2){ //role lock. //&& this.maxplayers == 6
                this.filledroles.push("Tank")  
            }
          }
          else if (this.maxplayers <= 5 && this.tank == 0) {
            this.tank=this.tank+1
            addedrole=addedrole+1
            this.filledroles.push("Tank") //set tank role to filled! we can only have 1 tank in a 5v5!
            this.achievedroles.push("Tank") //takes note we have an extra player of this type available
            PlayerName.queuedroles.push(roles)//make this a role that they can queue for
            }
        }
        if (roles == "DPS" && this.dps <=2 && this.filledroles.this.filledroles.filter(x => x === "DPS").length == 0){ //add dps
          this.dps=this.dps+1
          addedrole=addedrole+1
          this.achievedroles.push("DPS") //takes note we have an extra player of this type available
          PlayerName.queuedroles.push(roles)//make this a role that they can queue for
          if (this.dps ==2){ //check if this role is filled, mark it. can only happen with role lock
            this.filledroles.push("DPS") 
          }
        }
        if (roles == "DPS" && this.dps <=2 && this.filledroles.this.filledroles.filter(x => x === "DPS").length == 0){ //add dps
          this.dps=this.dps+1
          addedrole=addedrole+1
          this.achievedroles.push("DPS") //takes note we have an extra player of this type available
          PlayerName.queuedroles.push(roles)//make this a role that they can queue for
          if (this.dps ==2){ //check if this role is filled, mark it. can only happen with role lock
            this.filledroles.push("DPS") 
          }
        }
      }
      if (addedrole==0){ //if it gets to the end of this for loop && no roles have been added
        console.log("ERROR: Cannot add player! Role Filled (Role lock on)")
        return null
      }
      else {
          this.players.push(PlayerName)
          this.rank= this.rank + PlayerName.rank //add rank to team total

          if (this.addplayercheck()== null || this.addplayercheck()==null) { //make sure every role is accounted for
            return true
          }
          else {
            return false
          }
      }
    }
    else if (this.rolelock==true){ //only add player if they can fill a role not already filled, meaning they didnt just queue for one role
      deniedroles=0 //the amount of roles locked to this player
      i = 0
      while (i < PlayerName.role.length || this.filledroles.length !=0) {//go through the full list of roles queued by player; or not at all if there are no filled roles
        if (i == PlayerName.role.length) //if we start with i<len(playername). break out of loop
          break;
        if (this.filledroles.filter(x => x === PlayerName.role[i]).length >0) { //if player has queued for a role already filled, note that this is a locked role
            deniedroles=deniedroles+1
        }
        else {
            this.achievedroles.push(PlayerName.role[i])
            PlayerName.queuedroles.push(PlayerName.role[i])//make this a role that they can queue for
        i=i+1
        }
      }
      if (deniedroles==PlayerName.role.length){
        console.log("player queued for roles already filled!")
        return null }
      else { //if roles for player not already filled, then add player to the team!
        this.players.push(PlayerName)
        this.rank= this.rank + PlayerName.rank

        if (this.addplayercheck()==null || this.addplayercheck()==null){ //make sure every role is accounted for if team is full //if true or null (meaning team not full)
          return true
        }
        else{
          return false
        }
      }
    }

  //if role lock is off, add player regardless
  if (this.rolelock == false){ //if role lock is off,quickplay open queue: just check that the team isnt at max capacity yet
    this.players.push(PlayerName)
    this.rank= this.rank + PlayerName.rank
    
    for (let i = 0; i< PlayerName.role.length; i++) {
      roles=PlayerName.role[i]

      if (roles == "Tank"){
        this.tank=this.tank+1
        this.achievedroles.push("Tank") //takes note we have an extra player of this type available
      }  
      if (roles == "DPS"){
        this.dps=this.dps+1
        this.achievedroles.push("DPS") //takes note we have an extra player of this type available
      }
      if (roles == "Support"){
        this.support=this.support+1 
        this.achievedroles.push("Support") //takes note we have an extra player of this type available
      }
    return true
      }
    }  
  }

  isteamfull() {
      if (this.maxplayers==this.players.length){ //we hav to add +1 because it doesnt count 0
           return true }
      return false
  }

  addplayercheck() {
      if (this.isteamfull()==true){
          result = this.checkteamroles() //make sure every role is accounted for
          if (result==true){ //every role is accounted for
              console.log("Team is good to go!") //call create team function?
              this.balanceroles() //we need to reach here
              return true }
          else { //if every role is not accounted for, return null
              console.log("we are missing a {result[1]}!") 
              return false }}
  return null
  //console.log("team not full")
  }
  checkteamroles(){ //i believe i will kep this simple, because the addplayers method already accounts for filled roles
    //Do we have all roles accounted for? 
    
    // 6v6. Returns missing role
    if (this.maxplayers==6){
      if (this.achievedroles.filter(x => x === "Tank").length<2){
        return (false, "Tank") }
      else if(this.achievedroles.filter(x => x === "DPS")<2){
        return (false, "DPS") }
      else if(this.achievedroles.filter(x => x === "Support")<2){
        return (false, "Support")}
      else if(this.achievedroles.filter(x => x === "Tank")==2){ //this doesnt work && can be deleted
        return true} //make algo to accept this value
      return true
    }
    
    //5v5, same thing
    if (this.maxplayers==6){
      if (this.achievedroles.filter(x => x === "Tank").length==0){
        return (false, "Tank") }
      else if(this.achievedroles.filter(x => x === "DPS")<2){
        return (false, "DPS") }
      else if(this.achievedroles.filter(x => x === "Support")<2){
        return (false, "Support")}
      else if(this.achievedroles.filter(x => x === "Tank")==1){ //this doesnt work && can be deleted
        return true} //make algo to accept this value
      return true
    }
    
  }

  balanceroles(){//removes a player's queued roles if already filled
    if (this.filledroles){
      for(let i = 0; i < this.filledroles.length; i++){ //for all the filled roles
        filledroletemp=filledrole[i]
          for(let x = 0; x < this.players.length; x++) {//scroll through all the players
              playertemp=players[x]
              if (playertemp.role.length>1) {//check if a player has more than one role...
                  for (let y = 0; y < playertemp.queuedroles; y++) {//check through all the roles the player has
                      roles=playertemp.queuedroles[y]
                      if (roles == filledroletemp){ //if they have a role that is already filled
                          player.queuedroles.pop(roles) //remove it from their queue-able roles
                      }
                  }        
              }
          }
      }
    }
  }

  getplayers(){
  return this.players
  }
  removeplayer(player){
  return this.players
  }
  getteamid(){
  return this.teamid
  }

  //age() {
  //    const date = new Date();
  //    return date.getFullYear() - this.year;
  //  }
}

class Player{
  constructor(name, role=["Tank", "DPS", "Support"], rank=0) {
    //super().__init__()//how to make this a subclass?
    this.name = name
    this.role = role
    this.rank = rank //i can get this from overwatch?
    this.queuedroles = [] //these are the roles that the player can queue as for the team
  }
  
  toString() {
    return this.name;
  }
}


console.log('ok')

  //const myCar = new Car("Ford", 2014);
//document.getElementById("demo").innerHTML =
//"My car is " + myCar.age() + " years old.";

//const myCar2 = new Car("Audi", 2019);