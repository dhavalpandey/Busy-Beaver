-- ## 1. Model Definition
inductive Symbol | S0 | S1
  deriving Repr, DecidableEq

inductive State | A | HALT
  deriving Repr, DecidableEq

inductive MoveDir | L | R

structure Tape where
  left  : List Symbol
  head  : Symbol
  right : List Symbol
  deriving Repr

def Tape.blank : Tape := { left := [], head := .S0, right := [] }

def Machine := State → Symbol → (State × Symbol × MoveDir)


-- ## 2. Simulator
def step (m : Machine) (s : State) (t : Tape) : (State × Tape) :=
  if s == .HALT then (s, t) else
    let (s', write, move) := m s t.head
    let t' :=
      match move, t.left, t.right with
      | .R, l, r::rs => { left := l ++ [write], head := r, right := rs }
      | .R, l, []    => { left := l ++ [write], head := .S0, right := [] }
      | .L, l::ls, r => { left := ls, head := l, right := write :: r }
      | .L, [], r    => { left := [], head := .S0, right := write :: r }
    (s', t')

def run (m : Machine) (max_steps : Nat) : Option Tape :=
  let rec loop : Nat → State → Tape → Option Tape
    | 0, _, _ => none
    | _+1, .HALT, t => some t
    | n+1, s, t =>
        let (s', t') := step m s t
        loop n s' t'
  loop max_steps .A .blank


-- ## 3. Champion Machine and Proof
def bb1_champion : Machine
| .A, .S0 => (.HALT, .S1, .R)
| .A, .S1 => (.HALT, .S1, .L)
| .HALT, _ => (.HALT, .S0, .R)

def count_ones (tape : Tape) : Nat :=
  (tape.left.filter (· == .S1)).length +
  (if tape.head == .S1 then 1 else 0) +
  (tape.right.filter (· == .S1)).length

-- Theorem: The champion halts with a score of 1.
theorem champion_score_is_1 :
  let final_tape := { left := [.S1], head := .S0, right := [] }
  run bb1_champion 2 = some final_tape ∧ count_ones final_tape = 1 :=
by
  constructor
  · rfl
  · rfl

-- ## 4. Conclusion
-- This file formally proves that BB(1) ≥ 1.
def BusyBeaver1_Lower_Bound : Nat := 1
