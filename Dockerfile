
FROM mpioperator/openmpi-builder as builder


# set contextual labels
LABEL org.opencontainers.image.source="https://github.com/crambor/hpl"
LABEL org.opencontainers.image.description="Container Image for High Performance LINPACK"

# include dependencies
RUN apt update && apt install -y \
    wget \
    build-essential \
    gcc \
    libopenblas-dev \
    libopenmpi-dev

# download HPL
RUN wget https://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz && \
    tar -xzf hpl-2.3.tar.gz && \
    mv hpl-2.3 hpl

# compile HPL
WORKDIR "hpl"

COPY "Make.Linux_Intel64" .

RUN ./configure && make arch=intel64 -j$(nproc)

FROM mpioperator/openmpi

# include dependencies
RUN apt update && apt install -y \
    wget \
    build-essential \
    gcc \
    libopenblas-dev \
    libopenmpi-dev


COPY --from=builder /hpl /home/mpiuser/hpl
WORKDIR "/home/mpiuser/hpl/testing"

COPY HPL.dat .

CMD ["/bin/bash"]
