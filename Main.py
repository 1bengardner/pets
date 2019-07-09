import random
from Pet import *
class Main(object):
    def __init__(self):
        self.pet = None
        self.treatment1Count = 0
        self.treatment2Count = 0
        self.treatment3Count = 0
        self.timesPlayed = 0
        self.timesSlept = 0
        self.timesAte = 0
        
    def new(self, petInfo):
        self.pet = Pet(petInfo[0], petInfo[1], int(petInfo[2]),\
                       int(petInfo[3]), int(petInfo[4]), int(petInfo[5]),\
                       int(petInfo[6]), int(petInfo[7]), float(petInfo[8]),\
                       petInfo[9])
        
    def load(self, saveGame):
        fileIn = open("data\\"+saveGame+".txt", "r")
        line = []
        for l in fileIn:
            line = l.split("\t")
            self.pet = Pet(line[0], line[1], int(line[2]), int(line[3]),\
                           int(line[4]), int(line[5]), int(line[6]),\
                           int(line[7]), float(line[8]), eval(line[9]))
        fileIn.close()

    def save(self, saveGame):
        fileOut = open("data\\"+saveGame+".txt", "w")
        fileOut.write(self.pet.stats())
        fileOut.close()
        
    def tnl(self):
        return int(47+(float(self.getLevel())**1.3)*3.0)

    def getName(self):
        return self.pet.name

    def getSpecies(self):
        return self.pet.species

    def getLevel(self):
        return self.pet.level

    def getExperience(self):
        return self.pet.experience

    def getEvolution(self):
        return self.pet.evolution

    def getHappiness(self):
        return self.pet.happiness

    def getEnergy(self):
        return self.pet.energy

    def getHunger(self):
        return self.pet.hunger

    def getMoney(self):
        return self.pet.money

    def getInventory(self):
        return self.pet.inventory

    def modLevel(self, value):
        self.pet.level += value

    def modExperience(self, value):
        if self.getEnergy() > 50:
            self.pet.experience += value
        elif self.getEnergy() > 0:
            self.pet.experience += value/2

    def modEvolution(self, value):
        self.pet.evolution += value

    def modHappiness(self, value):
        self.pet.happiness += value
        if self.getHappiness() > 100:
            self.pet.happiness = 100
        elif self.getHappiness() < 0:
            self.pet.happiness = 0

    def modEnergy(self, value):
        self.pet.energy += value
        if self.getEnergy() > 100:
            self.pet.energy = 100
        elif self.getEnergy() < 0:
            self.pet.energy = 0

    def modHunger(self, value):
        self.pet.hunger += value
        if self.getHunger() < 0:
            self.pet.hunger = 0
        elif self.getHunger() > 100:
            self.pet.hunger = 100

    def modMoney(self, value):
        self.pet.money += value

    def modInventory(self, item):
        self.pet.inventory.append(item)

    def play(self):
        self.timesPlayed += 1
        self.timesAte = 0
        self.timesSlept = 0
        if self.timesPlayed > 7:
            self.modHappiness(-1)
        if self.timesPlayed > 5:
            return self.getName()+" is bored."
        toy = self.checkInv("happiness", ["happiness", "Hand", 0, 0, None])
        self.modHappiness(toy[2]+1)
        if self.getHappiness < 100:
            self.modExperience(1)
        breaks = random.randint(1, 30)
        if breaks == 1 and toy != ["happiness", "Hand", 0, 0, None]:
            self.pet.inventory.remove(toy)
            return random.choice(["The "+toy[1]+" wore out from overuse.",\
                                  self.getName()+" ripped the "+toy[1]+" to pieces! You'll have to get a new one from the store.",\
                                  "Your "+toy[1]+" suddenly broke! What a defective piece of junk.",\
                                  "As "+self.getName()+" begins chasing the "+toy[1]+", you notice there's a giant scratch on it. Time for a replacement."])
        return None

    def sleep(self):
        self.timesSlept += 1
        self.timesPlayed = 0
        self.timesAte = 0
        bed = self.checkInv("energy", ["energy", "Floor", 10, 0, None])
        if self.getEnergy() == 100:
            return self.getName()+" has some trouble getting to sleep."
        self.modEnergy(bed[2])
        if self.timesSlept > 2:
            self.modHappiness(-5)
            return self.getName()+" is tired of sleeping."
        self.modExperience(1)
        if bed[1] == "Doghouse":
            return self.getName()+" falls fast asleep in the "+bed[1]+"."
        return self.getName()+" falls fast asleep on the "+bed[1]+"."
        
    def feed(self, food):
        if (food == 1 and self.getMoney() >= 0.25) or\
           (food == 2 and self.getMoney() >= 2) or\
           (food == 3 and self.getMoney() >= 10):
            self.timesAte += 1
            self.timesPlayed = 0
            self.timesSlept = 0
            if food == 1:
                self.modMoney(-.25)
            elif food == 2:
                self.modMoney(-2)
            elif food == 3:
                self.modMoney(-10)
                
            if self.getHunger() == 0:
                self.modHappiness(-5)
                return self.getName()+"'s stuffed! Overfeeding your pet will not make it happy."
            self.modHunger(-food)
            if self.timesAte > 6:
                self.modHappiness(-3)
            if self.timesAte > 4:
                return self.getName()+" is getting cramps."
            self.modExperience(1)
            return None
        return "You can't afford that kind of food."   

    def salon(self, treatment):
        if self.getMoney() >= 10*treatment:
            self.timesPlayed = 0
            self.timesSlept = 0
            self.timesAte = 0
            self.modMoney(-10*treatment)
            if treatment == 1:
                self.treatment1Count += 1
                self.modHappiness(10)
                self.modExperience(50/self.treatment1Count+1)
                return self.getName()+" feels better after a nice shampoo wash." 
            elif treatment == 2:
                self.treatment2Count += 1
                self.modHappiness(15)
                self.modEnergy(5)
                self.modExperience(50/self.treatment2Count+1)
                return self.getName()+" is relaxed after a hot soak."
            elif treatment == 3:
                self.treatment3Count += 1
                self.modHappiness(30)
                self.modExperience(50/self.treatment3Count+1)
                return self.getName()+" loves the new haircut."
        return "You can't afford that kind of treatment."   

    def buy(self, item):
        if self.getMoney() >= item[3]:
            self.modMoney(-item[3])
            self.modInventory(item)
            return "You have purchased a(n) "+item[1]+"."
        return "You can't afford that item."

    def race(self, time):
        if ["other", "Race Ticket", 0, 0, None] not in self.getInventory() and int(time[-4:-2]) < 6:
            self.timesPlayed = 0
            self.timesSlept = 0
            self.timesAte = 0
            nameList = ["Bernie", "Ernest", "Roger", "Enrique", "Angelo",\
                        "Angel", "Rover", "Andy", "Stanley", "Hank",\
                        "Marley", "Pal", "Edgar", "Rod", "Ralph",\
                        "Max", "Patches", "Spot", "Spike", "Peaches",\
                        "Golly", "Marigold", "Joaquin", "Unagi", "Speckles",\
                        "Lulu", "Precious", "Flappy", "Spanky", "Wago"]
            winCount = 1
            for item in self.getInventory():
                if item == ["collection", "Trophy", 0, 0, None]:
                    winCount += 1
            if winCount >= 10:
                return self.getName()+" is the racing champion! There are no pets left to compete against."
            self.modInventory(["other", "Race Ticket", 0, 0, None])
            prizeMoney = winCount * 50
            tempScore = int(300+self.getLevel()*(100+self.getHappiness()+self.getEnergy()-self.getHunger()))
            score = random.randint(int(tempScore*0.8), int(tempScore*1.2))
            oppScore1 = random.randint(900*winCount, 1100*winCount)
            oppScore2 = random.randint(850*winCount, 950*winCount)
            oppScore3 = random.randint(820*winCount, 880*winCount)
            
            tempTime = 30000-score
            raceTime = str(tempTime/100/60)+":"+str((tempTime/100)-(tempTime/100/60*60))
            if raceTime[-2] == ":":
                temp = raceTime[-1]
                raceTime = raceTime[:-1]
                raceTime += "0"+temp
            tempTime = 30000-oppScore1
            oppRaceTime1 = str(tempTime/100/60)+":"+str((tempTime/100)-(tempTime/100/60*60))
            if oppRaceTime1[-2] == ":":
                temp = oppRaceTime1[-1]
                oppRaceTime1 = oppRaceTime1[:-1]
                oppRaceTime1 += "0"+temp
            tempTime = 30000-oppScore2
            oppRaceTime2 = str(tempTime/100/60)+":"+str((tempTime/100)-(tempTime/100/60*60))
            if oppRaceTime2[-2] == ":":
                temp = oppRaceTime2[-1]
                oppRaceTime2 = oppRaceTime2[:-1]
                oppRaceTime2 += "0"+temp
            tempTime = 30000-oppScore3
            oppRaceTime3 = str(tempTime/100/60)+":"+str((tempTime/100)-(tempTime/100/60*60))
            if oppRaceTime3[-2] == ":":
                temp = oppRaceTime3[-1]
                oppRaceTime3 = oppRaceTime3[:-1]
                oppRaceTime3 += "0"+temp
            scoreList = sorted([(score, raceTime, self.getName()),\
                                (oppScore1, oppRaceTime1, nameList.pop(random.randint(0,len(nameList)-1))),\
                                (oppScore2, oppRaceTime2, nameList.pop(random.randint(0,len(nameList)-1))),\
                                (oppScore3, oppRaceTime3, nameList.pop(random.randint(0,len(nameList)-1)))], reverse=True)
            results = ("--Race Results"+"-"*28+\
                       "\n"+"1. "+str(scoreList[0][2])+" - "+str(scoreList[0][1])+\
                       "\n"+"2. "+str(scoreList[1][2])+" - "+str(scoreList[1][1])+\
                       "\n"+"3. "+str(scoreList[2][2])+" - "+str(scoreList[2][1])+\
                       "\n"+"4. "+str(scoreList[3][2])+" - "+str(scoreList[3][1]))
            self.modExperience(20)
            self.modHunger(15)
            self.modEnergy(-30)
            if scoreList[0][0] == score:
                self.modHappiness(10)
                self.modInventory(["collection", "Trophy", 0, 0, None])
                self.modMoney(prizeMoney)
                return results + "\nCongratulations! You won a trophy and $"+str(prizeMoney)+" in prize money."
            self.modHappiness(-10)
            return results + "\nBetter luck next time."
        return "The races start every hour. Come back in "+str(60-int(time[-4:-2]))+" minutes."

    def talent(self, stats):
        earnings = self.getLevel()*(stats/75.)
        finalEarnings = round(random.uniform(earnings*0.8, earnings*1.2), 2)
        self.modHunger(5)
        self.modEnergy(-10)
        self.modExperience(10)
        self.modMoney(finalEarnings)
        if str(finalEarnings)[-2] == ".":
            finalEarnings = str(finalEarnings)+"0"
        return random.choice([self.getName()+"'s juggling artistry earns you $"+str(finalEarnings)+".",\
                              self.getName()+" plays a mean sax. You got $"+str(finalEarnings)+" from the performance.",\
                              self.getName()+"'s endless backflips never cease to amaze the audience. You earned $"+str(finalEarnings)+".",\
                              self.getName()+" actually sat when you told him to! You made a total of $"+str(finalEarnings)+" from the crowd of onlookers.",\
                              "You thought it was a bad idea to participate in the show today when your pet had gas, but you were proven wrong.\n"+self.getName()+" the farting "+self.getSpecies().lower()+" was a real hit, netting you $"+str(finalEarnings)+".",\
                              self.getName()+"'s fetching prowess earned you $"+str(finalEarnings)+".",\
                              self.getName()+"'s impersonation of Dick Cheney steals the show. You got $"+str(finalEarnings)+".",\
                              self.getName()+" solved a Rubik's Cube in "+str(random.randint(2,60))+" seconds! That's better than you can do, and apparently the audience as well: You made\n$"+str(finalEarnings)+"."])

    def beauty(self, time):
        if ["other", "Beauty Contest Ticket", 0, 0, None] not in self.getInventory() and (int(time[-4:-2]) < 6 or 29 < int(time[-4:-2]) < 36):
            self.timesPlayed = 0
            self.timesSlept = 0
            self.timesAte = 0
            nameList = ["Bernie", "Ernest", "Roger", "Enrique", "Angelo",\
                        "Angel", "Rover", "Andy", "Stanley", "Hank",\
                        "Marley", "Pal", "Edgar", "Rod", "Ralph",\
                        "Max", "Patches", "Spot", "Spike", "Peaches",\
                        "Golly", "Marigold", "Joaquin", "Unagi", "Speckles",\
                        "Lulu", "Precious", "Flappy", "Spanky", "Jorge"]
            self.modInventory(["other", "Beauty Contest Ticket", 0, 0, None])
            prizeMoney = int(random.randint(20,40)+self.getLevel()**1.6)
            treatments = self.treatment1Count + self.treatment2Count + self.treatment3Count
            accessory = self.checkInv("charm", ["charm", "Collar", 0, 0, None])
            score = treatments * accessory[2]
            oppScore1 = int(self.getLevel() ** 1.5 * random.random()+0.5 + random.randint(-1, 1))
            oppScore2 = int(self.getLevel() ** 1.45 * random.random()+0.5 + random.randint(-1, 1))
            oppScore3 = int(self.getLevel() ** 1.4 * random.random()+0.5 + random.randint(-1, 1))
            oppScore4 = int(self.getLevel() ** 1.35 * random.random()+0.5 + random.randint(-1, 1))
            oppScore5 = int(self.getLevel() ** 1.3 * random.random()+0.5 + random.randint(-1, 1))
            oppScore6 = int(self.getLevel() ** 1.25 * random.random()+0.5 + random.randint(-1, 1))
            oppScore7 = int(self.getLevel() ** 1.2 * random.random()+0.5 + random.randint(-1, 1))
            oppScore8 = int(self.getLevel() ** 1.15 * random.random()+0.5 + random.randint(-1, 1))
            oppScore9 = int(self.getLevel() ** 1.1 * random.random()+0.5 + random.randint(-1, 1))
            oppScore10 = int(self.getLevel() ** 1.05 * random.random()+0.5 + random.randint(-1, 1))
            oppScore11 = int(self.getLevel() * random.random()+0.5 + random.randint(-1, 1))
            scoreList = sorted([(score, self.getName()),\
                                (oppScore1, nameList.pop(random.randint(0,len(nameList)-1))),\
                                (oppScore2, nameList.pop(random.randint(0,len(nameList)-1))),\
                                (oppScore3, nameList.pop(random.randint(0,len(nameList)-1))),\
                                (oppScore4, nameList.pop(random.randint(0,len(nameList)-1))),\
                                (oppScore5, nameList.pop(random.randint(0,len(nameList)-1))),\
                                (oppScore6, nameList.pop(random.randint(0,len(nameList)-1))),\
                                (oppScore7, nameList.pop(random.randint(0,len(nameList)-1))),\
                                (oppScore8, nameList.pop(random.randint(0,len(nameList)-1))),\
                                (oppScore9, nameList.pop(random.randint(0,len(nameList)-1))),\
                                (oppScore10, nameList.pop(random.randint(0,len(nameList)-1))),\
                                (oppScore11, nameList.pop(random.randint(0,len(nameList)-1)))], reverse=True)
            results = ("--Contest Results"+"-"*25+\
                       "\n"+"1. "+str(scoreList[0][1])+" - "+str(scoreList[0][0])+" points"+\
                       "\n"+"2. "+str(scoreList[1][1])+" - "+str(scoreList[1][0])+" points"+\
                       "\n"+"3. "+str(scoreList[2][1])+" - "+str(scoreList[2][0])+" points"+\
                       "\n"+"4. "+str(scoreList[3][1])+" - "+str(scoreList[3][0])+" points"+\
                       "\n"+"5. "+str(scoreList[4][1])+" - "+str(scoreList[4][0])+" points"+\
                       "\n"+"6. "+str(scoreList[5][1])+" - "+str(scoreList[5][0])+" points"+\
                       "\n"+"7. "+str(scoreList[6][1])+" - "+str(scoreList[6][0])+" points"+\
                       "\n"+"8. "+str(scoreList[7][1])+" - "+str(scoreList[7][0])+" points"+\
                       "\n"+"9. "+str(scoreList[8][1])+" - "+str(scoreList[8][0])+" points"+\
                       "\n"+"10. "+str(scoreList[9][1])+" - "+str(scoreList[9][0])+" points"+\
                       "\n"+"11. "+str(scoreList[10][1])+" - "+str(scoreList[10][0])+" points"+\
                       "\n"+"12. "+str(scoreList[11][1])+" - "+str(scoreList[11][0])+" points")            
            
            self.modExperience(20)
            self.modHunger(15)
            self.modEnergy(-10)
            self.modHappiness(10)
            if scoreList[0][0] == score:
                self.modInventory(["collection", "Gold Medal", 0, 0, None])
                self.modMoney(prizeMoney)
                results += "\nOutstanding! You won a gold medal and $"+str(prizeMoney)+" in prize money."
            elif scoreList[1][0] == score:
                self.modInventory(["collection", "Silver Medal", 0, 0, None])
                self.modMoney(round(prizeMoney/2., 2))
                results += "\nFantastic! You won a silver medal and $"+str(prizeMoney/2.)+" in prize money."
            elif scoreList[2][0] == score:
                self.modInventory(["collection", "Bronze Medal", 0, 0, None])
                self.modMoney(round(prizeMoney/4., 2))
                results += "\nExcellent! You won a bronze medal and $"+str(prizeMoney/4.)+" in prize money."
            else:
                self.modHappiness(-20)
                results += "\nBetter luck next time."
            
            breaks = random.randint(1, 10)
            if breaks == 1 and accessory != ["charm", "Collar", 0, 0, None]:
                self.pet.inventory.remove(accessory)
                return results + "\n" + random.choice([self.getName()+"'s "+accessory[1]+" fell off in the heat of the moment.",\
                                      "The "+accessory[1]+" got wrinkled up from the contest.",\
                                      self.getName()+"'s "+accessory[1]+" has gone missing somehow.",\
                                      "Unluckily, some pet owner snatched "+self.getName()+"'s "+accessory[1]+" and ran off with it."])
            return results
        if int(time[-4:-2]) > 30:
            timeLeft = 30-(int(time[-4:-2])-30)
        else:
            timeLeft = 30-int(time[-4:-2])
        return "The beauty contest runs every half hour. Come back in "+str(timeLeft)+" minutes."

    def checkInv(self, itemType, temp):
        itemList = []
        for item in self.getInventory():
            if item[0] == itemType:
                itemList.append(item)
        for item in itemList:
            if item[2] > temp[2]:
                temp = item
        return temp
