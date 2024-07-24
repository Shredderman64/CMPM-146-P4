import pyhop
import json

def check_enough (state, ID, item, num):
	if getattr(state,item)[ID] >= num: return []
	return False

def produce_enough (state, ID, item, num):
	return [('produce', ID, item), ('have_enough', ID, item, num)]

pyhop.declare_methods ('have_enough', check_enough, produce_enough)

def produce (state, ID, item):
	return [('produce_{}'.format(item), ID)]

pyhop.declare_methods ('produce', produce)

def make_method (name, rule):
	def method (state, ID):
		tasks = []
		if 'Requires' in rule:
			for item in rule['Requires']:
				tasks.append(('have_enough', ID, item, rule['Requires'][item]))
		if 'Consumes' in rule:
			for item in rule['Consumes']:
				tasks.append(('have_enough', ID, item, rule['Consumes'][item]))
		tasks.append(('op_{}'.format(name), ID))
		# get list of subtasks
		return tasks
	return method

def declare_methods (data):
	# some recipes are faster than others for the same product even though they might require extra tools
	# sort the recipes so that faster recipes go first

	# your code here
	# hint: call make_method, then declare the method to pyhop using pyhop.declare_methods('foo', m1, m2, ..., mk)	

	# declaring lists for later use
	recipe_keys = [] # holds recipes when sorted by time

	# get times for all recipes and sort by time
	for key in data['Recipes'].keys():
		time = data['Recipes'][key]['Time']
		recipe_keys.append((time, key))
	recipe_keys = sorted(recipe_keys)

	# make and declare all methods to pyhop
	# for time, key in recipe_keys:
	#	method = make_method(key, data['Recipes'][key])
	#	pyhop.declare_methods('produce_' + key, method)
	for item in data['Items']:
		methods = [] # list of tasks sent to declare_methods
		for time, key in recipe_keys:
			product = data['Recipes'][key]['Produces']
			if item in product:
				name = key.replace(" ", "_")
				method = make_method(name, data['Recipes'][key])
				method.__name__ = name
				methods.append(method)
		pyhop.declare_methods('produce_{}'.format(item), *methods)
	

def make_operator (rule):
	def operator (state, ID):
		if state.time[ID] >= rule['Time']:
			state.time[ID] -= rule['Time']
			for item in rule['Produces']:
				prod_val = getattr(state,item)[ID] + rule['Produces'][item]
				setattr(state, item, {ID: prod_val})
			if 'Consumes' in rule:
				for item in rule['Consumes']:
					con_val = getattr(state,item)[ID] - rule['Consumes'][item]
					setattr(state, item, {ID: con_val})
			return state
		return False
	return operator

def declare_operators (data):
	# your code here
	# hint: call make_operator, then declare the operator to pyhop using pyhop.declare_operators(o1, o2, ..., ok)
	
	# Holds list of operators to be declared
	operators = []
	# make operators using the rules for each recipe
	for item in data['Recipes']:
		operator = make_operator(data['Recipes'][item])
		operator.__name__ = 'op_' + item.replace(" ", "_")
		operators.append(operator)
	for op in operators:
		pyhop.declare_operators(op)

def add_heuristic (data, ID):
	# prune search branch if heuristic() returns True
	# do not change parameters to heuristic(), but can add more heuristic functions with the same parameters: 
	# e.g. def heuristic2(...); pyhop.add_check(heuristic2)
	def heuristic (state, curr_task, tasks, plan, depth, calling_stack):
		# your code here

		# checks if a tool is repeatedly being tasked to be crafted and breaks the cycle if so
		for tool in data['Tools']:
			if curr_task == ('have_enough', ID, tool, 1):
				if tasks.count(curr_task) > 1:
					return True

		return False # if True, prune this branch

	pyhop.add_check(heuristic)


def set_up_state (data, ID, time=0):
	state = pyhop.State('state')
	state.time = {ID: time}

	for item in data['Items']:
		setattr(state, item, {ID: 0})

	for item in data['Tools']:
		setattr(state, item, {ID: 0})

	for item, num in data['Initial'].items():
		setattr(state, item, {ID: num})

	return state

def set_up_goals (data, ID):
	goals = []
	for item, num in data['Goal'].items():
		goals.append(('have_enough', ID, item, num))

	return goals

if __name__ == '__main__':
	rules_filename = 'crafting.json'

	with open(rules_filename) as f:
		data = json.load(f)

	state = set_up_state(data, 'agent', time=239) # allot time here
	goals = set_up_goals(data, 'agent')

	declare_operators(data)
	declare_methods(data)
	add_heuristic(data, 'agent')

	# pyhop.print_operators()
	pyhop.print_methods()

	# Hint: verbose output can take a long time even if the solution is correct; 
	# try verbose=1 if it is taking too long
	pyhop.pyhop(state, goals, verbose=3)
	# pyhop.pyhop(state, [('have_enough', 'agent', 'cart', 1),('have_enough', 'agent', 'rail', 20)], verbose=3)
