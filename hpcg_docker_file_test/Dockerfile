

# HPCG FILE
FROM mpioperator/openmpi-builder as builder
# FROM mpioperator/openmpi

# set contextual labels
# LABEL org.opencontainers.image.source="https://github.com/crambor/hpl"
# LABEL org.opencontainers.image.description="Container Image for High Performance LINPACK"

# include dependencies
RUN apt update && apt install -y \
    wget \
    build-essential \
    gcc \
    libopenblas-dev \
    libopenmpi-dev 

# download HPL
RUN wget http://www.hpcg-benchmark.org/downloads/hpcg-3.0.tar.gz && \
    tar -xzf hpcg-3.0.tar.gz 

RUN mkdir hello_world

WORKDIR "hpcg-3.0/setup"
# RUN cp Make.MPI_GCC_OMP Make.mpigccomp
RUN cp Make.Linux_MPI Make.linuxmpi

WORKDIR "../"
RUN mkdir build
WORKDIR "build"
RUN ../configure linuxmpi && make
# WORKDIR "../"


FROM mpioperator/openmpi


# include dependencies
RUN apt update && apt install -y \
    wget \
    build-essential \
    gcc \
    libopenblas-dev \
    libopenmpi-dev  \
    vim


COPY --from=builder /hpcg-3.0 /home/mpiuser/hpcg-3.0
WORKDIR "/home/mpiuser/hpcg-3.0/build/bin"


CMD ["/bin/bash"]
