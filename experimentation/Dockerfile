



FROM mpioperator/openmpi-builder as builder


RUN apt update
RUN apt install wget neovim -y
RUN apt install build-essential gcc -y
RUN apt install libopenblas-dev libopenmpi-dev -y 
RUN apt install openssh-server -y

# download HPL
RUN wget https://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz
RUN tar -xpf hpl-2.3.tar.gz
RUN mv hpl-2.3 hpl

# compile HPL
WORKDIR "/hpl"
RUN ./configure
RUN make -j
WORKDIR "/hpl/testing"


COPY HPL.dat .


CMD ["/bin/bash"]

