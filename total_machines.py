STATES = ('a', 'b', 'c', 'd', 'e')
CELLS = (0, 1)
MOVE = ('l', 'r')

HLT = '-'

# each instruction = (write, move, next_state)
total_cells = (len(STATES)*len(CELLS)*len(MOVE)) + 1

# each machine has 10 cells
diff_machines = (total_cells**10)/2
print(f'Total number of machines: {diff_machines:,}')
