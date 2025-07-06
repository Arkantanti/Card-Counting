#libraries
import random

import tkinter as tk
from PIL import Image, ImageTk

#create the list of cards
suits = ['clubs','spades','diamonds','hearts']
ranks = ['2','3','4','5','6','7','8','9','10','jack','queen','king','ace']
cards = []
for s in suits:
    for r in ranks:
        cards.append([r+'_of_'+s,r])

#divide cards into 4 random hands
hand1 = []
hand2 = []
hand3 = []
hand4 = []
random.shuffle(cards)

hand1 = cards[0:13]
hand2 = cards[13:26]
hand3 = cards[26:39]
hand4 = cards[39:52]
hands = [hand1,hand2,hand3,hand4]

#filters a hand for pairs, triples etc.
def rank_recount(hand_ranked,count):
    hand_recount = []
    for r in ranks:
        if hand_ranked.count(r)>count-1:
            hand_recount.append(r)
    if not hand_recount:
        return False
    else:
        return hand_recount

#check for straights
def straight_check(hand_ranked, minCount):
    temp_counter = 0
    straight_counter = 0
    for r in ranks:
        if r in hand_ranked:
            temp_counter += 1
            straight_counter = max(temp_counter,straight_counter)
            
        else:
            temp_counter = 0
    if straight_counter>minCount:
        straight_length = straight_counter
        temp_counter = 0
        straight_counter = 0       
        for r in ranks:
            if r in hand_ranked:
                temp_counter += 1
                straight_counter = max(temp_counter,straight_counter)
                if straight_counter==straight_length:
                    return [straight_length, r]
            else:
                temp_counter = 0
        
    else:
        return False
    
#checks for pair straights
def pairStraight_check(hand_ranked):
    hand_recount = rank_recount(hand_ranked,2)
    if hand_recount is False:
        return False
    else:
        return straight_check(hand_recount,1)

#function that checks which plays work from a given hand
def check_play(hand):
    hand_ranked = list(map(lambda x: x[1], hand))
    straightValue = straight_check(hand_ranked,4)
    pairStraightValue = pairStraight_check(hand_ranked)
    pairValue = rank_recount(hand_ranked,2)
    tripleValue = rank_recount(hand_ranked,3)
    if straightValue is not False:
        return ['s',straightValue]
    if pairStraightValue is not False:
        return ['ps',pairStraightValue]
    if (pairValue is not False) and (tripleValue is not False) and (len(pairValue)>1):
        if pairValue[0]==tripleValue[0]:
            return ['f',pairValue[1],tripleValue[0]]
        else:
            return ['f',pairValue[0],tripleValue[0]]
    if tripleValue is not False:
        return ['t',tripleValue[0]]
    if pairValue is not False:
        return ['p',pairValue[0]]
    return ['h',hand_ranked[0]]

#matching two arrays
def find_indices_to_delete(hand_ranked, cardsToDelete):
    indices = []
    used = set()

    for card in cardsToDelete:
        for i, val in enumerate(hand_ranked):
            if val == card and i not in used:
                indices.append(i)
                used.add(i)
                break 
    return indices

#function deletes cards from a hand after they've been played
def run_play(play,handNr):
    playType = play[0]
    cardsToDelete = []
    if playType == 'h':
        cardsToDelete.append(play[1])
    elif playType == 'p':
        cardsToDelete.append(play[1])
        cardsToDelete.append(play[1])
    elif playType == 't':
        cardsToDelete.append(play[1])
        cardsToDelete.append(play[1])
        cardsToDelete.append(play[1])
    elif playType == 'f':
        cardsToDelete.append(play[1])
        cardsToDelete.append(play[1])
        cardsToDelete.append(play[2])
        cardsToDelete.append(play[2])
        cardsToDelete.append(play[2])
    elif playType == 'ps':
        index = ranks.index(play[1][1])
        for i in range(play[1][0]):
            cardsToDelete.append(ranks[index - i])
            cardsToDelete.append(ranks[index - i])
    elif playType == 's':
        index = ranks.index(play[1][1])
        for i in range(play[1][0]):
            cardsToDelete.append(ranks[index - i])
    hand_ranked = list(map(lambda x: x[1], hands[handNr-1]))
    indicies = find_indices_to_delete(hand_ranked,cardsToDelete)
    cardsToDisplay = list(map(lambda x: hands[handNr-1][x][0], indicies))
    for i in cardsToDisplay:
        show_card(i+'.png')
    #delete the cards
    handTemp = hands[handNr-1]
    for i in sorted(indicies, reverse=True):
        del handTemp[i]
    hands[handNr-1] = handTemp
        




# Create the main window
root = tk.Tk()
root.title("Tichu Card Counter")
root.geometry("800x600")

# ---- Layout Frames ----

# Top Frame (info)
top_frame = tk.Frame(root, height=80, bg='lightgray')
top_frame.pack(side='top', fill='x')

# Middle Frame (card area)
middle_frame = tk.Frame(root, bg='green')  # use green like a table
middle_frame.pack(side='top', fill='both', expand=True)

# Bottom Frame (footer/buttons)
bottom_frame = tk.Frame(root, height=80, bg='lightgray')
bottom_frame.pack(side='bottom', fill='x')

card_area = tk.Frame(middle_frame, bg='green')
card_area.pack(expand=True)

header_text = tk.StringVar()
header_text.set("Counting Trainer")  # initial text

header_label = tk.Label(top_frame, textvariable=header_text, font=('Arial', 16), bg='lightgray')
header_label.pack(pady=20)

#function which shows cards on the screen
def show_card(card_filename):
    img = Image.open(f"cards/{card_filename}")
    img = img.resize((80, 120))  # scale down
    photo = ImageTk.PhotoImage(img)
    
    label = tk.Label(card_area, image=photo, borderwidth=1, relief="solid")
    label.image = photo  # prevent garbage collection
    label.pack(side='left', padx=5)    # add it to the screen


show_card('3_of_clubs.png')
show_card('4_of_clubs.png')


#function prints the output during each play
def play_output(handNr):
    header_text.set("Hand"+str(handNr)+":")
    currentHand = hands[handNr-1]
    play = check_play(currentHand)
    run_play(play,handNr)

currentHand = 0
def next_move():
    global currentHand
    if len(hands[0])+len(hands[1])+len(hands[2])+len(hands[3])>0:
        if currentHand==4:
            currentHand=1
        else:
            currentHand += 1
        if len(hands[currentHand-1])>0:
            for widget in card_area.winfo_children():
                widget.destroy()
            play_output(currentHand)
        else:
            next_move()
    else:
        header_text.set("All cards have been played")
    
def check_stats():
    for widget in card_area.winfo_children():
        widget.destroy()
    cards = hands[0]+hands[1]+hands[2]+hands[3]
    cards_ranked = list(map(lambda x: x[1], cards))
    occurences = []
    for r in ranks:
        occurences.append(cards_ranked.count(r))
    text = ''
    for r in ranks:
        text += '|'+r+'| '+str(occurences[ranks.index(r)])+', '
    label = tk.Label(card_area, text=text, font=("Arial", 15))
    label.pack()


next_button = tk.Button(bottom_frame, text="Next", font=('Arial', 16), command=next_move)
next_button.pack(pady=20)
stat_button = tk.Button(bottom_frame, text="Stats", font=('Arial', 16), command=check_stats)
stat_button.pack(pady=20)

root.mainloop()