style_1 = [5, [
"""   _|    
 _|  _|  
 _|  _|  
 _|  _|  
   _|    """,
"""   _|  
 _|_|  
   _|  
   _|  
   _|  """,
"""   _|_|    
 _|    _|  
     _|    
   _|      
 _|_|_|_|  """,
""" _|_|_|    
       _|  
   _|_|    
       _|  
 _|_|_|    """,
""" _|  _|    
 _|  _|    
 _|_|_|_|  
     _|    
     _|    """,
""" _|_|_|_|  
 _|        
 _|_|_|    
       _|  
 _|_|_|    """,
"""   _|_|_|  
 _|        
 _|_|_|    
 _|    _|  
   _|_|    """,
""" _|_|_|_|_|  
         _|  
       _|    
     _|      
   _|        """,
"""   _|_|    
 _|    _|  
   _|_|    
 _|    _|  
   _|_|    """,
"""   _|_|    
 _|    _|  
   _|_|_|  
       _|  
 _|_|_|    """,
]]

def numbers_splitter(style):
    numbers_split = []
    for number in style[1]:
        numbers_split[style[1].index(number)] = style[1][style[1].index(number)].split("\n")
    return numbers_split

def build_number_lines(number, style):
    """
    Creates a list of lines needed to print a stylized number.
    Style must be a list of lists of lines in each digit.
    """
    num_string = str(number)
    num_lines = ["" for i in range(0, len(style[0]))]
    for digit in num_string:
        for i in range(0, len(style[0])):
            num_lines[i] += style[int(digit)][i]
    return num_lines

# def add_number_lines(add_to, num_lines):
#     split_string = add_to.split("\n")
#     for line in split_string:
#         split_string[split_string.index(line)] = split_string[split_string.index(line)][:-2] +"  "+line
    