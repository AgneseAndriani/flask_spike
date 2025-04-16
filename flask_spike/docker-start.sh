echo 'Starting...'
docker start mysql-container

sleep 10

docker exec -it mysql-container mysql -uroot -p
