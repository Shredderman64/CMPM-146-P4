import pyhop

'''begin operators'''

def op_punch_for_wood (state, ID):
	if state.time[ID] >= 4:
		state.wood[ID] += 1
		state.time[ID] -= 4
		return state
	return False

def op_chop_for_wood (state, ID):
	if state.time[ID] >= 2:
		state.wood[ID] += 1
		state.time[ID] -= 2
		return state
	return False

def op_craft_wooden_axe_at_bench (state, ID):
	if state.time[ID] >= 1 and state.bench[ID] >= 1 and state.plank[ID] >= 3 and state.stick[ID] >=2:
		state.wooden_axe[ID] += 1
		state.plank[ID] -= 3
		state.stick[ID] -= 2
		state.time[ID] -= 1
		return state
	return False

def op_craft_bench (state, ID):
	if state.time[ID] >= 1 and state.plank[ID] >= 4:
		state.bench[ID] += 1
		state.plank[ID] -= 4
		state.time[ID] -= 1
		return state
	return False

def op_craft_planks (state, ID):
	if state.time[ID] >= 1 and state.wood[ID] >= 1:
		state.plank[ID] += 4
		state.wood[ID] -= 1
		state.time[ID] -= 1
		return state
	return False

def op_craft_sticks (state, ID):
	if state.time[ID] >= 1 and state.plank[ID] >= 2:
		state.stick[ID] += 4
		state.plank[ID] -= 2
		state.time[ID] -= 1
		return state
	return False

# your code here

pyhop.declare_operators (op_punch_for_wood, op_chop_for_wood, op_craft_wooden_axe_at_bench, op_craft_planks, op_craft_sticks, op_craft_bench)

'''end operators'''

def check_enough (state, ID, item, num):
	if getattr(state,item)[ID] >= num: return []
	return False

def produce_enough (state, ID, item, num):
	return [('produce', ID, item), ('have_enough', ID, item, num)]

def produce (state, ID, item):
	if item == 'wood':
		return [('produce_wood', ID)]
	# your code here
	elif item == 'wooden_axe':
		# this check to make sure we're not making multiple axes
		if state.made_wooden_axe[ID] is True:
			return False
		else:
			state.made_wooden_axe[ID] = True
		return [('produce_wooden_axe', ID)]
	elif item == 'bench':
		if state.made_bench[ID] is True:
			return False
		else:
			state.made_bench[ID] = True
		return [('produce_bench', ID)]
	elif item == 'plank':
		return [('produce_planks', ID)]
	elif item == 'stick':
		return [('produce_sticks', ID)]
	else:
		return False

pyhop.declare_methods ('have_enough', check_enough, produce_enough)
pyhop.declare_methods ('produce', produce)

'''begin recipe methods'''

def punch_for_wood (state, ID):
	return [('op_punch_for_wood', ID)]

def craft_wooden_axe_at_bench (state, ID):
	return [('have_enough', ID, 'bench', 1), ('have_enough', ID, 'stick', 2), ('have_enough', ID, 'plank', 3), ('op_craft_wooden_axe_at_bench', ID)]

def craft_bench (state, ID):
	return [('have_enough', ID, 'plank', 4), ('op_craft_bench', ID)]

def craft_planks (state, ID):
	return [('have_enough', ID, 'wood', 1), ('op_craft_planks', ID)]

def craft_sticks (state, ID):
	return [('have_enough', ID, 'plank', 2), ('op_craft_sticks', ID)]

def chop_for_wood (state, ID):
	return [('have_enough', ID, 'wooden_axe', 1), ('op_chop_for_wood', ID)]
# your code here

pyhop.declare_methods ('produce_wood', chop_for_wood, punch_for_wood)
pyhop.declare_methods ('produce_wooden_axe', craft_wooden_axe_at_bench)
pyhop.declare_methods ('produce_bench', craft_bench)
pyhop.declare_methods ('produce_planks', craft_planks)
pyhop.declare_methods ('produce_sticks', craft_sticks)

'''end recipe methods'''

# declare state
state = pyhop.State('state')
state.wood = {'agent': 0}
state.plank = {'agent': 0}
state.stick = {'agent': 0}
# state.time = {'agent': 4}
state.time = {'agent': 46}
state.wooden_axe = {'agent': 0}
state.made_wooden_axe = {'agent': False}
state.bench = {'agent': 0}
state.made_bench = {'agent': False}
# your code here

def heuristic(state, curr_task, tasks, plan, depth, calling_stack):
	return False

pyhop.add_check(heuristic)
# pyhop.print_operators()
pyhop.print_methods()

#pyhop.pyhop(state, [('have_enough', 'agent', 'wood', 4)], verbose=3)
pyhop.pyhop(state, [('have_enough', 'agent', 'wood', 12)], verbose=3)