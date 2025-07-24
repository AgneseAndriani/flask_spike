# Pull mysql official image from Docker Hub
docker pull mysql:latest

# Create container with name = mysql-container running on port 3306
# PW = root
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:latest

echo "

Waiting for MySQL to initialize...

"

sleep 15

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
    intro VARCHAR(100)
    theme VARCHAR(100)
    duration INT,
    km INT,
    calories INT,
    steps INT
 )

CREATE TABLE IF NOT EXISTS points (
  story_id INT,
  point_id INT,
  check_completed BOOLEAN,
  latitude INT,
  longitude INT,
  name VARCHAR(100),
  text VARCHAR(255)
)

CREATE TABLE IF NOT EXISTS questions(
  story_id INT,
  point_id INT,
  question VARCHAR(100),
  first_answer VARCHAR(100),
  second_answer VARCHAR(100),
  third_answer VARCHAR(100),
  correct_answer_index BOOLEAN
)


INSERT INTO users (name, email) VALUES
('John Doe', 'john@example.com'),
('Fabio', 'fabio@example.com');

INSERT INTO story (title, intro, theme, duration, km, calories, steps) VALUES
('The Eternal Walk', 'Discover the timeless wonders of ancient Rome.', 'History', 0230, 5, 300, 6500);

INSERT INTO points (story_id, point_id, check_completed, latitude, longitude, name, text) VALUES
(1, 1, FALSE, 41890234, 12488623, 'Colosseum', 'Welcome to the Colosseum, the heart of Roman gladiatorial battles.'),
(1, 2, FALSE, 41889500, 12488400, 'Roman Forum', 'Explore the Roman Forum, the hub of ancient Roman public life.'),
(1, 3, FALSE, 41891000, 12487900, 'Palatine Hill', 'Climb the Palatine Hill, the birthplace of Rome and home to emperors.');

INSERT INTO questions (story_id, point_id, question, first_answer, second_answer, third_answer, correct_answer_index) VALUES
(1, 1, 'What was the main use of the Colosseum?', 'Religious rituals', 'Gladiator fights', 'Senate meetings', 1),
(1, 1, 'How many people could the Colosseum hold?', '10,000', '25,000', '50,000', 2);



EOF

echo "

MySQL setup completed successfully!

"

docker exec -it mysql-container mysql -uroot -p