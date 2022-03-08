Robert Fabbro, 1001724536
Programming Language: Python3, Have not tested on OMEGA

Structure:
Code is commented.
File is read and a dictionary of routes are created e.g. hamburg bremen 116 for tree traversal.
Then traversal happens based on start node and end node in ucs_search.
I modified UCS search to put the check if children nodes are in closed and made the appropriate changes.

Definitions:
read_file
read_heuristic
create_node
binary_search
add_to_fringe
expand_node
ucs_search

Run:
python3 find_route input1.txt Bremen Kassel
python3 find_route input1.txt Bremen Kassel h_kassel.txt

