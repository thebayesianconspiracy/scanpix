'''Script to dynamically generate docker-compose.yml'''
def generate_volume_lines():
    lines = []
    with open(".directories", "r") as f:
        lines = f.readlines()
    return lines

def generate_volume_string(container_root_dir):
    import re
    volume_lines = generate_volume_lines()
    volume_lines = ['./.directories','./data/index.json'] + volume_lines
    volume_string = "volumes:\n"
    for line in volume_lines:
        line = line.strip("\n")
        dir_name = re.search(".*/(.*)",line).group(1)
        volume_string +=  "      - " + "\"" + line + f":/{container_root_dir}/{dir_name}"+ "\"" + "\n"
    return volume_string

if __name__ == "__main__":
    volumes_scanpix = generate_volume_string("scanpix")
    volumes_indexer = generate_volume_string("worker-app")
    docker_compose_string = f"""
services:
  scanpix:
    build:
      context: .
      dockerfile: Dockerfile
    image: scanpix-server
    ports:
      - "5001:5001"
    {volumes_scanpix}
  indexer:
    build:
      context: .
      dockerfile: worker/Dockerfile
    image: indexer-service
    ports:
      - "5000:5000"
    {volumes_indexer}
"""
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose_string)
