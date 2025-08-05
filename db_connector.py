import mysql.connector
from datetime import datetime


def create_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="mydatabase",
        port=3306
    )

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
    print(points)
    return points

def get_questions_by_story_id(story_id):
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM questions WHERE story_id = %s", (story_id,))
    questions = cursor.fetchall()
    cursor.close()
    conn.close()
    print(questions)
    return questions

def mark_point_as_completed(story_id, point_id):
    conn = create_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE points SET check_completed = 1 WHERE story_id = %s AND point_id = %s",
            (story_id, point_id)
        )
        conn.commit()
        updated_rows = cursor.rowcount
        return updated_rows > 0
    except mysql.connector.Error as error:
        print(f"Errore MySQL durante update point: {error}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def insert_story_completed(user_id, story_id):
    cnx = create_db_connection()
    cursor = cnx.cursor()
    try:
        insert_query = """
               INSERT INTO story_completed (user_id, story_id, completed_at)
               VALUES (%s, %s, CURDATE())
               """
        cursor.execute(insert_query, (user_id, story_id))
        cnx.commit()
        return True
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
        return False
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
            print("MySQL connection is closed")




def get_user_weekly_stats(user_id):
    try:
        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SET lc_time_names = 'en_US'")
        cursor.execute("""
            SELECT 
          DATE_FORMAT(sc.completed_at, '%a') AS day,
          SUM(s.km) AS total_km,
          SUM(s.steps) AS total_steps,
          SUM(s.calories) AS total_calories
        FROM 
          story_completed sc
        JOIN 
          story s ON sc.story_id = s.id
        WHERE 
          sc.user_id = %s
        GROUP BY 
          day
        ORDER BY 
          FIELD(day, 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun');
        """, (user_id,))

        result = cursor.fetchall()
        print("🎯 Weekly Stats Query Result:", result)

        for row in result:
            row['total_km'] = float(row['total_km'] or 0)
            row['total_steps'] = float(row['total_steps'] or 0)
            row['total_calories'] = float(row['total_calories'] or 0)

        return result
    except Exception as e:
        print(f"Errore get_user_weekly_stats: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_all_goals_with_user_progress(user_id):
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT
            g.goal_name,
            g.title,
            g.description,
            g.type,
            g.category,
            g.target,
            COALESCE(ug.progress, 0) AS progress,
            COALESCE(ug.completed, false) AS completed
        FROM goals g
        LEFT JOIN user_goal_progress ug
            ON g.goal_name = ug.goal_name AND ug.user_id = %s
    """
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def upsert_user_goal_progress(user_id, goal_name, progress, completed):
    conn = create_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO user_goal_progress (user_id, goal_name, progress, completed)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            progress = VALUES(progress),
            completed = VALUES(completed),
            updated_at = NOW()
    """
    cursor.execute(query, (user_id, goal_name, progress, completed))
    conn.commit()
    cursor.close()
    conn.close()
    return True


if __name__ == '__main__':
    get_story_by_genre("History")
