# pylint: disable=trailing-whitespace
from pprint import pprint
import pandas as pd


RESULT_DELIMETER = "T/V                N    NB     P     Q               Time                 Gflops"
RESULTS_FILE_NAME = "/Users/rohanjain/Desktop/3rd_Year/Individual Project/Crambor/hpl/Parsers/HPL/samplefile.out"

def get_parameter_grid(data): 
    
    start = None
    for i, value in enumerate(data):  
        if "The following parameter values will be used:" in value: 
            start = i 
    
    parameter_grid = { }

    for i, line in enumerate(data[start::]): 
        line = line.strip()
        if "----------------" in line: 
            break 
        else: 
            if line != "": 
                # value.split(":")
                value = line.split(":")

                key = value[0].strip()
                value = value[1].strip()
                parameter_grid[key] = value
            
    return parameter_grid
            


def parse_data(data): 
    results = []
    for i, line in enumerate(data): 
        if RESULT_DELIMETER in line: 
            value = data[i+2]
            value = value.split()
            results.append(
                {"N": value[1], 
                "NB": value[2], 
                "P": value[3],
                "Q": value[4],
                "Time": value[5], 
                "Gflops": value[6],})
            
    return results


def main(): 
    data = None
    with open(RESULTS_FILE_NAME, "r") as file: 
        data = file.readlines()

    parameter_grid = get_parameter_grid(data)        
    data = parse_data(data)
    # pprint(parameter_grid)
    # pprint(data)
    pprint(pd.DataFrame(data))







if __name__ == "__main__":
    main()
