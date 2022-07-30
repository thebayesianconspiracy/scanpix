# Download the models
cd models
if [ ! -d "clip-vit-large-patch14" ] ; then
    git clone https://huggingface.co/openai/clip-vit-large-patch14
    git lfs install
    git lfs pull
fi
cd ..

# Build docker (does not build by default)
if [ $BUILD -eq 1 ]; then
    echo "---BUILDING IMAGE---"
    docker compose build
fi

# Run docker
DOCKER_COMMAND="docker compose"
if [ $DEMO -eq 1 ]; then
    echo "---SETTING DEMO MODE---"
    export MODE="demo"
    DOCKER_COMMAND="${DOCKER_COMMAND} --profile demo"
else
    export MODE="local"
fi

if [ $INDEX -eq 1 ]; then
    echo "---STARTING INDEXER---"
    DOCKER_COMMAND="${DOCKER_COMMAND} --profile index"
fi


if [ $1 = "start" ]; then
    DOCKER_COMMAND="${DOCKER_COMMAND} up -d --remove-orphans"
elif 
    [ $1 = "stop" ]; then
    DOCKER_COMMAND="${DOCKER_COMMAND} down"
else
    echo "No option (start, stop) provided!"
    exit 1
fi

echo $DOCKER_COMMAND
$DOCKER_COMMAND
