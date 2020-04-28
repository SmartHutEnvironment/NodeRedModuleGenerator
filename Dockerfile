FROM python:3
ADD src /src
ADD data /data
WORKDIR /data
CMD [ "python", "/src/gen.py" ]
