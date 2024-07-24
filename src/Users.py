import pandas as pd
import bcrypt
import os

# User credentials
users = {
    'user1': '1234',
    'user2': '1234',
    'user3': '1234',
    'user4': '1234',
    'user5': '1234'
}

# Hash passwords
hashed_passwords = {username: bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') for username, password in users.items()}

# Create a DataFrame and save to Excel
df = pd.DataFrame(list(hashed_passwords.items()), columns=['username', 'password'])
df.to_excel('users.xlsx', index=False)
#df.to_excel(os.getcwd()+'/users.xlsx', index=False)

