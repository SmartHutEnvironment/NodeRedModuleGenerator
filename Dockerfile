FROM python:3
ADD src /src
ADD data /data
RUN pip3 install pyyaml
WORKDIR /data
CMD [ "python", "/src/generateModule.py", "/data", "/data/lib" ]
