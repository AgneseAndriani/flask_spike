# Pull mysql official image from Docker Hub
docker pull mysql:latest

# Create container with name = mysql-container running on port 3306
# PW = root
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:latest

echo "Waiting for MySQL to initialize..."

# Wait for MySQL to be ready
until docker exec mysql-container mysql -uroot -proot -e "SELECT 1" &> /dev/null
do
  echo "Initializing MySQL..."
  sleep 1
done

echo "MySQL is up and running!"

# Create database and table
docker exec -i mysql-container mysql -uroot -proot << EOF
CREATE DATABASE mydatabase;
USE mydatabase;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    username VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100),
    total_km INT,
    total_calories INT,
    total_steps INT
);

CREATE TABLE IF NOT EXISTS story (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    intro VARCHAR(255),
    theme TEXT,
    genre VARCHAR(100),
    duration INT,
    km INT,
    calories INT,
    steps INT
);

CREATE TABLE IF NOT EXISTS points (
    story_id INT,
    point_id INT,
    check_completed TINYINT,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    name VARCHAR(100),
    text VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS questions(
    story_id INT,
    point_id INT,
    question VARCHAR(100),
    first_answer VARCHAR(100),
    second_answer VARCHAR(100),
    third_answer VARCHAR(100),
    correct_answer_index TINYINT
);

CREATE TABLE IF NOT EXISTS story_completed (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    story_id INT,
    completed_at DATE
);

CREATE TABLE goals (
  goal_name VARCHAR(100) PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  type TEXT,
  category TEXT,
  target INTEGER NOT NULL
);

CREATE TABLE user_goal_progress (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  goal_name VARCHAR(100) NOT NULL,
  progress INTEGER DEFAULT 0,
  completed BOOLEAN DEFAULT FALSE,
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE (user_id, goal_name),
  FOREIGN KEY (goal_name) REFERENCES goals(goal_name)
);

CREATE TABLE preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    genre VARCHAR(100),
    point_of_interest VARCHAR(100)
);



INSERT INTO story (title, intro, theme, genre, duration, km, calories, steps) VALUES (
  'The Eternal Walk',
  'Discover the timeless wonders of ancient Rome.',
  'As you walk these legendary streets, you will uncover secrets long buried beneath centuries of history.
Follow the path of the ancients — a journey of glory, wisdom, and power.
Your mission: unlock the memory of the Eternal City, one landmark at a time.
Start walking to unlock points of interest.
',
  'History',
  150,
  5,
  300,
  6500
),
('Titolo', 'Intro', 'Trama', 'Adventure', 100, 5, 300, 600);


INSERT INTO points (story_id, point_id, check_completed, latitude, longitude, name, text) VALUES
(1, 1, 0, 40.503160, 17.6482112, 'Colosseum', 'Welcome to the Colosseum, the heart of Roman gladiatorial battles. Here, blood met sand in spectacles of courage and survival. To understand Rome''s strength, feel the echo of the crowd. Head northwest on Via dei Fori Imperiali for 350 meters.'),
(1, 2, 0, 40.503160, 17.6482112, 'Roman Forum', 'Explore the Roman Forum, the hub of ancient Roman public life. Speeches, trials, and triumphs happened here. To know their vision, stand where emperors stood. Head northwest on Via dei Fori Imperiali for 350 meters.'),
(1, 3, 0, 40.5031929, 17.6482502, 'Palatine Hill', 'Climb the Palatine Hill, the birthplace of Rome and home to emperors. This is where Romulus first laid the stones of the Eternal City. Every empire has a beginning. Conclusion: You have followed in the footsteps of gladiators, orators, and kings.'),
(2, 1, 0, 45.464211, 9.191383, 'punto 1', 'trama');

INSERT INTO questions (story_id, point_id, question, first_answer, second_answer, third_answer, correct_answer_index) VALUES
(1, 1, 'What was the main use of the Colosseum?', 'Religious rituals', 'Gladiator fights', 'Senate meetings', 1),
(1, 2, 'How many people could the Colosseum hold?', '10,000', '25,000', '50,000', 2),
(1, 3, 'What material was used for the Colosseum?', 'Wood', 'Marble', 'Concrete', 2),
(2, 1, 'Ciao?', 'ciaouno', 'ciaodue', 'ciaotre', 1);

INSERT INTO goals (goal_name, title, description, type, category, target) VALUES
  ('first_story', 'Completa la tua prima storia', 'Inizia il tuo viaggio e completa una storia qualsiasi.', 'one-time', 'story', 1),
  ('long_story_60min', 'Completa una storia da 60 minuti', 'Porta a termine una storia con una durata di almeno un’ora.', 'one-time', 'story', 60),
  ('walk_5km', 'Percorri 5 km', 'Cammina o corri almeno 5 chilometri.', 'one-time', 'movement', 5),
  ('monthly_steps_20000', 'Fai 20.000 passi in un mese', 'Muoviti costantemente e raggiungi 20.000 passi entro fine mese.', 'monthly', 'movement', 20000);

EOF

echo "MySQL setup completed successfully!"

# Connect to MySQL
docker exec -it mysql-container mysql -uroot -p
