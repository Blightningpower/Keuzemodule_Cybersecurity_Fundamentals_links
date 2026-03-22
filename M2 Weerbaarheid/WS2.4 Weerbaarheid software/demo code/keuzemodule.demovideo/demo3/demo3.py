import threading
import time

saldo = 100

def koop(product_prijs):
    global saldo
    if saldo >= product_prijs:
        oud = saldo
        time.sleep(0.1)   # vertraging om race condition zichtbaar te maken
        saldo = oud - product_prijs
        print(f"Aankoop gelukt, nieuw saldo: {saldo}")
    else:
        print("Niet genoeg saldo")

t1 = threading.Thread(target=koop, args=(80,))
t2 = threading.Thread(target=koop, args=(80,))

t1.start()
t2.start()

t1.join()
t2.join()

print("Eindsaldo:", saldo)


# veilige versie met lock
# lock = threading.Lock()

# def koop(product_prijs):
#     global saldo
#     with lock:
#         if saldo >= product_prijs:
#             oud = saldo
#             time.sleep(0.1)
#             saldo = oud - product_prijs
#             print(f"Aankoop gelukt, nieuw saldo: {saldo}")
#         else:
#             print("Niet genoeg saldo")