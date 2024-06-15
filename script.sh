cd /home/ak/lstm_reliance_stock

conda init

conda activate guppi

python3 fetch_data.py

python3 model.py

docker-compose down

docker images --filter "dangling=true" -q | xargs -r docker rmi

docker system prune -f

docker-compose up --build -d