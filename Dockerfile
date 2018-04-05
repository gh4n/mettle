FROM alpine:3.1
RUN apk add --update python py-pip
RUN pip install -r requirements.txt
ADD ./mettle/mettle.py /
CMD ["python", "./mettle/mettle.py"]
