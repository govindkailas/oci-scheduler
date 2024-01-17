FROM fnproject/python:3.9 as build-stage
WORKDIR /oci-src
ADD requirements.txt stop_start.py /oci-src/
RUN  pip3 install  --no-cache --no-cache-dir -r requirements.txt &&\
     rm -fr ~/.cache/pip /tmp* requirements.txt
ENV PYTHONPATH=/oci-src
ENTRYPOINT ["/usr/bin/python3", "stop_start.py"]
