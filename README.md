# The Formal Syntax and Semantics of Venn Diagrams

This project is a Python-based implementation of the formal syntax and semantics of Venn diagrams. It provides a mathematically precise framework for deriving, manipulating, visualizing, and evaluating Venn diagrams. In particular we will provide a framework  whereby the following hold:  
- Each Venn Diagram will be specified by a finite number of applications of a finite number of syntactic rules to an enumerable vocabulary. 
- The syntactic derivation of a Venn Diagram will be specified in a parse tree on analogy with the syntactic derivation of a formula of a natural or formal language.
- The truth conditions of a Venn Diagram will be compositionally specified in terms of its syntactic derivation. 

In his 1880 article "On the Diagrammatic and Mechanical Representation of Propositions and Reasonings", John Venn introduced a scheme of diagrammatic representation which he took to be an improvement over traditional Eulerian circles--the basic system of representation was further developed in a textbook (Venn 1894). Paradigmatically, a Venn Diagram is given by a set of overlapping basic regions. The basic regions represent sets in a domain. The intersection, union, or relative complement of regions in a diagram represent the intersection, union, or relative complement of the sets in the domain represented by these regions. 

In order to represent regions and points, and various operations on them, we will leverage the Shapely library for geometric operations. And to render the diagrams we will use Matplotlib for the visualization.
