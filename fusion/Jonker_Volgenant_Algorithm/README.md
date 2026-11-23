### Jonker-Volgenant algorithm
- `Jonker-Volgenant (LAPJV)` is an algorithm to solve linear assignment problem. It's preferred instead of Hungarian algorithm, due to following reasons- **Hungarian algorithm performs substantial matrix-wide operations and repeated searches, particularly for larger problems. (it transforms the cost matrix, while preserving the optimal solution.)**

## Algorithm
- JV uses the same underlying mathematical principle as the Hungarian algorithm, but changes how it searches for and maintains assignments.
- Instead of repeatedly transforming the entire matrix to find zeros, JV works directly with reduced costs, dual variables, and augmenting paths. Its implementation is designed to avoid unnecessary operations. There are two important phases:
- Phase 1 (Column reduction and reduction transfer)
    - Find the minimum element in each column.
    - Use these minimum values to initialize column potentials.
    - Assign columns to rows where possible.
    - Transfer reductions to improve the initial assignment.
- Phase 2 (Augmenting row reduction)
    - Identify rows that are still unassigned.
    - Search for the best column for each row.
    - If a preferred column is already occupied, explore alternatives.
    - Update potentials and reassign rows along an augmenting path.

### Differences from Hungarian algorithm
- Dual Initialization. Introduces fast column reduction, reduction transfer, and augmenting row reduction routines to establish a strong initial partial solution before path searching begins.
- Shortest Augmenting Path. Uses a specialized implementation of Dijkstra's algorithm to find minimum-cost augmenting paths to unassigned columns, achieving O(N³) worst-case time complexity while outperforming the standard Hungarian (Kuhn-Munkres) method in practice.
- Dense & Sparse Support. Adapts the data structures to handle both complete (dense) cost matrices and incomplete (sparse) graphs efficiently.
- Improvements over Hungarian algorithm
    - Avoiding unnecessary matrix operations. Traditional Hungarian implementations repeatedly adjust the cost matrix when they cannot find a complete matching. JV uses dual variables and reduced costs to perform these adjustments more selectively.
    - Better augmenting path search. JV uses shortest augmenting paths and maintains information about promising alternatives. This avoids repeatedly restarting the assignment search from scratch.
    - Native rectangular matrix handling. This is particularly useful in tracking applications. Suppose you have 100 existing tracks, 65 detections. You don't need to add 35 dummy rows just to create a square 100 × 100 matrix in a rectangular-capable implementation. JV can solve the 100 × 65 problem directly (or transpose it internally, depending on the implementation).
- **JV does not necessarily improve the theoretical worst-case complexity (still O(n^3)). Its advantage is primarily in practical execution speed and implementation efficiency. About 2x - 10x faster, for 10<= n_rows <= 1000**
- Integer vs floating point precision matters.


## Related papers
- [Original Jonker Volgenant paper - A Shortest Augmenting Path Algorithm for Dense and Sparse Linear Assignment Problems](https://link.springer.com/article/10.1007/BF02278710)
- [Linear and semi-assignment problems: A core oriented approach](https://www.sciencedirect.com/science/article/abs/pii/030505489600010X) - LAPMOD is the implementation for sparse matrices, that is much faster than the dense version


## Reference implementations
- [Public domain PASCAL implementation](http://www.assignmentproblems.com/LAPJV.htm) by A.Volgenant.
- [LAP](https://github.com/gatagat/lap) is faster compared to scipy's implementation for square matrices.
- [scipy's linear_sum_assigment implementation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html) works for 2D rectangular assignment problems, and uses variation of Jonker Volgenant algorithm. [scipy lsap cpp code](https://github.com/scipy/scipy/blob/main/scipy/optimize/rectangular_lsap/rectangular_lsap.cpp). [Paper used in scipy](https://ieeexplore.ieee.org/document/7738348)
- [C implementation of lapjv](https://github.com/yongyanghz/LAPJV-algorithm-c/tree/master)
