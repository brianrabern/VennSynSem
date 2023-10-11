from core.syntax import syn, form, inter, union, comp, destroy, save
from core.semantics import Model, sem
from core.renderer import render_venn  # , labels
from core.regions import R, A1, A2, A3  # , A4

# syntax
a = [comp, A1, [union, A2, A3]]
b = [comp, [inter, A1, A2], A3]
c = [inter, A3, [inter, A1, A2]]
d = [comp, [inter, A1, A3], A2]
e = [comp, A2, [union, A1, A3]]
f = [comp, [inter, A2, A3], A1]
g = [comp, A3, [union, A1, A2]]
h = [comp, R, [union, A3, [union, A1, A2]]]

D0 = [form, A1, A2, A3]
D1 = [destroy, D0, a]
D2 = [save, D1, [c, g]]
derived_D2 = syn(D2)

# display diagram
render_venn(derived_D2)

# semantics
U = {1, 2, 3, 4, 5}
I = lambda X: {  # noqa
    A1: {1, 2},
    A2: {1},
    A3: set(),
}.get(X)

M1 = Model(U, I)

print(sem(D1)(M1))


# def eval(diagram, model):
#     syntax_output = syn(diagram)
#     semantic_output = sem(diagram)
#     render_venn(syntax_output)

#     print("Universe: ", model.universe)
#     print("Interpretation: ")
#     for x in [A1, A2, A3, A4, A5, A6]:
#         if model.interpretation(x) is not None:
#             print(f"          A{labels[x][3]}:", model.interpretation(x))

#     print(f"Result: The diagram is {semantic_output(model)} on the model.")
