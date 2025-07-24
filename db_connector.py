import mysql.connector


def create_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="mydatabase",
        port=3306
    )

def get_single_user(user_id):
    cnx = create_db_connection()
    cursor = cnx.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users where id = %s", (user_id,))
        result = cursor.fetchone()
        print(result)
        return result
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
            print("MySQL connection is closed")

def get_user_by_email(email):
    cnx = create_db_connection()
    cursor = cnx.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users where email = %s", (email,))
        result = cursor.fetchone()
        print(result)
        return result
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
            print("MySQL connection is closed")


def get_all_users():
    cnx = create_db_connection()
    cursor = cnx.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        for u in result:
            print(u)
        return result
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
            print("MySQL connection is closed")


def insert_user(user_data):
    cnx = create_db_connection()
    cursor = cnx.cursor()
    try:
        insert_query = """INSERT INTO users (name, username, email, password, total_km, total_calories, total_steps ) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_query, (user_data['name'],  user_data['username'], user_data['email'],  user_data['password'],  user_data['total_km'], user_data['total_calories'], user_data['total_steps']))
        cnx.commit()
        print(f'MySQL: inserted with ID={cursor.lastrowid}')
        return {'id': cursor.lastrowid, **user_data}
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
            print("MySQL connection is closed")


def get_story_by_genre(genre):
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM story WHERE LOWER(genre) = LOWER(%s) LIMIT 1", (genre,))
    story = cursor.fetchone()
    cursor.close()
    conn.close()
    print(story)
    return story

def get_points_by_story_id(story_id):
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM points WHERE story_id = %s", (story_id,))
    points = cursor.fetchall()
    cursor.close()
    conn.close()
    return points

if __name__ == '__main__':
    get_single_user(1)
    #get_story_by_genre("History")
    # get_all_users()
    # insert_user({'name': 'Pippo', 'email': 'pippo@example.com'})
