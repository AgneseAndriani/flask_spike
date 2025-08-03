from flask import Flask, request, Response
from flask import jsonify
from waitress import serve
from functools import wraps
from flask_cors import CORS

import db_connector

app = Flask(__name__)
CORS(app)
#
# Non interessante
#
def handle_cors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            return Response(status=204, headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, GET, POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            })
        return f(*args, **kwargs)
    return wrapper


@app.route('/test-get-user', methods=['GET', 'OPTIONS'], strict_slashes=False)
def test_get_user():
    user_id = request.args.get('user_id')
    print(user_id)
    u = db_connector.get_single_user(user_id)
    return jsonify(u)


@app.route('/test-get-all-users', methods=['GET', 'OPTIONS'], strict_slashes=False)
def test_get_all_users():
    u = db_connector.get_all_users()
    return jsonify(u)

@app.route('/login', methods=['POST'], strict_slashes=False)
def login_user():
    print(" RICHIESTA POST /login RICEVUTA")

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')


    if not email or not password:
        return jsonify({'success': False, 'message': 'Missing credentials'}), 400

    user = db_connector.get_user_by_email(email)

    if user and user['password'] == password:
        return jsonify({'success': True, 'user': user}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


@app.route('/add-user', methods=['POST', 'OPTIONS'], strict_slashes=False)
@handle_cors
def add_user():
    try:
        data = request.get_json(force=True)
        user_data = data.get("user")
        user = db_connector.insert_user(user_data)
        return jsonify(user)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/complete-point', methods=['POST', 'OPTIONS'], strict_slashes=False)
@handle_cors
def complete_point():
    try:
        data = request.get_json(force=True)
        story_id = data.get('story_id')
        point_id = data.get('point_id')

        if not story_id or not point_id:
            return jsonify({'error': 'story_id e point_id sono obbligatori'}), 400

        updated = db_connector.mark_point_as_completed(story_id, point_id)

        if updated:
            return jsonify({'success': True, 'message': 'Punto completato'})
        else:
            return jsonify({'success': False, 'message': 'Punto non trovato'}), 404

    except Exception as e:
        print(f"Errore in /complete-point: {e}")
        return jsonify({'error': 'Errore interno del server'}), 500

@app.route('/story', methods=['POST', 'OPTIONS'], strict_slashes=False)
@handle_cors
def give_story():
    try:
        data = request.get_json(force=True)

        # Durata in minuti
        duration_str = data.get('duration', '00:00')
        hours, minutes = map(int, duration_str.split(':'))
        total_minutes = hours * 60 + minutes
        print(f"User selected total duration: {total_minutes} minutes")

        # Gestione temi
        genres = data.get('genres', [])
        if not genres:
            return jsonify({'error': 'No genre provided'}), 400

        selected_stories = []
        for genre in genres:
            story = db_connector.get_story_by_genre(genre)
            if story:
                selected_stories.append(story)

        if not selected_stories:
            return jsonify({'error': 'No stories found for the given genres'}), 404

        # Per ora prendi il primo valido, si può migliorare con random o ordinamento
        story = selected_stories[0]
        story_id = story['id']
        points = db_connector.get_points_by_story_id(story_id)
        questions = db_connector.get_questions_by_story_id(story_id)

        # Punti disponibili (nomi) per uso dinamico nel frontend
        point_names = [p['name'] for p in points]

        return jsonify({
            'story': story,
            'points': points,
            'questions': questions,
            'point_names': [p['name'] for p in points],
            'duration_minutes': total_minutes
        })


    except Exception as e:
        print(f"Error in /story: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/complete-story', methods=['POST', 'OPTIONS'], strict_slashes=False)
@handle_cors
def complete_story():
    try:
        data = request.get_json(force=True)
        user_id = data.get('user_id')
        story_id = data.get('story_id')

        if not user_id or not story_id:
            return jsonify({'error': 'user_id e story_id sono obbligatori'}), 400
        print(f"Inserimento storia completata per user {user_id}, story {story_id}")
        inserted = db_connector.insert_story_completed(user_id, story_id)

        if inserted:
            return jsonify({'success': True, 'message': 'Completamento registrato'})
        else:
            return jsonify({'success': False, 'message': 'Errore durante l\'inserimento'}), 500

    except Exception as e:
        print(f"Errore in /complete-story: {e}")
        return jsonify({'error': 'Errore interno del server'}), 500


@app.route('/user-weekly-stats', methods=['GET', 'OPTIONS'], strict_slashes=False)
@handle_cors
def user_weekly_stats():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id è obbligatorio'}), 400

        stats = db_connector.get_user_weekly_stats(user_id)
        return jsonify(stats)

    except Exception as e:
        print(f"Errore in /user-weekly-stats: {e}")
        return jsonify({'error': 'Errore interno del server'}), 500


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=3050)
