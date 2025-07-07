import Mathlib.Tactic

theorem halting_problem_undecidable
  (Halts : Nat → Nat → Prop)
  (d_exists : ∃ d, ∀ c, Halts d c ↔ ¬ (Halts c c))
  : ¬ (∃ (h : Nat → Nat → Bool), (∀ c x, h c x = true ↔ Halts c x)) :=
by
  rintro ⟨h, h_spec⟩
  rcases d_exists with ⟨d, d_spec⟩
  by_cases h_says_halts : (h d d = true)
  ·
    have d_actually_halts : Halts d d := (h_spec d d).mp h_says_halts
    have d_actually_loops : ¬ (Halts d d) := (d_spec d).mp d_actually_halts
    contradiction
  ·
    have d_actually_loops : ¬ (Halts d d) := mt (h_spec d d).mpr h_says_halts
    have d_actually_halts : Halts d d := (d_spec d).mpr d_actually_loops
    contradiction
