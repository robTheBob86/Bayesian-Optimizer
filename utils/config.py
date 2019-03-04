'''

This class stores all the current configurations including additional informations on them as 
well as convenience methods to save them and read them again, e.g. in a ini file in the source folder

'''
import os, sys, time
import configparser
from helpers import parse_result, get_expdir

import numpy as np


class ESP_configs:

	def __init__(self):
		# here are the default configuration parameters: 
		self.params = {

			# path settings
			'path_to_run' : {'value' : '/home/robert/espnet/egs/tedlium/asr1/', 'type' : str},

		    # general configurations
		    'backend' : {'value' : 'pytorch', 'type' : str},
		    'stage' : {'value' : -1, 'type' : int},
		    'ngpu' : {'value' : 1, 'type' : int},
		    'debugmode' : {'value' : 1, 'type' : int},
		    'dumpdir' : {'value' : 'dump', 'type' : str},
		    'N' : {'value' : 0, 'type' : int},
		    'verbose' : {'value' : 1, 'type' : int},
		    'resume' : {'value' : None, 'type' : int},

		    # feature configuration
		    'do_delta' : {'value' : 'false', 'type' : str},

			# encoder
			'etype'   : {'value' : 'vggblstmp', 'type' : str, },
			'elayers' : {'value' : 6, 'type' : int, 'lower_bound' : 1,  'upper_bound' : 10},
			'eunits'  : {'value' : 320, 'type' : int, 'lower_bound' : 250, 'upper_bound' : 400},
			'eprojs'  : {'value' : 320, 'type' : int, 'lower_bound' : 250, 'upper_bound' : 400},
			'subsample' : {'value' : '1_2_2_1_1', 'type' : str},

			# decoder
			'dlayers' : {'value' : 1, 'type' : int, 'lower_bound' : 1, 'upper_bound' : 5},
			'dunits'  : {'value' : 300, 'type' : int, 'lower_bound' : 200, 'upper_bound' : 400},

			# attention related
			'atype' : {'value' : 'location', 'type' : str},
			'adim' : {'value' : 320, 'type' : int, 'lower_bound' : 250, 'upper_bound' : 400},
			'aconv_chans' : {'value' : 10, 'type' : int, 'lower_bound' : 1, 'upper_bound' : 20},
			'aconv_filts' : {'value' : 100, 'type' : int, 'lower_bound' : 30, 'upper_bound' : 150},

			# hybrid attention
			'mtlalpha' : {'value' : 0.5, 'type' : float, 'lower_bound' : 0.0, 'upper_bound' : 0.99},

			# minibatch related
			'batchsize' : {'value' : 30, 'type' : int, 'lower_bound' : 10, 'upper_bound' : 50},
			'maxlen_in' : {'value' : 800, 'type' : int, 'lower_bound' : 600, 'upper_bound' : 1000},
			'maxlen_out' : {'value' : 150, 'type' : int, 'lower_bound' : 100, 'upper_bound' : 250},

			# optimization related
			'opt' : {'value' : 'adadelta', 'type' : str},
			'epochs' : {'value' : 15, 'type' : int, 'lower_bound' : 5, 'upper_bound' : 20},

			# rnnlm related
			'lm_layers' : {'value' : 2, 'type' : int, 'lower_bound' : 1, 'upper_bound' : 6},
			'lm_units'  : {'value' : 650, 'type' : int, 'lower_bound' : 450, 'upper_bound' : 800},
			'lm_opt'    : {'value' : 'sgd', 'type' : str},
			'lm_batchsize' : {'value' : 1024, 'type' : int, 'lower_bound' : 800, 'upper_bound' : 1200},
			'lm_epochs'    : {'value' : 20, 'type' : int, 'lower_bound' : 10,  'upper_bound' : 30},
			'lm_maxlen'    : {'value' : 150, 'type' : int, 'lower_bound' : 50, 'upper_bound' : 250},
			'lm_resume'    : {'value' : None, 'type' : str}, #TODO: type finden
			'lmtag'        : {'value' : None, 'type' : str}, # TODO: type finden

			# decoding parameter
			'lm_weight' : {'value' : 1.0, 'type' : float, 'lower_bound' : 0.0, 'upper_bound' : 1.0},
			'beam_size' : {'value' : 20, 'type' : int, 'lower_bound' : 5, 'upper_bound' : 30},
			'penalty'   : {'value' : 0.0, 'type' : float, 'lower_bound' : 0.0, 'upper_bound' : 1.0},
			'maxlenratio' : {'value' : 0.0, 'type' : float, 'lower_bound' : 0.0, 'upper_bound' : 0.0},
			'minlenratio' : {'value' : 0.0, 'type' : float, 'lower_bound' : 0.0, 'upper_bound' : 0.0},
			'ctc_weight'  : {'value' : 0.3, 'type' : float, 'lower_bound' : 0.0, 'upper_bound' : 1.0},
			'recog_model' : {'value' : 'model.acc.best', 'type' : str}, # ['model.acc.best', 'model.loss.best'],

			# scheduled sampling option
			'samp_prob' : {'value' : 0.0, 'type' : float, 'lower_bound' : 0.0, 'upper_bound' : 0.0},

			# exp tag
			'tag' : {'value' : '""', 'type' : str}, # TODO: stimmt der typ?

		}


	def read_ini(self, filename = '../src/initialize.ini'):
		"""Parse the .ini file to load the written parameters into the program."""
		config = configparser.ConfigParser()
		config.optionxform=str # preserves uppercase for keys

		if os.path.isfile(filename):
			config.read(filename)
		else: 
			print("\nNo .ini in folder.\nProceed with default tedlium-configurations.\n")
			return

		for entry in config['NUMERICAL_VALUES']:
			try:
				self.params[entry]['value'] = self.params[entry]['type'](config['NUMERICAL_VALUES'][entry])
			except: 
				if config['NUMERICAL_VALUES'][entry] == 'None':
					self.params[entry]['value'] = None
				else: 
					print("Unexpected error: ", sys.exc_info()[0])

		for entry in config['LITERAL_VALUES']:
			if not config['LITERAL_VALUES'][entry] == 'None':
				self.params[entry]['value'] = self.params[entry]['type'](config['LITERAL_VALUES'][entry])
			else:
				self.params[entry]['value'] = None


	def write_ini(self, filename = '../src/initialize.ini'): 
		"""This function will write the .ini file. Parameters will be sorted by numerical and 
		non-numerical."""

		config = configparser.ConfigParser()
		config.optionxform=str # preserves uppercase for keys

		lit_dic = {}
		num_dic = {}
		for entry in self.params:
			if self.params[entry]['type'] in [int, float]:
				num_dic[entry] = str(self.params[entry]['value'])
			else:
				lit_dic[entry] = str(self.params[entry]['value'])

		config['NUMERICAL_VALUES'] = num_dic
		config['LITERAL_VALUES'] = lit_dic

		with open(filename, 'w') as configfile:
			config.write(configfile)


	def write_log(self, timestamp):
		"""Write the current parameters into a log file, in a .ini style. Name will be a timestamp, 
		and the /log folder will be sorted by the underlying benchmark, e.g. tedlium or an4."""

		path_to_run = self.params['path_to_run']['value']
		if not path_to_run.endswith('/'):
			path_to_run = path_to_run + '/'
		
		if not os.path.isfile(path_to_run + 'run.sh'):
			print("path_to_run variable has been set wrongly. No run.sh found in: ", path_to_run)
			sys.exit()

		path_to_run = path_to_run.split('/')
		# following [-3] because path always like egs/"benchmark"/asr1/, hence always 3rd from end
		benchmark = path_to_run[-3] # e.g. tedlium or an4
		if not os.path.isdir('../log/' + benchmark):
			os.mkdir('../log/' + benchmark)
		if not os.path.isdir('../log/' + benchmark + '/' + timestamp):
			os.mkdir('../log/' + benchmark + '/' + timestamp)
		self.write_ini('../log/' + benchmark + '/' + timestamp + '/parameters.log')


	def read_logs(self, parameters, measure_name = 'Err'):
		"""Read in all the logs that correspond to the benchmark that is being extracted from
		the path_to_run and return them as a matrix. measure_name is the name of the measure
		that we address, see also extract_results(...)."""

		path_to_run = self.params['path_to_run']['value']
		if not path_to_run.endswith('/'):
			path_to_run = path_to_run + '/'
		
		if not os.path.isfile(path_to_run + 'run.sh'):
			print("path_to_run variable has been set wrongly. No run.sh found in: ", path_to_run)
			sys.exit()

		path_to_run = path_to_run.split('/')
		# following [-3] because path always like egs/"benchmark"/asr1/, hence always 3rd from end
		benchmark_path = '../log/' + path_to_run[-3]
		if not os.path.isdir(benchmark_path):
			print("The folder " + benchmark_path + " could not be found. Do .log files of this benchmark exist?")
			sys.exit()

		d = [os.path.join(benchmark_path, o) for o in os.listdir(benchmark_path) if os.path.isdir(os.path.join(benchmark_path,o))]
		expdir = get_expdir(self)
		X = None
		Y = None
		for dir in d:
			if not dir.endswith('/'):
				dir = dir + '/'

			# construct Y
			if not os.path.isfile(dir + 'result.txt'):
				continue
			new_y = self.parse_result(dir, measure_name)
			print("dir: ", dir)
			print("new_y: ", new_y)
			if new_y is None: 
				# this case will happen if something went wrong in the espnet training. there will be a result.txt file in the folder, however, it is empty and hence cannot be used but leads to an error later in conditioning out gaussian function. we omit this case
				continue

			if Y is None:
				Y = np.array([new_y])
			else:
				Y = np.vstack((Y, new_y))
			
			# construct X
			self.read_ini(dir + 'parameters.log') # overwrites self.params
			row = np.array(self.retrieve_params(parameters))
			if X is None:
				X = row
			elif row.tolist() in X.tolist(): # to make sure we use each point only once, avoids potential conflicts in setting up the function due to noise
				Y = np.delete(Y, -1, 0) # delete the last row of Y
				continue
			else:
				X = np.vstack((X, row))

		return X, Y


	def store_params(self, parameters, values):
		"""parameters will be a list with all the parameters to overwrite, values is a list of the 
		corresponding values"""
		for i, param in enumerate(parameters):
			self.default_config_params[param] = values[i]


	def retrieve_params(self, parameters):
		"""Params is a list of the names of the parameters, and this function returns the corresponding
		values as a list again."""
		values = []
		for param in parameters: 
			values.append(self.params[param]['value'])

		return values

	def retrieve_boundaries(self, parameters):
		"""Get the bounds to the handed over list of parameters, in order to compute better"""

		lower_bounds = []
		upper_bounds = []
		
		for param in parameters:
			lower_bounds.append(self.params[param]['lower_bound'])
			upper_bounds.append(self.params[param]['upper_bound'])

		return lower_bounds, upper_bounds		

	def parse_result(self, path_to_result, metric = 'Err'):
		"""Get the result in the specified folder"""

		with open(path_to_result + 'result.txt') as f:
			index = None
			value = None
			for line in f:
				if metric in line:
					line = line.split()
					while '#' in line:
						line.remove('#') # see the header line in one of those
					index = line.index(metric)
				elif 'Mean' in line and index:
					value = float(line.split()[index])

				if not value==None and value<=100.0:
					return value  
