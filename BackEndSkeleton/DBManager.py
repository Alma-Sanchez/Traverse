#Python version 2.7.9

import sqlite3 #Imports sqlite3 module. Needed to work with the Database.
import db_creator

def connectToDB():
    return sqlite3.connect("SAAM_database_test2.db") #Connects database

def cursorForDB(connection):
    return connection.cursor()

def checkDB():
    cur = cursorForDB(connectToDB())
    cur.execute("select * from sqlite_master where type='table'")
    if 14 != len(cur.fetchall()):
        db_creator.dropTables(connectToDB())
        db_creator.createTables(connectToDB())
        db_creator.populateTables(connectToDB())

checkDB()

def getPlayerFromDB(ip):
    """
    This function will get the player's IP address from the database and returns the player data.

    Parameters:
        ip (int): The IP address of the player connecting to the web.py server.

    Returns:
        tuple: A row from the Player_Data table associated with the player's IP address.

    Examples:
        getPlayerFromDB(playerinfo.ip) => (1,1.1.1.1,2)
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select * from Player_Data where IP=:ip", {"ip": ip})
    return cur.fetchone()

def getPlayerCharacterActionFromDB(player_id):
    """
    NEED DOCSTRING.
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select * from Player_Character_Action where Player_ID =:player_id", {"player_id": player_id})
    return cur.fetchone()

def getPlayerStoryActionFromDB(player_id):
    """
    NEED DOCSTRING.
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select * from Player_Story_Action where Player_ID =:player_id", {"player_id": player_id})
    return cur.fetchone()

def getPlayerStepActionFromDB(player_id):
    """
    NEED DOCSTRING.
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select * from Player_Step_Action where Player_ID =:player_id", {"player_id": player_id}) 
    return cur.fetchone()

def getCharacterFromDB(player_ID):
    """
    This function will return the character the player has most recently selected
    
    Parameters:
        Player_ID

    Returns:
        tuple: character fields
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select max(Current_Character_ID) from Player_Action where Player_ID=:playerID", {"playerID": player_ID})
    return cur.fetchone()[0]

def getStoryFromDB(player_ID):
    """
    This function will query the database and return the correct story associated with the player.

    Parameters:
        Player_ID

    Returns:
        tuple: Story fields
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select max(Current_Story_ID) from Player_Action where Player_ID=:playerID", {"playerID": player_ID})
    return cur.fetchone()[0]

def getStepDataFromDB(current_step_ID):
    """
    This function will query the database and return the correct step data for the step the player is currently on.

    Parameters:
        Current_Step_ID

    Returns:
        tuple: Step fields
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select * from Step_Data where Current_Step_ID =:Step_ID", {"Step_ID": current_step_ID})
    return cur.fetchone()


def getAccessionNumbersFromDB(accession_association):
    """
    This function will query the database and return the list of possible accesion numbers associated with a particular accession association keyword

    Parameters:
        accession_association

    Returns:
        tuple: accession numbers
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select Accession_Number from Accession_Data where Accession_Association =: accessionAssociation", {"accessionAssociation": accession_association})
    return cur.fetchall()

def getAccessionAssociationFromDB(accession_number):
    """
    Need Docstring
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select Accession_Association from Accession_Association where Accession_Number =:accession_number", {"accession_number":accession_number})
    accession_association = cur.fetchone()[0]
    return accession_association

def getCharacterData(current_character_ID):
    """
    This function will query the database and return the correct character data for the character the player is currently using.

    Parameters:
        Current_Character_ID

    Returns:
        tuple: character fields 
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select * from Step_Data where Current_Character_ID =:currentCharacterID", {"currentCharacterID": current_character_ID})
    return cur.fetchone()

def getStoryData(current_story_ID):
    """
    This function will query the database and return the correct story data for the story the player is currently playing.

    Parameters:
        Current_Story_ID

    Returns:
        tuple: story fields
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select * from Story_Data where Current_Story_ID =:currentStoryID", {"currentStoryID": current_story_ID})
    return cur.fetchone()

def checkPlayerCharacterInput(player_character_input):
    """
    NEED DOCSTRING.
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select Character_ID from Character_Data where Character_ID =:player_character_input", {"player_character_input": player_character_input})
    
    if None != cur.fetchone():
        return True
    else:
        return False

def checkPlayerStoryInput(player_story_input):
    """
    NEED DOCSTRING.
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select Story_ID from Story_Data where Story_ID =:player_story_input", {"player_story_input": player_story_input})
    
    if None != cur.fetchone():
        return True
    else:
        return False

def checkPlayerStepInput(player_input):
    """
    This function checks the player input with the current step 
    and returns a boolean if the player's input is correct.

    Parameters:
        player_input: The player's input.
        current_step_ID: The current step of the story which the player is on.

    Returns:
        boolean: True if player's input is correct. False if the player's input is incorrect.

    Examples:
        checkPlayerInput(123.12,1) => False
    """
    cur = cursorForDB(connectToDB())
    cur.execute("select * from Accession_Association where Accession_Number =:player_input", {"player_input":player_input})
    
    if None != cur.fetchone():
        return True
    else:
        return False

def shouldPlayerAdvance(player_input,current_step_id):
    """
    NEED DOCSTRING.
    """
    cur = cursorForDB(connectToDB())

    if checkPlayerStepInput(player_input):
        cur.execute("select Accession_Association from Step_Data where Step_ID =:current_step_id", {"current_step_id",current_step_id})
        current_step_association = cur.fetchone()[0]
        cur.execute("select Accession_Association from Accession_Association where Accession_Number =:player_input", {"player_input":player_input})
        if current_step_association == cur.fetchone()[0]:
            return True
        else: 
            return False
    else:
        return False


def insertPlayerData(ip):
    """
    This function will insert a new player's data into the SQLite Database.

    Parameters:
        ip: The new player's IP address.
        current_story: The current story that the player has chosen. This will be used to get the step number.

    Returns:
        None
    """
    conn = connectToDB()
    cur = cursorForDB(conn)
    cur.execute("insert into Player_Data values (?,?,?,?,?)", (None,ip,None,None,None))
    conn.commit()

def insertPlayerCharacterAction(player_id, player_character_input):
    conn = connectToDB()
    cur = cursorForDB(conn)
    if checkPlayerCharacterInput(player_character_input):
        cur.execute("select Character_ID from Character_Data where Character_ID =:player_character_input", {"player_character_input": player_character_input})
        current_character_id = cur.fetchone()[0]
        cur.execute("insert into Player_Character_Action values (?,?,?,?)", (None,player_id,current_character_id,player_character_input))

        cur.execute("select max(Character_Action_ID) from Player_Character_Action where Player_ID =:player_id", {"player_id":player_id})
        current_character_id = cur.fetchone()[0]
        cur.execute("update player_data set Current_Character_Action_ID=:current_character_id where player_ID =:player_id", {"current_character_id":current_character_id, "player_id":player_id})
        conn.commit()

def insertPlayerAction(player_ID,current_story_ID,current_character_ID,player_input):
    """
    This function inserts player action into the database.

    Parameters:
        player_ID: The player's unique ID in the database.
        current_story_ID: The player's current story ID.
        current_character_ID: The player's current character ID.

    Returns:
        None
    """
    conn = connectToDB()
    cur = cursorForDB(conn)

    cur.execute("select Current_Action_ID from Player_Data where Player_ID =:player_ID", {"player_ID":player_ID})
   
    if None == cur.fetchone()[0]:
        if None == current_character_ID or None == current_story_ID:
            cur.execute("insert into Player_Action values (?,?,?,?,?,?,?)", (None,player_ID,None,None,current_story_ID,current_character_ID,None))
        else:
            cur.execute("select * from Step_Data where Story_ID =:current_story_ID", {"current_story_ID":current_story_ID})
            step_data = cur.fetchone()
            cur.execute("insert into Player_Action values (?,?,?,?,?,?,?)", (None,player_ID,step_data[1],step_data[2],current_story_ID,current_character_ID,None))
    else:
        cur.execute("select Current_Action_ID from Player_Data where Player_ID =:player_ID", {"player_ID":player_ID})
        action_ID = cur.fetchone()[0]
        cur.execute("select Current_Step_ID from Player_Action where Action_ID =:action_ID", {"action_ID":action_ID})
        current_step_ID = cur.fetchone()[0]

        if checkPlayerInput(player_input,current_step_ID) == True:
            cur.execute("select * from Step_Data where Step_ID =:current_step_ID", {"current_step_ID":current_step_ID})
            step_data = cur.fetchone()
            cur.execute("insert into Player_Action values (?,?,?,?,?,?,?)", (None,player_ID,step_data[3],step_data[1],current_story_ID,current_character_ID,player_input))
        else:
            if None == current_character_ID or None == current_story_ID:
                cur.execute("insert into Player_Action values (?,?,?,?,?,?,?)", (None,player_ID,None,None,current_story_ID,current_character_ID,None))
            else:
                cur.execute("select * from Step_Data where Story_ID =:current_story_ID", {"current_story_ID":current_story_ID})
                step_data = cur.fetchone()
                cur.execute("insert into Player_Action values (?,?,?,?,?,?,?)", (None,player_ID,step_data[1],step_data[2],current_story_ID,current_character_ID,player_input))

    cur.execute("select max(Action_ID) from Player_Action where Player_ID =:player_ID", {"player_ID":player_ID})
    current_action_ID = cur.fetchone()[0]
    cur.execute("update player_data set Current_Action_ID=:current_action_ID where player_ID =:player_ID", {"current_action_ID":current_action_ID, "player_ID":player_ID})
    conn.commit()

insertPlayerCharacterAction(1,1)