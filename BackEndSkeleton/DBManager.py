#Python version 2.7.9

import sqlite3 #Imports sqlite3 module. Needed to work with the Database.
import db_creator

def connectToDB():
    """
    This function returns a connection to the database and a cursor for querying the database.

    Parameters:
        None

    Returns:
        conn: Connection to the database.
        cur: a cursor for querying the database.
    """
    conn = sqlite3.connect("SAAM_database_test2.db") #Connects database
    cur = conn.cursor()
    return conn,cur

def commitToDB(connection):
    """
    This function commits all changes done to the database.

    Parameter:
        connection: A connection to a database.

    Return:
        None
    """
    connection.commit()

def closeDB(connection):
    """
    This function closes connection to the connected database.

    Parameter:
        connection: A connection to a database.

    Return:
       None 
    """
    connection.close()

def checkDB():
    """
    This function checks to see if the connected database has 13 tables. 
    If the table number is not 13, then this function drops pre-existing tables and creates new tables.

    Parameter:
        None

    Returns:
        None
    """
    conn,cur = connectToDB()
    cur.execute("select * from sqlite_master where type='table'")
    if 19 != len(cur.fetchall()):
        db_creator.dropTables(connectToDB())
        db_creator.createTables(connectToDB())
        db_creator.populateTables(connectToDB())

    closeDB(conn)

checkDB()

def getPlayerFromDB(ip):
    """
    This function will get the player's IP address from the database and returns the player data.

    Parameters:
        ip (int): The IP address of the player connecting to the web.py server.

    Returns:
        tuple: A row from the Player_Data table associated with the player's IP address.

    Example:
        getPlayerFromDB(playerinfo.ip) => (1,1.1.1.1,2)
    """

    conn,cur = connectToDB()
    cur.execute("select max(Player_ID) from Player_Data where IP=:ip", {"ip": ip})
    player_id = cur.fetchone()[0]
    cur.execute("select * from Player_Data where Player_ID =:player_id", {"player_id":player_id})
    player_data = cur.fetchone()
    closeDB(conn)
    return player_data

def getPlayerCharacterActionFromDB(player_id):
    """GET
    This funciton will return the player's most recently selected character

    Parameters:
        id (int): the ID of the player connecting to the web.py server

    Returns:
        tuple: a Row from the Player_Character_Action table associated with the player's ID.

    Example:
        getPlayerCharacterActionFromDB(1.1.1.1.1) => (2,1,3,3)
    """
    conn,cur = connectToDB()
    cur.execute("select Max(Character_Action_ID) from Player_Character_Action where Player_ID =:player_id", {"player_id":player_id})
    player_character_action_id = cur.fetchone()[0]
    closeDB(conn)
    return player_character_action_id

def getPlayerStoryActionFromDB(player_id):
    """
    This funciton will return the player's most recently selected story

    Parameters:
        ip (int): the IP address of the player connecting to the web.py server

    Returns:
        tuple: a Row from the Player_Story_Action table associated with the player's ip address

    Example:
        getPlayerStoryActionFromDB(1.1.1.1.1) => (1,3,2,2)
    """
    conn,cur = connectToDB()
    cur.execute("select * from Player_Story_Action where Player_ID =:player_id", {"player_id": player_id})
    player_story_action = cur.fetchone()
    closeDB(conn)
    return player_story_action

def getStoryTitles(player_id):
    """
    This function gets the titles for a particular character based off of what character the player has selected.

    Parameter:
        ip: the IP address of the player connection to the web.py server

    Returns:
        tuple: a tuple containing all story titles for a specific character

    Example:
        getStoryTitles(1.1.1.1.1)=> (Washington(1),Washington(2),Washington(3),Washington(4))

    """
    conn,cur = connectToDB()
    cur.execute("select max(Current_Character_Action_ID) from Player_Data where Player_ID=:player_id", {"player_id":player_id})
    current_character_action_id = cur.fetchone()[0]
    cur.execute("select Current_Character_ID from Player_Character_Action where Character_Action_ID=:current_character_action_id", {"current_character_action_id":current_character_action_id})
    character_id = cur.fetchone()[0]
    cur.execute("select Title_Of_Story from Story_Data where Character_ID =:character_id", {"character_id":character_id})
    story_titles = cur.fetchall()
    story_title_tuple = ()
    for story_title in story_titles:
        story_title_tuple += story_title
    return story_title_tuple

def getStoryData():
    conn,cur=connectToDB()
    cur.execute("select Walk_Level from Story_Data")
    walk_levels=cur.fetchall()
    walk_tuple=()
    for walk_level in walk_levels:
        walk_tuple += walk_level
    cur.execute("select Kid_Friendly from Story_Data")
    kids=cur.fetchall()
    kid_tuple=()
    for kid in kids:
        kid_tuple += kid
    return walk_tuple, kid_tuple

def getStoryIDFromTitle(title_of_story):
    """
    This function find the id of a story from its title.

    Paramter: 
        title_of_story (str): title of story that is passed in 

    Returns:
        int: the story id of the title

    Example: 
        getStoryIDFromTitle(Washington(1))=> 1
    """
    conn,cur=connectToDB()
    cur.execute("select Story_ID from Story_Data where Title_Of_Story=:title_of_story", {"title_of_story":title_of_story})
    story_id= cur.fetchone()[0]
    return story_id

def getCharacterIDFromName(character_name):
    """
    This function finds the character id from a character name.

    Parameter:
        character_name (str): name of character that is passed in 

    Returns:
        int: the character id of the character 

    Example:
        getCharacterIDFromName("George Washington")=> 1
    """
    conn,cur=connectToDB()
    cur.execute("select Character_ID from Character_Data where Character_Name=:character_name", {"character_name":character_name})
    character_id=cur.fetchone()[0]
    return str(character_id)

def getStoriesFromDB(player_id):
    """
    This funciton returns a list of all stories associated with a particular Character

    Parameters:
        Character_ID (int): the ID associated wiht a particular character

    Returns:
        tuple: all Story_IDs associated with the Character_ID

    Example: 
        getStoriesFromDB(2) => 2,3,4
    """
    conn,cur = connectToDB()
    cur.execute("select max(Current_Character_Action_ID) from Player_Data where Player_ID =:player_id", {"player_id":player_id})
    character_action_id = cur.fetchone()[0]
    cur.execute("select Current_Character_ID from Player_Character_Action where Character_Action_Id =:character_action_id", {"character_action_id":character_action_id})
    character_id = cur.fetchone()[0]
    #print character_id
    cur.execute("select Story_ID from Story_Data where Character_ID =:character_id", {"character_id":character_id})
    story_ids = cur.fetchall()
    story_id_tuple = ()
    for story_id in story_ids:
        story_id_tuple += story_id
    return story_id_tuple

def getCharacterData():
    """
    This function will query the database and return the correct character 
    data for the character the player is currently using.

    Parameters:
        Current_Character_ID

    Returns:
        tuple: character fields 

    Example:
        getCharacterData(2) => 2, Diana, 1965.16.32a-b
    """
    conn,cur = connectToDB()
    cur.execute("select Character_ID from Character_Data")
    character_id = cur.fetchall() # if you get too many choice boxes it could be b/c the header is in the table itself, if so, please add this or append the db [1:]
    character_id_tuple = ()
    for character in character_id:
        character_id_tuple += character
    return character_id_tuple

def getCharacterNames():
    """
    This function gets all character names that are in the database. 

    Parameters: 
        None

    Returns: 
        tuple: a tuple that contains all character names

    Example:
        getCharacterNames()=> (George Washington, Salome, Diana, Turing)
    """
    conn,cur=connectToDB()
    cur.execute("select Character_Name from Character_Data")
    character_names=cur.fetchall()
    character_names_tuple=()
    for character_name in character_names:
        character_names_tuple +=character_name
    return character_names_tuple

#___________VVVVVVVVVVVVVVVVVVV____________
def needLastScreen(player_id, input):
    """
    This function uses the player's id to determine if they need the last game screen or not.

    Parameters:
        ip: the IP address of the player connection to the web.py server

    Returns:
        boolean: reutrns True if there is no next step, returns False if there is 

    Example:
        needLastScreen(1.1.1.1.1)=>False
    """
    conn,cur=connectToDB()

    cur.execute("select Max(Step_Action_ID) from Player_Step_Action where Player_ID =:player_id", {"player_id":player_id})
    current_step_row = cur.fetchone()[0]
    cur.execute("select Current_Step_ID from Player_Step_Action where Current_Step_ID =:current_step_row", {"current_step_row":current_step_row})
    current_step_id = cur.fetchone()[0]
    cur.execute("select Answer_ID from Step_Transition_Data where Step_ID =:current_step_id", {"current_step_id":current_step_id})
    answer_id =cur.fetchall()[0]
    


#accession    1
#text    2
#number    3
#mc        4
#boolean     5

    #if "null" == next_step_id:
     #   return True
    #else:
     #   return False
#_____AAAAAAAAAAAAAAAAAAAA__________


def checkforExistingPlayer(player_ip):
    """
    This funciton will check to see if there is player associated with the IP.

    Parameter:
        IP: The current client's IP

    Returns:
        Boolean: True if client has data already saved in the DB. False if there is no data.

    Example:
        checkforExistingPlayer(1.1.1.1) => True
    """
    coon,cur = connectToDB()
    cur.execute("select Player_ID from Player_Data where IP =:player_ip", {"player_ip":player_ip})
    if None != cur.fetchone()[0]:
        return True
    else:
        return False
    closeDB(conn)

def hasPlayerChosenCharacter(player_character_input):  
    """
    This function checks to see if the player has selected a character and returns a boolean

    Parameters:
        player_character_input - the player's input
        current_character_ID - the player's selected character

    Returns:
        Boolean: True is character is selected, False if no character is selected 
    
    Example:
        hasPlayerChosenCharacter(2,2) => True

    """
    conn,cur = connectToDB()
    cur.execute("select Character_ID from Character_Data where Character_ID =:player_character_input", {"player_character_input": player_character_input})
    
    if None != cur.fetchone():
        return True
    else:
        return False
    closeDB(conn)

def checkPlayerStoryInput(player_story_input):
    """
    This function checks to see if the player has selected a story and return a boolean

    Parameters
        player_story_input - the player's input
        current_story_ID - the player's selected story

    Returns
        boolean - True if player has selected a story, False is player has not yet selected a story

    Example
        checkPlayerStoryInput(3,3) => True
    """
    conn,cur = connectToDB()

    cur.execute("select Story_ID from Story_Data where Story_ID =:player_story_input", {"player_story_input": player_story_input})
    
    if None != cur.fetchone():
        return True
    else:
        return False
    closeDB(conn)

def checkPlayerStepInput(player_id, player_input):
    """
    This function checks the player input with the current step 
    and returns a boolean if the player's input is correct.

    Parameters:
        player_input: The player's input.
        current_step_ID: The current step of the story which the player is on.

    Returns:
        boolean: True if player's input is correct. False if the player's input is incorrect.

    Example:
        checkPlayerInput(123.12,1) => False
    """
    conn,cur = connectToDB()

    cur.execute("select Max(Step_Action_ID) from Player_Step_Action where Player_ID =: player_id", {"player_id":player_id})
    current_step_row = cur.fetchone()[0]
    cur.execute("select Current_Step_ID from Player_Step_Action where Current_Step_ID =: current_step_row", {"current_step_row":current_step_row})
    current_step_id = cur.fetchone()[0]
    cur.execute("select Answer_ID from Step_Transition_Data where Step_ID =: current_step_id", {"current_step_id":current_step_id})
    answer_id =cur.fetchall()[0]
    print answer_id

    cur.execute("select * from Accession_Answers where Accession_Number =:player_input", {"player_input":player_input})
    if None != cur.fetchone():
        return True
    else:
        return False
    closeDB(conn)

def loadPlayerAction(player_id):
    """
    This function will retreive the current client's last player action.
    """
    conn,cur = connectToDB()


#___VVVVVVVVVVVVVVVVVVVVVVVVVVVVVV______
def shouldPlayerAdvance(player_id, cursor,player_input,current_step_id):
    """
    This function determines if the player has entered a correct accession number 
    and is thus able to go on to the next step.  It returns a boolean 

    Parameters:
        player_input  -the player's input
        current_step_id - the step Id the player is curenntly on
        accession_association - the accession association associated wiht the current step

    Returns:
        boolean - True if the accession number entered by the player matches one of the assession numbers 
        associated with the assession association, False if the assession numbers do not matches

    Example:
    shouldPlayerAdvance(Prey, 2002.3, 9) => True

    """
    cur = cursor

    if checkPlayerStepInput(player_id, player_input):
        cur.execute("select Accession_Association from Step_Data where Step_ID =:current_step_id", {"current_step_id":current_step_id})
        current_step_association = cur.fetchone()[0]
        cur.execute("select Accession_Association from Accession_Association where Accession_Number =:player_input", {"player_input":player_input})
        if current_step_association == cur.fetchone()[0]:
            return True
        else: 
            return False
    else:
        return False
#_____AAAAAAAAAAAAAAAAAAAA__________


def updatePlayerData(cursor, player_id, action_type):
    """
    This function updates the player's data as s/he moves through the game

    Parameters:
        player_id - the unique number associated with the player
        action_type - the type of action being updated (character, story or step)

    Returns:
        None
    """
    cur = cursor

    cur.execute("select max(%s_ID) from Player_%s where player_id=:player_id" % (action_type, action_type),{"player_id":player_id})
    id_to_update = cur.fetchone()[0]
    cur.execute("update Player_data set Current_%s_ID =:id_to_update" % (action_type), {"id_to_update":id_to_update})
    
def insertPlayerCharacterAction(player_id, player_character_input):
    """
    This function will insert a player's new character choice into the SQLite database
  
    Parameters:
        player_id - the unique number associated with the player
        player_character_input - the character selected by the player

    Returns:
        None
    """
    conn,cur = connectToDB()
    action_type = "Character_Action"

    if hasPlayerChosenCharacter(player_character_input):
        cur.execute("select Character_ID from Character_Data where Character_ID =:player_character_input", {"player_character_input": player_character_input})
        current_character_id = cur.fetchone()[0]
        print "current_character_id is: " + str(current_character_id)
        cur.execute("insert into Player_Character_Action values (?,?,?,?)", (None,player_id,current_character_id,player_character_input))

        updatePlayerData(cur,player_id,action_type)
  
        commitToDB(conn)
    closeDB(conn)

def insertPlayerStoryAction(player_id, player_story_input):
    """
    Thus function inserts the player's new story choice into the SQLite database

    Parameters
        player_id - the unique number associated with the player
        player_story_input - the story the player has chosen

    Returns
        None

    """
    conn,cur = connectToDB()
    action_type = "Story_Action"

    if checkPlayerStoryInput(player_story_input):
        cur.execute("select Story_ID from Story_Data where Story_ID =:player_story_input", {"player_story_input": player_story_input})
        current_story_id = cur.fetchone()[0]
        cur.execute("insert into Player_Story_Action values (?,?,?,?)", (None,player_id,current_story_id,player_story_input))

        updatePlayerData(cur,player_id,action_type)
        action_type = "Step_Action"
        cur.execute("select * from Step_Data where Story_ID =:current_story_id", {"current_story_id":current_story_id})
        step_id = cur.fetchone()[1] #Returns a tuple of all the step data that will be used to update player step action.
        cur.execute("insert into Player_Step_Action values (?,?,?,?,?,?,?)", (None, player_id, None, step_id, None, None, None))

        updatePlayerData(cur,player_id,action_type)

        commitToDB(conn)
    closeDB(conn)

def insertPlayerStepAction(player_id, player_step_input=None):
    """
    This function inserts player action into the database.

    Parameters:
        player_ID: The player's unique ID in the database.
        current_story_ID: The player's current story ID.
        current_character_ID: The player's current character ID.

    Returns:
        None
    """
    conn,cur = connectToDB()
    action_type = "Step_Action"

    cur.execute("select Current_Step_Action_ID from Player_Data where Player_ID =:player_id", {"player_id":player_id})
    step_action_id = cur.fetchone()[0]
    cur.execute("select Current_Step_ID from Player_Step_Action where Step_Action_ID =:step_action_id", {"step_action_id":step_action_id})
    current_step_id = cur.fetchone()[0]
    if shouldPlayerAdvance(cur,player_id, player_step_input, current_step_id):
        cur.execute("select * from Step_Data where Step_ID =:current_step_id",{"current_step_id":current_step_id})
        step_data = cur.fetchone() #Returns a tuple of all the step data that will be used to update player step action.
        cur.execute("select Next_Step_ID from Step_Data where Step_ID =:next_step_id",{"next_step_id":step_data[3]})
        next_step_id = cur.fetchone()[0]
        cur.execute("insert into Player_Step_Action values (?,?,?,?,?,?,?)", (None, player_id, step_data[1], step_data[3], next_step_id, player_step_input, None))
    else:
        cur.execute("select Misses from Player_Step_Action where Step_Action_ID =:step_action_id", {"step_action_id":step_action_id})
        misses = cur.fetchone()[0]
        if None == misses:
            misses = 1
        else:
            misses += 1
        cur.execute("select * from Step_Data where Step_ID =:current_step_id",{"current_step_id":current_step_id})
        step_data = cur.fetchone() #Returns a tuple of all the step data that will be used to update player step action.
        cur.execute("insert into Player_Step_Action values (?,?,?,?,?,?,?)", (None, player_id, step_data[2], step_data[1], step_data[3], player_step_input, misses))

    updatePlayerData(cur,player_id,action_type)
    commitToDB(conn)
    closeDB(conn)

def getAllCharactersFromDB():
    conn,cur = connectToDB()
    cur.execute("select Character_Name from Character_Data")
    all_characters = cur.fetchall()
    character_name_tuple = ()
    for character_name in all_characters:
        character_name_tuple +=character_name
    return character_name_tuple
        
def getAllStoriesDataFromDB():
    conn,cur = connectToDB()
    cur.execute("select Title_Of_Story from Story_Data")
    all_stories = cur.fetchall()
    stories_tuple = ()
    for story_title in all_stories:
        stories_tuple += story_title
    return stories_tuple

def getStoryDataForGameScreen(player_id):
    conn,cur = connectToDB()
    cur.execute("select Max(Character_Action_ID) from Player_Character_Action where Player_ID =:player_id", {"player_id":player_id})
    char_action_id = cur.fetchone()[0]
    cur.execute("select Current_Character_ID from Player_Character_Action where Character_Action_ID =:char_action_id", {"char_action_id":char_action_id})
    current_character = cur.fetchone()[0]
    cur.execute("select Max(Story_Action_ID) from Player_Story_Action where Player_ID =:player_id", {"player_id":player_id})
    story_action_id = cur.fetchone()[0]
    cur.execute("select Current_Story_ID from Player_Story_Action where Story_Action_ID =:story_action_id", {"story_action_id":story_action_id})
    current_story = cur.fetchone()[0]
    cur.execute("select Title_Of_Story from Story_Data where Story_ID =:current_story", {"current_story":current_story})
    title_of_story = cur.fetchone()[0]
    closeDB(conn)
    return current_story,title_of_story

def getGameScreenDataFromDB(player_id):
    """
    This function returns all the informaiton neccessary to populate the game screen. This
    incudes the title of the story the player selected, the game text for the relevant step, all three hints for the
    relevant step, as well as the progress (step the player is on out of the total number of steps).
    
    Parameter:
        ip: the IP address of the player connection to the web.py server

    Returns:
        tuple: tuple contains the title, game text, 1st hint, 2nd hint, 3rd hint, and progress respectively

    Example:
        getDataFromDBForGameScreen(1.1.1.1.1) => (Enigma, Please go find a box!, You need to find a box., Look in the Luce Foundation Center,
            The title of the piece you're looking for is "The Box", 1/6)

    """
    conn,cur = connectToDB()
    current_story,title_of_story = getStoryDataForGameScreen(player_id)

    cur.execute("select Step_ID from Step_Transition_Data where Story_ID =:current_story", {"current_story":current_story})

    cur.execute("select Max(Step_Action_ID) from Player_Step_Action where Player_ID =:player_id", {"player_id":player_id})
    step_action_id = cur.fetchone()[0]

    cur.execute("select Current_Step_ID from Player_Step_Action where Step_Action_ID =:step_action_id", {"step_action_id":step_action_id})

    cur.execute("select Max(Step_Action_ID) from Player_Step_Action where Player_ID =:player_id", {"player_id":player_id})
    step_action_id = cur.fetchone()[0]        
    cur.execute("select Current_Step_ID from Player_Step_Action where Step_Action_ID =:step_action_id", {"step_action_id":step_action_id})
    current_step = cur.fetchone()[0]
    cur.execute("select Step_Text from Step_Data where Step_ID =:current_step", {"current_step":current_step})
    game_text = cur.fetchone()[0]
    cur.execute("select Step_Hint_1 from Step_Data where Step_ID =:current_step", {"current_step":current_step})
    game_hint_1 = cur.fetchone()[0]
    cur.execute("select Step_Hint_2 from Step_Data where Step_ID =:current_step", {"current_step":current_step})
    game_hint_2 = cur.fetchone()[0]
    cur.execute("select Step_Hint_3 from Step_Data where Step_ID =:current_step", {"current_step":current_step})
    game_hint_3 = cur.fetchone()[0]
    if game_hint_1 == None:
        relevant_game_hint_1 = " "
    else:
        relevant_game_hint_1 = game_hint_1
    if game_hint_2 == None:
        relevant_game_hint_2 = " "
    else:
        relevant_game_hint_2 = game_hint_2
    if game_hint_3 == None:
        relevant_game_hint_3 = " "
    else:
        relevant_game_hint_3 = game_hint_3
    data_to_return = title_of_story , game_text, relevant_game_hint_1, relevant_game_hint_2, relevant_game_hint_3
    return data_to_return
    closeDB(conn)

def getPlayerIP(ip):
    """
    This function will insert a new player's data into the SQLite Database.

    Parameters:
        ip: The new player's IP address.
        current_story: The current story that the player has chosen. This will be used to get the step number.

    Returns:
        None
    """
    conn,cur = connectToDB()
    cur.execute("insert into Player_Data values (?,?,?,?,?)", (None,ip,None,None,None))
    
    commitToDB(conn)
    closeDB(conn)

def insertPlayerCharacterAction(player_id, player_character_input):
    conn,cur = connectToDB()

    if hasPlayerChosenCharacter(player_character_input):
        cur.execute("select Character_ID from Character_Data where Character_ID =:player_character_input", {"player_character_input": player_character_input})
        current_character_id = cur.fetchone()[0]
        cur.execute("insert into Player_Character_Action values (?,?,?,?)", (None,player_id,current_character_id,player_character_input))
        cur.execute("select max(Character_Action_ID) from Player_Character_Action where player_id=:player_id",{"player_id":player_id})
        id_to_update = cur.fetchone()[0]
        cur.execute("update Player_data set Current_Character_Action_ID =:id_to_update", {"id_to_update":id_to_update})
        commitToDB(conn)
    closeDB(conn)

def compareInputToAnswers(player_id,player_input):
    conn,cur = connectToDB()
    cur.execute("select Max(Step_Action_ID) from Player_Step_Action where Player_ID=:player_id",{"player_id":player_id})
    max_step_action_id = cur.fetchone()[0]
    cur.execute("select Current_Step_ID from Player_Step_Action where Step_Action_ID=:max_step_action_id",{"max_step_action_id":max_step_action_id})
    current_step_id = cur.fetchone()[0]
    cur.execute("insert into Player_Step_Action values (?,?,?,?,?,?,?)", (None,player_id,None,current_step_id,None,player_input,None))
    commitToDB(conn)
    cur.execute("select Answer_ID from Step_Transition_Data where Step_ID=:current_step_id",{"current_step_id":current_step_id})
    answer_ids=cur.fetchall()
    print answer_ids
    answer_tuple=()
    for answer in answer_ids:
        answer_tuple += answer
        print answer_tuple
    for answer in answer_tuple:
        cur.execute("select Answer_Type from Answer_Key where Answer_ID=:answer",{"answer":answer})
        answer_type=cur.fetchone()[0]
        if answer_type=="1":
            cur.execute("select Accession_Number from Accession_Answers where Accession_ID=:answer",{"answer":answer})
            accession_numbers=cur.fetchall()
            print "accession numbers:" + str(accession_numbers)
            accession_tuple=()
            for accession in accession_numbers:
                accession_tuple +=accession
            for accession in accession_tuple: 
                if player_input == accession:
                    cur.execute("select Next_Step_ID from Step_Transition_Data where Answer_ID=:answer",{"answer":answer})
                    new_current_step=cur.fetchone()[0]
                    print "the new step is: " + str(new_current_step)
                    cur.execute("insert into Player_Step_Action values (?,?,?,?,?,?,?)", (None,player_id,None,new_current_step,None,None,None))
                    commitToDB(conn)
    closeDB(conn)