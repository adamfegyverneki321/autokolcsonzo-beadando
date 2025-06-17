from abc import ABC, abstractmethod
from datetime import datetime


# ======= Fő osztályok =======

class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij

    @abstractmethod
    def info(self):
        pass


class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, ajtok_szama, szin):
        super().__init__(rendszam, tipus, berleti_dij)
        self.ajtok_szama = ajtok_szama
        self.szin = szin

    def info(self):
        return f"Személyautó - {self.rendszam}, {self.tipus}, {self.berleti_dij} Ft/nap, Ajtók: {self.ajtok_szama}, Szín: {self.szin}"


class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, rakter_meret):
        super().__init__(rendszam, tipus, berleti_dij)
        self.rakter_meret = rakter_meret

    def info(self):
        return f"Teherautó - {self.rendszam}, {self.tipus}, {self.berleti_dij} Ft/nap, Raktér: {self.rakter_meret} m³"


class Berles:
    def __init__(self, auto: Auto, datum: str, berlo_nev: str):
        self.auto = auto
        self.datum = datum
        self.berlo_nev = berlo_nev

    def info(self):
        return f"{self.datum} - {self.auto.rendszam} ({self.auto.tipus}) - Bérlő: {self.berlo_nev}"


class Autokolcsonzo:
    def __init__(self, nev: str):
        self.nev = nev
        self.autok: list[Auto] = []
        self.berlesek: list[Berles] = []

    def auto_hozzaadas(self, auto: Auto):
        self.autok.append(auto)

    def get_auto_by_rendszam(self, rendszam: str):
        return next((auto for auto in self.autok if auto.rendszam == rendszam), None)

    def is_auto_berelve(self, rendszam: str, datum: str):
        return any(b.auto.rendszam == rendszam and b.datum == datum for b in self.berlesek)

    def berles_hozzaadas(self, rendszam: str, datum: str, berlo_nev: str):
        auto = self.get_auto_by_rendszam(rendszam)
        if not auto:
            print("❌ Ilyen rendszámú autó nem található.")
            return

        try:
            datum_obj = datetime.strptime(datum, "%Y-%m-%d").date()
            if datum_obj < datetime.today().date():
                print("❌ Múltbeli dátumra nem lehet bérlést rögzíteni.")
                return
        except ValueError:
            print("❌ Hibás dátumformátum. Használja: ÉÉÉÉ-HH-NN.")
            return

        if self.is_auto_berelve(rendszam, datum):
            print("❌ Ez az autó már ki van bérelve ezen a napon.")
            return

        self.berlesek.append(Berles(auto, datum, berlo_nev))
        print(f"✅ Bérlés sikeres! Ár: {auto.berleti_dij} Ft")

    def berles_lemondas(self, rendszam: str, datum: str, berlo_nev: str):
        for berles in self.berlesek:
            if (berles.auto.rendszam == rendszam and
                berles.datum == datum and
                berles.berlo_nev == berlo_nev):
                self.berlesek.remove(berles)
                print("✅ Bérlés lemondva.")
                return
        print("❌ Nem található ilyen bérlés.")

    def listaz_berlesek(self):
        if not self.berlesek:
            print("❗ Nincs aktív bérlés.")
        for b in self.berlesek:
            print(b.info())

    def listaz_autok(self):
        for auto in self.autok:
            print(auto.info())


# ======= Előkészítés =======

def rendszer_inditasa():
    kolcsonzo = Autokolcsonzo("City Rent")

    kolcsonzo.auto_hozzaadas(Szemelyauto("ABC123", "Toyota Corolla", 12000, 4, "piros"))
    kolcsonzo.auto_hozzaadas(Szemelyauto("XYZ789", "Volkswagen Golf", 10000, 5, "fekete"))
    kolcsonzo.auto_hozzaadas(Teherauto("DEF456", "Mercedes Sprinter", 15000, 12.5))

    kolcsonzo.berlesek.append(Berles(kolcsonzo.get_auto_by_rendszam("ABC123"), "2025-06-01", "Kiss Anna"))
    kolcsonzo.berlesek.append(Berles(kolcsonzo.get_auto_by_rendszam("XYZ789"), "2025-06-01", "Nagy Béla"))
    kolcsonzo.berlesek.append(Berles(kolcsonzo.get_auto_by_rendszam("DEF456"), "2025-06-02", "Tóth Gabi"))
    kolcsonzo.berlesek.append(Berles(kolcsonzo.get_auto_by_rendszam("XYZ789"), "2025-06-02", "Kovács Márk"))

    return kolcsonzo


# ======= Felhasználói interfész =======

def menu():
    kolcsonzo = rendszer_inditasa()

    while True:
        print("\n=== AUTÓKÖLCSÖNZŐ RENDSZER ===")
        print("1 - Autók listázása")
        print("2 - Autó bérlése")
        print("3 - Bérlés lemondása")
        print("4 - Bérlések listázása")
        print("0 - Kilépés")
        valasz = input("Választás: ")

        if valasz == "1":
            kolcsonzo.listaz_autok()
        elif valasz == "2":
            rendszam = input("Rendszám: ").upper()
            datum = input("Bérlés dátuma (ÉÉÉÉ-HH-NN): ")
            berlo = input("Bérlő neve: ")
            kolcsonzo.berles_hozzaadas(rendszam, datum, berlo)
        elif valasz == "3":
            rendszam = input("Rendszám: ").upper()
            datum = input("Bérlés dátuma (ÉÉÉÉ-HH-NN): ")
            berlo = input("Bérlő neve: ")
            kolcsonzo.berles_lemondas(rendszam, datum, berlo)
        elif valasz == "4":
            kolcsonzo.listaz_berlesek()
        elif valasz == "0":
            print("Kilépés...")
            break
        else:
            print("❌ Hibás választás.")


# ======= Indítás =======
if __name__ == "__main__":
    menu()
