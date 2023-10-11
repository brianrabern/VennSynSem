import matplotlib.pyplot as plt
from matplotlib.patches import Path, PathPatch
from shapely.geometry import Point, Polygon, MultiPolygon, LineString
import random

# helper function to generate destroyed patches (potentially with holes in them)
def create_destroyed_patch(region):
    
    # get coords
    exterior_destroyed = list(region.exterior.coords)
    if region.interiors:
        interior_destroyed = [list(interior.coords) for interior in region.interiors]
    else:
        interior_destroyed = []
        
    # get paths    
    exterior_path = Path(exterior_destroyed)
    interior_paths = [Path(interior) for interior in interior_destroyed]
    
    # get codes
    combined_codes = [Path.MOVETO] + [Path.LINETO] * (len(exterior_path) - 2) + [Path.CLOSEPOLY]
    combined_vertices = list(exterior_path.vertices)
    for interior_path in interior_paths:
        combined_codes += [Path.MOVETO] + [Path.LINETO] * (len(interior_path) - 2) + [Path.CLOSEPOLY]
        combined_vertices += list(interior_path.vertices)
        
    # return destroyed patch
    return PathPatch(
        Path(combined_vertices, combined_codes),
        fill=True,
        facecolor='gray',
        edgecolor='none'
    )

# helper function to place salvation indices in cells when called
def random_point(region, used_points, label_points, base_regions_coords):
        while True:
            min_x, max_x = region.bounds[0], region.bounds[2]
            min_y, max_y = region.bounds[1], region.bounds[3]
            x = random.uniform(min_x, max_x)
            y = random.uniform(min_y, max_y)
            random_point = Point(x, y)

            # buffers
            basic_padding = 0.3
            region_buffered = region.buffer(-basic_padding)
            border_padding = 1
            border_buffered = R.buffer(-border_padding)

            # check if the point is in region and not too close to other points, edges, and labels
            if random_point.within(region_buffered) and random_point.within(border_buffered):
                try:
                    used_point_distance = min(random_point.distance(used_point) for used_point in used_points)
                except ValueError:
                    used_point_distance = 0.3
                    
                regions_lines = [LineString(region_coords) for region_coords in base_regions_coords]
                line_distance = min(random_point.distance(region_line) for region_line in regions_lines)
                                    
                label_distance = min(random_point.distance(label_point) for label_point in label_points)
                
                if label_distance >= (basic_padding*2) and used_point_distance >= basic_padding and line_distance >= basic_padding:
                    return random_point

def render_venn(D):
    # create a Matplotlib figure 
    fig, ax = plt.subplots()
    
    # label the base regions
    X1 = D["base"][0]
    X2 = D["base"][1]
    X3 = D["base"][2]

    label_pos_X1 = (X1.centroid.x, X1.centroid.y+2.5)
    label_pos_X2 = (X2.centroid.x-2.5,X2.centroid.y)
    label_pos_X3 = (X3.centroid.x+2.5,X3.centroid.y)
    label_points = [Point(label_pos_X1),Point(label_pos_X2),Point(label_pos_X3)]

    # get base region coords
    base_regions_coords =[]
    for region in D["base"]:
        region_coords = list(region.exterior.coords)
        base_regions_coords.append(region_coords)
    
    # destruction rendering covering both polygons and multipolygons
    destroyed_patches = []
    for region in D["destroyed"]:
        if isinstance(region, MultiPolygon):
            for polygon in region.geoms:
                destroyed_patch = create_destroyed_patch(polygon)
                destroyed_patches.append(destroyed_patch)
        elif isinstance(region, Polygon):
            destroyed_patch = create_destroyed_patch(region)
            destroyed_patches.append(destroyed_patch)

    for destroyed_patch in destroyed_patches:
        ax.add_patch(destroyed_patch)

    # salvation rendering
    index = 1
    used_points = []
    regions = []
    
    for arr in D["saved"]:
        for region in arr:
            if region not in regions and not region.interiors:
                index_point = region.centroid
                used_points.append(index_point)
            else:
                index_point = random_point(region, used_points, label_points, base_regions_coords)
                used_points.append(index_point)
            ax.text(index_point.x, index_point.y, str(index), ha='center', va='center', fontweight='bold',fontsize=10)
            regions.append(region)
        index += 1
        
    # form rendering
    for region_coords in base_regions_coords:
        ax.add_patch(plt.Polygon(region_coords, fill=None))
     
    #labels
    ax.text(*label_pos_X1, labels[X1], ha='center', va='center', fontsize=12)
    ax.text(*label_pos_X2, labels[X2], ha='center', va='center', fontsize=12)
    ax.text(*label_pos_X3, labels[X3], ha='center', va='center', fontsize=12)

    # set the aspect ratio and axis limits so it looks right
    ax.set_aspect('equal')
    ax.set_xlim(-3, 5)
    ax.set_ylim(-2.5, 5)

    # remove graph junk, axis labels, and ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')

    # display
    plt.show()