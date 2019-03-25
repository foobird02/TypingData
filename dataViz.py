#!/usr/bin/python

import os
import logging
import csv
import numpy as np

ROOT_DIR = "C:\\Users\\gross\\Documents"

class LoadFromCSV(object):
    
    def __init__(self):
        self._fileName = 'race_data.csv'
        self._logger = createLoggerFile()

    def findFile(self):
        """
        Search the user's documents folder to find a specific file for processing.
        
        Returns
        -------
        str
            Path for the desired data file.
        
        Raises
        ------
        PermissionError
            Raises `PermissionError` if folder in Windows system is unaccessable. 

        FileNotFoundError
            Raises `FileNotFoundError` if no files contained in Windows directory.

        """
        for root, dirs, _ in os.walk(ROOT_DIR):
            for directory in dirs:
                path = os.path.join(ROOT_DIR, directory)
                try:
                    files = [f for f in os.listdir(path)]
                    if self._fileName in files:
                        return os.path.join(path, self._fileName)

                except PermissionError as e:
                    self._logger.exception('Directory %r does not allow access.' % (path))

                except FileNotFoundError as e:
                    self._logger.exception('Directory %r does not have file access.' % (path)) 
        
    def readFile(self):
        """
        Read in the .csv file and process the data into sorted objects. 

        Notes
        -----
        Use np.genfromtxt to import taht data  without having to know what the data types
        for each of the columns is. Last column is a timestamp, which doesn't jive with the 
        other columns that are integer or float vlaues.
        """
        workingFile = self.findFile()
        with open(workingFile, newline='') as f:
            reader = csv.reader(f)
            header = set(next(reader))
            print(header)       
        data = np.genfromtxt(workingFile, delimiter=',', dtype=None,skip_header=True, names=None, 
                             encoding=None)

        print(data)


def runDataViz():
    """
    Main program runner.
    """
    input = LoadFromCSV()
    input.readFile()

def createLoggerFile():
    """
    Function that creates an exception logging file in the working directory.

    Returns
    -------
    obj
        Returns log file. 
    """
    cwd = os.getcwd()
    logging.basicConfig(filename='stderr.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    return logging.getLogger(__name__)



if __name__ == "__main__":
    runDataViz()
