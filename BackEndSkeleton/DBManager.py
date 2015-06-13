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
    """
    cur = conn.cursor()
    cur.execute("select * from Player_Data where IP=:ip", {"ip": ip})
    return cur.fetchone()

def getCurrentPlayerActionFromDB(currentStepID):
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
    cur.execute("select * from Player_Action where Current_Step_ID =:current_Step_ID", {"Current_Step_ID": Current_Step_ID})
    return cur.fetchone()


def getPrevioustPlayerActionFromDB(previousStepID):
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
    cur.execute("select * from Player_Action where Previous_Step_ID=:Previous_Step_ID", {"Previous_Step_ID": Previous_Step_ID})
    return cur.fetchone()


def getCharacterFromDB(Player_ID):
    """
    This function will return the character the player has most recently selected
    
    Parameters:
    (Player_ID

    Returns:
    tuple: character fields
    """
    cur = conn.cursor()
    cur.execute("select Character_ID from Player_Action where Character_ID=:Character_ID", {"Character_ID": Character_ID})
    return cur.fetchone()
    pass

def getStoryFromDB(Player_ID):
    """
    This function will query the database and return the correct story associated with the player.

    Parameters:
    player_ID

    Returns:
    tuple: Story fields
    """
    cur = conn.cursor()
    cur.execute("select Story_ID from Player_Action where max Action_ID in Story_ID=:Story_ID", {"Story_ID": Story_ID})
    return cur.fetchone()
    pass

def getStepDataFromDB(Current_Step_ID):
    """
    This function will query the database and return the correct step data for the step the player is currently on.

    Parameters:
    Current_Step_ID

    Returns:
    tuple: Step fields
    """
    cur = conn.cursor()
    cur.execute("select * from Step_Data where Current_Step_ID =:Step_ID", {"Step_ID": Current_Step_ID})
    return cur.fetchone()


def getAccessionNumberFromDB(Accession_Association):
    cur = conn.cursor()
    cur.execute("select Accession_Number from Accession_Data where Accession_Number =: Accession_Number", {"Accession_Number": Accesion_Number})
    return cur.fetchall()


def getCharacterData(Current_Character_ID):
    """
    This function will query the database and return the correct character data for the character the player is currently using.

    Parameters:
    Current_Character_ID

    Returns:
    tuple: character fields 
    """
    cur = conn.cursor()
    cur.execute("select * from Step_Data where Current_Character_ID =:Character_ID", {"Character_ID": Current_Character_ID})
    return cur.fetchone()

def getStoryData(Current_Story_ID):
    """
    This function will query the database and return the correct story data for the story the player is currently playing.

    Parameters:
    Current_Story_ID

    Returns:
    tuple: story fields
    """
    cur = conn.cursor()
    cur.execute("select * from Story_Data where Current_Story_ID =:Story_ID", {"Story_ID": Current_Story_ID})
    return cur.fetchone()