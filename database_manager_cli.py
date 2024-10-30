import argparse
import sqlite3

# Connect to the database
conn = sqlite3.connect('sale_reminders.db')
cursor = conn.cursor()

def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS reminders
                      (discord_username_id INTEGER, game_title TEXT, channel_id INTEGER)''')
    conn.commit()

def add_reminder(discord_username_id, game_title, channel_id):
    cursor.execute('INSERT INTO reminders (discord_username_id, game_title, channel_id) VALUES (?, ?, ?)', 
                   (discord_username_id, game_title, channel_id))
    conn.commit()
    print(f"Reminder added for {game_title}")

def remove_reminder(discord_username_id, game_title):
    cursor.execute('DELETE FROM reminders WHERE discord_username_id = ? AND game_title = ?', 
                   (discord_username_id, game_title))
    conn.commit()
    print(f"Reminder removed for {game_title}")

def list_reminders():
    cursor.execute('SELECT discord_username_id, game_title, channel_id FROM reminders')
    reminders = cursor.fetchall()
    for reminder in reminders:
        print(f"User ID: {reminder[0]}, Game: {reminder[1]}, Channel ID: {reminder[2]}")

def clear_reminders():
    cursor.execute('DELETE FROM reminders')
    conn.commit()
    print("All reminders cleared")

def main():
    parser = argparse.ArgumentParser(description="Manage the sale reminders database.")
    subparsers = parser.add_subparsers(dest="command")

    # Add reminder
    parser_add = subparsers.add_parser('add', help='Add a new reminder')
    parser_add.add_argument('discord_username_id', type=int, help='Discord user ID')
    parser_add.add_argument('game_title', type=str, help='Game title')
    parser_add.add_argument('channel_id', type=int, help='Channel ID')

    # Remove reminder
    parser_remove = subparsers.add_parser('remove', help='Remove an existing reminder')
    parser_remove.add_argument('discord_username_id', type=int, help='Discord user ID')
    parser_remove.add_argument('game_title', type=str, help='Game title')

    # List reminders
    parser_list = subparsers.add_parser('list', help='List all reminders')

    # Clear reminders
    parser_clear = subparsers.add_parser('clear', help='Clear all reminders')

    args = parser.parse_args()

    if args.command == 'add':
        add_reminder(args.discord_username_id, args.game_title, args.channel_id)
    elif args.command == 'remove':
        remove_reminder(args.discord_username_id, args.game_title)
    elif args.command == 'list':
        list_reminders()
    elif args.command == 'clear':
        clear_reminders()
    else:
        parser.print_help()

if __name__ == '__main__':
    create_table()
    main()