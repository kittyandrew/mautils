FROM ubuntu:latest as builder
# Install dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    # build dependencies
    python3.8 python3.8-dev python3-pip wget git build-essential cmake swig \
 \
 # Install PDFTron package (Optimization Pipeline)
 && mkdir pdftron \
 && cd pdftron \
 && git clone https://github.com/PDFTron/PDFNetWrappers \
 && cd /pdftron/PDFNetWrappers/PDFNetC \
 # Download and unpack PDFNetC
 #    see: https://www.pdftron.com/documentation/python/get-started/python3/linux
 && wget http://www.pdftron.com/downloads/PDFNetC64.tar.gz \
 && tar xvzf PDFNetC64.tar.gz \
 && mv PDFNetC64/Headers/ . \
 && mv PDFNetC64/Lib/ . \
 && rm PDFNetC64.tar.gz \
 # Compile PDFTron
 && cd /pdftron/PDFNetWrappers \
 && mkdir Build \
 && cd Build \
 && cmake -D BUILD_PDFNetPython=ON .. \
 && make \
 && make install \
 && cd .. \
 && rm -rf Build


# Main stuff
FROM python:3.8-slim-buster as main
# Install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade pip wheel setuptools \
 && pip3 install --no-cache-dir -r requirements.txt

COPY --from=builder /pdftron/PDFNetWrappers/PDFNetC/Lib /pdftron
# Server source files
COPY server server
# Launch
CMD ["python3.8", "-m", "server"]
