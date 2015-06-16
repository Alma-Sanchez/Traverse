#Python version 2.7.9

import sqlite3 #Imports sqlite3 module. Needed to work with the Database.

conn = sqlite3.connect("SAAM_database_test2.db") #Connects database 

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
    cur = conn.cursor()
    cur.execute("select * from Player_Data where IP=:ip", {"ip": ip})
    return cur.fetchone()

def getCurrentPlayerActionFromDB(current_action_ID):
    """
    This function returns a row from the Player_Action table that corresponds 
    to the current player action.

    Parameters:
        currentStepID (int): The ID of the current step taken from the Player_Data table.

    Returns:
        tuple: The tuple containing the row information.

    Examples:
        getCurrentPlayerActionFromDB(playerInfo.currentStepID) => (4 50, 22, 21, 2, 1)
    """
    cur = conn.cursor()
    cur.execute("select * from Player_Action where Action_ID =:currentActionID", {"currentActionID": current_action_ID})
    return cur.fetchone()


def getPrevioustPlayerActionFromDB(previous_step_ID):
    """
    This function returns a row from the Player_Action table that corresponds 
    to the previous player action.

    Parameters:
        PreviousStepID (int): The ID of the previous step taken from the Player_Data table.

    Returns:
        tuple: The tuple containing the row information.

    Examples:
        getPlayerActionFromDB(playerInfo.PreviousStepID) => (4 50, 22, 21, 2, 1)
    """
    cur = conn.cursor()
    cur.execute("select * from Player_Action where Previous_Step_ID=:previousStepID", {"previousStepID": previous_step_ID})
    return cur.fetchone()


def getCharacterFromDB(player_ID):
    """
    This function will return the character the player has most recently selected
    
    Parameters:
        Player_ID

    Returns:
        tuple: character fields
    """
    cur = conn.cursor()
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
    cur = conn.cursor()
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
    cur = conn.cursor()
    cur.execute("select * from Step_Data where Current_Step_ID =:Step_ID", {"Step_ID": current_step_ID})
    return cur.fetchone()


def getAccessionNumbersFromDB(accession_association):
    """
    This function will query the database and return the list of possible accesion numbers associated with a particular accession association keyword

    Parameters:
        accessionAssociation

    Returns:
        tuple: accession numbers
    """
    cur = conn.cursor()
    cur.execute("select Accession_Number from Accession_Data where Accession_Association =: accessionAssociation", {"accessionAssociation": accession_association})
    return cur.fetchall()


def getCharacterData(current_character_ID):
    """
    This function will query the database and return the correct character data for the character the player is currently using.

    Parameters:
        Current_Character_ID

    Returns:
        tuple: character fields 
    """
    cur = conn.cursor()
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
    cur = conn.cursor()
    cur.execute("select * from Story_Data where Current_Story_ID =:currentStoryID", {"currentStoryID": current_story_ID})
    return cur.fetchone()

def insertPlayerData(ip,current_story_ID):
    """
    This function will insert a new player's data into the SQLite Database.

    Parameters:
        ip: The new player's IP address.
        current_story: The current story that the player has chosen. This will be used to get the step number.

    Returns:
        None
    """
    cur = conn.cursor()
    cur.execute("select Step_ID from Step_Data where Story_ID =:current_story_ID", {"current_story_ID":current_story_ID})
    current_step_ID = cur.fetchone()
    cur.execute("insert into Player_Data values (?,?,?)", (None,ip,None))
    conn.commit()

def insertPlayerAction(player_ID,current_story_ID,current_character_ID):
    """
    This function inserts player action into the database.

    Parameters:
        player_ID: The player's unique ID in the database.
        current_story_ID: The player's current story ID.
        current_character_ID: The player's current character ID>

    Returns:
        None
    """
    cur = conn.cursor()

    cur.execute("select * from Step_Data where Story_ID =:current_story_ID", {"current_story_ID":current_story_ID})
    step_data = cur.fetchone()
    cur.execute("insert into Player_Action values (?,?,?,?,?,?)", (None,player_ID,step_data[1],step_data[2],current_story_ID,current_character_ID))

    cur.execute("select max(Action_ID) from Player_Action where Player_ID =:player_ID", {"player_ID":player_ID})
    current_action_ID = cur.fetchone()[0]
    cur.execute("update player_data set Current_Action_ID=:current_action_ID where player_ID =:player_ID", {"current_action_ID":current_action_ID, "player_ID":player_ID})
    conn.commit()