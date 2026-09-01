"""Experiment 9 — Hierarchical clustering and dendrograms.

Reproduces Unit 5 section 5.4's worked dendrogram and Practice Problem 2
exactly, and shows how single and complete linkage differ on the same matrix.
"""
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from scipy.spatial.distance import squareform


def merge_heights(matrix, method):
    """Return the merge heights in order, from a square distance matrix."""
    Z = linkage(squareform(np.array(matrix, dtype=float), checks=False), method=method)
    return Z, [round(float(h), 4) for h in Z[:, 2]]


def unit5_worked_dendrogram():
    """Section 5.4: five points A-E, single linkage, merges at 2, 3, 4, 5."""
    labels = list("ABCDE")
    D = [[0,  2,  6, 10,  9],
         [2,  0,  5,  9,  8],
         [6,  5,  0,  4,  5],
         [10, 9,  4,  0,  3],
         [9,  8,  5,  3,  0]]

    Z, heights = merge_heights(D, "single")
    assert heights == [2.0, 3.0, 4.0, 5.0], heights

    # Cutting at 4.5 must give exactly {A,B} and {C,D,E}.
    groups = fcluster(Z, t=4.5, criterion="distance")
    clusters = sorted(sorted(labels[i] for i in range(5) if groups[i] == g)
                      for g in set(groups))
    assert clusters == [["A", "B"], ["C", "D", "E"]], clusters

    # Cutting at 3.5 gives three.
    g3 = fcluster(Z, t=3.5, criterion="distance")
    c3 = sorted(sorted(labels[i] for i in range(5) if g3[i] == g) for g in set(g3))
    assert c3 == [["A", "B"], ["C"], ["D", "E"]], c3

    # Complete linkage: SAME merge order here, but LARGER heights, because it
    # always reports the farthest pair.
    _, comp = merge_heights(D, "complete")
    assert comp == [2.0, 3.0, 5.0, 10.0], comp
    assert all(c >= s for c, s in zip(comp, heights)), \
        "complete linkage heights are never below single linkage heights"

    print(f"  5.4: single-linkage merges at {heights}; cut at 4.5 -> {clusters}")
    print(f"       complete linkage on the same matrix: {comp}")


def unit5_practice_2():
    """Practice Problem 2: P1-P5, single linkage, merges at 2, 3, 5, 6."""
    labels = ["P1", "P2", "P3", "P4", "P5"]
    D = [[0,  9,  3,  6, 11],
         [9,  0,  7,  5, 10],
         [3,  7,  0,  9,  2],
         [6,  5,  9,  0,  8],
         [11, 10, 2,  8,  0]]

    Z, heights = merge_heights(D, "single")
    assert heights == [2.0, 3.0, 5.0, 6.0], heights

    # Cut just above 5 -> two clusters.
    g = fcluster(Z, t=5.5, criterion="distance")
    clusters = sorted(sorted(labels[i] for i in range(5) if g[i] == c) for c in set(g))
    assert clusters == [["P1", "P3", "P5"], ["P2", "P4"]], clusters

    # Cut just below 5 -> three, as the notes point out for the tie.
    g2 = fcluster(Z, t=4.5, criterion="distance")
    c2 = sorted(sorted(labels[i] for i in range(5) if g2[i] == c) for c in set(g2))
    assert c2 == [["P1", "P3", "P5"], ["P2"], ["P4"]], c2

    print(f"  Practice 2: merges at {heights}; cut above 5 -> {clusters}")
    print(f"       cut below 5 -> {c2} (the notes flag this tie)")


def linkage_changes_the_answer():
    """Section 5.4: single linkage CHAINS; complete linkage does not.

    Two compact blobs joined by a thin bridge of points. Single linkage follows
    the bridge and merges them; complete linkage refuses.
    """
    left = np.array([[0.0, 0.0], [0.4, 0.2], [0.2, 0.5], [0.5, 0.5]])
    right = np.array([[6.0, 0.0], [6.4, 0.2], [6.2, 0.5], [6.5, 0.5]])
    bridge = np.array([[1.5, 0.25], [3.0, 0.25], [4.5, 0.25]])
    X = np.vstack([left, bridge, right])

    def two_clusters(method):
        Z = linkage(X, method=method)
        g = fcluster(Z, t=2, criterion="maxclust")
        return sorted(int((g == c).sum()) for c in set(g))

    single = two_clusters("single")
    complete = two_clusters("complete")

    assert single != complete, "the two linkages must disagree on this data"
    print(f"  chaining: single linkage splits {single}, "
          f"complete linkage splits {complete}")
    print(f"       same data, same k -- the LINKAGE decides the answer")


def main():
    print("Experiment 9 -- Hierarchical clustering")
    unit5_worked_dendrogram()
    unit5_practice_2()
    linkage_changes_the_answer()
    print("  all Unit 5 hierarchical calculations reproduced")


if __name__ == "__main__":
    main()
