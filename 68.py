# 4:25 PM - 4:49 PM - 5:04 PM

from typing import List

class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:

        # buffer for current line
        # buffer stores [word, trailing_spaces]
        # buffer_capacity is remaining width after reserving one trailing space per buffered word
        buffer = [] # [word,spaces] : word:string, spaces: trailing spaces
        buffer_capacity = maxWidth # remaining capacity of buffer

        def buffer_to_str():
            str_array = []
            for buf in buffer:
                str_array.append(buf[0] + (' '*buf[1]))
            return ''.join(str_array)


        result = [] # List[str] holds final result

        i = 0
        while i< len(words):
            w = words[i]
            # print(f"       buffer={buffer} capacity={buffer_capacity} w={w}")
            if len(w) > buffer_capacity: # no capacity for w
                # adjust buffer spaces
                # distribute remaining spaces evenly across gaps;
                # extra spaces go to the leftmost gaps
                if len(buffer) == 1:
                    buffer[0][1] += buffer_capacity
                else:
                    buffer[-1][1] = 0 # remove trailing space and move last word to right
                    spaces = buffer_capacity+1
                    avg_spaces = spaces//(len(buffer)-1)
                    remainder = spaces % (len(buffer)-1)
                    for j in range(len(buffer)-1):
                        buffer[j][1] += avg_spaces
                    for j in range(remainder): # add remaining space to left word
                        buffer[j][1] += 1    

                result.append(buffer_to_str())

                buffer.clear()
                buffer_capacity = maxWidth
                # keep i unchanged for next line
            elif len(w) == buffer_capacity:
                # exact fit
                buffer.append([w, 0])
                result.append(buffer_to_str())

                buffer.clear()
                buffer_capacity = maxWidth
                i += 1
            else: # len(w) < buffer_capacity
                buffer.append([w, 1]) # put a trailing space after each word in buffer
                buffer_capacity -= (len(w)+1)
                i += 1

        # output last line
        if buffer_capacity < maxWidth:
            last_line = buffer_to_str()
            last_line += (' '*buffer_capacity)
            result.append(last_line)

        return result    

if __name__ == '__main__':
    sol = Solution()

    words = ["This", "is", "an", "example", "of", "text", "justification."]
    maxWidth = 16        
    expected = [
        "This    is    an",
        "example  of text",
        "justification.  "
        ]
    output = sol.fullJustify(words, maxWidth)
    print(f"words={words}  maxWidth={maxWidth}")
    print(f"    expected={expected}")
    print(f"    output  ={output}")
    print(f"    {'PASS' if output==expected else 'FAIL'}\n\n")    

    words = ["What","must","be","acknowledgment","shall","be"]
    maxWidth = 16        
    expected = [
                "What   must   be",
                "acknowledgment  ",
                "shall be        "
                ]
    output = sol.fullJustify(words, maxWidth)
    print(f"words={words}  maxWidth={maxWidth}")
    print(f"    expected={expected}")
    print(f"    output  ={output}")
    print(f"    {'PASS' if output==expected else 'FAIL'}\n\n")   

    words = ["Science","is","what","we","understand","well","enough","to","explain","to","a","computer.","Art","is","everything","else","we","do"]
    maxWidth = 20
    expected =  [
                    "Science  is  what we",
                    "understand      well",
                    "enough to explain to",
                    "a  computer.  Art is",
                    "everything  else  we",
                    "do                  "
                    ]
    output = sol.fullJustify(words, maxWidth)
    print(f"words={words}  maxWidth={maxWidth}")
    print(f"    expected={expected}")
    print(f"    output  ={output}")
    print(f"    {'PASS' if output==expected else 'FAIL'}\n\n")                   
