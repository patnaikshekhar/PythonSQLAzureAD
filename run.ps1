echo "Building image"
docker build -t patnaikshekhar/python-ad-test:1 .

echo "Deleting running container if any"
docker rm -vf adtest

echo "Running container"
docker run --rm -it --name=adtest -v ${pwd}/config:/app/config patnaikshekhar/python-ad-test:1 