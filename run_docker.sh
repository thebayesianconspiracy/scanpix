# Download the models
cd models
if [ ! -d "clip-vit-large-patch14" ] ; then
    git clone https://huggingface.co/openai/clip-vit-large-patch14
fi
cd ..

# Build docker
docker compose build

# Run docker
DOCKER_COMMAND="docker compose"
if [ $1 = "demo" ]; then
    export MODE="demo"
    DOCKER_COMMAND="${DOCKER_COMMAND} --profile demo"
else
    export MODE="local"
fi

DOCKER_COMMAND="${DOCKER_COMMAND} up"
echo $DOCKER_COMMAND
$DOCKER_COMMAND