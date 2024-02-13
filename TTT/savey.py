base=[[([['x', 'x', 'x'], ['o', 'o', ''], ['', '', 'o']], 'x'), ([['x', 'o', 'o'], ['o', 'o', 'x'], ['o', 'x', 'x']], 'o'), ([['o', 'o', 'o'], ['x', 'o', ''], ['x', 'x', 'x']], 'o')]]
base.append( [([['o', '', 'x'], ['o', 'x', 'o'], ['x', '', '']], 'x'), ([['o', 'o', 'x'], ['o', 'o', 'x'], ['x', 'x', 'o']], 'o')])
end=base
import numpy as np
new_end=np.array(end)
print(new_end)