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
    if 13 != len(cur.fetchall()):
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
    cur.execute("select * from Player_Data where IP=:ip", {"ip": ip})
    player_data = cur.fetchone()
    closeDB(conn)
    return player_data

def getPlayerCharacterActionFromDB(player_id):
    """
    This funciton will return the player's most recently selected character

    Parameters:
        id (int): the ID of the player connecting to the web.py server

    Returns:
        tuple: a Row from the Player_Character_Action table associated with the player's ID.

    Example:
        getPlayerCharacterActionFromDB(1.1.1.1.1) => (2,1,3,3)
    """
    conn,cur = connectToDB()
    cur.execute("select * from Player_Character_Action where Player_ID =:player_id", {"player_id": player_id})
    player_character_action = cur.fetchone()
    closeDB(conn)
    return player_character_action

def getPlayerStoryActionFromDB(player_id):
    """
    This funciton will return the player's most recently selected story

    Parameters:
        ip (int): the IP addess of the player connecting to the web.py server

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

def getPlayerStepActionFromDB(player_id):
    """
    This funciton will return the player's most recent step and all associated data

    Parameters:
        ip (int): the IP addess of the player connecting to the web.py server

    Returns:
        tuple: a Row from the Player_Step_Action table associated with the player's ip address

    Example:
        getPlayerStepActionFromDB(1.1.1.1.1) => (1,3,2,3,4,5,1)
    """
    conn,cur = connectToDB()
    cur.execute("select * from Player_Step_Action where Player_ID =:player_id", {"player_id": player_id})
    player_step_action = cur.fetchone() 
    closeDB(conn)
    return player_step_action

def getStoriesFromDB(Character_ID):
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
    cur.execute("select Story_ID from Story_Data where Character_ID =: Character_ID", {"Character_ID": Character_ID})
    return cur.fetchall()

def getStepDataFromDB(current_step_ID):
    """
    This function will query the database and return the correct step data for the step the player is currently on.

    Parameters:
        int: Current_Step_ID

    Returns:
        tuple: Step fields

    Example:
        getStepDataFromDB(3) => (1,3,2,4)

    """
    cur = cursorForDB(connectToDB())
    cur.execute("select * from Step_Data where Current_Step_ID =:Step_ID", {"Step_ID": current_step_ID})
    return cur.fetchone()


def getAccessionNumbersFromDB(accession_association):
    """
    This function will query the database and return the list of possible 
    accesion numbers associated with a particular accession association keyword

    Parameters:
        string: accession_association

    Returns:
        tuple: accession numbers

    Example:
        getAccessionNumbersFromDB(Predator) => 2002.31, 1985.4, 1913.1.3
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select Accession_Number from Accession_Data where Accession_Association =: accessionAssociation", {"accessionAssociation": accession_association})
    return cur.fetchall()

def getAccessionAssociationFromDB(accession_number):
    """
    This function will query the database and return the assession association
    associated wiht a particular assession number

    Parameters:
        string: accession_number 

    Returns:
        string: accession_association

    Example:
        getAccessionAssociationFromDB(1965.16.32a-b) => Diana
    """
    conn,cur = connectToDB()
    cur.execute("select Accession_Association from Accession_Association where Accession_Number =:accession_number", {"accession_number":accession_number})
    accession_association = cur.fetchone()[0]
    closeDB(conn)
    return accession_association

def getCharacterData(player_id):
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
    cur.execute("select Current_Character_Action_ID from Player_Data where Player_ID =:player_id", {"player_id",player_id})
    current_character_action = cur.fetchone()[0]
    cur.execute("select Current_Character_ID from Player_Character_Action where Character_Action_ID =:current_character_action", {"current_character_action":current_character_action})
    return cur.fetchone()[0]

def getStoryData(current_story_ID):
    """
    This function will query the database and return the correct story data
    for the story the player is currently playing.

    Parameters:
        Current_Story_ID

    Returns:
        tuple: story fields

    Example:
        getStoryData(3) => (3,2,Mixed Dimensions,6)
    """
    conn,cur = connectToDB()
    cur.execute("select * from Story_Data where Current_Story_ID =:currentStoryID", {"currentStoryID": current_story_ID})
    return cur.fetchone()

def checkPlayerCharacterInput(cursor,player_character_input):
    """
    This function checks to see if the player has selected a character and returns a boolean

    Parameters:
        player_character_input - the player's input
        current_character_ID - the player's selected character

    Returns:
        Boolean: True is character is selected, False if no character is selected 
    
    Example:
        checkPlayerCharacterInput(2,2) => True

    """
    cur = cursor
    cur.execute("select Character_ID from Character_Data where Character_ID =:player_character_input", {"player_character_input": player_character_input})
    
    if None != cur.fetchone():
        return True
    else:
        return False

def checkPlayerStoryInput(cursor,player_story_input):
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
    cur = cursor

    cur.execute("select Story_ID from Story_Data where Story_ID =:player_story_input", {"player_story_input": player_story_input})
    
    if None != cur.fetchone():
        return True
    else:
        return False

def checkPlayerStepInput(cursor,player_input):
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
    cur = cursor
    
    cur.execute("select * from Accession_Association where Accession_Number =:player_input", {"player_input":player_input})
    
    if None != cur.fetchone():
        return True
    else:
        return False

def shouldPlayerAdvance(cursor,player_input,current_step_id):
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

    if checkPlayerStepInput(cur, player_input):
        cur.execute("select Accession_Association from Step_Data where Step_ID =:current_step_id", {"current_step_id":current_step_id})
        current_step_association = cur.fetchone()[0]
        cur.execute("select Accession_Association from Accession_Association where Accession_Number =:player_input", {"player_input":player_input})
        if current_step_association == cur.fetchone()[0]:
            return True
        else: 
            return False
    else:
        return False

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
    
    #cur.execute("update player_data set Current_Action_ID=:current_action_ID where player_ID =:player_ID", {"current_action_ID":current_action_ID, "player_ID":player_ID})
def insertPlayerData(ip):
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

    if checkPlayerCharacterInput(cur,player_character_input):
        cur.execute("select Character_ID from Character_Data where Character_ID =:player_character_input", {"player_character_input": player_character_input})
        current_character_id = cur.fetchone()[0]
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

    if checkPlayerStoryInput(cur,player_story_input):
        cur.execute("select Story_ID from Story_Data where Story_ID =:player_story_input", {"player_story_input": player_story_input})
        current_story_id = cur.fetchone()[0]
        cur.execute("insert into Player_Story_Action values (?,?,?,?)", (None,player_id,current_story_id,player_story_input))

        updatePlayerData(cur,player_id,action_type)

        commitToDB(conn)
    closeDB(conn)

def insertPlayerStepAction(player_id, player_step_input, current_step_id):
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


    if shouldPlayerAdvance(cur, player_step_input, current_step_id):
        cur.execute("select * from Step_Data where Step_ID =:current_step_id",{"current_step_id":current_step_id})
        step_data = cur.fetchone() #Returns a tuple of all the step data that will be used to update player step action.
        cur.execute("select Next_Step_ID from Step_Data where Step_ID =:next_step_id",{"next_step_id":step_data[3]})
        next_step_id = cur.fetchone()[0]
        cur.execute("insert into Player_Step_Action values (?,?,?,?,?,?,?)", (None, player_id, step_data[1], step_data[3], next_step_id, player_step_input, None))
    else:
        cur.execute("select * from Step_Data where Step_ID =:current_step_id",{"current_step_id":current_step_id})
        step_data = cur.fetchone() #Returns a tuple of all the step data that will be used to update player step action.
        cur.execute("insert into Player_Step_Action values (?,?,?,?,?,?,?)", (None, player_id, step_data[2], step_data[1], step_data[3], player_step_input, None))

    updatePlayerData(cur,player_id,action_type)
    commitToDB(conn)
    closeDB(conn)
