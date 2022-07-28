# Download the models
cd models
if [ ! -d "clip-vit-large-patch14" ] ; then
    git clone https://huggingface.co/openai/clip-vit-large-patch14
    git lfs install
    git lfs pull
fi
cd ..

# Build docker (does not build by default)
if [ $1 = "build" ]; then
    docker compose build
fi

# Run docker
DOCKER_COMMAND="docker compose"
if [ $2 = "demo" ]; then
    export MODE="demo"
    DOCKER_COMMAND="${DOCKER_COMMAND} --profile demo"
else
    export MODE="local"
fi

DOCKER_COMMAND="${DOCKER_COMMAND} up"
echo $DOCKER_COMMAND
$DOCKER_COMMAND
