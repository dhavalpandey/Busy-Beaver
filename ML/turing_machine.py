class Machine:
    def __init__(self, code: str):
        self.code = code
     
    def describe(self) -> None:
        """
        Given a BB5‐style code string (with or without underscores), prints a markdown table:
        rows = states A–E; cols = read 0 / read 1; cells = transition or HALT.

        e.g. 1RB1LE_1LC1RA_1LA0LD_0LB1LD_---0RB
        becomes: 
        | State | 0    | 1   |
        |-------|------|-----|
        | A     | 1RB  | 1LE |
        | B     | 1LC  | 1RA |
        | C     | 1LA  | 0LD |
        | D     | 0LB  | 1LD |
        | E     | HALT | 0RB |
        """
        code = self.code
        flat = code.replace("_", "")
        parts = [flat[i:i+3] for i in range(0, len(flat), 3)]
        states = ["A","B","C","D","E"]
        table = [["State","0","1"]]
        for i, st in enumerate(states):
            r0 = parts[2*i]
            r1 = parts[2*i+1]
            cell0 = r0 if r0!="---" else "HALT"
            cell1 = r1 if r1!="---" else "HALT"
            table.append([st, cell0, cell1])
        widths = [max(len(row[j]) for row in table) for j in range(3)]
        hdr = "| " + " | ".join(table[0][j].ljust(widths[j]) for j in range(3)) + " |"
        sep = "|-" + "-|-".join("-"*widths[j] for j in range(3)) + "-|"
        print(hdr); print(sep)
        for row in table[1:]:
            print("| " + " | ".join(row[j].ljust(widths[j]) for j in range(3)) + " |")

    def parse(self) -> list[int]:
            """
            Split into state‐blocks
            It takes your machine code string (e.g. "1RB1LE_---1RA_…") and cuts it at each underscore.
            This gives five “blocks”, one per state (A through E), each block containing exactly two three-character instructions (for reading 0 and for reading 1).

            Turn each three-letter instruction into three numbers
            For each instruction triplet, like "1RB" or "---", it produces:

            Write bit: the first character, 0 or 1, becomes the number 0 or 1.
            If the triplet is "---", we treat that as “halt” and set the write bit to 0.

            Move code: the second character, L or R, becomes 0 for left or 1 for right.
            If the triplet is "---", we use 2 to mean “this instruction halts instead of moving.”

            Next‐state index: the third character, A–E, becomes 0–4 respectively.
            If the triplet is "---", we use –1 to show “no next state, because we halted.”

            Flatten into one long list
            You end up with 3 numbers per instruction, and there are 10 instructions (5 states × 2 read‐symbols), so you get a list of 30 integers."""

            flat = self.code.replace("_", "")
            feats: list[int] = []
            # iterate over each 3-char instruction
            for i in range(0, len(flat), 3):
                instr = flat[i:i+3]
                if instr == "---":
                    # HALT
                    feats += [0, 2, -1]
                else:
                    # write_bit = first char, '0' or '1'
                    w = ord(instr[0]) - ord('0')
                    # move_dir = 'L'→0, 'R'→1
                    d = 1 if instr[1] == 'R' else 0
                    # next_state = 'A'→0 … 'E'→4
                    ns = ord(instr[2]) - ord('A')
                    feats += [w, d, ns]
            return feats

    def unparse(self, feats: list[int]) -> str:
        parts = []
        for w,d,ns in zip(*(iter(feats),)*3):
            if d == 2:            # HALT
                parts.append("---")
            else:
                move = "R" if d==1 else "L"
                state = chr(ord("A") + ns)
                parts.append(f"{w}{move}{state}")
        blocks = ["".join(parts[i:i+2]) for i in range(0, len(parts), 2)]
        return "_".join(blocks)