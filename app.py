import streamlit as st
import matplotlib.pyplot as plt
from core.syntax import syn, form, inter, union, comp, destroy, save
from core.semantics import Model, sem
from core.renderer import render_venn
from core.regions import R, A1, A2, A3


# syntax
a = [comp, A1, [union, A2, A3]]
b = [comp, [inter, A1, A2], A3]
c = [inter, A3, [inter, A1, A2]]
d = [comp, [inter, A1, A3], A2]
e = [comp, A2, [union, A1, A3]]
f = [comp, [inter, A2, A3], A1]
g = [comp, A3, [union, A1, A2]]
h = [comp, R, [union, A3, [union, A1, A2]]]


# semantics
U = {1, 2, 3, 4, 5}
I = lambda X: {  # noqa
    A1: {1, 2},
    A2: {1},
    A3: set(),
}.get(X)

M1 = Model(U, I)


x = [save, [destroy, [form, A1, A2, A3], a], [c, g]]  # this isn't used

string_derivation1 = "[save, [destroy, [form, A1, A2, A3], a], [c, g]]"
diagram_derivation1 = eval(string_derivation1)
diagram1 = syn(diagram_derivation1)


# display
st.title("Venn Diagram")


fig, ax = render_venn(diagram1)


st.pyplot(fig)
plt.close(fig)
st.write("Syntax:", string_derivation1)

st.write("Universe:", M1.universe)
st.write(
    "Interpretation:",
    {
        "A1": M1.interpretation(A1),
        "A2": M1.interpretation(A2),
        "A3": M1.interpretation(A3),
    },
)
st.write(f"Result: The diagram is {sem(diagram_derivation1)(M1)} on the model")
