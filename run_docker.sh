# Download the models
cd models
if [ ! -d "clip-vit-large-patch14" ] ; then
    git clone https://huggingface.co/openai/clip-vit-large-patch14
    git lfs install
    git lfs pull
fi
cd ..

# Build docker (does not build by default)
if [ $BUILD = 1 ]; then
    echo "---BUILDING IMAGE---"
    docker compose build
fi

# Run docker
DOCKER_COMMAND="docker compose"
if [ $DEMO = 1 ]; then
    echo "---SETTING DEMO MODE---"
    export MODE="demo"
    DOCKER_COMMAND="${DOCKER_COMMAND} --profile demo"
else
    export MODE="local"
fi

if [ $INDEX = 1 ]; then
    echo "---STARTING INDEXER---"
    DOCKER_COMMAND="${DOCKER_COMMAND} --profile index"
fi

DOCKER_COMMAND="${DOCKER_COMMAND} up -d --remove-orphans"
echo $DOCKER_COMMAND
$DOCKER_COMMAND
