#Import library socket karena akan menggunakan IPC socket
import socket

#Import library time untuk proses delay
import time

#Membuat socket dan deklarasi variabel global
s = socket.socket()
host = "localhost"
port = 5005
matriks = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

pemainSatu = 1
pemainDua = 2

pemainConn = list()
pemainAddr = list()

#Fungsi untuk handle input dari pemain
def get_input(pemainSekarang):
    #Untuk pemain 1
    if pemainSekarang == pemainSatu:
        pemain = "Giliran Pemain Satu"
        conn = pemainConn[0]
    else:
    #Untuk pemain 2
        pemain = "Giliran Pemain Dua"
        conn = pemainConn[1]
    print(pemain) #Menampilkan pemain yang ikut bermain
    send_common_msg(pemain)
    try:
        #Mengirim kembali data yang diterima dari server ke client
        conn.send("Input".encode())
        data = conn.recv(2048 * 10)
        conn.settimeout(200)
        dataDecoded = data.decode().split(",")
        x = int(dataDecoded[0])
        y = int(dataDecoded[1])
        matriks[x][y] = pemainSekarang
        send_common_msg("Matriks")
        send_common_msg(str(matriks))
    except:
        conn.send("Error".encode())
        print("Error!")

#Fungsi untuk mengecek apakah baris berisi karakter yang sama atau tidak
def check_rows():
    result = 0
    for i in range(3):
        if matriks[i][0] == matriks[i][1] and matriks[i][1] == matriks[i][2]:
            result = matriks[i][0]
            if result != 0:
                break
    return result

#Fungsi untuk mengecek apakah kolom berisi karakter yang sama atau tidak
def check_columns():
    result = 0
    for i in range(3):
        if matriks[0][i] == matriks[1][i] and matriks[1][i] == matriks[2][i]:
            result = matriks[0][i]
            if result != 0:
                break
    return result

#Fungsi untuk mengecek apakah diagonal berisi karakter yang sama atau tidak
def check_diagonals():
    result = 0
    if matriks[0][0] == matriks[1][1] and matriks[1][1] == matriks[2][2]:
        result = matriks[0][0]
    elif matriks[0][2] == matriks[1][1] and matriks[1][1] == matriks[2][0]:
        result = matriks[0][2]
    return result

#Fungsi untuk mengecek pemenang
def check_winner():
    result = 0
    result = check_rows()
    if result == 0:
        result = check_columns()
    if result == 0:
        result = check_diagonals()
    return result

#Socket program
def start_server():
    #Binding ke port
    #Menunggu dua client yang terhubung (s.listen(2))
    try:
        s.bind((host, port))
        print("Tic Tac Toe server \nBinding menuju port", port)
        s.listen(2)
        accept_players()
    except socket.error as e:
        print("Server binding error:", e)

def accept_players():
    try:
        for i in range(2):
            #Menerima koneksi
            conn, addr = s.accept()
            #Menampilkan message
            msg = "<<< Kamu Pemain {} >>>".format(i+1)
            conn.send(msg.encode())

            pemainConn.append(conn)
            pemainAddr.append(addr)
            print("Pemain {} - [{}:{}]".format(i+1, addr[0], str(addr[1])))

        start_game()
        s.close()
    except socket.error as e:
        print("Koneksi pemain error", e)
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt")
        exit()
    except Exception as e:
        print("Error :", e)

#Fungsi untuk memulai game
def start_game():
    result = 0
    i = 0
    while result == 0 and i < 9 :
        if (i%2 == 0):
            get_input(pemainSatu)
        else:
            get_input(pemainDua)
        result = check_winner()
        i = i + 1
    
    #Send message "Selesai"
    send_common_msg("Selesai")

    #Send message hasil game
    if result == 1:
        lastmsg = "Pemain satu menang !!!"
    elif result == 2:
        lastmsg = "Pemain dua menang !!!"
    else:
        lastmsg = "Permainan berakhir seri"
    send_common_msg(lastmsg)
    time.sleep(10)
    #Menutup koneksi
    for conn in pemainConn:
        conn.close()

#Fungsi untuk mengirimkan pesan
def send_common_msg(text):
    pemainConn[0].send(text.encode())
    pemainConn[1].send(text.encode())
    time.sleep(1)

#Memulai server
start_server()