import requests
import random
import wx


def chooseRandomPlayer()->int:
    """
    Chooses Random Player from Current Nhl Rosters by selecting a random team and then
    selecting a random player from that team. Returns the numerical Id of that player
    """
    fullString = "https://statsapi.web.nhl.com/api/v1/teams"
    teamids=tuple(range(1,11))
    teamids+=tuple(range(12,27))
    teamids+=(28,29,30,52,53,54,55)
    teamid=random.choice(teamids)
    fullString += "/"+str(teamid)+"/roster"
    response=requests.get(fullString)
    roster=response.json()
    randindex=random.randrange(0,len(roster['roster'])-15) #-15 to make it easier to guess(rookies are at the end of the list)
    return roster['roster'][randindex]['person']['id']# roster['roster] is a list of all players

def getPlayerInfo(id)->dict:
    """
    Returns player info in a dictionary
    """
    fullString = "https://statsapi.web.nhl.com/api/v1/people/" + str(id)
    response = requests.get(fullString)
    return response.json()['people'][0]

def guessPlayer(name)->bool:
    """
    Returns whether guess is correct
    """
    guess = input("Please Enter a Player Name: ")
    return name.lower() == guess.lower()
        
def giveHints(playerdict,index):
    """
    Gives hints on player
    """
    hintslist=['currentTeam','primaryPosition','nationality','primaryNumber','currentAge','firstName','fullName']
    print(hintslist[index]+":")
    print(playerdict[hintslist[index]])

def runGame():
    """
    Runs entire Guess Hockey Player Game
    """
    playerid=chooseRandomPlayer()
    playerdict=getPlayerInfo(playerid)
    name=playerdict['fullName']
    for x in range(0,6):
        giveHints(playerdict,x)
        answer=guessPlayer(name)
        if answer:
            print('Congratulations!')
            return
        elif not answer and x < 6:
            print("Wrong Player")
            continue
    print('You have ran out of guesses')
    print('Player is '+name)

if __name__=="__main__":
    runGame()
    