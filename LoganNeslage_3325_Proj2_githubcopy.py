import sqlite3

#database class for manipulating the items in the database!
class Database:
    #initialization
    def __init__(self, db_name: str = 'iteminventory.csv'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    #creates a table, uses an existing table if there already is one.
    def _create_table(self): 
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Inventory
                                (ItemID INTEGER PRIMARY KEY NOT NULL,
                                ItemName TEXT,
                                ItemType TEXT,
                                Rarity TEXT,
                                Damage REAL VARCHAR(4))''')
            self.conn.commit()
        #error message just in case there's an error creating the table.
        except sqlite3.Error as err:
            print('There was an error creating the table.', err)

    #adds an item, items can have a name, type, rarity, and damage stat, like in a video game.
    def add_item(self, name, itype, rarity, damage): 
        conn = None
        try:
            self.cursor.execute('''INSERT INTO Inventory
                                (ItemName, ItemType, Rarity, Damage)
                                VALUES (?, ?, ?, ?)''',
                                (name, itype, rarity, damage))
            self.conn.commit()
        #vague error message in case there's an error adding items to the table
        except sqlite3.Error as err:
            print('\nA database error has occured.', err)

    #displays all items in the table
    def display_items(self):
        try:
            self.cursor.execute('''SELECT * FROM Inventory''')
            return self.cursor.fetchall()
        #error message in case something goes wrong displaying all the table items.
        except sqlite3.Error as err:
            print('\nA database error has occured.', err)
            return []

    #updates an item in the table, you can change the name, type, rarity, and damage of your item.
    def update_item(self, id, name, itype, rarity, damage): 
        conn = None
        try:
            self.cursor.execute('''UPDATE Inventory
                                    SET ItemName = ?,
                                        ItemType = ?,
                                        Rarity = ?,
                                        Damage = ?
                                    WHERE ItemID == ?''',
                                (name, itype, rarity, damage, id))
            self.conn.commit()
        #error message if there is an error adding items to the table
        except sqlite3.Error as err:
            print('\nA database error has occured.', err)

    #deletes an item of your choosing from the table.
    def delete_item(self, id):
        conn = None
        try:
            self.cursor.execute('''DELETE FROM Inventory
                                    WHERE ItemID == ?''',
                                    (id,))
            self.conn.commit()
        #error message.
        except sqlite3.Error as err:
            print('\nA database error has occured.', err)

    #closes the database!
    def close_db(self):
        self.conn.close()

#item manager class to organize all of the business logic. 
class ItemManager:
    
    #initialization
    def __init__(self):
        self.db = Database()
        
    #function for adding items.
    def add_item(self, name, itype, rarity, damage):
        self.db.add_item(name, itype, rarity, damage)
        
    #updating items
    def update_item(self, id, name, itype, rarity, damage):
        self.db.update_item(id, name, itype, rarity, damage)
        
    #display all items in inventory
    def display_items(self):
        return self.db.display_items()
    
    #delete a specified item based on item id
    def delete_item(self, id):
        self.db.delete_item(id)
        
    #closing the database
    def close_db(self):
        self.db.close_db()

#interface class, for handling all the user interactions.
class Interface:
    #initialization
    def __init__(self):
        self.item = ItemManager()

    #main menu
    def display_menu(self):
        while True:
            print('\n---- Welcome to your Inventory! ----')
            print('1. Acquire a new item')
            print('2. Show inventory')
            print('3. Update an items attributes')
            print('4. Dismantle an item')
            print('5. Close the inventory')
            #the user is prompted to enter a number.
            choice = input('\nSelect an option: ')

            #depending on what number the user chooses, is what operation is carried out.
            #most operations require an item to be in your inventory in order to work.
            if choice == '1':
                self.add_item()
            elif choice == '2':
                self.display_items()
            elif choice == '3':
                self.update_item()
            elif choice == '4':
                self.delete_item()
            elif choice == '5':
                self.close_db()
            else: #hopefully the user enters a number between 1-5, otherwise nothing will happen.
                print(f'Please choose a number between 1-5')

    #the add item function that matters to the user.
    #they enter in all of the desired attributes they want the item to have and it is saved.
    def add_item(self):
        print('\nYouve acquired a new item!')
        name = input('Item Name: ')
        itype = input('Item Type: ')
        rarity = input('Rarity: ')
        damage = input('Damage: ')
        self.item.add_item(name, itype, rarity, damage)
        print('Your weapon was deposited into your inventory.')

    #displays any items the user has in their inventory.
    def display_items(self):
        items = self.item.display_items()
        if items:
            print('\nItems:')
            for item in items:
                print(f'\n------------ '
                      f'\nID: {item[0]} '
                      f'\nName: {item[1]} '
                      f'\nType: {item[2]} '
                      f'\nRarity: {item[3]} '
                      f'\nAttack Power: {item[4]} '
                      f'\n------------')
        else: #this is displayed if the user has no items.
            print('You have no items. Go out and get some!')

    #the user can update the attributes of their item, even changing the item entirely.
    def update_item(self):
        try:
            item_id = int(input('Select an Item ID to Update: '))
            name = input('Enter the new item name: ')
            itype = input('Enter the new items type: ')
            rarity = input('Enter the new items rarity: ')
            damage = input('Enter the new items attack power: ')
            self.item.update_item(item_id, name, itype, rarity, damage)
            print('Item attributes successfully updated.')
        except ValueError: #error message in case the user input is invalid.
            print('Please enter a valid Item ID')

    #deletes an item chosen by the user input.
    def delete_item(self):
        try:
            item_id = int(input("Select an Item ID to Dismantle: "))
            #are you sure message
            sure = input('\nAre you sure you want to dismantle this item? (y/n): ')
            if sure.lower() == 'y':
                self.item.delete_item(item_id)
                #message to make the user question their actions
                print('Item has been dismantled. Was it worth it?')
            else:
                #message to acknowledge the user's choice.
                print('Ok.')
        except ValueError: #error message in case the user input is invalid.
            print('Please enter a valid Item ID')

    #closes the database, and exits the program.
    def close_db(self):
        self.item.close_db()
        print('Program is closing...')
        exit()

if __name__ == '__main__':
    menu = Interface()
    menu.display_menu()
            
    
