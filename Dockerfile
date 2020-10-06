FROM ubuntu:latest

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
 && rm -rf Build \
 \
 # Clean up
 && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    wget \
    git \
    build-essential \
    cmake \
    swig \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get clean

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip wheel setuptools \
 && pip3 install -r requirements.txt

# Server source files
COPY server server
# Launch
CMD ["python3.8", "-m", "server"]
