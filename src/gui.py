from tkinter import *
import sys
import subprocess

sys.path.insert(0, '../utils/')
from config import ESP_configs

class Window: 

	def __init__(self, root):

		# ------------------------------------------------------------------------------------------
		# first define the three frames
		self.topframe = Frame(root)
		self.topframe.pack(side = TOP)
		self.middleframe = Frame(root)
		self.middleframe.pack(side = TOP)
		self.bottomframe = Frame(root)
		self.bottomframe.pack(side = BOTTOM)

		# ------------------------------------------------------------------------------------------
		# Variables for the checkboxes. Needed in Tkinter
		# The total number of variables at this stage is 34 and needs to be adjusted upon changing the 
		# parameters list
		self.checkbox_variables = list(map(lambda y : IntVar(), range(34)))

		# ------------------------------------------------------------------------------------------
		# now the top frame. this frame consists of all the parameters/variables that we wanna check 
		# with both a checkbox and a value that we can set. 

		# first, start with the left side
		self.encoder_label = Label(self.topframe, text = "Encoder")
		self.encoder_label.grid(row = 0, column = 0, sticky = W)
		self.etype = Checkbutton(self.topframe, variable = self.checkbox_variables[0], text = "etype")
		self.etype.grid(row = 1, column = 0, sticky = W)
		self.etype_entry = Entry(self.topframe)
		self.etype_entry.grid(row = 1, column = 1, sticky = W)
		self.elayers = Checkbutton(self.topframe, variable = self.checkbox_variables[1], text = "elayers")
		self.elayers.grid(row = 2, column = 0, sticky = W)
		self.elayers_entry = Entry(self.topframe)
		self.elayers_entry.grid(row = 2, column = 1, sticky = W)
		self.eunits = Checkbutton(self.topframe, variable = self.checkbox_variables[2], text = "eunits")
		self.eunits.grid(row = 3, column = 0, sticky = W)
		self.eunits_entry = Entry(self.topframe)
		self.eunits_entry.grid(row = 3, column = 1, sticky = W)
		self.eprojs = Checkbutton(self.topframe, variable = self.checkbox_variables[3], text = "eprojs")
		self.eprojs.grid(row = 4, column = 0, sticky = W)
		self.eprojs_entry = Entry(self.topframe)
		self.eprojs_entry.grid(row = 4, column = 1, sticky = W)
		self.subsample = Checkbutton(self.topframe, variable = self.checkbox_variables[4], text = "subsample")
		self.subsample.grid(row = 5, column = 0, sticky = W)
		self.subsample_entry = Entry(self.topframe)
		self.subsample_entry.grid(row = 5, column = 1, sticky = W)

		self.decoder_label = Label(self.topframe, text = "Decoder")
		self.decoder_label.grid(row = 6, column = 0, sticky = W)
		self.dlayers = Checkbutton(self.topframe, variable = self.checkbox_variables[5], text = "dlayers")
		self.dlayers.grid(row = 7, column = 0, sticky = W)
		self.dlayers_entry = Entry(self.topframe)
		self.dlayers_entry.grid(row = 7, column = 1, sticky = W)
		self.dunits = Checkbutton(self.topframe, variable = self.checkbox_variables[6], text = "dunits")
		self.dunits.grid(row = 8, column = 0, sticky = W)
		self.dunits_entry = Entry(self.topframe)
		self.dunits_entry.grid(row = 8, column = 1, sticky = W)

		self.attention_label = Label(self.topframe, text = "Attention")
		self.attention_label.grid(row = 9, column = 0, sticky = W)
		self.atype = Checkbutton(self.topframe, variable = self.checkbox_variables[7], text = "atype")
		self.atype.grid(row = 10, column = 0, sticky = W)
		self.atype_entry = Entry(self.topframe)
		self.atype_entry.grid(row = 10, column = 1, sticky = W)
		self.adim = Checkbutton(self.topframe, variable = self.checkbox_variables[8], text = "adim")
		self.adim.grid(row = 11, column = 0, sticky = W)
		self.adim_entry = Entry(self.topframe)
		self.adim_entry.grid(row = 11, column = 1, sticky = W)
		self.aconv_chans = Checkbutton(self.topframe, variable = self.checkbox_variables[9], text = "aconv_chans")
		self.aconv_chans.grid(row = 12, column = 0, sticky = W)
		self.aconv_chans_entry = Entry(self.topframe)
		self.aconv_chans_entry.grid(row = 12, column = 1, sticky = W)
		self.aconv_filts = Checkbutton(self.topframe, variable = self.checkbox_variables[10], text = "aconv_filts")
		self.aconv_filts.grid(row = 13, column = 0, sticky = W)
		self.aconv_filts_entry = Entry(self.topframe)
		self.aconv_filts_entry.grid(row = 13, column = 1, sticky = W)

		self.hybrid_attention_label = Label(self.topframe, text = "Hybrid Attention")
		self.hybrid_attention_label.grid(row = 14, column = 0, sticky = W)
		self.mtlalpha = Checkbutton(self.topframe, variable = self.checkbox_variables[11], text = "mtlalpha")
		self.mtlalpha.grid(row = 15, column = 0, sticky = W)
		self.mtlalpha_entry = Entry(self.topframe)
		self.mtlalpha_entry.grid(row = 15, column = 1, sticky = W)

		self.minibatch_label = Label(self.topframe, text = "Minibatch related")
		self.minibatch_label.grid(row = 16, column = 0, sticky = W)
		self.batchsize = Checkbutton(self.topframe, variable = self.checkbox_variables[12], text = "batchsize")
		self.batchsize.grid(row = 17, column = 0, sticky = W)
		self.batchsize_entry = Entry(self.topframe)
		self.batchsize_entry.grid(row = 17, column = 1, sticky = W)
		self.maxlen_in = Checkbutton(self.topframe, variable = self.checkbox_variables[13], text = "maxlen_in")
		self.maxlen_in.grid(row = 18, column = 0, sticky = W)
		self.maxlen_in_entry = Entry(self.topframe)
		self.maxlen_in_entry.grid(row = 18, column = 1, sticky = W)
		self.maxlen_out = Checkbutton(self.topframe, variable = self.checkbox_variables[14], text = "maxlen_out")
		self.maxlen_out.grid(row = 19, column = 0, sticky = W)
		self.maxlen_out_entry = Entry(self.topframe)
		self.maxlen_out_entry.grid(row = 19, column = 1, sticky = W)

		self.optimization_label = Label(self.topframe, text = "Optimization Related")
		self.optimization_label.grid(row = 20, column = 0, sticky = W)
		self.opt = Checkbutton(self.topframe, variable = self.checkbox_variables[15], text = "opt")
		self.opt.grid(row = 21, column = 0, sticky = W)
		self.opt_entry = Entry(self.topframe)
		self.opt_entry.grid(row = 21, column = 1, sticky = W)
		self.epochs = Checkbutton(self.topframe, variable = self.checkbox_variables[16], text = "epochs")
		self.epochs.grid(row = 22, column = 0, sticky = W)
		self.epochs_entry = Entry(self.topframe)
		self.epochs_entry.grid(row = 22, column = 1, sticky = W)


		# secondly, we do the right side
		self.rnn_label = Label(self.topframe, text = "RNN-LM")
		self.rnn_label.grid(row = 0, column = 2, sticky = W)
		self.lm_layers = Checkbutton(self.topframe, variable = self.checkbox_variables[17], text = "lm_layers")
		self.lm_layers.grid(row = 1, column = 2, sticky = W)
		self.lm_layers_entry = Entry(self.topframe)
		self.lm_layers_entry.grid(row = 1, column = 3, sticky = W)
		self.lm_units = Checkbutton(self.topframe, variable = self.checkbox_variables[18], text = "lm_units")
		self.lm_units.grid(row = 2, column = 2, sticky = W)
		self.lm_units_entry = Entry(self.topframe)
		self.lm_units_entry.grid(row = 2, column = 3, sticky = W)
		self.lm_opt = Checkbutton(self.topframe, variable = self.checkbox_variables[19], text = "lm_opt")
		self.lm_opt.grid(row = 3, column = 2, sticky = W)
		self.lm_opt_entry = Entry(self.topframe)
		self.lm_opt_entry.grid(row = 3, column = 3, sticky = W)
		self.lm_batchsize = Checkbutton(self.topframe, variable = self.checkbox_variables[20], text = "lm_batchsize")
		self.lm_batchsize.grid(row = 4, column = 2, sticky = W)
		self.lm_batchsize_entry = Entry(self.topframe)
		self.lm_batchsize_entry.grid(row = 4, column = 3, sticky = W)
		self.lm_epochs = Checkbutton(self.topframe, variable = self.checkbox_variables[21], text = "lm_epochs")
		self.lm_epochs.grid(row = 5, column = 2, sticky = W)
		self.lm_epochs_entry = Entry(self.topframe)
		self.lm_epochs_entry.grid(row = 5, column = 3, sticky = W)
		self.lm_maxlen = Checkbutton(self.topframe, variable = self.checkbox_variables[22], text = "lm_maxlen")
		self.lm_maxlen.grid(row = 6, column = 2, sticky = W)
		self.lm_maxlen_entry = Entry(self.topframe)
		self.lm_maxlen_entry.grid(row = 6, column = 3, sticky = W)
		self.lm_resume = Checkbutton(self.topframe, variable = self.checkbox_variables[23], text = "lm_resume")
		self.lm_resume.grid(row = 7, column = 2, sticky = W)
		self.lm_resume_entry = Entry(self.topframe)
		self.lm_resume_entry.grid(row = 7, column = 3, sticky = W)
		self.lmtag = Checkbutton(self.topframe, variable = self.checkbox_variables[24], text = "lmtag")
		self.lmtag.grid(row = 8, column = 2, sticky = W)
		self.lmtag_entry = Entry(self.topframe)
		self.lmtag_entry.grid(row = 8, column = 3, sticky = W)

		self.decoding_params_label = Label(self.topframe, text = "Decoding Parameters")
		self.decoding_params_label.grid(row = 9, column = 2, sticky = W)
		self.lm_weight = Checkbutton(self.topframe, variable = self.checkbox_variables[25], text = "lm_weight")
		self.lm_weight.grid(row = 10, column = 2, sticky = W)
		self.lm_weight_entry = Entry(self.topframe)
		self.lm_weight_entry.grid(row = 10, column = 3, sticky = W)
		self.beam_size = Checkbutton(self.topframe, variable = self.checkbox_variables[26], text = "beam_size")
		self.beam_size.grid(row = 11, column = 2, sticky = W)
		self.beam_size_entry = Entry(self.topframe)
		self.beam_size_entry.grid(row = 11, column = 3, sticky = W)
		self.penalty = Checkbutton(self.topframe, variable = self.checkbox_variables[27], text = "penalty")
		self.penalty.grid(row = 12, column = 2, sticky = W)
		self.penalty_entry = Entry(self.topframe)
		self.penalty_entry.grid(row = 12, column = 3, sticky = W)
		self.maxlenratio = Checkbutton(self.topframe, variable = self.checkbox_variables[28], text = "maxlenratio")
		self.maxlenratio.grid(row = 13, column = 2, sticky = W)
		self.maxlenratio_entry = Entry(self.topframe)
		self.maxlenratio_entry.grid(row = 13, column = 3, sticky = W)
		self.minlenratio = Checkbutton(self.topframe, variable = self.checkbox_variables[29], text = "minlenratio")
		self.minlenratio.grid(row = 14, column = 2, sticky = W)
		self.minlenratio_entry = Entry(self.topframe)
		self.minlenratio_entry.grid(row = 14, column = 3, sticky = W)
		self.ctc_weight = Checkbutton(self.topframe, variable = self.checkbox_variables[30], text = "ctc_weight")
		self.ctc_weight.grid(row = 15, column = 2, sticky = W)
		self.ctc_weight_entry = Entry(self.topframe)
		self.ctc_weight_entry.grid(row = 15, column = 3, sticky = W)
		self.recog_model = Checkbutton(self.topframe, variable = self.checkbox_variables[31], text = "recog_model")
		self.recog_model.grid(row = 16, column = 2, sticky = W)
		self.recog_model_entry = Entry(self.topframe)
		self.recog_model_entry.grid(row = 16, column = 3, sticky = W)

		self.scheduled_sampling_label = Label(self.topframe, text = "Scheduled_Sampling_Option")
		self.scheduled_sampling_label.grid(row = 17, column = 2, sticky = W)
		self.samp_prob = Checkbutton(self.topframe, variable = self.checkbox_variables[32], text = "samp_prob")
		self.samp_prob.grid(row = 18, column = 2, sticky = W)
		self.samp_prob_entry = Entry(self.topframe)
		self.samp_prob_entry.grid(row = 18, column = 3, sticky = W)

		self.exp_tag_label = Label(self.topframe, text = "Exp Tag")
		self.exp_tag_label.grid(row = 19, column = 2, sticky = W)
		self.exp_tag = Checkbutton(self.topframe, variable = self.checkbox_variables[33], text = "tag")
		self.exp_tag.grid(row = 20, column = 2, sticky = W)
		self.exp_tag_entry = Entry(self.topframe)
		self.exp_tag_entry.grid(row = 20, column = 3, sticky = W)


		# ------------------------------------------------------------------------------------------
		# the middle frame. here we only do have the path that we wanna enter
		self.path_label = Label(self.middleframe, text = "Please choose the path to a valid run.sh file:")
		self.path_label.grid(row = 0)
		self.path_entry = Entry(self.middleframe)
		self.path_entry.grid(row = 1)


		# ------------------------------------------------------------------------------------------
		# as the last frame the bottom frame. the three buttons that come 
		self.reset_button = Button(self.bottomframe, text = "Reset values")
		self.sel_button = Button(self.bottomframe, text = "Select all")
		self.desel_button = Button(self.bottomframe, text = "Deselect all")
		self.start_button = Button(self.bottomframe, text = "Start", fg = "green")
		self.reset_button.grid(row = 1, column = 0, sticky = W)
		self.sel_button.grid(row = 1, column = 1, sticky = W)
		self.desel_button.grid(row = 1, column = 2, sticky = W)
		self.start_button.grid(row = 1, column = 3, sticky = E)


		# ------------------------------------------------------------------------------------------
		# additional attributes that are useful

		# the current configurations
		self.configs = ESP_configs()

		# a checkbox-list for convenience
		self.all_checkboxes = [self.etype, self.elayers, self.eunits, self.eprojs, self.subsample, self.dlayers,
		self.dunits, self.atype, self.adim, self.aconv_chans, self.aconv_filts, self.mtlalpha, self.batchsize, 
		self.maxlen_in, self.maxlen_out, self.opt, self.epochs, self.lm_layers, self.lm_units, self.lm_opt, 
		self.lm_batchsize, self.lm_epochs, self.lm_maxlen, self.lm_resume, self.lmtag, self.lm_weight, self.beam_size,
		self.penalty, self.maxlenratio, self.minlenratio, self.ctc_weight, self.recog_model, self.samp_prob, self.exp_tag]

		self.all_entries = [self.etype_entry, self.elayers_entry, self.eunits_entry, self.eprojs_entry, self.subsample_entry,
		self.dlayers_entry, self.dunits_entry, self.atype_entry, self.adim_entry, self.aconv_chans_entry, 
		self.aconv_filts_entry, self.mtlalpha_entry, self.batchsize_entry, self.maxlen_in_entry, self.maxlen_out_entry,
		self.opt_entry, self.epochs_entry, self.lm_layers_entry, self.lm_units_entry, self.lm_opt_entry,
		self.lm_batchsize_entry, self.lm_epochs_entry, self.lm_maxlen_entry, self.lm_resume_entry, self.lmtag_entry,
		self.lm_weight_entry, self.beam_size_entry, self.penalty_entry, self.maxlenratio_entry, self.minlenratio_entry,
		self.ctc_weight_entry, self.recog_model_entry, self.samp_prob_entry, self.exp_tag_entry]


		# ------------------------------------------------------------------------------------------
		# functions that run upon initialization
		self.bind_functions()
		self.reset_values("<Button-1>")


	# ----------------------------------------------------------------------------------------------
	# here come all the button-click functions

	def bind_functions(self): 
		"""Simply binding the functions to the buttons."""
		self.reset_button.bind("<Button-1>", self.reset_values)
		self.sel_button.bind("<Button-1>", self.select_all_boxes)
		self.desel_button.bind("<Button-1>", self.deselect_all_boxes)
		self.start_button.bind("<Button-1>", self.run_program)


	def select_all_boxes(self, event):
		"""Select all the checkboxes."""
		for box in self.all_checkboxes:
			box.select()

	def deselect_all_boxes(self, event):
		"""Deselect all the checkboxes."""
		for box in self.all_checkboxes:
			box.deselect()

	def reset_values(self, event):
		"""Resets all the values to default and displays them in the GUI's entries"""
		self.configs = ESP_configs()
		for (i, param) in enumerate(self.configs.all_config_params):
			# because insert will just insert, but not overwrite, we will need to delete all the entries first
			self.all_entries[i].delete(0, END)
			if self.configs.all_config_params[param] == None:
				self.all_entries[i].insert(0, "")
			else:
				self.all_entries[i].insert(0, self.configs.all_config_params[param])


	# ----------------------------------------------------------------------------------------------
	# all the functions that help parsing the GUI widgets

	def find_all_selected_boxes(self):
		"""Parse all the checkboxes and return a list of all of them which are checked"""
		selected_boxes = []
		indices = []

		for (i,variable) in enumerate(self.checkbox_variables):
			if variable.get() == 1:
				selected_boxes.append(self.all_checkboxes[i].cget("text"))
				indices.append(i)

		return selected_boxes, indices


	def get_values(self, indices):
		"""Gets the current values out of the entry boxes and returns them as a list corresponding 
		to the indices. We usually would obtain the indices running the find_all_selected_boxes()
		method."""
		values = []

		for i in indices:
			values.append(self.all_entries[i].get())
		return values


	def run_program(self, with_parameter_optimization = False):
		"""Runs the run.sh file with the parameters set as in the GUI.
		with_parameter_optmization runs the Guassian hyperparameter tuning, but will cost a lot of time, 
		since the networks of ESPnet will be retrained multiple times."""

		current_boxes, indices = self.find_all_selected_boxes()
		current_values = self.get_values(indices)
		self.configs.write_params(zip(current_boxes, current_values))


if __name__ == "__main__":
	root = Tk()
	myWindow = Window(root)
	root.mainloop()
