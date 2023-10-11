from shapely.geometry import Polygon
from core.regions import R
import copy


# form rule
def form(X1, X2, X3):
    D = {"base": [X1, X2, X3], "destroyed": [], "saved": []}
    return D


# set operation rules
def inter(X1, X2):
    return X1.intersection(X2)


def union(X1, X2):
    return X1.union(X2)


def comp(X1, X2):
    return X1.difference(X2)


# destruction rule
def destroy(D, X):
    D_prime = copy.deepcopy(D)
    D_prime["destroyed"].append(X)
    return D_prime


# salvation rule
def save(D, cell_array):
    D_prime = copy.deepcopy(D)
    D_prime["saved"].append(cell_array)
    return D_prime


# powerset helper function
def powerset(s):
    if not s:
        return [set()]
    subsets = powerset(s[:-1])
    item = s[-1]
    return subsets + [subset.union({item}) for subset in subsets]


# the mutual overlap constaint
def mutual_overlap_constraint(basic_regions, background):
    for subset in powerset(basic_regions):
        # sets for regions in subset and not in subset
        subset_regions = subset | {background}
        remaining_regions = set(basic_regions) - subset

        # initialize result
        result = None

        # in
        for region in subset_regions:
            reg_poly = Polygon(list(region.exterior.coords))
            if result is None:
                result = reg_poly
            else:
                result = result.intersection(reg_poly)

        # out
        for region in remaining_regions:
            reg_poly = Polygon(list(region.exterior.coords))
            if result is not None:
                result = result.difference(reg_poly)

        # check if result is non-empty
        if result.is_empty:
            return False

    return True


# structures encoding the syntactic derivations regions and diagrams
def is_wellformed_region(input):
    if isinstance(input, Polygon):
        return True
    elif isinstance(input, list) and len(input) == 3:
        return all(
            isinstance(child, Polygon) or is_wellformed_region(child)
            for child in input[1:]
        )
    return False


def is_wellformed_diagram(input):
    if not isinstance(input, list) or not (3 <= len(input) <= 4):
        return False

    if input[0] == form:
        all_basic = all(isinstance(child, Polygon) for child in input[1:])
        mutual_overlap = mutual_overlap_constraint(input[1:], R)
        if not all_basic:
            return False
        if not mutual_overlap:
            return False
    elif input[0] == destroy:
        if not is_wellformed_diagram(input[1]):
            return False
        if not is_wellformed_region(input[2]):
            return False
    elif input[0] == save:
        if not is_wellformed_diagram(input[1]):
            return False
        for reg in input[2]:
            if not is_wellformed_region(
                reg
            ):  # strictly need further restriction to cells
                return False
    else:
        return False

    return True


def syn(tree):
    # check if tree is a terminal node
    if isinstance(tree, Polygon):
        return tree
    # else if non-terminal node
    elif isinstance(tree, list) and tree[0] in [inter, union, comp]:
        result = tree[0](syn(tree[1]), syn(tree[2]))
        return result
    elif isinstance(tree, list) and tree[0] == form:
        result = tree[0](syn(tree[1]), syn(tree[2]), syn(tree[3]))
        return result
    elif isinstance(tree, list) and tree[0] == destroy:
        result = tree[0](syn(tree[1]), syn(tree[2]))
        return result
    elif isinstance(tree, list) and tree[0] == save:
        reg_array = []
        for reg_der in tree[2]:
            reg = syn(reg_der)
            reg_array.append(reg)
        result = tree[0](syn(tree[1]), reg_array)
        # result = tree[0](*[syn(child) for child in tree[1:]])
        return result

    # else invalid tree
    else:
        return None


# helper function for topological equivelance
def topo_equivalance(region_list1, region_list2):
    # check if the sets have the same number of elements
    S1 = set(region_list1)
    S2 = set(region_list2)

    if len(S1) != len(S2):
        return False

    # check if each Polygon in S1 has an equal counterpart in S2
    for polygon1 in S1:
        found_match = False
        for polygon2 in S2:
            if polygon1.equals(polygon2):
                found_match = True
                break
        if not found_match:
            return False

    return True


# check two diagrams for equivelance
def diagrams_equal(diagram1, diagram2):
    bases_equal = topo_equivalance(diagram1["base"], diagram2["base"])
    destroys_equal = topo_equivalance(
        diagram1["destroyed"], diagram2["destroyed"]
    )  # noqa
    saves_equal = topo_equivalance(diagram1["saved"], diagram2["saved"])

    if bases_equal and destroys_equal and saves_equal:
        return True

    else:
        return False
