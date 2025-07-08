CELLS = (0, 1)
MOVE  = ('l', 'r')

"""
Computed results:
n = 1: 64
n = 2: 20,736
n = 3: 16,777,216
n = 4: 25,600,000,000
n = 5: 63,403,380,965,376
"""

def evaluate(n: int) -> int:
    # each instruction = (write, move, next_state or halt)
    total_choices = len(CELLS) * len(MOVE) * (n + 1)
    # each machine has n * len(CELLS) instruction slots
    return total_choices ** (n * len(CELLS))

print(evaluate(1))
