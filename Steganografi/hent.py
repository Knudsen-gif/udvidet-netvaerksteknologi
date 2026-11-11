import os
from PIL import Image

# Find mappen, hvor Python-filen ligger
mappe = os.path.dirname(os.path.abspath(__file__))
billed_fil = os.path.join(mappe, "skjult.png")


def hent_tekst(input_fil):
    billede = Image.open(input_fil).convert("RGB")
    pixels = list(billede.getdata())

    # Udtræk bits fra billedet
    bits = ''.join(
        str(farve & 1)
        for pixel in pixels
        for farve in pixel
    )

    # Kontroller billedets størrelse
    if len(bits) < 32:
        print("Billedet er for lille.")
        return None

    # Læs beskedens længde
    længde = int(bits[:32], 2)

    # Kontroller beskedens længde
    if 32 + længde * 8 > len(bits):
        print("Ingen gyldig besked fundet.")
        return None

    # Udtræk beskedens bits
    besked_bits = bits[32:32 + længde * 8]

    # Konverter bits til bytes
    data = bytes(
        int(besked_bits[i:i + 8], 2)
        for i in range(0, len(besked_bits), 8)
    )

    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        print("Kunne ikke finde en gyldig besked.")
        return None


# --- 1. PASSWORD TJEK ---
korrekt_password = "0000"

indtastet_kode = input(
    "Indtast password for at dekode billedet: "
)

if indtastet_kode != korrekt_password:
    print("Forkert password! Programmet lukker.")
    exit()

print("Kode godkendt!")


# --- 2. FIND SKJULT BESKED ---
print("\n--- STEGANOGRAFI DEKODER ---")

try:
    besked = hent_tekst(billed_fil)

    if besked:
        print("\nSkjult besked fundet:")
        print(besked)
    else:
        print("\nIngen besked fundet.")

except FileNotFoundError:
    print("Filen skjult.png blev ikke fundet.")

except Exception as e:
    print("Der opstod en fejl:", e)

    