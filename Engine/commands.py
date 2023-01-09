from database_manager import DatabaseManager

db = DatabaseManager('data/bookmarks.db')

class CreateUserTableCommand:
    def execute(self):
        db.create_table('bookmarks', {
            'id':'integer primary key autoincrement',
            'name':'text not null',            
        })