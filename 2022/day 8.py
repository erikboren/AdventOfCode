with open("day8 data.in") as file:
    trees = file.readlines()

ymax = len(trees)-1
xmax = len(trees[0].strip())-1

edge_visible = 0
interior_visible = 0
maxview_score = 0
for idx1,treeline in enumerate(trees):
    treeline = treeline.strip()
    for idx2, tree in enumerate(treeline):
        ycoord = idx1
        xcoord = idx2

        if xcoord in [0,xmax] or ycoord in [0,ymax]:
            edge_visible +=1
            # If on the edge
        else:
            east_trees = [*treeline[xcoord+1:]]
            west_trees = [*treeline[:xcoord]]
            
            east = max(east_trees) #Largest east of tree
            west = max(west_trees)  #Largest west of tree
            
            north_trees = []
            south_trees = []
            
            for treelineY in trees[:ycoord]:
                north_trees.append(treelineY[xcoord])

            for treelineY in trees[ycoord+1:]:
                south_trees.append(treelineY[xcoord])
            
            north_trees=north_trees[::-1]
            west_trees = west_trees[::-1]


            north = max(north_trees)
            south = max(south_trees)

            maxtrees = [north, south, east, west]


            treelines = [north_trees,south_trees, west_trees, east_trees]
            tree_score=[0,0,0,0]

            for idxtd,tree_direction in enumerate(treelines):
                for idxtd2, tree_comp in enumerate(tree_direction):
                    tree_score[idxtd] +=1
                    if tree_comp >= tree:
                        break
                        
            view_score = tree_score[0] * tree_score[1] * tree_score[2] * tree_score[3]
            if view_score > maxview_score:
                maxview_score = view_score


            if(int(tree) >  int(min(maxtrees))):
                interior_visible += 1
                

print(edge_visible,interior_visible, edge_visible + interior_visible)
print(maxview_score)
