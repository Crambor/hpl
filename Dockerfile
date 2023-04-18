

# HPCG FILE

# FROM mpioperator/intel-builder as builder
FROM mpioperator/openmpi-builder as builder

# set contextual labels
LABEL org.opencontainers.image.source="https://github.com/crambor/hpl"
LABEL org.opencontainers.image.description="Container Image for High Performance LINPACK"
# 
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
# RUN cp Make.MPI_GCC_OMP Make.mpi_gcc_omp
# RUN cp Make.MPI_ICPC_OMP Make.mpi_icpc_omp
# COPY "Make.mpi_icpc_omp_rons" .


WORKDIR "../"
RUN mkdir build
WORKDIR "build"
RUN ../configure linuxmpi && make
WORKDIR "../../../"

RUN wget https://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz && \
    tar -xzf hpl-2.3.tar.gz && \
    mv hpl-2.3 hpl


# compile HPL
WORKDIR "hpl"
# RUN ./configure && make -j$(nproc)

COPY "Make.Linux_Intel64" .

RUN ./configure && make arch=intel64 -j$(nproc)








# FROM mpioperator/intel
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
COPY --from=builder /hpl /home/mpiuser/hpl
WORKDIR "/home/mpiuser/hpcg-3.0/build/bin"
COPY hpcg.dat .

WORKDIR "/home/mpiuser/hpl/testing"
COPY HPL.dat .

WORKDIR "/home/mpiuser"

CMD ["/bin/bash"]



# mpirun --allow-run-as-root -np 1 hpcg-3.0/build/bin/xhpcg 
# cd hpl/testing && mpirun -np 1  ./xhpl 

# cd hpl/testing/ && mpirun --bind-to core --allow-run-as-root -np 1 ./xhpl