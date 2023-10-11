from shapely.geometry import Point, Polygon, MultiPolygon, LineString
import matplotlib.pyplot as plt
from matplotlib.patches import Path, PathPatch
import random
import copy
from venn_syntax import *
from venn_semantics import *
from venn_renderer import *


# the plane (or a finite square of it)
R = Polygon([(-3, -3), (-3, 5), (5, 5), (5, -3)])

# center points for some basic regions
centers = [(1, 2), (0, 0), (2, 0), (3, 2), (1, 1), (1.75, .85)]

# specify six basic regions
A1 = Point(centers[0]).buffer(2)
A2 = Point(centers[1]).buffer(2)
A3 = Point(centers[2]).buffer(2)
A4 = Point(centers[3]).buffer(1.5)
A5 = Point(centers[4]).buffer(.3)
A6 = Point(centers[5]).buffer(2.2)

basic_regions = {A1,A2,A3,A4,A5,A6}
# the labels are just for rendering 
labels = {
    A1: '$A_1$', 
    A2: '$A_2$', 
    A3: '$A_3$', 
    A4: '$A_4$',
    A5: '$A_5$',
    A6: '$A_6$',
}

render_venn(form(A1,A2,A3))
input("Press Enter to close the plot...")

def eval(diagram, model):
    syntax_output = syn(diagram)
    semantic_output = sem(diagram)
    render_venn(syntax_output)
    
    print("Universe: ", model.universe)
    print("Interpretation: ")
    for x in [A1,A2,A3,A4,A5,A6]:
        if model.interpretation(x) is not None:
            print(f'          A{labels[x][3]}:', model.interpretation(x))
    
    print(f"Result: The diagram is {semantic_output(model)} on the model.")