
# # # ---->>>> Direct copy
# # FROM mpioperator/openmpi-builder as builder
# # # FROM mpioperator/openmpi

# # # set contextual labels
# # # LABEL org.opencontainers.image.source="https://github.com/crambor/hpl"
# # # LABEL org.opencontainers.image.description="Container Image for High Performance LINPACK"

# # # include dependencies
# # RUN apt update && apt install -y \
# #     wget \
# #     build-essential \
# #     gcc \
# #     libopenblas-dev \
# #     libopenmpi-dev 

# # # download HPL
# # RUN wget http://www.hpcg-benchmark.org/downloads/hpcg-3.0.tar.gz && \
# #     tar -xzf hpcg-3.0.tar.gz 

# # RUN mkdir hello_world

# # WORKDIR "hpcg-3.0/setup"
# # # RUN cp Make.MPI_GCC_OMP Make.mpigccomp
# # RUN cp Make.Linux_MPI Make.linuxmpi

# # WORKDIR "../"
# # RUN mkdir build
# # WORKDIR "build"
# # RUN ../configure linuxmpi && make
# # # WORKDIR "../"


# FROM ghcr.io/crambor/hpl:v0.2.1

# WORKDIR "/home/mpiuser/"
# # COPY --from=builder /hpcg-3.0 /home/mpiuser/hpcg-3.0



# CMD ["/bin/bash"]



# # docker buildx build --push --platform linux/amd64,linux/arm64 -t ronnydonny/project-benchmarks-y3:hpl-v2 .



# # docker buildx build --push --platform linux/amd64,linux/arm64 -t ronnydonny/project-benchmarks-y3:hpl-v2 .



#----


FROM mpioperator/openmpi-builder as builder


# set contextual labels
LABEL org.opencontainers.image.source="https://github.com/crambor/hpl"
LABEL org.opencontainers.image.description="Container Image for High Performance LINPACK"

# include dependencies
RUN apt update && apt install -y \
    wget \
    build-essential \
    gcc \
    libopenblas-dev 
    # libopenmpi-dev

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
    libopenblas-dev 
    # libopenmpi-dev/


COPY --from=builder /hpl /home/mpiuser/hpl
WORKDIR "/home/mpiuser/hpl/testing"

COPY HPL.dat .


CMD ["/bin/bash"]
# RUN export OMPI_ALLOW_RUN_AS_ROOT=1 \
#     export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

# ${OMPI_ALLOW_RUN_AS_ROOT}