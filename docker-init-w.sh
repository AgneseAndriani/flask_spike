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
    latitude INT,
    longitude INT,
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

INSERT INTO story (title, intro, theme, genre, duration, km, calories, steps) VALUES (
  'The Eternal Walk',
  'Discover the timeless wonders of ancient Rome.',
  'As you walk these legendary streets, you will uncover secrets long buried beneath centuries of history.
Follow the path of the ancients — a journey of glory, wisdom, and power.
Your mission: unlock the memory of the Eternal City, one landmark at a time.

1. The Colosseum - Piazza del Colosseo
Here, blood met sand in spectacles of courage and survival.
"To understand Romes strength, feel the echo of the crowd." Head northwest on Via dei Fori Imperiali for 350 meters.

2. Roman Forum - Via della Salara Vecchia
This was the hub of public life in Ancient Rome.
Speeches, trials, and triumphs happened here.
"To know their vision, stand where emperors stood."

3. Palatine Hill - Via di San Gregorio
Birthplace of Rome, home to its emperors.
This is where Romulus first laid the stones of the Eternal City.
"Every empire has a beginning."

Conclusion:
You have followed in the footsteps of gladiators, orators, and kings.
The Eternal Walk lives on — in the stories you now carry with you.',
  'History',
  150,
  5,
  300,
  6500
),
('Titolo', 'Intro', 'Trama', 'Adventure', 100, 5, 300, 600);


INSERT INTO points (story_id, point_id, check_completed, latitude, longitude, name, text) VALUES
(1, 1, 0, 41890234, 12488623, 'Colosseum', 'Welcome to the Colosseum, the heart of Roman gladiatorial battles.'),
(1, 2, 0, 41889500, 12488400, 'Roman Forum', 'Explore the Roman Forum, the hub of ancient Roman public life.'),
(1, 3, 0, 41891000, 12487900, 'Palatine Hill', 'Climb the Palatine Hill, the birthplace of Rome and home to emperors.'),
(2,1,0, 0000, 0000, 'punto 1', 'trama');

INSERT INTO questions (story_id, point_id, question, first_answer, second_answer, third_answer, correct_answer_index) VALUES
(1, 1, 'What was the main use of the Colosseum?', 'Religious rituals', 'Gladiator fights', 'Senate meetings', 1),
(1, 1, 'How many people could the Colosseum hold?', '10,000', '25,000', '50,000', 2),
(2,1,'ciao', 'ciaouno', 'ciaodue', 'ciaotre', 1);
EOF

echo "MySQL setup completed successfully!"

# Connect to MySQL
docker exec -it mysql-container mysql -uroot -p
