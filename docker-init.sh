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

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

INSERT INTO users (name, email) VALUES
('John Doe', 'john@example.com'),
('Fabio', 'fabio@example.com');

EOF

echo "

MySQL setup completed successfully!

"

docker exec -it mysql-container mysql -uroot -p