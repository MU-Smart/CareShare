from collections import OrderedDict
def get_parameters():
	config_file_name = "ride_sharing.config"

	f = open(config_file_name, 'r')
	lines = f.readlines()
	params = OrderedDict()

	for line in lines:
		line = line.split('\n')[0]
		param_list = line.split(' ')
		param_name = param_list[0]
		param_value = param_list[1]
		params[param_name] = param_value

	return params
