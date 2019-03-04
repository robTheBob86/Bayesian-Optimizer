# 1. Introduction

# 1.1. Preface

This project implements a Gaussian hyperparameter tuning. It is suited for the ESPnet network or similar structures, 
and is meant to automatically tune hyperparameters. 

Background knowledge on Gaussian hyperparameter tuning and the ESPnet can be obtained from the references and the appendix
in the end of this file. This readme mainly aims at introducing on how this work is strucured, how to use it and how 
to properly troubleshoot/modify the file in case it should be adapted to new sets.

A more detailed explanation of the code is given in the doc/ directory, where another README.md exists.

# 1.2. Content

1. Introduction 
	- 1.1. Preface
	- 1.2. Content
	- 1.3. The Directory Structure

2. How to use the Interface
	- 2.1. The First Run
	- 2.2. Starting from the script run_terminal.py
	- 2.3. Starting from the run.sh

3. How to Modify Properly
	- 3.1. Adding or Deleting Options 
	- 3.2. Hanging in New Benchmark

4. Troubleshooting

5. Desicions Made

6. Sources
	- 6.1. Related Papers
	- 6.2. Useful Links


# 1.3. The Directory Strucure 

The directories are the following:

- /src
This is the main code, where the terminal and the optimizing code sit in.

- /utils
Auxiliary functions such as parsers are stored in here. Furthermore, the current program status is stored in here.

- /log
This is where the logging takes place, i.e. each test run setting and the parameters are stored in here. 

- /eval
Here is an auxiliary python-notebook to evaluate the results. Of course it can be modified by the user.  

- /doc
Here is a documentation of the code as well as a few refences and reads.

Furthermore, there might be a folder with the virtual environment. 


# 2. How to use the Interface

### 2.1. The First Run

When running the program, at first it loads all the standard settings provided by the Tedlium data set. Additional settings
are also provided during this step, such as how many GPUs will be used and path settings. The settings are both in the 

src/initialize.ini
utils/config.py.

, where the **settings in the config.py are only loaded if the initialize.ini does not exist.**
Before you run the program please make sure at least the following parameters:

- path_to_run
- backend
- n_gpu

, where the path_to_run will be the path starting in the root folder and into one of the folders of ESPnet that contains 
a run.sh file, e.g. /home/robert/espnet/an4/asr1/.

Additionally, in the 

utils/config.py

there are bounds given for the trainable parameters. **Please adjust the bounds to your needs** if necessary.

When running the first also, the script stops after training, because the Gaussian Process Regressor from sklearn needs at least two
samples to run. **Let the test stop and give it the next point by writing the desired parameters into the initialize.ini.** After this,
the script should be able to run through without any problem. 


### 2.2. Starting from the script run_terminal.py

The interface has two runnable modes, an interactive mode and a normal mode. The interactive mode starts with the parameter

--interactive

, when thereafter the parameters can be handed over to the tool. The interactive mode provides a "manual".
In normal mode, the parameters are just handed over. It is **recommended to use the run.sh** script, since this gives an overview 
of all possible parameters. All parameters can be shown by the --help option, emphasis shall be put on 

--n_interations # the number of iterations 
--network # the network type, e.g. tedlium, an4 or freudnet

For adding or removing options see section 3.1.

### 2.3. Starting from the run.sh

The run.sh is the main starting script. The parameters are all taken from the tedlium benchmark of ESPnet. In order to run the 
test simply run this file. 

Please note: 
It first executes a virtual environment. In case you deleted that or did change it you have to change that line.


# 3. How to Modify Properly

## 3.1 Adding or Deleting Options 

All possible main options are in the utils/configs.py script, where they come in the form of a dictionary. The main key
of that dictionary is the parameter, followed by an initial value (that is used if no src/initialize.ini exists), its type and possible 
bounds. Since the **Gaussian Process Regressor can only work with numerical values**, only those are made trainable.

A list of non-trainable numerical values exists in the first few lines of the run_terminal.py script, when the parameters are loaded.

Hence, adding or deleting parameters goes by simply adding or deleting entries in the dictionary. **Please make sure that the parameter
name must match the key of the dictionary.** **Trainable parameters must furthermore have upper and lower bounds**, please follow the 
structure given by the other entries.

## 3.2 Hanging in New Benchmark

When inserting a new benchmark, a few adjustments have to be made.
First of all, please make sure that the results can properly be parsed. The current parser, which parses the result.txt of the 
ESPnet results, is the function **parse_result in utils/configs.py**.

Also, the folder where the results are in have to be found. Here, again the structure of ESPnet is assumed:
The path where the run.sh is in should have a folder called 'exp/', in the the result folders are saved. Then, the folder with the 
result is being found in that with the function **get_path_to_result in utils/helpers.py**. Currently, this function assumes a 'test' 
in the folder, because ESPnet throws out two folders, distinct in the beginning: one says test, the says train. Obviously, we want 
the test-folder in the ESPnet setting. 

# 4. Troubleshooting

## When the result.txt cannot be found in the log-folder

This happens when the espnet could not execute succesfully. In this please try to check the input to espnet. 
Examples would be to set the upper and lower bounds correctly, as a non-defined may have been handed over. Do not forget to 
rewrite the current value in the initialize.ini, if it is wrong at this moment. 

## Test is being Aborted After Training

This can have three possible (here discussed) roots:

- You started the first test with a new benchmark. In that case the test will stop after one training, and an src/initialize.ini file 
will be written. Open this file, and give the tool a new point by at least altering one of the trainable parameters. Then, the tests 
should be able to run through thereafter

- One of the parameters is in a forbidden domain. E.g. the number of layers of a neural network can not be negative, or a 
learning rate cannot be larger than 1. Please adjust the boundaries accordingly in the utils/configs.py and put the 
out-of-range parameter in the src/initialize.ini in a good domain again.

- Something went wrong with the neural network or benchmark to train, and the file with the results could not be found. Please make sure 
a correct execution of those trainings. 

# 5. Choices Made on Optimization

## Kernel

The kernel utilized by the tool is choosable, but here a **Matern kernel** is used. This Kernel has been proposed by Snoek et al.,
[1] and proven to be working with several setups including convolutional neural networks. Please note that the parameters of the
kernel do not have to be tuned, as the GaussianProcessRegressor-object does this by itself with the optional argument n_restarts_optimizer.

## Acquisition Function

There are multiple acquisition functions possible, however, every serious source that was available the time this project finished
used the expected improvement (EI). A discussion of possible acquisition functions can be found in the links "Discussion of Acquisition 
Functions". 

## Finding the Maximum

In order to maximize the EI the minimize function from the scipy library is being used. We switch the sign in the next_point function and 
then minimize. A for-loop with random sampled points is used, because the minimize-function uses gradient descent methods. That way local 
optima can be circumvented. The starting points are sampled with respect to the upper and lower bounds of the parameters, hence do not 
fall out of allowed domains. The number of sample points can be adjusted with n_minimize_restarts in hp_optimizer, which can be higher, 
because the cost of time for the gradient descent is marginal compared to the network trainings. 


# 6. Sources

## 6.1. Related Papers

- [1] Practical Bayesian Optimization of Machine Learning Algorithms, Snoek et al., arXiv:1206.2944, 2012
- [2] Sequential Model-Based Optimization for General Algorithm Configuration, Hutter et al., LION, DOI: 10.1007/978-3-642.3_40, 2011
- [3] A Tutorial on Bayesian Optimization, Frazier, arXiv:1807.02811, 2018

## 6.2. Useful Links

- TUM Videos: https://www.youtube.com/watch?v=9hKfsuoFdeQ&t=201s
- Blog-Entry with example code: http://krasserm.github.io/2018/03/21/bayesian-optimization/
- Derivation of EI: http://ash-aldujaili.github.io/blog/2018/02/01/ei/
- Discussion of Acquisition Functions: https://www.cse.wustl.edu/~garnett/cse515t/spring_2015/files/lecture_notes/12.pdf

- Possibly intersting: Using Deep Neural Networks as Alternative: https://arxiv.org/abs/1502.05700







