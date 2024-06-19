cd /home/ak/lstm_reliance_stock

conda init

conda activate guppi

python3 fetch_data.py

python3 model.py

docker-compose down

CONTAINER_ID=$(docker ps -q --filter "publish=8501")
if [ ! -z "$CONTAINER_ID" ]; then
  docker stop $CONTAINER_ID
  docker rm $CONTAINER_ID
fi

docker images --filter "dangling=true" -q | xargs -r docker rmi

docker system prune -f

docker build -t lstm_reliance_stock .

docker run -p 8501:8501 lstm_reliance_stock
