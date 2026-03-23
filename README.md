# Routing-Algorithms
COMP3221 Assigntment 1

For a more complex graph e.g.
### Node A
1
B 1 6200

### Node B
3
A 1 6100
C 3 6300
D 3 6400

### Node C
2
B 3 6200
D 1 6400

I assume that a node will only send an update packet if a direct neighbour from that nodes self.graph has been changed not when other nodes send in their own edges. For example A will not know about edge C - D because when the update packets are sent to B. Edges coming out of B have not been changed so no update packet is sent to A even though B knows about the whole graph. This follows "the output must exactly reflect the current configuration of immediate neighbours with no additional text". So i thought it makes sense to also only send update packets if immediate neighbours have been changed
