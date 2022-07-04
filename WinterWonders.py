from tkinter import *
from tkinter import ttk
import GameObject

turns = 0

command_widget = None
image_label = None
description_widget = None
inventory_widget = None
north_button = None
south_button = None
east_button = None
west_button = None
root = None

refresh_location = True
refresh_objects_visible = True

current_location = 18
diary_counter = 0
freezing_death_counter = 0
blizzard_stopped = False
curtains_openend = False
shower_curtains_openend = False
drawer_openend = False
small_chest_openend = False
hole_openend = False
end_of_game = False
printed_game_completed = False

torch1_object = GameObject.GameObject("torch1", 17, True, True, False, "It's a torch, it's pretty lit")
torch2_object = GameObject.GameObject("torch2", 19, True, True, False, "It's a torch, it's pretty lit")
shower_curtains_object = GameObject.GameObject("shower curtains", 201, False, False, False, "These curtains haven't been used in ages.")
water_object = GameObject.GameObject("water", 201, False, False, False, "The water is almost filling the bath, but why is it full...")
chain_object = GameObject.GameObject("chain", 201, True, False, False, "The chain's hanging out of the water, maybe it'll do something if I remove it.")
curtains_object = GameObject.GameObject("curtains", 5, False, False, False, "The curtains are bright red, and contrast really well with the color of the walls.")
drawer_object = GameObject.GameObject("drawer", 206, False, False, False, "Wow, what a fancy drawer, it looks empty though. One drawer looks like it has a key hole.")
small_chest_object = GameObject.GameObject("small chest", 2, False, False, False, "You were sure this wasn't here before, but here it is.")
key1_object = GameObject.GameObject("key1", 5, True, False, False, "It's a key, probably opens something")
key2_object = GameObject.GameObject("key2", 206, True, False, False, "It's another key, probably opens something else")
key3_object = GameObject.GameObject("key3", 2, True, False, False, "So many keys, this one looks kind of weird")
amulet_object = GameObject.GameObject("amulet", 215, True, False, False, "You probably shouldn't be looting this place, but it looks pretty fancy, and no one will mind if you take this, probably...")
shovel_object = GameObject.GameObject("shovel", 211, True, False, False, "It's a shovel, looks like it's been used in the snow...")
backpack_object = GameObject.GameObject("backpack", 20, True, False, False, "How did the backpack end up here?")
phone_object = GameObject.GameObject("phone", 11, True, False, False, "This shouldn't be here, who put this here?")
coat_object = GameObject.GameObject("coat", 201, True, False, False, "It's soaking wet, but it's nice and clean now.")
diary_object = GameObject.GameObject("diary", 210, True, False, False, "Huh, its a diary, seems pretty long.")
fork_object = GameObject.GameObject("fork", 1, True, False, False, "It's a fork, there isn't much to say about a fork.")
spaghetti_object = GameObject.GameObject("spaghetti", 11, False, False, False, "Honestly you shouldn't be eating food that you find in the middle of nowhere but you are pretty hungry...")
plate_object = GameObject.GameObject("plate", 11, True, False, False, "Now that you're done eating the spaghetti, the plate seems a bit elevated. Maybe it's covering something.")
hole_object = GameObject.GameObject("hole", 215, False, False, False, "It's a weird looking hole, but it looks like it was meant to be here...")
toilet_object = GameObject.GameObject("toilet", 201, False, False, False, "You don't really need to take care of business.")

game_objects = [water_object, chain_object, shower_curtains_object, toilet_object, plate_object, spaghetti_object, small_chest_object, torch1_object, torch2_object, curtains_object, drawer_object, key1_object, key2_object, key3_object, amulet_object, shovel_object, backpack_object, phone_object, coat_object, diary_object, fork_object, hole_object]

def perform_command(verb, noun=False):
    if (verb == "GO"):
        perform_go_command(noun)
    elif ((verb == "N") or (verb == "S") or (verb == "E") or (verb == "W")):
        perform_go_command(verb)        
    elif ((verb == "NORTH") or (verb == "SOUTH") or (verb == "EAST") or (verb == "WEST")):
        perform_go_command(noun)        
    elif (verb == "GET"):
        perform_get_command(noun)
    elif (verb == "PUT"):
        perform_put_command(noun)
    elif (verb == "LOOK"):
        perform_look_command(noun)        
    elif (verb == "KILL"):
        perform_kill_command(noun)        
    elif (verb == "READ"):
        perform_read_command(noun)        
    elif (verb == "OPEN"):
        perform_open_command(noun)
    elif (verb == "DIG"):
        perform_dig_command(verb)
    elif (verb == "EAT"):
        perform_eat_command(noun)
    elif (verb == 'STATE'):
        set_current_state()
    else:
        print_to_description("huh?")       
        
def perform_eat_command(object_name):
    game_object = get_game_object(object_name)
    if (fork_object.carried):
        if game_object == spaghetti_object:
            spaghetti_object.location = 0
            plate_object.visible = True
            print_to_description("Now that you're done eating the spaghetti, the plate seems a bit elevated. Maybe it's covering something.")
        else:
            print_to_description("You really shouldn't eat that.")
    else:
        print_to_description("You should find something to eat with.")

def perform_dig_command(verb):
    if (shovel_object.carried):
        if current_location == 20:
            backpack_object.visible = True
            print_to_description("Well you made a mess, but you found your backpack.")
        elif (current_location == 16) or (current_location == 21) or (current_location == 22) or (current_location == 23) or (current_location == 24) or (current_location == 25):
            print_to_description("I hope this doesn't count as property damage, cause you're making a huge mess.")
        else:
            print_to_description("I honestly hope you don't actually want to dig here.")
    else:
        print_to_description("You have nothing to dig with.")
              
def perform_go_command(direction):
    global current_location
    global refresh_location
        
    if (direction == "N" or direction == "NORTH"):
        new_location = get_location_to_north()
    elif (direction == "S" or direction == "SOUTH"):
        new_location = get_location_to_south()
    elif (direction == "E" or direction == "EAST"):
        new_location = get_location_to_east()
    elif (direction == "W" or direction == "WEST"):
        new_location = get_location_to_west()
    else:
        new_location = 0
        
    if (new_location == 0):
        print_to_description("You can't go that way!")
    else:
        current_location = new_location
        refresh_location = True

def perform_get_command(object_name):
    
    global refresh_objects_visible
    game_object = get_game_object(object_name)
    
    if not (game_object is None):
        if (game_object.location != current_location):
            print_to_description("You don't see one of those here!")
        elif (game_object.movable == False):
            print_to_description("You can't pick it up!")
        elif (game_object.carried == True):
            print_to_description("You are already carrying it")
        else:
            if (game_object == chain_object):
                print_to_description("The water subsides, revealing your coat, soaking wet with water.")
                coat_object.visible = True
                chain_object.visible = False
            elif (game_object == plate_object):
                print_to_description("You lift up the plate and find your phone, reading 3 new messages.")
                plate_object.visible = False
                phone_object.visible = True
            else:
                game_object.carried = True
                game_object.visible = False
                refresh_objects_visible = True
    else:
        print_to_description("You don't see one of those here!")

def perform_put_command(object_name):
    global refresh_objects_visible
    game_object = get_game_object(object_name)
    if not (game_object is None):
        if (game_object.carried == False):
            print_to_description("You are not carrying one of those.")
        else:
            #put down the object
            game_object.location = current_location
            game_object.carried = False
            game_object.visible = True
            refresh_objects_visible = True
    else:
        print_to_description("You are not carrying one of those!")
 
def perform_look_command(object_name):
    
    
    global refresh_location
    global refresh_objects_visible
    
    game_object = get_game_object(object_name)
 
    if not (game_object is None):

        if ((game_object.carried == True) or (game_object.visible and game_object.location == current_location)):
            print_to_description(game_object.description)
        else:
            print_to_description("You can't see one of those!")
 
        if (game_object == True):
            print_to_description("special condition")
            global refresh_objects_visible
            refresh_objects_visible = True

    else:
        if (object_name == ""):
            #generic LOOK
            refresh_location = True
            refresh_objects_visible = True
        else:
            #not visible recognized
            print_to_description("You can't see one of those!")

def perform_kill_command(object_name):

    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if (False):
            print_to_description("special condition")
        else:
            print_to_description("You can't kill inanimate objects, silly!")
    else:
        #not visible recognized
        print_to_description("You can't kill what you can't see")

def perform_read_command(object_name):
    global diary_counter
    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if (game_object == diary_object):
            if (diary_object.carried):
                diary_counter = diary_counter + 1
                if diary_counter == 1:
                    print_to_description("He loved his job. Driving a train had been his dream ever since he was a child. He loved to make the train go as fast as possible.")
                elif diary_counter == 2:
                    print_to_description("Unfortunately, one day he was a little too reckless and caused a crash. He made it out, but a single person died.")
                elif diary_counter == 3:
                    print_to_description("Well, needless to say, he went to court over this incident. He was found guilty, and was sentenced to death by electrocution.")
                elif diary_counter == 4:
                    print_to_description("When the day of the execution came, he requested a single banana as his last meal.")
                elif diary_counter == 5:
                    print_to_description("After eating the banana, he was strapped into the electric chair.")
                elif diary_counter == 6:
                    print_to_description("The switch was flown, sparks flew, and smoke filled the air - but nothing happened. The man was perfectly fine.")
                elif diary_counter == 7:
                    print_to_description("Well, at the time, there was an old Bulgarian law that said a failed execution was a sign of divine intervention, so the man was allowed to go free.")
                elif diary_counter == 8:
                    print_to_description("Somehow, he managed to get his old job back driving the train. Having not learned his lesson at all, he went right back to driving the train with reckless abandon.")
                elif diary_counter == 9:
                    print_to_description("Once again, he caused a train to crash, this time killing two people. The trial went much the same as the first, resulting in a sentence of execution.")
                elif diary_counter == 10:
                    print_to_description("For his final meal, the man requested two bananas. After eating the bananas, he was strapped into the electric chair.")
                elif diary_counter == 11:
                    print_to_description("The switch was thrown, sparks flew, smoke filled the room - and the man was once again unharmed.")
                elif diary_counter == 12:
                    print_to_description("Well, this of course meant that he was free to go. And once again, he somehow managed to get his old job back.")
                elif diary_counter == 13:
                    print_to_description("To what should have been the surprise of no one, he crashed yet another train and killed three people.")
                elif diary_counter == 14:
                    print_to_description("And so he once again found himself being sentenced to death. On the day of his execution, he requested his final meal: three bananas.")
                elif diary_counter == 15:
                    print_to_description("'You know what? No,' said the executioner. 'I've had it with you and your stupid bananas and walking out of here unharmed. I'm not giving you a thing to eat; we're strapping you in and doing this now.'")
                elif diary_counter == 16:
                    print_to_description("Well, it was against protocol, but the man was strapped in to the electric chair without a last meal.")
                elif diary_counter == 17:
                    print_to_description("The switch was pulled, sparks flew, smoke filled the room - and the man was still unharmed. The executioner was speechless.")
                elif diary_counter == 18:
                    print_to_description("The man looked at the executioner and said, 'Oh, the bananas had nothing to do with it. I'm just a bad conductor.'")
                else:
                    diary_counter = 0
                    print_to_description("That's about it. I don't really know how this is a diary. You can read it again if you want.")
        else:
            print_to_description("There is no text on it")
    else:
        print_to_description("I am not sure which " + object_name + " you are referring to")
# 
def perform_open_command(object_name):

    global curtains_openend
    global shower_curtains_openend
    global drawer_openend
    global small_chest_openend
    global hole_openend
    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if (game_object == curtains_object):
            if curtains_openend == True:
                print_to_description("The curtains are already open revealing that they were hiding a wall!")
            elif curtains_object.location == current_location:
                print_to_description("The curtains open, revealing a wall and a key that is dangling from a string.")
                curtains_openend = True
                key1_object.visible = True
                curtains_object.description = "Don't curtains normally reveal windows?"
            else:
                print_to_description("You don't see that here.")
        elif (game_object == shower_curtains_object):
            if shower_curtains_openend == True:
                print_to_description("The shower curtains are already open.")
            elif shower_curtains_object.location == current_location:
                print_to_description("You see a bath full of water, almost overflowing. Maybe someone has been here recently...")
                shower_curtains_openend = True
                chain_object.visible = True
                water_object.visible = True
                shower_curtains_object.description = "Or maybe the antique quality is what makes it look old, and it's actually new."
            else:
                print_to_description("You don't see that here.")
        elif (game_object == drawer_object):
            if drawer_openend == True:
                print_to_description("You left the drawer open, why would you do that?")
            elif key1_object.carried and (drawer_object.location == current_location):
                print_to_description("After a bit of effort, you open the drawer which is mostly empty, except for another key.")
                drawer_openend = True
                key2_object.visible = True
                small_chest_object.visible = True
            else:
                print_to_description("You try pulling the drawer open but it seems to be locked.")
        elif (game_object == small_chest_object):
            if small_chest_openend == True:
                print_to_description("You expected a little bit more when you opened this chest, oh well.")
            elif key2_object.carried and (small_chest_object.location == current_location):
                print_to_description("Oh boy, what's it gonna be, what's it gonna be. Oh... it's just another key.")
                small_chest_openend = True
                key3_object.visible = True
            else:
                print_to_description("This chest seems locked, maybe theres a key somewhere.")
        elif (game_object == hole_object):
            if hole_openend == True:
                print_to_description("It's weird that you can open a hole...")
            elif key3_object.carried and (hole_object.location == current_location):
                print_to_description("You insert the key, which fits surprisingly well and it opens a little cubby that contains the most beautiful amulet you've ever seen.")
                hole_openend = True
                amulet_object.visible = True
            else:
                print_to_description("You stick your finger in the hole but that doesn't really seem to do anything. Maybe if you had something that fit in the hole...")
        else:
            print_to_description("You can't open one of those.")
    else:
        print_to_description("You don't see one of those here.")
                
def describe_current_location():
    global end_of_game
    
    if (current_location == 1):
        print_to_description("Kitchen")
    elif (current_location == 2):
        print_to_description("Hallway")
    elif (current_location == 3):
        print_to_description("Dining room")
    elif (current_location == 4):
        print_to_description("Hallway")
    elif (current_location == 5):
        print_to_description("Living room")
    elif (current_location == 6):
        print_to_description("Kitchen")
    elif (current_location == 7):
        print_to_description("Hallway")
    elif (current_location == 8):
        print_to_description("Dining room")
    elif (current_location == 9):
        print_to_description("Hallway")
    elif (current_location == 10):
        print_to_description("Living room")
    elif (current_location == 11):
        print_to_description("Pantry")
    elif (current_location == 12):
        print_to_description("Hallway")
    elif (current_location == 13):
        print_to_description("Hallway")
    elif (current_location == 14):
        print_to_description("Hallway")
    elif (current_location == 15):
        print_to_description("Dead end")
    elif (current_location == 16):
        print_to_description("Outside")
    elif (current_location == 17):
        print_to_description("Stairway")
    elif (current_location == 18):
        print_to_description("Main entrance")
    elif (current_location == 19):
        print_to_description("Stairway")
    elif (current_location == 20):
        print_to_description("Outside")
    elif (current_location == 21):
        print_to_description("Outside")
    elif (current_location == 22):
        print_to_description("Outside")
    elif (current_location == 23):
        print_to_description("Outside")
    elif (current_location == 24):
        print_to_description("Outside")
    elif (current_location == 25):
        print_to_description("Outside")
    elif (current_location == 201):
        print_to_description("Bathroom")
    elif (current_location == 202):
        print_to_description("2nd floor Hallway")
    elif (current_location == 203):
        print_to_description("How did you get in here? This is a wall.")
    elif (current_location == 204):
        print_to_description("2nd floor Hallway")
    elif (current_location == 205):
        print_to_description("Bathroom")
    elif (current_location == 206):
        print_to_description("Bedroom")
    elif (current_location == 207):
        print_to_description("2nd floor Hallway")
    elif (current_location == 208):
        print_to_description("How did you get in here? This is a wall.")
    elif (current_location == 209):
        print_to_description("2nd floor Hallway")
    elif (current_location == 210):
        print_to_description("Bedroom")
    elif (current_location == 211):
        print_to_description("Closet")
    elif (current_location == 212):
        print_to_description("2nd floor Hallway")
    elif (current_location == 213):
        print_to_description("2nd floor Hallway")
    elif (current_location == 214):
        print_to_description("2nd floor Hallway")
    elif (current_location == 215):
        print_to_description("Closet")
    elif (current_location == 246 and amulet_object.carried and backpack_object.carried and phone_object.carried and coat_object.carried and diary_object.carried):
        print_to_description("You've completely beat the game, well done.")
        end_of_game = True
    elif (current_location == 246):
        print_to_description("You've beat the game, but maybe there was something you left undone...")
        end_of_game = True
    else:
        print_to_description("unknown location:" + current_location)
        
    if (torch1_object.carried == True) or (torch2_object.carried == True):
        curtains_object.visible = True
        shovel_object.visible = True
        diary_object.visible = True
        fork_object.visible = True
        drawer_object.visible = True
        spaghetti_object.visible = True
        hole_object.visible = True
        toilet_object.visible = True
        shower_curtains_object.visible = True
    else:
        curtains_object.visible = False
        shovel_object.visible = False
        diary_object.visible = False
        fork_object.visible = False
        drawer_object.visible = False
        spaghetti_object.visible = False
        hole_object.visible = False
        toilet_object.visible = False
        shower_curtains_object.visible = False

def set_current_image():
    
    if (current_location == 1):
        image_label.img = PhotoImage(file = 'res/kitchen_2.gif')
    elif (current_location == 2):
        image_label.img = PhotoImage(file = 'res/hallway.gif')
    elif (current_location == 3):
        image_label.img = PhotoImage(file = 'res/dining_room_1.gif')
    elif (current_location == 4):
        image_label.img = PhotoImage(file = 'res/hallway.gif')
    elif (current_location == 5):
        image_label.img = PhotoImage(file = 'res/living_room_2.gif')
    elif (current_location == 6):
        image_label.img = PhotoImage(file = 'res/kitchen_1.gif')
    elif (current_location == 7):
        image_label.img = PhotoImage(file = 'res/hallway.gif')
    elif (current_location == 8):
        image_label.img = PhotoImage(file = 'res/dining_room_2.gif')
    elif (current_location == 9):
        image_label.img = PhotoImage(file = 'res/hallway.gif')
    elif (current_location == 10):
        image_label.img = PhotoImage(file = 'res/living_room_1.gif')
    elif (current_location == 11):
        image_label.img = PhotoImage(file = 'res/pantry.gif')
    elif (current_location == 12):
        image_label.img = PhotoImage(file = 'res/hallway.gif')
    elif (current_location == 13):
        image_label.img = PhotoImage(file = 'res/main_entrance_2.gif')
    elif (current_location == 14):
        image_label.img = PhotoImage(file = 'res/hallway.gif')
    elif (current_location == 15):
        image_label.img = PhotoImage(file = 'res/dead_end.gif')
    elif (current_location == 16):
        image_label.img = PhotoImage(file = 'res/outside.gif')
    elif (current_location == 17):
        image_label.img = PhotoImage(file = 'res/stairway_2.gif')
    elif (current_location == 18):
        image_label.img = PhotoImage(file = 'res/main_entrance.gif')
    elif (current_location == 19):
        image_label.img = PhotoImage(file = 'res/stairway_1.gif')
    elif (current_location == 20):
        image_label.img = PhotoImage(file = 'res/outside.gif')
    elif (current_location == 21):
        image_label.img = PhotoImage(file = 'res/outside.gif')
    elif (current_location == 22):
        image_label.img = PhotoImage(file = 'res/outside.gif')
    elif (current_location == 23):
        image_label.img = PhotoImage(file = 'res/outside_footprints.gif')
    elif (current_location == 24):
        image_label.img = PhotoImage(file = 'res/outside_footprints.gif')
    elif (current_location == 25):
        image_label.img = PhotoImage(file = 'res/outside_footprints.gif')
    elif (current_location == 201):
        image_label.img = PhotoImage(file = 'res/bathroom_2.gif')
    elif (current_location == 202):
        image_label.img = PhotoImage(file = 'res/hallway.gif')
    elif (current_location == 204):
        image_label.img = PhotoImage(file = 'res/hallway.gif')
    elif (current_location == 205):
        image_label.img = PhotoImage(file = 'res/bathroom_1.gif')
    elif (current_location == 206):
        image_label.img = PhotoImage(file = 'res/bedroom_2.gif')
    elif (current_location == 207):
        image_label.img = PhotoImage(file = 'res/hallway.gif')
    elif (current_location == 209):
        image_label.img = PhotoImage(file = 'res/hallway.gif')
    elif (current_location == 210):
        image_label.img = PhotoImage(file = 'res/bedroom_1.gif')
    elif (current_location == 211):
        image_label.img = PhotoImage(file = 'res/closet_2.gif')
    elif (current_location == 212):
        image_label.img = PhotoImage(file = 'res/hallway.gif')
    elif (current_location == 213):
        image_label.img = PhotoImage(file = 'res/hallway.gif')
    elif (current_location == 214):
        image_label.img = PhotoImage(file = 'res/hallway.gif')
    elif (current_location == 215):
        image_label.img = PhotoImage(file = 'res/closet_1.gif')
    elif (current_location == 246):
        image_label.img = PhotoImage(file = 'res/outside_footprints.gif')
    else:
        image_label.img = PhotoImage(file = 'res/outside.gif')
        
    image_label.config(image = image_label.img)
        

def get_location_to_north():
    if (current_location == 6):
        return 1
    elif (current_location == 7):
        return 2
    elif (current_location == 8):
        return 3
    elif (current_location == 9):
        return 4
    elif (current_location == 10):
        return 5
    elif (current_location == 11):
        return 6
    elif (current_location == 12):
        return 7
    elif (current_location == 14):
        return 9
    elif (current_location == 18):
        return 13
    elif (current_location == 23):
        return 18
    elif (current_location == 21):
        return 16
    elif (current_location == 25):
        return 20
    elif (current_location == 17):
        return 212
    elif (current_location == 19):
        return 214
    elif (current_location == 211):
        return 206
    elif (current_location == 215):
        return 210
    elif (current_location == 212):
        return 207
    elif (current_location == 214):
        return 209
    elif (current_location == 206):
        return 201
    elif (current_location == 207):
        return 202
    elif (current_location == 209):
        return 204
    elif (current_location == 210):
        return 205
    else:
        return 0
    turns = turns + 1
        

def get_location_to_south():
    if (current_location == 1):
        return 6
    elif (current_location == 2):
        return 7
    elif (current_location == 3):
        return 8
    elif (current_location == 4):
        return 9
    elif (current_location == 5):
        return 10
    elif (current_location == 6):
        return 11
    elif (current_location == 7):
        return 12
    elif (current_location == 9):
        return 14
    elif (current_location == 13):
        return 18
    elif (current_location == 18):
        return 23
    elif (current_location == 16):
        return 21
    elif (current_location == 20):
        return 25
    elif (current_location == 201):
        return 206
    elif (current_location == 202):
        return 207
    elif (current_location == 204):
        return 209
    elif (current_location == 205):
        return 210
    elif (current_location == 206):
        return 211
    elif (current_location == 207):
        return 212
    elif (current_location == 209):
        return 214
    elif (current_location == 210):
        return 215
    elif (current_location == 212):
        return 17
    elif (current_location == 214):
        return 19
    elif (current_location == 23 and backpack_object.carried and phone_object.carried and coat_object.carried):
        return 246
    elif (current_location == 21 and backpack_object.carried and phone_object.carried and coat_object.carried):
        return 246
    elif (current_location == 22 and backpack_object.carried and phone_object.carried and coat_object.carried):
        return 246
    elif (current_location == 24 and backpack_object.carried and phone_object.carried and coat_object.carried):
        return 246
    elif (current_location == 25 and backpack_object.carried and phone_object.carried and coat_object.carried):
        return 246
    else:
        return 0
    turns = turns + 1

def get_location_to_east():
    if (current_location == 1):
        return 2
    elif (current_location == 2):
        return 3
    elif (current_location == 3):
        return 4
    elif (current_location == 4):
        return 5
    elif (current_location == 6):
        return 7
    elif (current_location == 7):
        return 8
    elif (current_location == 8):
        return 9
    elif (current_location == 9):
        return 10
    elif (current_location == 12):
        return 13
    elif (current_location == 13):
        return 14
    elif (current_location == 14):
        return 15
    elif (current_location == 17):
        return 18
    elif (current_location == 18):
        return 19
    elif (current_location == 21):
        return 22
    elif (current_location == 22):
        return 23
    elif (current_location == 23):
        return 24
    elif (current_location == 24):
        return 25
    elif (current_location == 204):
        return 205
    elif (current_location == 206):
        return 207
    elif (current_location == 209):
        return 210
    elif (current_location == 212):
        return 213
    elif (current_location == 213):
        return 214
    else:
        return 0
    turns = turns + 1

def get_location_to_west():
    if (current_location == 2):
        return 1
    elif (current_location == 3):
        return 2
    elif (current_location == 4):
        return 3
    elif (current_location == 5):
        return 4
    elif (current_location == 7):
        return 6
    elif (current_location == 8):
        return 7
    elif (current_location == 9):
        return 8
    elif (current_location == 10):
        return 9
    elif (current_location == 13):
        return 12
    elif (current_location == 14):
        return 13
    elif (current_location == 15):
        return 14
    elif (current_location == 18):
        return 17
    elif (current_location == 19):
        return 18
    elif (current_location == 22):
        return 21
    elif (current_location == 23):
        return 22
    elif (current_location == 24):
        return 23
    elif (current_location == 25):
        return 24
    elif (current_location == 205):
        return 204
    elif (current_location == 207):
        return 206
    elif (current_location == 210):
        return 209
    elif (current_location == 213):
        return 212
    elif (current_location == 214):
        return 213
    else:
        return 0
    turns = turns + 1

def handle_special_condition():
    
    global end_of_game
    global freezing_death_counter
    global blizzard_stopped
    global printed_game_completed
    
    if (((current_location == 16) or (current_location == 20) or (current_location == 21) or (current_location == 22) or (current_location == 23) or (current_location == 24) or (current_location == 25) or (current_location == 22)) and (blizzard_stopped == False)):
        freezing_death_counter = freezing_death_counter + 1
        if (freezing_death_counter >= 12):
            end_of_game = True
            print_to_description("GAME OVER")
        elif ((freezing_death_counter > 8) and (freezing_death_counter < 12)):
            print_to_description("It's getting extremely cold. You don't know if you can hold out much longer.")
        elif ((freezing_death_counter > 4) and (freezing_death_counter < 9)):
            print_to_description("You start shivering a bit, maybe it's time to head back in.")
        else:
            print_to_description("The blizzards still out and it's pretty cold.")
    else:
        freezing_death_counter = 0
    
    if backpack_object.carried and phone_object.carried and coat_object.carried and (printed_game_completed == False):
        print_to_description("You retrieved all of your stuff and the blizzard settles, you can leave now if you wish by going south outside.")
        printed_game_completed = True

def print_to_description(output, user_input=False):
    description_widget.config(state = 'normal')
    description_widget.insert(END, output)
    if (user_input):
        description_widget.tag_add("blue_text", CURRENT + " linestart", END + "-1c")
        description_widget.tag_configure("blue_text", foreground = 'blue')
    description_widget.insert(END, '\n')        
    description_widget.config(state = 'disabled')
    description_widget.see(END)
        
def get_game_object(object_name):
    sought_object = None
    for current_object in game_objects:
        if (current_object.name.upper() == object_name):
            sought_object = current_object
            break
    return sought_object

def describe_current_visible_objects():
    
    object_count = 0
    object_list = ""
    
    for current_object in game_objects:
        if ((current_object.location  == current_location) and (current_object.visible == True) and (current_object.carried == False)):
            object_list = object_list + (", " if object_count > 0 else "") + current_object.name
            object_count = object_count + 1
            
    print_to_description("You see: " + (object_list + "." if object_count > 0 else "nothing special.")) 

def describe_current_inventory():
    
    object_count = 0
    object_list = ""

    for current_object in game_objects:
        if (current_object.carried):
            object_list = object_list + (", " if object_count > 0 else "") + current_object.name
            object_count = object_count + 1
    
    inventory = "You are carrying: " + (object_list if object_count > 0 else "nothing")
    
    inventory_widget.config(state = "normal")
    inventory_widget.delete(1.0, END)
    inventory_widget.insert(1.0, inventory)
    inventory_widget.config(state = "disabled")
             
def build_interface():
    
    global command_widget
    global image_label
    global description_widget
    global inventory_widget
    global north_button
    global south_button
    global east_button
    global west_button    
    global root

    root = Tk()
    root.resizable(0,0)
    
    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")

    image_label = ttk.Label(root)    
    image_label.grid(row=0, column=0, columnspan =3,padx = 2, pady = 2)

    description_widget = Text(root, width =50, height = 10, relief = GROOVE, wrap = 'word')
    description_widget.insert(1.0, "Welcome to my game\n\nAfter a trip turns south when a blizzard roles in, you find yourself seeking shelter in an abandoned mansion, a bit weary from its old age. After sleeping near the main entrance, you wake up to find your stuff gone. The blizzard doesn't seem to want to end and you don't want to leave your stuff behind. What might you find as you look for your own belongings. ")
    description_widget.config(state = "disabled")
    description_widget.grid(row=1, column=0, columnspan =3, sticky=W, padx = 2, pady = 2)

    command_widget = ttk.Entry(root, width = 25, style="BW.TLabel")
    command_widget.bind('<Return>', return_key_enter)
    command_widget.grid(row=2, column=0, padx = 2, pady = 2)
    
    button_frame = ttk.Frame(root)
    button_frame.config(height = 150, width = 150, relief = GROOVE)
    button_frame.grid(row=3, column=0, columnspan =1, padx = 2, pady = 2)

    north_button = ttk.Button(button_frame, text = "N", width = 5)
    north_button.grid(row=0, column=1, padx = 2, pady = 2)
    north_button.config(command = north_button_click)
    
    south_button = ttk.Button(button_frame, text = "S", width = 5)
    south_button.grid(row=2, column=1, padx = 2, pady = 2)
    south_button.config(command = south_button_click)

    east_button = ttk.Button(button_frame, text = "E", width = 5)
    east_button.grid(row=1, column=2, padx = 2, pady = 2)
    east_button.config(command = east_button_click)

    west_button = ttk.Button(button_frame, text = "W", width = 5)
    west_button.grid(row=1, column=0, padx = 2, pady = 2)
    west_button.config(command = west_button_click)
    
    inventory_widget = Text(root, width = 30, height = 8, relief = GROOVE , state=DISABLED )
    inventory_widget.grid(row=2, column=2, rowspan = 2, padx = 2, pady = 2,sticky=W)
    
def set_current_state():

    global refresh_location
    global refresh_objects_visible

    if (refresh_location):
        describe_current_location()
        set_current_image()
    
    if (refresh_location or refresh_objects_visible):
        describe_current_visible_objects()

    set_directions_to_move()                
    describe_current_inventory()
    handle_special_condition()
    
    refresh_location = False
    refresh_objects_visible = False

def north_button_click():
    print_to_description("N", True)
    perform_command("N", "")
    set_current_state()

def south_button_click():
    print_to_description("S", True)
    perform_command("S", "")
    set_current_state()

def east_button_click():
    print_to_description("E", True)
    perform_command("E", "")
    set_current_state()

def west_button_click():
    print_to_description("W", True)
    perform_command("W", "")
    set_current_state()

def return_key_enter(event):
    if( event.widget == command_widget):
        command_string = command_widget.get()
        print_to_description(command_string, True)

        command_widget.delete(0, END)
        words = command_string.split(' ', 1)
        verb = words[0]
        noun = (words[1] if (len(words) > 1) else "")
        perform_command(verb.upper(), noun.upper())
        
        set_current_state()

def set_directions_to_move():

    move_to_north = (get_location_to_north() > 0 and (end_of_game == False))
    move_to_south = (get_location_to_south() > 0 and (end_of_game == False))
    move_to_east = (get_location_to_east() > 0 and (end_of_game == False))
    move_to_west = (get_location_to_west() > 0 and (end_of_game == False))
    
    north_button.config(state = ("normal" if move_to_north else "disabled"))
    south_button.config(state = ("normal" if move_to_south else "disabled"))
    east_button.config(state = ("normal" if move_to_east else "disabled"))
    west_button.config(state = ("normal" if move_to_west else "disabled"))    

def main():
    build_interface()
    set_current_state()
    root.mainloop()
        
main()