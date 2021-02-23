import sqlite3

def check_users():
    connection = sqlite3.connect('todolist.db',check_same_thread=False)
    cursor= connection.cursor()
    cursor.execute(f"select username from users order by id desc;")
    db_users=cursor.fetchall()
    usrs=[]
    for i in range(len(db_users)):
        person=db_users[i][0]
        usrs.append(person)
    
    connection.commit()
    cursor.close()
    connection.close()
    return usrs

def signup(username, password):
    connection = sqlite3.connect('todolist.db',check_same_thread=False)
    cursor= connection.cursor()
    cursor.execute(f"select password from users where username like '{username}'")
    exist=cursor.fetchone()
    if exist is None:
        cursor.execute(f"insert into users(username, password, reg_date) values('{username}','{password}',datetime('now','localtime'));")
        connection.commit()
        cursor.close()
        connection.close()
        message= 'You have successfully signed up!'
        return message
    else:
        error_message='User already exists!'
        return error_message

def check_password(username):
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f'select password from users where username like "{username}";')
    passwd= cursor.fetchone()
    if passwd is None:
        connection.commit()
        cursor.close()
        connection.close()
        return passwd
    else:
        passwd=passwd[0]
        connection.commit()
        cursor.close()
        connection.close()
        return passwd

def list_add(listname, created_by):
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f'select listname from lists where listname like "{listname}";')
    passwd= cursor.fetchone()
    if passwd is None:
        cursor.execute(f"insert into lists(listname, created_by, created_on, done) values('{listname}','{created_by}',datetime('now','localtime'), False);")
        connection.commit()
        cursor.close()
        connection.close()
        return ''
    else:
        return f"There is listname like '{listname}'."

def get_lists(username):
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f"select * from lists where created_by like '{username}' order by id desc;")
    db_lists=cursor.fetchall()
    usrs=[]
    for i in range(len(db_lists)):
        person=db_lists[i]
        usrs.append(person)
    connection.commit()
    cursor.close()
    connection.close()
    return usrs

def deleteList(list_name_for_database, username):
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f"delete from lists where id={list_name_for_database};")
    connection.commit()
    cursor.close()
    connection.close()

def doneList(done, username):
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f"select done from lists WHERE  id={done};")
    booool=cursor.fetchone()[0]
    if booool:
        cursor.execute(f"UPDATE lists SET done=False WHERE  id={done};")
    else:
        cursor.execute(f"UPDATE lists SET done=True WHERE  id={done};")
    connection.commit()
    cursor.close()
    connection.close()

def deleteAllLists(username):
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f"delete from lists where created_by like '{username}' and created_by like '{username}';")
    connection.commit()
    cursor.close()
    connection.close()

def changeList(id, new_name):
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f"UPDATE lists SET listname={new_name} WHERE  id={id};")
    connection.commit()
    cursor.close()
    connection.close()

def check_admin(admin_name):
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f'select password from admins where admin_name like "{admin_name}";')
    passwd= cursor.fetchone()
    if passwd is None:
        connection.commit()
        cursor.close()
        connection.close()
        return passwd
    else:
        passwd=passwd[0]
        connection.commit()
        cursor.close()
        connection.close()
        return passwd

def get_total_users():
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f'select count(*) from users;')
    users=cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return users



def get_total_lists():
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f"SELECT seq FROM sqlite_sequence where name LIKE ('lists');")
    lists=cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return lists

def get_total_users_24():
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f"SELECT count(*) FROM users where reg_date > strftime('%Y-%m-%d %H:%H:%S', 'now', '-1 days');")
    users=cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return users



def get_total_lists_24():
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f"SELECT count(*) FROM lists where created_on > strftime('%Y-%m-%d %H:%H:%S', 'now', '-1 days');")
    lists=cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return lists

def get_total_users_all():
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f'select username, reg_date from users;')
    users_l=cursor.fetchall()
    users= users_l
    connection.commit()
    cursor.close()
    connection.close()
    return users



def get_total_lists_all():
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f"SELECT listname, created_by, created_on, done FROM lists;")
    lists=cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return lists

def get_total_users_24_all():
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f"SELECT username, reg_date FROM users where reg_date > strftime('%Y-%m-%d %H:%H:%S', 'now', '-1 days');")
    users=cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return users



def get_total_lists_24_all():
    connection= sqlite3.connect('todolist.db', check_same_thread=False)
    cursor=connection.cursor()
    cursor.execute(f"SELECT listname, created_by, created_on, done FROM lists where created_on > strftime('%Y-%m-%d %H:%H:%S', 'now', '-1 days');")
    lists=cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return lists