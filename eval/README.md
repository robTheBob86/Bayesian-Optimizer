# Analyzing the test Results

In this folder there is a jupyter-notebook to analyse the test results. A toy example has been provided in the eval/example-folder.
For analyzing your own test, please follow the following steps:

### 1: Run tests

There is a logs.txt in the log/benchmark folder, where benchmark is e.g. tedlium, an4 or other benchmarks provided by ESPnet. 
The script writes all the relevant data from the tests in here. If you want to evaluate a new test streak, delete this file. If not, 
the results from previous will also be evaluated, which might also be desired.

### 2: Create a new folder

On your personal PC, i.e. not the server, create a new folder in the eval-folder. Copy the Analyzer.ipynb script from one of the folders into your newly created folder.

### 3: Get the data

Copy the logs.txt file from the log-folder in your newly created folder. You should NOT rename the file. 
Also, please note again that this evaluates all the runs that have been run with the selected benchmark since the logs.txt has been deleted latest. 

### 4: Run the Analyzer

By sequentially running the Analyzer, you will get informations about the parameters and tests results and their relations, just carefully read the outputs and plots.

# Troubleshooting:

- If you cannot run the test, please make sure you have jupyter-notebook installed and the files name is logs.txt, as well as that the file and the notebook are in the same directory. 
- If you have it installed and still cannot run it, update jupyter-notebook onto at least version 5.6.0
- If you do find syntax-errors, you might use a non-compatible version of Python. In this case, try using Python 3.6 or 3.7. This is to be set in the jupyter-notebook settings. 
- If it is still not working, maybe someone has overwritten the script you are using. In this case, redownload the script from the git-server
