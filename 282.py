from functools import cache
from typing import List
DEBUG = True

class Solution:
    def addOperators(self, num: str, target: int) -> List[str]:
        n = len(num)

        @cache
        def operand_val(start_idx, end_idx):
            if num[start_idx] != '0' or end_idx-start_idx==1:
                # if DEBUG:
                #     print(f"            int(num[{start_idx}:{end_idx}])=int({num[start_idx:end_idx]})={int(num[start_idx:end_idx])}")
                return int(num[start_idx:end_idx])
            else:
                raise Exception(f"invalid operand num[{start_idx}, {end_idx}]={num[start_idx:end_idx]}")

        answer = []

        def list_all_add_subtractions(term_sequence, start_idx, partial_expr, partial_result):
            if DEBUG:
                print(f"        list_all_add_subtractions({term_sequence}, {start_idx}, {partial_expr}, {partial_result})")
            if start_idx >= len(term_sequence):
                if partial_result == target:
                    answer.append(partial_expr)
                return

            term_val, term_str = term_sequence[start_idx]

            if partial_result is None:
                list_all_add_subtractions(term_sequence, start_idx+1, term_str, term_val)
            else:
                list_all_add_subtractions(term_sequence, start_idx+1, f"{partial_expr}+{term_str}", partial_result + term_val)
                list_all_add_subtractions(term_sequence, start_idx+1, f"{partial_expr}-{term_str}", partial_result - term_val)
        

        def list_all_terms(num, start_idx, term_sequence:List):
            if DEBUG:
                print(f"    list_all_terms({num[start_idx:]}, {start_idx}, {term_sequence})")
            if start_idx >= n:
                list_all_add_subtractions(term_sequence, 0, "", None)
                return

            if num[start_idx] == '0':
                new_term = (0, "0")
                new_term_sequence = term_sequence.copy()

                # keep new_term as is
                new_term_sequence.append(new_term)
                list_all_terms(num, start_idx+1, new_term_sequence)                

                # multiply new term with previous term
                if len(term_sequence)>0:
                    new_term_sequence = term_sequence.copy()
                    prev_term_operand, prev_term_str = new_term_sequence[-1]
                    new_term_sequence[-1] = (prev_term_operand*new_term[0], prev_term_str+"*"+new_term[1])
                    list_all_terms(num, start_idx+1, new_term_sequence)                
            else:
                for i in range(start_idx+1, n+1):
                    new_term = (operand_val(start_idx, i), "".join(num[start_idx:i]))    
                    new_term_sequence = term_sequence.copy()
                    new_term_sequence.append(new_term)

                    # keep new term as is
                    list_all_terms(num, i, new_term_sequence)

                    # multiply new term with previous term
                    if len(term_sequence)>0:
                        new_term_sequence = term_sequence.copy()
                        prev_term_operand, prev_term_str = new_term_sequence[-1]
                        new_term_sequence[-1] = (prev_term_operand*new_term[0], prev_term_str+"*"+new_term[1])

                        list_all_terms(num, i, new_term_sequence)

        list_all_terms(num, 0, [])

        return answer


