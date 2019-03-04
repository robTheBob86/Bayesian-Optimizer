#!/usr/bin/env bash

. environment_GOptimization/bin/activate

cd src/
python run_terminal.py \
	--network tedlium \
	--n_iterations 5 \
	--lm_weight \
	--lm_epochs \
	--lm_layers \
	--mtlalpha \
	--aconv_filts \
	--penalty \
	--samp_prob \
	--lm_batchsize \
	--dunits \
	--lm_units \
	--eprojs \
	--epochs \
	--maxlen_in \
	--ctc_weight \
	--beam_size \
	--eunits \
	--dlayers \
	--adim \
	--elayers \
	--lm_maxlen \
	--aconv_chans \
	--maxlen_out

cd .. # getting back into the previous folder

deactivate

