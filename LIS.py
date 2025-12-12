# Longest Increasing Subsequence (LIS)



#  SEGMENT TREE 
class SegmentTree:
    def __init__(self, n):
        # Cari ukuran tree (power of two)
        self.N = 1
        while self.N < n:
            self.N *= 2

        # Setiap node menyimpan: (panjang_LIS, index_dalam_array_asli)
        self.tree = [(0, -1)] * (2 * self.N)

    # Update posisi p dengan nilai v (v = (length, index))
    def update(self, p, v):
        p += self.N  # geser ke posisi leaf

        # Hanya update jika LIS baru lebih besar dari yang tersimpan
        if v[0] > self.tree[p][0]:
            self.tree[p] = v

        p //= 2
        # Update node parent sampai root
        while p >= 1:
            # pilih anak yang punya LIS lebih panjang
            self.tree[p] = max(self.tree[2*p], self.tree[2*p+1], key=lambda x: x[0])
            p //= 2

    # Query maksimal LIS pada range [l, r]
    def query(self, l, r):
        l += self.N
        r += self.N
        res = (0, -1)  # default: belum ada LIS

        while l <= r:
            # jika l adalah right-child (odd), proses dia lalu pindah ke kanan
            if l % 2 == 1:
                res = max(res, self.tree[l], key=lambda x: x[0])
                l += 1

            # jika r adalah left-child (even), proses dia lalu pindah ke kiri
            if r % 2 == 0:
                res = max(res, self.tree[r], key=lambda x: x[0])
                r -= 1

            # naik ke parent
            l //= 2
            r //= 2

        return res


# LIS + SEQUENCE 
def lis_with_sequence(arr):

    #  Step 1: Coordinate compression 
    # Membuat nilai array menjadi index kecil (urut unik)
    sorted_unique = sorted(set(arr))
    comp = {v: i for i, v in enumerate(sorted_unique)}

    # Buat segment tree sebesar jumlah nilai unik
    seg = SegmentTree(len(sorted_unique))

    n = len(arr)

    # parent[i] menyimpan index sebelum elemen i dalam LIS
    parent = [-1] * n

    best_len = 0     # panjang LIS terbaik
    best_end = -1    # index akhir LIS terbaik

    # Step 2: Proses setiap elemen 
    for i, x in enumerate(arr):
        cx = comp[x]     # index setelah compression

        # Query: cari LIS terbaik untuk semua nilai yang lebih kecil dari x
        if cx > 0:
            prev_len, prev_index = seg.query(0, cx - 1)
        else:
            prev_len, prev_index = (0, -1)

        # LIS akhir = LIS sebelumnya + 1
        curr_len = prev_len + 1

        # Simpan parent untuk rekonstruksi
        parent[i] = prev_index

        # Update segment tree pada posisi cx
        seg.update(cx, (curr_len, i))

        # Track LIS terbaik
        if curr_len > best_len:
            best_len = curr_len
            best_end = i

    # Step 3: Rekonstruksi Subsequence 
    lis = []
    idx = best_end

    while idx != -1:
        lis.append(arr[idx])
        idx = parent[idx]

    lis.reverse()  # karena kita rekonstruksi dari belakang

    return best_len, lis


# contoh
arr = [4, 1, 13, 7, 0, 2, 8, 11, 3]

# Jalankan LIS
length, sequence = lis_with_sequence(arr)

# Cetak hasil
print("Input:", arr)
print("LIS length:", length)
print("LIS sequence:", sequence)
