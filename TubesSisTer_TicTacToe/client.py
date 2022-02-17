#Import library pygame untuk mengambil fungsi yang diperlukan pada game ini
import pygame

#Import library socket karena akan menggunakan IPC socket
import socket

#Import library time untuk proses delay
import time

#Import library threading
import threading

#Membuat socket dan input IP
s = socket.socket()
host = input("Masukkan IP Server:")

#Deklarasi variabel global
port = 5005
pemainSatu = 1
warnaPemainSatu = (255, 0, 0)
pemainDua = 2
warnaPemainDua = (0, 0, 255)
bottomMsg = ""
pesan = "Menunggu Pemain Lain..."
pemainSekarang = 0
xy = (-1, -1)
allow = 0
Matriks = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

#Buat threads
def create_thread(target):
    t = threading.Thread(target = target)
    #Memulai threads
    t.start()

#Initialisasi pygame
pygame.init()

#Pembuatan ukuran screen
width = 600
height = 550
screen = pygame.display.set_mode((width, height))

#set judul
pygame.display.set_caption("Tic Tac Toe")

#Set icon
icon = pygame.image.load("tictactoe.png")
pygame.display.set_icon(icon)

#Fonts
fontbesar = pygame.font.Font('freesansbold.ttf', 64)
fontkecil = pygame.font.Font('freesansbold.ttf', 32)

#warna
warnaLatar = (255, 255, 255)
warnaJudul = (0, 0, 0)
warnaSubJudul = (0, 204, 0)
warnaGaris = (0, 0, 0)

#Fungsi untuk membuat screen (plotting) 
def buildScreen(bottomMsg, string, warnaPemain = warnaSubJudul):
    screen.fill(warnaLatar)
    #inisialisasi warna untuk tiap player
    if "Satu" in string or "satu" in string  or "1" in string:
        warnaPemain = warnaPemainSatu
    elif "Dua" in string or "dua" in string  or "2" in string:
        warnaPemain = warnaPemainDua

    #Garis vertikal
    pygame.draw.line(screen, warnaGaris, (250-2, 150), (250-2, 450), 4)
    pygame.draw.line(screen, warnaGaris, (350-2, 150), (350-2, 450), 4)
    #Garis horizontal
    pygame.draw.line(screen, warnaGaris, (150, 250-2), (450, 250-2), 4)
    pygame.draw.line(screen, warnaGaris, (150, 350-2), (450, 350-2), 4)

    #Teks yang ditampilkan
    judul = fontbesar.render("TIC TAC TOE", True, warnaJudul)
    screen.blit(judul, (100, 0))
    subJudul = fontkecil.render(str.upper(string), True, warnaPemain)
    screen.blit(subJudul, (95, 70))
    centerMessage(bottomMsg, warnaPemain)

#Fungsi untuk menampilkan pesan di bawah Matriks tic tac toe
def centerMessage(pesan, warna = warnaJudul):
    pos = (100, 480)
    if "Satu" in pesan or "satu" in pesan or "1" in pesan:
        warna = warnaPemainSatu
    elif "Dua" in pesan or "dua" in pesan  or "2" in pesan:
        warna = warnaPemainDua
    pesanRendered = fontkecil.render(pesan, True, warna)
    screen.blit(pesanRendered, pos)

#Fungsi untuk menampilkan text saat dipanggil
def printCurrent(current, pos, warna):
    r = fontbesar.render(str.upper(current), True, warna)
    screen.blit(r, pos)

#Fungsi untuk menampilkan koordinat matriks yang dipilih player
def printMatrix(Matriks):
    for i in range(3):
        #Saat row bertambah y ikut bertambah
        y = int((i + 1.75) * 100)
        for j in range(3):
            #Saat kolom bertambah x ikut bertambah
            x =  int((j + 1.75) * 100)
            current = " "
            warna = warnaJudul
            if Matriks[i][j] == pemainSatu:
                current = "X"
                warna = warnaPemainSatu
            elif Matriks[i][j] == pemainDua:
                current = "O"
                warna = warnaPemainDua
            printCurrent(current, (x, y), warna)

def validate_input(x, y):
    #Jika ukuran matriks lebih
    if x > 3 or y > 3:
        print("\nDiluar Batas, coba lagi ...\n")
        return False
    #Jika matriks sudah diisi lagi yang ingin diisikan kembali
    elif Matriks[x][y] != 0:
        print("\nSudah terisi, coba lagi...\n")
        return False
    return True

#Fungsi untuk menghandle inputan dari mouse
def handleMouseEvent(pos):
    x = pos[0]
    y = pos[1]
    global pemainSekarang
    global xy
    #Jika ukuran lebih daripada line maka inisialisasikan ulang
    if(x < 150 or x > 450 or y < 150 or y > 450):
        xy = (-1, -1)
    else:
        #Saat x bertambah, kolom berubah
        col = int(x/100 - 1.5)
        #Saat y bertambah, baris berubah
        row = int(y/100 - 1.5)
        print("({}, {})".format(row,col))
        if validate_input(row, col):
            Matriks[row][col] = pemainSekarang
            xy = (row,col)

#Memulai game tiap player
def start_player():
    global pemainSekarang
    global bottomMsg
    try:
        #Koneksi ke server dengan parameter ip dan port yang telah didefinisikan
        s.connect((host, port))
        print("Terhubung ke :", host, ":", port)
        #Menerima data dari server
        recvData = s.recv(2048 * 10)
        #Menampilkan pesan dari server
        bottomMsg = recvData.decode()
        if "1" in bottomMsg:
            pemainSekarang = 1
        else:
            pemainSekarang = 2
        #Memulai game
        start_game()
        #Menutup koneksi
        s.close()
    except socket.error as e:
        print("Koneksi Socket Error:", e) 

#Fungsi untuk menjalankan game
def start_game():
    running = True
    global pesan
    global Matriks
    global bottomMsg
    create_thread(accept_msg)
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if allow:
                    handleMouseEvent(pos)
    
        if pesan == "":
            break
        
        buildScreen(bottomMsg, pesan)                      
        printMatrix(Matriks) 
        pygame.display.update()

#Fungsi untuk menghandle pesan pada tiap percabangan yang akan ditampilkan
def accept_msg():
    global Matriks
    global pesan
    global bottomMsg
    global allow
    global xy
  
    while True:
        try: 
            recvData = s.recv(2048 * 10)
            recvDataDecode = recvData.decode()
            buildScreen(bottomMsg, recvDataDecode)

            if recvDataDecode == "Input":
                print(recvDataDecode)
                failed = 1
                allow = 1
                xy = (-1, -1)
                while failed:
                    try:
                        if xy != (-1, -1):
                            koordinat = str(xy[0])+"," + str(xy[1])
                            s.send(koordinat.encode())
                            failed = 0
                            allow = 0
                    except:
                        print("Error")

            elif recvDataDecode == "Error":
                print("Error")
            
            elif recvDataDecode == "Matriks":
                print(recvDataDecode)
                matrixRecv = s.recv(2048 * 100)
                matrixRecvDecoded = matrixRecv.decode("utf-8")
                Matriks = eval(matrixRecvDecoded)

            elif recvDataDecode == "Selesai":
                print(recvDataDecode)
                msgRecv = s.recv(2048 * 100)
                msgRecvDecoded = msgRecv.decode("utf-8")
                bottomMsg = msgRecvDecoded
                pesan = "~~~~Game Selesai~~~~"
                break
            else:
                pesan = recvDataDecode

        except KeyboardInterrupt:
            print("\nKeyboard Interrupt")
            time.sleep(1)
            break

        except:
            print("Error")
            break
    
start_player()