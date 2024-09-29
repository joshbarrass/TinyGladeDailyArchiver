FROM python:3.8

RUN mkdir /code
RUN addgroup --gid 10001 --system nonroot && adduser -u 10000 --system --gid 10001 --home /home/nonroot nonroot
RUN chown -R nonroot:nonroot /home/nonroot \
 && chown -R nonroot:nonroot /code
USER nonroot
WORKDIR /code

COPY requirements.txt /code/
COPY archiver.py /code/
COPY tgdaily/ /code/tgdaily

RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/local/bin/python3", "/code/archiver.py"]
CMD ["-h"]
