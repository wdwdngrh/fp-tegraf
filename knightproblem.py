import sys

# Ukuran papan catur 8x8
N = 8

# Definisi 8 kemungkinan gerakan kuda (x, y)
gerakan_kuda = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

def cetak_papan(papan):
    """Mencetak matriks papan ke layar"""
    print("\n--- Solusi Papan Catur ---")
    for baris in papan:
        print(' '.join(f'{x:2d}' for x in baris))
    print("-" * 30)

def is_valid(x, y, papan):
    """Cek apakah langkah ada di dalam papan dan belum dikunjungi"""
    return 0 <= x < N and 0 <= y < N and papan[y][x] == -1

def hitung_degree(x, y, papan):
    """
    Heuristik (Warnsdorff's Rule):
    Menghitung berapa banyak langkah valid selanjutnya dari posisi (x, y).
    Tujuannya agar kita tidak menemui jalan buntu terlalu cepat.
    """
    count = 0
    for dx, dy in gerakan_kuda:
        if is_valid(x + dx, y + dy, papan):
            count += 1
    return count

def selesaikan_tour(x, y, langkah_ke, papan):
    """Fungsi rekursif (Backtracking)"""
    # Base Case: Jika langkah mencapai 64 (N*N), berarti selesai
    if langkah_ke == N * N:
        return True

    # Cari semua langkah yang mungkin dari posisi sekarang
    langkah_berikutnya = []
    for dx, dy in gerakan_kuda:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, papan):
            # Simpan langkah beserta 'degree'-nya untuk optimasi
            degree = hitung_degree(nx, ny, papan)
            langkah_berikutnya.append((degree, nx, ny))

    # Urutkan langkah berdasarkan degree terkecil (Optimasi Graf)
    langkah_berikutnya.sort(key=lambda item: item[0])

    # Coba langkah satu per satu
    for _, nx, ny in langkah_berikutnya:
        papan[ny][nx] = langkah_ke  # Tandai langkah
        
        # Rekursi ke langkah selanjutnya
        if selesaikan_tour(nx, ny, langkah_ke + 1, papan):
            return True
        
        papan[ny][nx] = -1  # Backtracking (hapus tanda jika gagal)

    return False

def cek_closed_tour(start_x, start_y, end_x, end_y):
    """Cek apakah posisi terakhir bisa menyerang posisi awal (Membentuk Cycle)"""
    for dx, dy in gerakan_kuda:
        if end_x + dx == start_x and end_y + dy == start_y:
            return True
    return False

def main():
    # Inisialisasi papan dengan -1 (artinya belum dikunjungi)
    papan = [[-1 for _ in range(N)] for _ in range(N)]

    print("=== THE KNIGHT'S TOUR (Teori Graf) ===")
    try:
        start_x = int(input("Masukkan Posisi Awal X (0-7): "))
        start_y = int(input("Masukkan Posisi Awal Y (0-7): "))
    except ValueError:
        print("Input harus angka!")
        return

    if not (0 <= start_x < N and 0 <= start_y < N):
        print("Error: Koordinat harus 0-7")
        return

    # Langkah pertama (0)
    papan[start_y][start_x] = 0

    # Jalankan algoritma
    if selesaikan_tour(start_x, start_y, 1, papan):
        cetak_papan(papan)
        
        # Cari posisi langkah terakhir (63)
        last_x, last_y = -1, -1
        for y in range(N):
            for x in range(N):
                if papan[y][x] == 63:
                    last_x, last_y = x, y
        
        print(f"Mulai: ({start_x}, {start_y}) -> Akhir: ({last_x}, {last_y})")
        
        if cek_closed_tour(start_x, start_y, last_x, last_y):
            print("Status: CLOSED TOUR (Membentuk Sirkuit/Cycle Graf)")
        else:
            print("Status: OPEN TOUR (Lintasan Hamiltonian)")
    else:
        print("Solusi tidak ditemukan!")

if __name__ == "__main__":
    main()
