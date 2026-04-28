import cv2
try:
    import pygame_ce as pygame
except ImportError:
    import pygame

# --- CARA PANGGIL PALING AMAN ---
import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as mp_drawing

# Hubungkan variabel ke sistem MediaPipe
hands = mp_hands.Hands(
    max_num_hands=2, 
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
# --------------------------------

# --- 2. INISIALISASI MUSIK (PYGAME-CE) ---
pygame.mixer.init()
try:
    pygame.mixer.music.load("kicau_mania.mp3")
    print("Sistem Musik: SIAP")
except:
    print("Peringatan: File 'kicau_mania.mp3' tidak ditemukan di folder!")

# --- 3. INISIALISASI KAMERA & VIDEO ---
cap = cv2.VideoCapture(0)
cat_video = cv2.VideoCapture("cat_dance.mp4")

# Variabel Status
show_second_window = False
is_playing = False
WIN_W, WIN_H = 600, 450

print("\n--- PROGRAM KICAU MANIA AKTIF ---")
print("Tips: Gerakkan tangan ke KIRI layar untuk memutar video & musik.")
print("Tips: Gerakkan tangan ke KANAN layar untuk mematikan.")
print("Tekan 'q' pada keyboard untuk keluar.")

while True:
    success, img = cap.read()
    if not success:
        print("Gagal mengakses kamera.")
        break

    # Balik gambar agar seperti cermin dan resize
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (WIN_W, WIN_H))

    # Konversi warna untuk MediaPipe
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Logika Deteksi Tangan
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Gambar garis tangan (Perbaikan nama variabel mp_drawing)
            mp_drawing.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            
            # Ambil koordinat ujung jari telunjuk (Landmark nomor 8)
            x_pos = handLms.landmark[8].x 
            
            # JIKA TANGAN DI KIRI (x < 0.3) -> AKTIFKAN KUCING & MUSIK
            if x_pos < 0.3 and not show_second_window: 
                show_second_window = True
                if not is_playing:
                    try:
                        pygame.mixer.music.play(-1) # -1 artinya loop terus
                        is_playing = True
                    except:
                        pass
                    
            # JIKA TANGAN DI KANAN (x > 0.7) -> MATIKAN
            if x_pos > 0.7 and show_second_window: 
                show_second_window = False
                pygame.mixer.music.stop()
                is_playing = False

    # Tampilkan Kamera Utama
    cv2.imshow("Face Cam - Kicau Mania", img)
    cv2.moveWindow("Face Cam - Kicau Mania", 50, 150)

    # Logika Jendela Kedua (Kucing Joget)
    if show_second_window:
        ret_cat, cat_frame = cat_video.read()
        if not ret_cat:
            # Jika video habis, ulangi dari awal (loop)
            cat_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret_cat, cat_frame = cat_video.read()
        
        if ret_cat:
            cat_frame = cv2.resize(cat_frame, (WIN_W, WIN_H))
            cv2.imshow("Kucing Joget", cat_frame)
            cv2.moveWindow("Kucing Joget", 50 + WIN_W + 10, 150)
    else:
        # Tutup jendela kucing jika statusnya False
        try:
            if cv2.getWindowProperty("Kucing Joget", cv2.WND_PROP_VISIBLE) >= 1:
                cv2.destroyWindow("Kucing Joget")
        except:
            pass

    # Tombol keluar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bersihkan Memori
cap.release()
cat_video.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()
print("Program ditutup. Sampai jumpa, Bu Nur!")