import sys
import argparse

sys.path.insert(0, '../utils/')
from config import ESP_configs

from hp_optimizer import Hyperparam_Optimizer

configs = ESP_configs() 
configs.read_ini() # load the configurations

n_iterations = 1 # will be actualized later

# At first, we initialize the parser. the parser shall have a flag indicating whether we 
# want to start an interactive session. if this flag exists, all the other options will be 
# omitted and the interactive session will be started
parser = argparse.ArgumentParser(description='Gaussian Hyperparameter Optimization Interface.', 
								 epilog = 'To start an interactive session type --interactive.\
Else, give the parameters that are to be trained on.\
To set the number of iterations, use --n_iterations.\n\
The arguments above are the trainable arguments. Hand\
them over to optimize on them.\n')

parser.add_argument('-i', '--interactive', action = 'store_true', help = 'Start an interactive session')
parser.add_argument('--n_iterations',type = int, default = 1, help = 'The number of iterations that the Gaussian optimization algorithm is supposed to run. Default = 1')
parser.add_argument('--network', type = str, choices = ['an4', 'tedlium', 'freudnet'] , help = 'The network that is supposed to run.')

# Add all the arguments from the configurations to the parser. We could possibly only train on 
# the numerical parameters, hence we will only consider them at this stage.
all_options = [i for i in configs.params if configs.params[i]['type'] in [int, float] and i not in ['maxlenratio', 'minlenratio', 'resume', 'stage', 'ngpu', 'N', 'batchsize', 'debugmode', 'verbose']]


for option in all_options: 
	parser.add_argument('--' + option, action = 'store_true')

args = parser.parse_args()


# We are going to have two options: one is for the normal start, and we can start an 
# interactive session. this branch here will start the interactive session

# -----------------------------------------Interactive Session-----------------------------------------------------

if args.interactive:

	parser = argparse.ArgumentParser(description='Interactive session: Gaussian Hyperparameter Optimization', add_help = False)
	parser.add_argument('-r', '--run', action = 'store_true', help = 'Run the session.')
	parser.add_argument('--n_iterations',type = int, default = 1, help = 'The number of iterations that the Gaussian optimization algorithm is supposed to run. Default = 1')
	parser.add_argument('--selected', action = 'store_true', help = 'List all the so-far selected parameters.')
	#parser.add_argument('--network', type = str, choices = ['an4', 'tedlium', 'freudnet'] , help = 'The network that is supposed to run.')


	print("Started the interactive session. Please type in the arguments one after another.\n\
To display the options type any letter and press enter.\n")

	for option in all_options: 
		parser.add_argument('--' + option, action = 'store_true')

	run_session = False
	args = []

	while not run_session:

		command = input().split()
		while len(command)>1 and not (len(command) == 2 and command[0] == '--n_iterations'):
			print("Please only type one argument at a time or give the number of iterations with --_iterations and an integer")
			command = input().split()
		try:
			arg = parser.parse_args(command) # TODO: check this guy here on possible syntax difficulties
			if command[0] not in ['-r', '--run', '--n_iterations', '--selected']:
				args.append(*[i for i in vars(arg) if getattr(arg, i) == True and i not in ['run', 'n_iterations'] and i not in args])
			elif command[0] == '--n_iterations':
				n_iterations = arg.n_iterations
			elif command[0] == '--selected':
				print("\nThe selected parameters so far are:")
				print("\n".join('{}: {}'.format(*k) for k in enumerate(args)))
			run_session = arg.run
		except SystemExit:
			print("Invalid command in" + str(command) + ". Please choose a command followed by the following list, preceded by a --:")
			print('\n'.join('{}: {}'.format(*k) for k in enumerate(all_options)))
			print('\nAdditionally, you can use\n\n-r or --run\n\nto start the program and\n\n--n_iterations\n\nto set the number of iteration the program will run.\n\n')
		except:
			print("Unexpected error: ", sys.exc_info()[0])



# -----------------------------------------Non-Interactive Session-----------------------------------------------------

else:
	n_iterations = args.n_iterations 
	network = args.network
	args = [i for i in vars(args) if getattr(args, i) == True and i not in ['run', 'n_iterations', 'network']]


# -----------------------------------------Run the optimization-----------------------------------------------------

if len(args) == 0:
	print("\n No arguments given for training. Quitting current run.\n")
	sys.exit()

print("Starting the training with: \n ")
print("{} iterations running the tests.".format(n_iterations))
print('\n'.join('{}: {}'.format(*k) for k in enumerate(args)) + '\n\n')

values = configs.retrieve_params(args)
optimizer = Hyperparam_Optimizer(zip(args, values), configs, n_iterations, network)
