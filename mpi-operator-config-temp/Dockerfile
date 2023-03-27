
FROM mpioperator/openmpi-builder as builder


# set contextual labels
RUN apt update
RUN apt install wget -y
RUN apt install build-essential gcc -y
RUN apt install libopenblas-dev libopenmpi-dev -y 
RUN apt install openssh-server -y

# download HPL
RUN wget https://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz
RUN tar -xpf hpl-2.3.tar.gz
RUN mv hpl-2.3 hpl

# compile HPL
WORKDIR "hpl"
RUN ./configure
RUN make -j4
# CMD ["/bin/bash"]

FROM mpioperator/openmpi

RUN apt update
RUN apt install wget -y
RUN apt install build-essential gcc -y
RUN apt install libopenblas-dev libopenmpi-dev -y 


COPY --from=builder /hpl /home/mpiuser/hpl
WORKDIR "/home/mpiuser/hpl/testing"

COPY HPL.dat .

CMD ["/bin/bash"]
