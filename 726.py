from typing import Any, Dict, Tuple

DEBUG = False

LPAREN=1
RPAREN=2
LABEL=3
NUM=4
END=5

token_type_map = {}
token_type_map[LPAREN] = 'LPAREN'
token_type_map[RPAREN] = 'RPAREN'
token_type_map[LABEL] = 'LABEL'
token_type_map[NUM] = 'NUM'
token_type_map[END] = 'END'

class Solution:
    def countOfAtoms(self, formula: str) -> str:
        if DEBUG:
            print(f"acount atoms of {formula}")

        
        next_char_idx = 0
        n = len(formula)

        def peek_token_type():
            if next_char_idx >= n:
                return END

            c = formula[next_char_idx]
            if  c == '(':
                return LPAREN

            if c == ')':
                return RPAREN

            if c.isdigit():
                return NUM

            if c.isalpha():
                return LABEL

            raise Exception(f"invalid char {c}")

        def next_token()->Tuple[int, Any]:
            nonlocal next_char_idx

            if next_char_idx >= n:
                return (END, None)

            c = formula[next_char_idx]
            if  c == '(':
                next_char_idx += 1
                return (LPAREN, None)

            if c == ')':
                next_char_idx += 1
                return (RPAREN, None)

            if c.isdigit():
                j = next_char_idx
                while j<n and formula[j].isdigit():
                    j += 1
                i = next_char_idx
                next_char_idx = j
                return (NUM, int(formula[i:j]))

            if c.isalpha():
                j = next_char_idx+1 # skip upper case letter
                while j < n and formula[j]>='a' and formula[j]<='z':
                    j += 1
                i = next_char_idx
                next_char_idx = j
                return (LABEL, formula[i:j])

        # def next_token()->Tuple[int, any]:
        #     token = _next_token()
        #     if DEBUG:
        #         print(f"    next_token => ({token_type_map[token[0]]},{token[1]}) next_char_idx={next_char_idx} remaining formular={formula[next_char_idx:]}")
        #     return token

        def add_atom(atom_dict:Dict[str, int], label:str, cnt:int):
            old_cnt = atom_dict.get(label, 0)
            atom_dict[label] = old_cnt + cnt

        def multiply_atom(atom_dict:Dict[str, int], factor:int):
            for k, v in atom_dict.items():
                atom_dict[k] = v * factor    

        def merge_atom_dict(atom_dict_from:Dict[str, int], atom_dict_to:Dict[str, int]):
            for k, v in atom_dict_from.items():
                add_atom(atom_dict_to, k, v)


        def parse_formula():
            atoms_dict = {}

            while True:
                token = next_token()
                if token[0] == END:
                    break;

                if token[0] == LABEL:
                    complete_one_atom(atoms_dict, token[1])
                    continue

                if token[0] == LPAREN:
                    sub_atoms_dict = complete_parenthesis()
                    merge_atom_dict(sub_atoms_dict, atoms_dict) 
                    continue    


                raise Exception(f"parse_formula: unexpected token {token}")

            return atoms_dict

        def complete_one_atom(atoms_dict:Dict[str, int], label:str):
            if DEBUG:
                print(f"start complete_one_atom label={label}")
            if peek_token_type() == NUM:
                token2 = next_token()
                add_atom(atoms_dict, label, token2[1])
                if DEBUG:
                    print(f"end complete_one_atom label={label} cnt={token2[1]}")
            else:
                add_atom(atoms_dict, label, 1)
                if DEBUG:
                    print(f"end complete_one_atom label={label} cnt=None")
                    


        def complete_parenthesis():
            atoms_dict = {}

            if DEBUG:
                print(f"start complete_parenthesis")

            while True:
                token = next_token()
                if token[0] == LABEL:
                    complete_one_atom(atoms_dict, token[1])
                    continue

                if token[0] == LPAREN:
                    sub_atoms_dict = complete_parenthesis()
                    merge_atom_dict(sub_atoms_dict, atoms_dict) 
                    continue    

                if token[0] == RPAREN:
                    if peek_token_type() == NUM:
                        token2 = next_token()
                        multiply_atom(atoms_dict, token2[1])

                    if DEBUG:
                        print(f"end complete_parenthesis atoms_dict={atoms_dict}")
                    return atoms_dict                
                           
                raise Exception(f"complete_parenthesis: unexpected token {token}")

        # Return the count of all elements as a string in the following form: 
        # the first name (in sorted order), followed by its count (if that count is more than 1), 
        # followed by the second name (in sorted order), followed by its count (if that count is more than 1), and so on.
        final_atom_dict = parse_formula()
        if DEBUG:
            print(f"final_atom_dict={final_atom_dict}")

        keys = [x for x in final_atom_dict.keys()]
        keys.sort()    

        results = []
        for k in keys:
            cnt = final_atom_dict[k]
            if cnt > 1:
                results.append(f"{k}{cnt}")
            else:
                results.append(k)    
        
        return "".join(results)        

        