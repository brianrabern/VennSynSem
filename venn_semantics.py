from shapely.geometry import Polygon

class Model:
    def __init__(self, universe, interpretation):
        self.universe = universe
        self.interpretation = interpretation

def is_region_arr(input):
    return not (is_wellformed_diagram(input) or is_wellformed_region(input))

# compositional semantics 
def sem(input):
    if input == R:
        return lambda M: M.universe
    elif isinstance(input, Polygon):
        return lambda M: M.interpretation(input)
    elif input == inter:
        return lambda M: lambda s1, s2: s1 & s2
    elif input == union:
        return lambda M: lambda s1, s2: s1 | s2
    elif input == comp:
        return lambda M: lambda s1, s2: s1 - s2
    elif input == form:
        return lambda M: lambda s1, s2, s3: True
    elif input == destroy:
        return lambda M: lambda p, s: p and (s == set())
    elif input == save:
        return lambda M: lambda p, s: p and (s != set())
    elif is_region_arr(input):
        return lambda M: set().union(*(sem(child)(M) for child in input))
    # composition via functional application
    else:       
       return lambda M: sem(input[0])(M)(*[sem(child)(M) for child in input[1:]])

