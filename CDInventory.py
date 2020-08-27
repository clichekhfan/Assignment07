#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# AHanson, 2020-Aug-15, moved code into functions
# AHanson, 2020-Aug-15, added docstring to new functions.
# AHanson, 2020-Aug-15, added @static method to functions.
# AHanson, 2020-Aug-24, fixed bug with non integer inputs for IDs
# AHanson, 2020-Aug-25, amended program to use .dat file instead of .txt
# AHanson, 2020-Aug-25, amended program to loop when requesting user entries to allow multiple user entries


#------------------------------------------#
import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:

    @staticmethod
    def add_2(userinputs, table):
        """proccesses user inputs into dictionary entries and puts dictionary in table
                    Appends dictionary of user inputs to lstTbl as global.

        loops through list of tuples
        unpacks tuple of user inputs
        sorts indiviual user inputs into dictionary entries
        appends dictionary into table

        Args:
            lstTplUserinput (list of tuples): 2D data structure (list of tuples) that holds multiple user input tuples. from add_1
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        for item in userinputs:
            intID = int(item[0])
            strTitle = item[1]
            strArtist = item[2]
            dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
            table.append(dicRow)

        
    @staticmethod
    def delete_entry(ID, table):
        """Deletes an entry from memory.
                    Modifies table to remove selected entry.

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            ID (integer): numerical ID for dict entry
            
        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == ID:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        with open(file_name, 'rb') as objFile:
            table = pickle.load(objFile) #note: load() loads one line of data
        return table

    @staticmethod
    def write_file(file_name, table):
        """Function writes inventory to file

        opens the file
        takes in the inventory table
        writes each entry in table on seperate line
        closes file

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        with open(file_name, 'wb') as objFile:
           pickle.dump(table, objFile)

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def add_1():
        """
        takes initial user input
        checks that the ID entry is an Integer before return.
        loops until input is 'back'
        returns the user's inputs as a list of tuples.

        Args:
            None.

        Returns:
            lstTplUserinput (list of tuples): 2D data structure (list of tuples) that holds multiple user input tuples.

        """
        print('input "BACK" to exit')
        lstTplUserinputs = []
        while True:
            while True:
                strID = input('Enter ID: ').strip()
                if strID.lower().strip() == 'back':
                    break
                try:
                    int(strID)
                    break
                except(ValueError):
                    print('Invalid entry, please enter a number.')
                    continue
            if strID.lower().strip() == 'back':
                break
            strTitle = input('What is the CD\'s title? ').strip()
            if strTitle.lower().strip() == 'back':
                break
            strArtist = input('What is the Artist\'s name? ').strip()
            if strArtist.lower().strip() == 'back':
                break
            tplUserinputs = (strID,strTitle,strArtist)
            lstTplUserinputs.append(tplUserinputs)
        return lstTplUserinputs

# 0. Create inventory file if none exists
with open(strFileName, 'a') as objFile:
    pass

# 1. When program starts, read in the currently saved Inventory
lstTbl = FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        lstTplUserInputs = IO.add_1()
        # 3.3.2 Add item to the table
        DataProcessor.add_2(lstTplUserInputs, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
        DataProcessor.delete_entry(intIDDel, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




