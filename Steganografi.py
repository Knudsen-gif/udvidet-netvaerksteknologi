from PIL import Image

def skjul_tekst(input_fil, tekst, output_fil):
    billede = Image.open(input_fil).convert("RGB")
    pixels = list(billede.getdata())
    
    # Konverter tekst til bits
    data = tekst.encode("utf-8")
    bits = ''.join(format(byte, '08b') for byte in data)
    
    # Gem beskedens længde som 32 bits
    længde = format(len(data), '032b')
    bits = længde + bits
    
    if len(bits) > len(pixels) * 3:
        raise ValueError("Beskeden er for lang til billedet!")
        
    nye_pixels = []
    bit_index = 0
    for pixel in pixels:
        nye_farver = []
        for farve in pixel:
            if bit_index < len(bits):
                # Erstat farvens mindst betydende bit
                farve = (farve & 254) | int(bits[bit_index])
                bit_index += 1
            nye_farver.append(farve)
        nye_pixels.append(tuple(nye_farver))
        
    billede.putdata(nye_pixels)
    billede.save(output_fil, "PNG")
    print("Beskeden er skjult i billedet!")

def hent_tekst(input_fil):
    billede = Image.open(input_fil).convert("RGB")
    # Hent alle pixels
    pixels = list(billede.getdata())
    
    # Udtræk mindst betydende bit fra farveværdierne
    bits = ''.join(
        str(farve & 1)
        for pixel in pixels
        for farve in pixel
    )
    
    # Læs beskedens længde (32 bits)
    længde = int(bits[:32], 2)
    
    # Hent beskedens bits
    besked_bits = bits[32:32 + længde * 8]
    
    # Konverter bits til bytes og derefter tekst
    data = bytes(
        int(besked_bits[i:i + 8], 2)
        for i in range(0, len(besked_bits), 8)
    )
    return data.decode("utf-8")

# --- 1. PASSWORD TJEK ---
korrekt_password = "0000"

indtastet_kode = input("Indtast password for at køre steganografi: ")

if indtastet_kode != korrekt_password:
    print("Forkert password! Programmet lukker.")
    exit()

print("Kode godkendt!")

# --- 2. SKRIV BESKED ---
hemmelig_besked = input("Skriv den besked du vil skjule i billedet: ")

# --- 3. GEM OG HENT ---
skjul_tekst(
    "billede.png",
    hemmelig_besked,
    "skjult.png"
)

besked = hent_tekst("skjult.png")
print("Skjult besked fundet:", besked)