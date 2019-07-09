from Tkinter import *
import tkMessageBox
import random
import os
from datetime import datetime
from Main import *

def reInitialize():
    m.timesPlayed = 0
    m.timesSlept = 0
    m.timesAte = 0

def levelUp():
    if m.getExperience() >= m.tnl():
        m.modExperience(int(-(47+(float(m.getLevel())**1.3)*3.0)))
        m.modLevel(1)
        msg = (m.getName()+" has grown.")
        if m.getEvolution()*5 == m.getLevel() and m.getLevel() < 21:
            m.modEvolution(1)
            msg += (" "+m.getName()+" looks a little different, too.")
        
        addMessage(msg)
        levelUp()


def disableButtons():
    food1['state'] = "disabled"
    food2['state'] = "disabled"
    food3['state'] = "disabled"
    feed['state'] = "disabled"
    play['state'] = "disabled"
    sleep['state'] = "disabled"
    town['state'] = "disabled"
    filemenu.entryconfig(0, state="disabled")
    filemenu.entryconfig(1, state="disabled")    

def update():
    levelUp()
    title['text'] = m.getName()
    if m.getSpecies() == "Cat":
        firstIndex = 0
    elif m.getSpecies() == "Dog":
        firstIndex = 1
    elif m.getSpecies() == "Bat":
        firstIndex = 2
    elif m.getSpecies() == "Frog":
        firstIndex = 3
    elif m.getSpecies() == "Monkey":
        firstIndex = 4
    elif m.getSpecies() == "Panda":
        firstIndex = 5

    if str(m.getMoney())[-2] == ".":
        moneyText = str(m.getMoney())+"0"
    else:
        moneyText = str(m.getMoney())
    secondIndex = m.getEvolution()-1
    petImage['image'] = petList[firstIndex][secondIndex]
    levelLabel['text'] = "Level "+str(m.getLevel())
    moneyLabel['text'] = "$"+moneyText
    expBar['image'] = expBarList[int(((float(m.getExperience()-1)/float(m.tnl()))*10)+1)]
    hapBar['image'] = hpBarList[20 - (((m.getHappiness()-1)/5)+1)]
    eneBar['image'] = hpBarList[20 - (((m.getEnergy()-1)/5)+1)]
    hunBar['image'] = nrgBarList[20 - (((m.getHunger()-1)/5)+1)]
    autosaveButton['state'] = "normal"

def updateMenu():
    if m.pet:
        menubar.entryconfig(2, state="normal")
        filemenu.entryconfig(2, state="normal")
    else:
        menubar.entryconfig(2, state="disabled")
    if os.path.exists(os.path.abspath("data\\autosave")+".txt"):
        loadmenu.entryconfig(0, state="normal")
    else:
        loadmenu.entryconfig(0, state="disabled")
    if os.path.exists(os.path.abspath("data\\save1")+".txt"):
        loadmenu.entryconfig(2, state="normal")
    else:
        loadmenu.entryconfig(2, state="disabled")
    if os.path.exists(os.path.abspath("data\\save2")+".txt"):
        loadmenu.entryconfig(3, state="normal")
    else:
        loadmenu.entryconfig(3, state="disabled")
    if os.path.exists(os.path.abspath("data\\save3")+".txt"):
        loadmenu.entryconfig(4, state="normal")
    else:
        loadmenu.entryconfig(4, state="disabled")

def timeUpdate():
    if m.pet:
        experienceValue = 10
        happinessValue = -1
        for i in range(m.getEnergy(), 91, 10):
            experienceValue -= 1
        for i in range(100-m.getHunger(), 91, 20):
            happinessValue -= 1
        m.modExperience(experienceValue)
        m.modHappiness(happinessValue)
        m.modEnergy(-1)
        m.modHunger(int(2*(m.getLevel()/20.+1.)))

        if (int(curTime[-4:-2]) > 5 or int(curTime[-4:-2]) == 0) and\
           ["other", "Race Ticket", 0, 0, None] in m.getInventory():
                m.pet.inventory.remove(["other", "Race Ticket", 0, 0, None])
        if ((5 < int(curTime[-4:-2]) < 30) or int(curTime[-4:-2]) > 35\
            or int(curTime[-4:-2]) == 0 or int(curTime[-4:-2]) == 30) and\
            ["other", "Beauty Contest Ticket", 0, 0, None] in m.getInventory():
                m.pet.inventory.remove(["other", "Beauty Contest Ticket", 0, 0, None])
        if int(curTime[-4:-2]) % 15 == 0:
            reInitialize()
        if int(curTime[-4:-2]) % 30 == 0 and m.treatment1Count != 0:
            m.treatment1Count -= 1
        if int(curTime[-4:-2]) == 0 and m.treatment1Count != 0:
            m.treatment2Count -= 1
                
        update()
    if saveVar.get() == 1:
        m.save("autosave")
        updateMenu()

def addMessage(msg):
    elBox['state'] = "normal"
    elBox.insert(END, "\n"+msg)
    elBox.yview(END)
    elBox['state'] = "disabled"

def patGUI():
    msg = m.play()
    if msg:
        addMessage(msg)
    update()

def wake():
    addMessage(m.getName()+" woke up.")
    filemenu.entryconfig(0, state="normal")
    filemenu.entryconfig(1, state="normal")
    homeSetup()

def sleepGUI():
    msg = m.sleep()
    if msg:
        addMessage(msg)
    update()
    disableButtons()
    root.after(random.randint(30000, 60000), wake)
    
def feedGUI():
    if int(foodVar.get()) > 0:
        msg = m.feed(int(foodVar.get()))
        if msg:
            addMessage(msg)
        update()
    else:
        addMessage("Select a food item first.")

def townGUI():
    global hider
    hider = Label(frame, image=townImg)
    hider.grid(column=1, row=2, rowspan=4, sticky=N+E+S+W)
    foodVar.set(0)
    feed.config(text="Pet Supplies", relief="raised", command=supplySetup,\
                state="normal")
    play.config(text="Grooming Salon", relief="raised", command=salonSetup,\
               state="normal")
    sleep.config(text="Pet Show", relief="raised", command=showSetup,\
                 state="normal")
    town.config(text="Go Home", relief="raised", command=homeSetup,\
                state="normal")
    
def homeSetup():
    global hider
    if hider:
        hider.destroy()
    hider = None
    foodFrame['text'] = "Food"
    food1.config(image=food1Img, value=1, state="normal")
    food2.config(image=food2Img, value=2, state="normal")
    food3.config(image=food3Img, value=3, state="normal")
    food1price['text'] = "$0.25"
    food2price['text'] = "$2"
    food3price['text'] = "$10"
    feed.config(text="Feed", command=feedGUI, state="normal", relief="raised")
    play.config(text="Play", command=patGUI, state="normal", relief="raised")
    sleep.config(text="Sleep", command=sleepGUI, state="normal", relief="raised")
    town.config(text="Go to Town", command=townGUI, state="normal", relief="raised")

def buyGUI():
    for category in ([[["energy", "Pink Pet Bed", 25, 10, "bedList[0]"],\
                       ["energy", "Doghouse", 40, 45, "bedList[1]"],\
                       ["energy", "Large Comfy Chair", 55, 300, "bedList[2]"],\
                       ["energy", "White Bed", 70, 550, "bedList[3]"],\
                       ["energy", "King-Sized Bed", 85, 1000, "bedList[4]"]],\
                      \
                      [["happiness", "Toy Mouse", 1, 3, "toyList[0]"],\
                       ["happiness", "Laser Pointer", 2, 8, "toyList[1]"],\
                       ["happiness", "Ball", 3, 15, "toyList[2]"],\
                       ["happiness", "Teddy Bear", 4, 30, "toyList[3]"],\
                       ["happiness", "RC Bird", 5, 80, "toyList[4]"]],\
                      \
                      [["charm", "Ribbon", 1, 2, "accList[0]"],\
                       ["charm", "Balloon", 2, 5, "accList[1]"],\
                       ["charm", "Top Hat", 3, 25, "accList[2]"],\
                       ["charm", "Fancy Coat", 4, 100, "accList[3]"],\
                       ["charm", "Rhinestone Collar", 5, 200, "accList[4]"]]]):
        for item in category:
            if foodVar.get() == item[1]:
                msg = m.buy(item)
                if "can't" not in msg:
                    update()
                    if food1['value'] == foodVar.get():
                        food1['state'] = "disabled"
                    elif food2['value'] == foodVar.get():
                        food2['state'] = "disabled"
                    elif food3['value'] == foodVar.get():
                        food3['state'] = "disabled"
                    foodVar.set(0)
                addMessage(msg)
                return
    addMessage("Select an item to purchase first.")

def supplySetup():
    global hider
    hider.destroy()
    foodFrame['text'] = "Store"
    supplyInv = ([[["energy", "Pink Pet Bed", 25, 10, "bedList[0]"],\
                   ["energy", "Doghouse", 40, 45, "bedList[1]"],\
                   ["energy", "Large Comfy Chair", 55, 300, "bedList[2]"],\
                   ["energy", "White Bed", 70, 550, "bedList[3]"],\
                   ["energy", "King-Sized Bed", 85, 1000, "bedList[4]"]],\
                  \
                  [["happiness", "Toy Mouse", 1, 3, "toyList[0]"],\
                   ["happiness", "Laser Pointer", 2, 8, "toyList[1]"],\
                   ["happiness", "Ball", 3, 15, "toyList[2]"],\
                   ["happiness", "Teddy Bear", 4, 30, "toyList[3]"],\
                   ["happiness", "RC Bird", 5, 80, "toyList[4]"]],\
                  \
                  [["charm", "Ribbon", 1, 2, "accList[0]"],\
                   ["charm", "Balloon", 2, 5, "accList[1]"],\
                   ["charm", "Top Hat", 3, 25, "accList[2]"],\
                   ["charm", "Fancy Coat", 4, 100, "accList[3]"],\
                   ["charm", "Rhinestone Collar", 5, 200, "accList[4]"]]])
    for categoryInv in supplyInv:
        for item in m.getInventory():
            if item in categoryInv:
                categoryInv.remove(item)
    if supplyInv[0] != []:
        food1.config(image=eval(supplyInv[0][0][4]), value=supplyInv[0][0][1],\
                     state="normal")
        food1price['text'] = "$"+str(supplyInv[0][0][3])
    else:
        food1.config(image=bed5, state="disabled")
        food1price['text'] = "Sold"
    if supplyInv[1] != []:    
        food2.config(image=eval(supplyInv[1][0][4]), value=supplyInv[1][0][1],\
                     state="normal")
        food2price['text'] = "$"+str(supplyInv[1][0][3])
    else:
        food2.config(image=toy5, state="disabled")
        food2price['text'] = "Sold"
    if supplyInv[2] != []:
        food3.config(image=eval(supplyInv[2][0][4]), value=supplyInv[2][0][1],\
                     state="normal")
        food3price['text'] = "$"+str(supplyInv[2][0][3])
    else:
        food3.config(image=acc5, state="disabled")
        food3price['text'] = "Sold"
    feed.config(text="Buy", command=buyGUI, state="normal")
    play.config(text="", relief="flat", state="disabled")
    sleep.config(text="", relief="flat", state="disabled")
    town.config(text="Back", command=townGUI, state="normal")

def salonGUI():
    if int(foodVar.get()) > 0:
        msg = m.salon(int(foodVar.get()))
        if msg:
            addMessage(msg)
        update()
    else:
        addMessage("Select a salon treatment first.")
    
def salonSetup():
    global hider
    hider.destroy()
    foodFrame['text'] = "Salon"
    food1.config(image=salon1Img, value=1, state="normal")
    food2.config(image=salon2Img, value=2, state="normal")
    food3.config(image=salon3Img, value=3, state="normal")
    food1price['text'] = "$10"
    food2price['text'] = "$20"
    food3price['text'] = "$30"
    feed.config(text="Buy", command=salonGUI, state="normal")
    play.config(text="", relief="flat", state="disabled")
    sleep.config(text="", relief="flat", state="disabled")
    town.config(text="Back", command=townGUI, state="normal")

def talentResults():
    addMessage(m.talent(curStats))
    filemenu.entryconfig(0, state="normal")
    filemenu.entryconfig(1, state="normal")
    update()
    showSetup()

def showGUI():
    global curStats
    if int(foodVar.get()) == 1:
        addMessage(m.race(curTime))
        update()
    elif int(foodVar.get()) == 2:
        addMessage("You enter "+m.getName()+" in the talent show.")
        disableButtons()
        curStats = 100+m.getHappiness()+m.getEnergy()-m.getHunger()
        root.after(300000, talentResults)
    elif int(foodVar.get()) == 3:
        addMessage(m.beauty(curTime))
        update()

def showSetup():
    global hider
    hider.destroy()
    foodFrame['text'] = "Competitions"
    food1.config(image=show1Img, value=1, state="normal")
    food2.config(image=show2Img, value=2, state="normal")
    food3.config(image=show3Img, value=3, state="normal")
    food1price['text'] = "Speed"
    food2price['text'] = "Talent"
    food3price['text'] = "Beauty"
    feed.config(text="Participate", command=showGUI, state="normal")
    play.config(text="", relief="flat", state="disabled")
    sleep.config(text="", relief="flat", state="disabled")
    town.config(text="Back", command=townGUI, state="normal")

def greeting():
    if m.getSpecies()[-1] == "a" or\
       m.getSpecies()[-1] == "e" or\
       m.getSpecies()[-1] == "i" or\
       m.getSpecies()[-1] == "o" or\
       m.getSpecies()[-1] == "u" or\
       m.getSpecies()[-1] == "y":
        ish = m.getSpecies().lower()
    else:
        ish = (m.getSpecies()+m.getSpecies()[-1]).lower()
    msgList = ["\nWelcome back "+m.getName()+"!",\
               "\n"+m.getName()+" missed you dearly.",\
               "\n"+m.getName()+" just woke up from a long nap.",\
               "\n"+m.getName()+" is feeling very "+ish+"ish today.",\
               "\nIt's "+curTime+"! Where have you been? "+m.getName()+" has been looking all over for you.",\
               "\n"+m.getName()+" is ready for another exciting day.",\
               "\n"+m.getName()+" is ecstatic to see you!"]
    msg = "-"*40+random.choice(msgList)
    addMessage(msg)

def load0():
    m.load("autosave")
    reInitialize()
    greeting()
    homeSetup()
    updateMenu()
    update()
        
def load1():
    m.load("save1")
    reInitialize()
    greeting()
    homeSetup()
    updateMenu()
    update()

def load2():
    m.load("save2")
    reInitialize()
    greeting()
    homeSetup()
    updateMenu()
    update()

def load3():
    m.load("save3")
    reInitialize()
    greeting()
    homeSetup()
    updateMenu()
    update()

def save1():
    m.save("save1")
    updateMenu()

def save2():
    m.save("save2")
    updateMenu()

def save3():
    m.save("save3")
    updateMenu()

def newPopUp():
    global topWindow
    topWindow = Toplevel()
    topWindow.title("New")
    popUpTitle = Label(topWindow, text="New Pet", font=("Tahoma", 24))
    nameLabel = Label(topWindow, text="Name: ")
    nameBox = Entry(topWindow, textvariable=n, width=16)
    speciesFrame = LabelFrame(topWindow, text="Species")
    species1Button = Radiobutton(speciesFrame, text="Cat", variable=speciesVar, value="Cat")
    species2Button = Radiobutton(speciesFrame, text="Dog", variable=speciesVar, value="Dog")
    species3Button = Radiobutton(speciesFrame, text="Bat", variable=speciesVar, value="Bat")
    species4Button = Radiobutton(speciesFrame, text="Frog", variable=speciesVar, value="Frog")
    species5Button = Radiobutton(speciesFrame, text="Monkey", variable=speciesVar, value="Monkey")
    species6Button = Radiobutton(speciesFrame, text="Panda", variable=speciesVar, value="Panda")
    species7Button = Radiobutton(speciesFrame, text="Surprise Me!", variable=speciesVar, value="random")
    sheepLabel = Label(topWindow, image=sheepImg)
    confirm = Button(topWindow, text="Ok", command=newGame, width=10)
    popUpTitle.grid(column=1, row=1, columnspan=4, padx=10)
    nameLabel.grid(column=1, row=2, padx=5)
    nameBox.grid(column=2, row=2)
    speciesFrame.grid(column=3, row=2, columnspan=2, rowspan=4, padx=5, ipadx=10)
    sheepLabel.grid(column=1, row=3, columnspan=2, rowspan=3)
    species1Button.grid(row=1, column=1, sticky=W)
    species2Button.grid(row=2, column=1, sticky=W)
    species3Button.grid(row=3, column=1, sticky=W)
    species4Button.grid(row=4, column=1, sticky=W)
    species5Button.grid(row=5, column=1, sticky=W)
    species6Button.grid(row=6, column=1, sticky=W)
    species7Button.grid(row=7, column=1, sticky=W)
    confirm.grid(column=1, row=6, columnspan=4, ipadx=10, pady=5)

def collectionPopUp():
    tempInv = list(m.getInventory())
    topWindow = Toplevel()
    topWindow.title("Collection")
    popUpTitle = Label(topWindow, text=m.getName()+"'s Collection", font=("Tahoma", 24))
    trophyFrame = LabelFrame(topWindow, text="Trophies")
    shelfLabel = Label(trophyFrame, image=shelfImg)
    medalFrame = LabelFrame(topWindow, text="Medals")
    medal1 = Label(medalFrame, image=medal1Img)
    medal2 = Label(medalFrame, image=medal2Img)
    medal3 = Label(medalFrame, image=medal3Img)

    for i in [["collection", "Gold Medal", 0, 0, None],["collection", "Silver Medal", 0, 0, None],["collection", "Bronze Medal", 0, 0, None]]:
        medals = 0
        while i in tempInv:
            tempInv.remove(i)
            medals += 1
        if i == ["collection", "Gold Medal", 0, 0, None]:
            medal1Text = Label(medalFrame, text=medals)
        elif i == ["collection", "Silver Medal", 0, 0, None]:
            medal2Text = Label(medalFrame, text=medals)
        elif i == ["collection", "Bronze Medal", 0, 0, None]:
            medal3Text = Label(medalFrame, text=medals)

    xCount = 1
    yCount = 1
    while ["collection", "Trophy", 0, 0, None] in tempInv:
        tempInv.remove(["collection", "Trophy", 0, 0, None])
        trophyLabel = Label(trophyFrame, image=trophyImg, border=0)
        trophyLabel.grid(column=xCount, row=yCount)
        xCount += 1
        if xCount > 3:
            xCount -= 3
            yCount += 1

    while yCount < 4 and xCount < 4:
        trophyLabel = Label(trophyFrame, image=tileImg, border=0)
        trophyLabel.grid(column=xCount, row=yCount)
        xCount += 1
        if xCount > 3:
            xCount -= 3
            yCount += 1

    popUpTitle.grid(column=1, row=1, padx=20, pady=10)
    trophyFrame.grid(column=1, row=2, padx=20, pady=10)
    shelfLabel.grid(column=1, row=1, columnspan=3, rowspan=3)
    medalFrame.grid(column=1, row=3, pady=10)
    medal1.grid(column=1, row=1, sticky=W, ipadx=10)
    medal1Text.grid(column=1, row=1, sticky=E)
    medal2.grid(column=2, row=1, sticky=W, ipadx=10)
    medal2Text.grid(column=2, row=1, sticky=E)
    medal3.grid(column=3, row=1, sticky=W, ipadx=10)
    medal3Text.grid(column=3, row=1, sticky=E)

def viewItem():
    global infoBox
    itemInfo = eval(invVar.get())[0]
    infoBox['state'] = "normal"
    infoBox.delete(1.0, END)
    infoBox.insert(END, itemInfo[1]+"\n"+"Increases "+itemInfo[0]+" by "+\
                   str(itemInfo[2])+"\nWorth $"+str(itemInfo[3]))
    infoBox['state'] = "disabled"
    

def inventoryPopUp():
    global infoBox
    invVar.set(0)
    topWindow = Toplevel()
    topWindow.title("Inventory")
    popUpTitle = Label(topWindow, text="Your Items", font=("Tahoma", 24))
    bedsFrame = LabelFrame(topWindow, text="Beds")
    toysFrame = LabelFrame(topWindow, text="Toys")
    accessoriesFrame = LabelFrame(topWindow, text="Accessories")
    boxFrame = LabelFrame(topWindow, text="Info")
    infoBox = Text(boxFrame, width=25, height=3, font=("Tahoma", 8), state="disabled")

    buttonList = []
    tempList = []
    for i in range(1,6):
        itemButton = Radiobutton(bedsFrame, variable=invVar, command=viewItem,\
                                 value=i, width=32, height=32, indicatoron=0,\
                                 activebackground="#71A6D2")
        tempList.append(itemButton)
        itemButton.grid(row=1, column=i)
    buttonList.append(tempList)
    tempList = []
    for i in range(1,6):
        itemButton = Radiobutton(toysFrame, variable=invVar, command=viewItem,\
                                 value=i*10, width=32, height=32, indicatoron=0,\
                                 activebackground="#71A6D2")
        tempList.append(itemButton)
        itemButton.grid(row=1, column=i)
    buttonList.append(tempList)
    tempList = []
    for i in range(1,6):
        itemButton = Radiobutton(accessoriesFrame, variable=invVar, command=viewItem,\
                                 value=i*100, width=32, height=32, indicatoron=0,\
                                 activebackground="#71A6D2")
        tempList.append(itemButton)
        itemButton.grid(row=1, column=i)
    buttonList.append(tempList)

    for item in m.getInventory():
        if item[0] == "energy":
            buttonList[0][0].config(image=eval(item[4]), value=[item])
            del buttonList[0][0]
        elif item[0] == "happiness":
            buttonList[1][0].config(image=eval(item[4]), value=[item])
            del buttonList[1][0]
        elif item[0] == "charm":
            buttonList[2][0].config(image=eval(item[4]), value=[item])
            del buttonList[2][0]

    for category in buttonList:
        for item in category:
            item.config(image=qmark, state="disabled")
        
    popUpTitle.grid(column=1, row=1, padx=10, pady=10, columnspan=2)
    bedsFrame.grid(column=1, row=2, padx=10, pady=10)
    toysFrame.grid(column=1, row=3, padx=10, pady=10)
    accessoriesFrame.grid(column=1, row=4, padx=10, pady=10)
    boxFrame.grid(column=2, row=2, rowspan=3, padx=10)
    infoBox.grid(column=1, row=1)

def newGame():
    global m
    if speciesVar.get() == "random":
        species = random.choice(["Bat","Cat","Dog","Frog","Monkey","Panda"])
    else:
        species = speciesVar.get()
    title['text'] = n.get()
    petInfo = [n.get(), species, 1, 0, 1, 100, 100, 0, 1, []]
    topWindow.destroy()
    m.new(petInfo)
    addMessage("-"*40+"\nYou have adopted "+m.getName()+" the baby "+m.getSpecies()+".")
    reInitialize()
    homeSetup()
    updateMenu()
    update()

def exitDialog():
    if tkMessageBox.askyesno("Exit", "Are you sure?"):
        if saveVar.get() == 1:
            m.save("autosave")
        root.destroy()

def setTime():
    global curTime
    if datetime.time(datetime.now()).hour > 12:
        hour = datetime.time(datetime.now()).hour - 12
        AMPM = "PM"
    else:
        hour = datetime.time(datetime.now()).hour
        AMPM = "AM"
    if hour == 12:
        AMPM = "PM"
    elif hour == 0:
        hour = 12
    minute = datetime.time(datetime.now()).minute
    if len(str(minute)) == 1:
        minute = "0"+str(minute)
    curTime = str(hour)+":"+str(minute)+AMPM
    timeLabel['text'] = curTime
    if datetime.time(datetime.now()).second < 3:
        timeUpdate()
        root.after(60000, setTime)
    else:
        root.after(1000, setTime)

m = Main()
root = Tk()
root.title("Pets")

root.after(1, setTime)

moneyImg = PhotoImage(file="data\\make-money.gif")
shelfImg = PhotoImage(file="data\\shelf.gif")
trophyImg = PhotoImage(file="data\\trophy.gif")
medal1Img = PhotoImage(file="data\\medal1.gif")
medal2Img = PhotoImage(file="data\\medal2.gif")
medal3Img = PhotoImage(file="data\\medal3.gif")
tileImg = PhotoImage(file="data\\tile.gif")
clockImg = PhotoImage(file="data\\clock.gif")
food1Img = PhotoImage(file="data\\apple.gif")
food2Img = PhotoImage(file="data\\meat.gif")
food3Img = PhotoImage(file="data\\chicken.gif")
salon1Img = PhotoImage(file="data\\groom1.gif")
salon2Img = PhotoImage(file="data\\groom2.gif")
salon3Img = PhotoImage(file="data\\groom3.gif")
show1Img = PhotoImage(file="data\\show1.gif")
show2Img = PhotoImage(file="data\\show2.gif")
show3Img = PhotoImage(file="data\\show3.gif")
townImg = PhotoImage(file="data\\town.gif")
qmark = PhotoImage(file="data\\questionmark.gif")
sheepImg = PhotoImage(file="data\\sheep.gif")
cat1 = PhotoImage(file="data\\cat1.gif")
cat2 = PhotoImage(file="data\\cat2.gif")
cat3 = PhotoImage(file="data\\cat3.gif")
cat4 = PhotoImage(file="data\\cat4.gif")
cat5 = PhotoImage(file="data\\cat5.gif")
dog1 = PhotoImage(file="data\\dog1.gif")
dog2 = PhotoImage(file="data\\dog2.gif")
dog3 = PhotoImage(file="data\\dog3.gif")
dog4 = PhotoImage(file="data\\dog4.gif")
dog5 = PhotoImage(file="data\\dog5.gif")
bat1 = PhotoImage(file="data\\bat1.gif")
bat2 = PhotoImage(file="data\\bat2.gif")
bat3 = PhotoImage(file="data\\bat3.gif")
bat4 = PhotoImage(file="data\\bat4.gif")
bat5 = PhotoImage(file="data\\bat5.gif")
frog1 = PhotoImage(file="data\\frog1.gif")
frog2 = PhotoImage(file="data\\frog2.gif")
frog3 = PhotoImage(file="data\\frog3.gif")
frog4 = PhotoImage(file="data\\frog4.gif")
frog5 = PhotoImage(file="data\\frog5.gif")
monkey1 = PhotoImage(file="data\\monkey1.gif")
monkey2 = PhotoImage(file="data\\monkey2.gif")
monkey3 = PhotoImage(file="data\\monkey3.gif")
monkey4 = PhotoImage(file="data\\monkey4.gif")
monkey5 = PhotoImage(file="data\\monkey5.gif")
panda1 = PhotoImage(file="data\\panda1.gif")
panda2 = PhotoImage(file="data\\panda2.gif")
panda3 = PhotoImage(file="data\\panda3.gif")
panda4 = PhotoImage(file="data\\panda4.gif")
panda5 = PhotoImage(file="data\\panda5.gif")
hp0 = PhotoImage(file="data\\hpbar0.gif")
hp1 = PhotoImage(file="data\\hpbar1.gif")
hp2 = PhotoImage(file="data\\hpbar2.gif")
hp3 = PhotoImage(file="data\\hpbar3.gif")
hp4 = PhotoImage(file="data\\hpbar4.gif")
hp5 = PhotoImage(file="data\\hpbar5.gif")
hp6 = PhotoImage(file="data\\hpbar6.gif")
hp7 = PhotoImage(file="data\\hpbar7.gif")
hp8 = PhotoImage(file="data\\hpbar8.gif")
hp9 = PhotoImage(file="data\\hpbar9.gif")
hp10 = PhotoImage(file="data\\hpbar10.gif")
hp11 = PhotoImage(file="data\\hpbar11.gif")
hp12 = PhotoImage(file="data\\hpbar12.gif")
hp13 = PhotoImage(file="data\\hpbar13.gif")
hp14 = PhotoImage(file="data\\hpbar14.gif")
hp15 = PhotoImage(file="data\\hpbar15.gif")
hp16 = PhotoImage(file="data\\hpbar16.gif")
hp17 = PhotoImage(file="data\\hpbar17.gif")
hp18 = PhotoImage(file="data\\hpbar18.gif")
hp19 = PhotoImage(file="data\\hpbar19.gif")
nrg0 = PhotoImage(file="data\\nrgbar0.gif")
nrg1 = PhotoImage(file="data\\nrgbar1.gif")
nrg2 = PhotoImage(file="data\\nrgbar2.gif")
nrg3 = PhotoImage(file="data\\nrgbar3.gif")
nrg4 = PhotoImage(file="data\\nrgbar4.gif")
nrg5 = PhotoImage(file="data\\nrgbar5.gif")
nrg6 = PhotoImage(file="data\\nrgbar6.gif")
nrg7 = PhotoImage(file="data\\nrgbar7.gif")
nrg8 = PhotoImage(file="data\\nrgbar8.gif")
nrg9 = PhotoImage(file="data\\nrgbar9.gif")
nrg10 = PhotoImage(file="data\\nrgbar10.gif")
nrg11 = PhotoImage(file="data\\nrgbar11.gif")
nrg12 = PhotoImage(file="data\\nrgbar12.gif")
nrg13 = PhotoImage(file="data\\nrgbar13.gif")
nrg14 = PhotoImage(file="data\\nrgbar14.gif")
nrg15 = PhotoImage(file="data\\nrgbar15.gif")
nrg16 = PhotoImage(file="data\\nrgbar16.gif")
nrg17 = PhotoImage(file="data\\nrgbar17.gif")
nrg18 = PhotoImage(file="data\\nrgbar18.gif")
nrg19 = PhotoImage(file="data\\nrgbar19.gif")
exp0 = PhotoImage(file="data\\expbar0.gif")
exp1 = PhotoImage(file="data\\expbar1.gif")
exp2 = PhotoImage(file="data\\expbar2.gif")
exp3 = PhotoImage(file="data\\expbar3.gif")
exp4 = PhotoImage(file="data\\expbar4.gif")
exp5 = PhotoImage(file="data\\expbar5.gif")
exp6 = PhotoImage(file="data\\expbar6.gif")
exp7 = PhotoImage(file="data\\expbar7.gif")
exp8 = PhotoImage(file="data\\expbar8.gif")
exp9 = PhotoImage(file="data\\expbar9.gif")
exp10 = PhotoImage(file="data\\expbar10.gif")
bed1 = PhotoImage(file="data\\bed1.gif")
bed2 = PhotoImage(file="data\\bed2.gif")
bed3 = PhotoImage(file="data\\bed3.gif")
bed4 = PhotoImage(file="data\\bed4.gif")
bed5 = PhotoImage(file="data\\bed5.gif")
toy1 = PhotoImage(file="data\\toy1.gif")
toy2 = PhotoImage(file="data\\toy2.gif")
toy3 = PhotoImage(file="data\\toy3.gif")
toy4 = PhotoImage(file="data\\toy4.gif")
toy5 = PhotoImage(file="data\\toy5.gif")
acc1 = PhotoImage(file="data\\acc1.gif")
acc2 = PhotoImage(file="data\\acc2.gif")
acc3 = PhotoImage(file="data\\acc3.gif")
acc4 = PhotoImage(file="data\\acc4.gif")
acc5 = PhotoImage(file="data\\acc5.gif")

petList = [[cat1, cat2, cat3, cat4, cat5],\
           [dog1, dog2, dog3, dog4, dog5],\
           [bat1, bat2, bat3, bat4, bat5],\
           [frog1, frog2, frog3, frog4, frog5],\
           [monkey1, monkey2, monkey3, monkey4, monkey5],\
           [panda1, panda2, panda3, panda4, panda5]]

hpBarList = [hp0, hp1, hp2, hp3, hp4, hp5, hp6, hp7,\
             hp8, hp9, hp10, hp11, hp12, hp13, hp14,\
             hp15, hp16, hp17, hp18, hp19, exp0]
nrgBarList = [nrg0, nrg1, nrg2, nrg3, nrg4, nrg5, nrg6, nrg7,\
              nrg8, nrg9, nrg10, nrg11, nrg12, nrg13, nrg14,\
              nrg15, nrg16, nrg17, nrg18, nrg19, exp0]
expBarList = [exp0, exp1, exp2, exp3, exp4, exp5,\
              exp6, exp7, exp8, exp9, exp10]

bedList = [bed1, bed2, bed3, bed4, bed5]
toyList = [toy1, toy2, toy3, toy4, toy5]
accList = [acc1, acc2, acc3, acc4, acc5]

speciesVar = StringVar()
speciesVar.set("random")
invVar = StringVar()
invVar.set(0)
saveVar = IntVar()
foodVar = StringVar()
foodVar.set(0)
n = StringVar()
hider = None
curStats = 0

frame = Frame(root, relief="ridge")
title = Label(frame, text="Pets", font=("Tahoma", 24))
autosaveButton = Checkbutton(frame, text="Autosave", variable = saveVar,\
                             bg="red", bd=3, selectcolor="green",\
                             indicatoron=False, state="disabled")
petImage = Label(frame, image=random.choice(random.choice(petList)),\
                 width=160, height=160)
foodFrame = LabelFrame(frame, text="Food")
food1 = Radiobutton(foodFrame, image=food1Img, variable=foodVar, value=1,\
                    indicatoron=False, activebackground="#FF7518",\
                    width=32, height=32, state="disabled")
food2 = Radiobutton(foodFrame, image=food2Img, variable=foodVar, value=4,\
                    indicatoron=False, activebackground="#FF7518",\
                    width=32, height=32, state="disabled")
food3 = Radiobutton(foodFrame, image=food3Img, variable=foodVar, value=10,\
                    indicatoron=False, activebackground="#FF7518",\
                    width=32, height=32, state="disabled")
food1price = Label(foodFrame, text="$0.25")
food2price = Label(foodFrame, text="$2")
food3price = Label(foodFrame, text="$10")

timeFrame = Frame(frame)
timeImage = Label(timeFrame, image=clockImg)
timeLabel = Label(timeFrame, font=("Tahoma", 10), width=7)

statsFrame = LabelFrame(frame, text="Stats")
levelLabel = Label(statsFrame, text="Level 0", font=("Tahoma", 10),\
                   relief="ridge", width=8, height=2)
moneyFrame = Frame(statsFrame)
moneyImage = Label(moneyFrame, image=moneyImg)
moneyLabel = Label(moneyFrame, text="$0.00", font=("Tahoma", 10))
experienceLabel = Label(statsFrame, text="Experience")
happinessLabel = Label(statsFrame, text="Happiness")
energyLabel = Label(statsFrame, text="Energy")
hungerLabel = Label(statsFrame, text="Hunger")
expBar = Label(statsFrame, image=exp0)
hapBar = Label(statsFrame, image=exp0)
eneBar = Label(statsFrame, image=exp0)
hunBar = Label(statsFrame, image=exp0)
feed = Button(frame, text="Feed", command=feedGUI, width=14, state="disabled")
play = Button(frame, text="Play", command=patGUI, width=14, state="disabled")
sleep = Button(frame, text="Sleep", command=sleepGUI, width=14,\
               state="disabled")
town = Button(frame, text="Go to Town", command=townGUI, width=14,\
              state="disabled")

scroll = Scrollbar(frame, orient="vertical")
elBox = Text(frame, font=("Tahoma", 8), width=100, height=6,\
             yscrollcommand=scroll.set)
elBox.insert(END, "Welcome to Pets! Click File > New to start a new game.")
elBox['state'] = "disabled"
scroll['command'] = elBox.yview

menubar = Menu(root)
root['menu'] = menubar

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=newPopUp)
menubar.add_cascade(label="File", menu=filemenu)

loadmenu = Menu(menubar, tearoff=0)
loadmenu.add_command(label="Autosave", command=load0)
loadmenu.add_separator()
loadmenu.add_command(label="File 1", command=load1)
loadmenu.add_command(label="File 2", command=load2)
loadmenu.add_command(label="File 3", command=load3)
filemenu.add_cascade(label="Load", menu=loadmenu)

savemenu = Menu(menubar, tearoff=0)
savemenu.add_command(label="File 1", command=save1)
savemenu.add_command(label="File 2", command=save2)
savemenu.add_command(label="File 3", command=save3)
filemenu.add_cascade(label="Save", menu=savemenu, state="disabled")

filemenu.add_command(label="Exit", command=exitDialog)

viewmenu = Menu(menubar, tearoff=0)
viewmenu.add_command(label="Collection", command=collectionPopUp)
viewmenu.add_command(label="Inventory", command=inventoryPopUp)
menubar.add_cascade(label="View", menu=viewmenu)

frame.grid()
title.grid(column=1, columnspan=3, row=1, padx=100, pady=10)
autosaveButton.grid(column=1, row=1)
petImage.grid(column=2, row=2, rowspan=8)
foodFrame.grid(column=1, row=2, rowspan=4)
food1.grid(column=1, row=1)
food2.grid(column=2, row=1)
food3.grid(column=3, row=1)
food1price.grid(column=1, row=2)
food2price.grid(column=2, row=2)
food3price.grid(column=3, row=2)
timeFrame.grid(column=3, row=1, columnspan=2, padx=10, sticky=E)
timeImage.grid(column=1, row=1)
timeLabel.grid(column=2, row=1)
statsFrame.grid(column=3, row=2, rowspan=8, columnspan=2, padx=10)
levelLabel.grid(column=1, row=1, padx=5)
moneyFrame.grid(column=2, row=1)
moneyImage.grid(column=1, row=1)
moneyLabel.grid(column=2, row=1)
experienceLabel.grid(column=1, row=2)
happinessLabel.grid(column=1, row=3)
energyLabel.grid(column=1, row=4)
hungerLabel.grid(column=1, row=5)
expBar.grid(column=2, row=2)
hapBar.grid(column=2, row=3)
eneBar.grid(column=2, row=4)
hunBar.grid(column=2, row=5)
feed.grid(column=1, row=6)
play.grid(column=1, row=7)
sleep.grid(column=1, row=8)
town.grid(column=1, row=9)
elBox.grid(column=1, row=10, columnspan=3)
scroll.grid(column=4, row=10,  sticky=N+S)

updateMenu()
root.protocol("WM_DELETE_WINDOW", exitDialog)
root.mainloop()
