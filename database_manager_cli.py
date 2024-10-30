import argparse
import sqlite3

# Connect to the database
conn = sqlite3.connect('sale_reminders.db')
cursor = conn.cursor()

def create_table():
    """Create the reminders table if it doesn't exist."""
    cursor.execute('''CREATE TABLE IF NOT EXISTS reminders
                      (discord_username TEXT, game_title TEXT)''')
    conn.commit()
    print("Table created successfully.")

def add_reminder(discord_username, game_title):
    """Add a sale reminder to the database."""
    cursor.execute('INSERT INTO reminders (discord_username, game_title) VALUES (?, ?)', 
                   (discord_username, game_title))
    conn.commit()
    print(f"Reminder added for {discord_username} - {game_title}")

def list_reminders():
    """List all sale reminders in the database."""
    cursor.execute('SELECT * FROM reminders')
    reminders = cursor.fetchall()
    for reminder in reminders:
        print(f"Discord Username: {reminder[0]}, Game Title: {reminder[1]}")

def delete_reminder(discord_username, game_title):
    """Delete a sale reminder from the database."""
    cursor.execute('DELETE FROM reminders WHERE discord_username = ? AND game_title = ?', 
                   (discord_username, game_title))
    conn.commit()
    print(f"Reminder deleted for {discord_username} - {game_title}")

def delete_all():
    """Delete all sale reminders from the database."""
    cursor.execute('DELETE FROM reminders')
    conn.commit()
    print("All reminders deleted.")

def delete_duplicates():
    """Delete duplicate sale reminders from the database."""
    cursor.execute('''DELETE FROM reminders
                      WHERE rowid NOT IN (
                          SELECT MIN(rowid)
                          FROM reminders
                          GROUP BY discord_username, game_title
                      )''')
    conn.commit()
    print("Duplicate reminders deleted.")

def main():
    parser = argparse.ArgumentParser(description="Manage the sale reminders database.")
    subparsers = parser.add_subparsers(dest='command')

    # Create table command
    subparsers.add_parser('create_table', help='Create the reminders table.')

    # Add reminder command
    add_parser = subparsers.add_parser('add', help='Add a sale reminder.')
    add_parser.add_argument('discord_username', type=str, help='Discord username')
    add_parser.add_argument('game_title', type=str, help='Game title')

    # List reminders command
    subparsers.add_parser('list', help='List all sale reminders.')

    # Delete reminder command
    delete_parser = subparsers.add_parser('delete', help='Delete a sale reminder.')
    delete_parser.add_argument('discord_username', type=str, help='Discord username')
    delete_parser.add_argument('game_title', type=str, help='Game title')

    # Delete all reminders command
    subparsers.add_parser('delete_all', help='Delete all sale reminders.')

    # Delete duplicates command
    subparsers.add_parser('delete_duplicates', help='Delete duplicate sale reminders.')

    args = parser.parse_args()

    if args.command == 'create_table':
        create_table()
    elif args.command == 'add':
        add_reminder(args.discord_username, args.game_title)
    elif args.command == 'list':
        list_reminders()
    elif args.command == 'delete':
        delete_reminder(args.discord_username, args.game_title)
    elif args.command == 'delete_all':
        delete_all()
    elif args.command == 'delete_duplicates':
        delete_duplicates()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
    conn.close()