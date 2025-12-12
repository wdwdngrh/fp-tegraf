# Longest Increasing Subsequence using Segment Tree + Reconstruction

class SegmentTree:
    def __init__(self, n):
        self.N = 1
        while self.N < n:
            self.N *= 2
        # menyimpan pasangan (panjang LIS, index)
        self.tree = [(0, -1)] * (2 * self.N)

    # update posisi p dengan value v (v = (length, index))
    def update(self, p, v):
        p += self.N
        if v[0] > self.tree[p][0]:
            self.tree[p] = v
        p //= 2
        while p >= 1:
            self.tree[p] = max(self.tree[2*p], self.tree[2*p+1], key=lambda x: x[0])
            p //= 2

    # query [l, r] mencari yang LIS-nya terbesar
    def query(self, l, r):
        l += self.N
        r += self.N
        res = (0, -1)
        while l <= r:
            if l % 2 == 1:
                res = max(res, self.tree[l], key=lambda x: x[0])
                l += 1
            if r % 2 == 0:
                res = max(res, self.tree[r], key=lambda x: x[0])
                r -= 1
            l //= 2
            r //= 2
        return res


def lis_with_sequence(arr):
    # coordinate compression
    sorted_unique = sorted(set(arr))
    comp = {v: i for i, v in enumerate(sorted_unique)}

    n = len(arr)
    seg = SegmentTree(len(sorted_unique))

    # menyimpan predecessor
    parent = [-1] * n
    best_len = 0
    best_end = -1

    for i, x in enumerate(arr):
        cx = comp[x]

        # query semua nilai yang lebih kecil
        prev_len, prev_index = seg.query(0, cx - 1) if cx > 0 else (0, -1)

        curr_len = prev_len + 1
        parent[i] = prev_index  # link ke predecessor

        # update segment tree
        seg.update(cx, (curr_len, i))

        # update best global
        if curr_len > best_len:
            best_len = curr_len
            best_end = i

    # Rekonstruksi LIS
    lis = []
    idx = best_end
    while idx != -1:
        lis.append(arr[idx])
        idx = parent[idx]
    lis.reverse()

    return best_len, lis



# ---- Test ----
arr = [4, 1, 13, 7, 0, 2, 8, 11, 3]
length, sequence = lis_with_sequence(arr)

print("Input:", arr)
print("LIS length:", length)
print("LIS sequence:", sequence)
