# pylint: disable=line-too-long
import os 
import subprocess
import yaml
from pprint import pprint

MPI_YAML_FILE_NAME = "Parsers/HPL/mpi_sample.yaml"
HPL_DAT_FILE_NAME = "Parsers/HPL/sample_hpl_dat.dat"


ERROR_FOUND = False


class bc:
    # https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_meta_data(): 
    data = None
    with open(MPI_YAML_FILE_NAME, "r") as file: 
        data = yaml.safe_load(file)
    return data



def check_and_get_hpl_dat(): 

    hpl_config = {}


    data = None 
    with open(HPL_DAT_FILE_NAME, "r") as file: 
        data = file.readlines()

    # --> Number of Ns 
    base_index = None
    for i, value in enumerate(data): 
        value = value.strip()
        if "of problems sizes (N)" in value.strip(): 
            # print(value)
            base_index = i
    
    print(data[base_index+1].split())
    number_of_ns_stated = int(data[base_index].split()[0])
    number_of_ns_actual = len(data[base_index + 1].split()) -1
# 
    # print(number_of_ns_stated)
    # print(number_of_ns_actual)

    if number_of_ns_actual != number_of_ns_stated: 
        print(f"{bc.FAIL}Number of Ns is different to Problem Sizes declared {bc.ENDC}")
        ERROR_FOUND = True


    hpl_config["Problem Sizes N"] = data[base_index + 1].split()[:-1]


    # --> Number of NBs

    base_index = None
    for i, value in enumerate(data): 
        value = value.strip()
        if "# of NBs" in value.strip(): 
            # print(value)
            base_index = i
    
    print(data[base_index+1].split())
    number_of_ns_stated = int(data[base_index].split()[0])
    number_of_ns_actual = len(data[base_index + 1].split()) -1

    # print(number_of_ns_stated)
    # print(number_of_ns_actual)

    if number_of_ns_actual != number_of_ns_stated: 
        print(f"{bc.FAIL}Number of NBs is different to #NB declared {bc.ENDC}")
        ERROR_FOUND = True

    hpl_config["Blocks NB"] = data[base_index + 1].split()[:-1]


    # --> Number of Process Grid configurations

    base_index = None
    for i, value in enumerate(data): 
        value = value.strip()
        if "of process grids (P x Q)" in value.strip(): 
            # print(value)
            base_index = i
    
    print(data[base_index+1].split())
    number_of_ns_stated = int(data[base_index].split()[0])
    
    number_of_ns_actual_p = len(data[base_index + 1].split()) -1
    number_of_ns_actual_q = len(data[base_index + 2].split()) -1


    if number_of_ns_actual_p != number_of_ns_actual_q: 
        print("P and Q lines in HPL do not match length")
    elif number_of_ns_actual_p != number_of_ns_stated: 
        print(f"{bc.FAIL}Number of PQ Process Configurations is different to PQs declared {bc.ENDC}")
        ERROR_FOUND = True
    
    hpl_config["PQ Configs"] = list(zip(data[base_index + 1].split()[:-1], data[base_index + 2].split()[:-1]))

    return hpl_config


def check_slots_per_worker(yaml_meta): 
    slots_per_worker = yaml_meta["spec"]["slotsPerWorker"]
    num_cpus_req = yaml_meta["spec"]["mpiReplicaSpecs"]["Worker"]["template"]["spec"]["containers"][0]["resources"]["requests"]["cpu"]
    if slots_per_worker != num_cpus_req: 
        print("Slots per worker should equal number of cpus requested!!")

# def check_HPL_dat_file()


def check_np_vs_PQ(yaml_meta, hpl_configs): 
    
    np_stated = yaml_meta["spec"]["mpiReplicaSpecs"]["Launcher"]["template"]["spec"]["containers"][0]["args"]
    np_stated = int(np_stated[np_stated.index("-np") + 1])
    print(np_stated)

    for value in hpl_configs["PQ Configs"]: 
        mul = int(value[0])* int(value[1])
        if mul != np_stated: 
            print(f"{bc.FAIL}There is a mismatch with the number of processes and the number of grids you have stated")
            print(f"pq: {value}, np: {np_stated} {bc.ENDC}")






def main(): 
    yaml_meta = get_meta_data()
    check_slots_per_worker(yaml_meta)
    hpl_configs = check_and_get_hpl_dat()
    
    pprint(hpl_configs)
    check_np_vs_PQ(yaml_meta, hpl_configs)
    
    # check slots_per_worker -> number of cpu requested
    # np_ranks = yaml_meta["spec"]["mpiReplicaSpecs"]["Launcher"]["template"]["spec"]["containers"][0]["args"]
    # print(np_ranks[np_ranks.index("-np") + 1])


if __name__ == "__main__": 
    main()