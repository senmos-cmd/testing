import struct, datetime

def saberi_polja(polje1, polje2):
    """Sabere dve liste brojeva element po element."""
    return [a + b for a, b in zip(polje1, polje2)]

polje1 = [1, 2, 3]
polje2 = [4, 5, 6]
rezultat = saberi_polja(polje1, polje2)
print("Rezultat sabiranja polja:", rezultat)