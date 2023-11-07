import numpy as np
import matplotlib.pyplot as plt


class Skala:

    kwota_wolna_od_podatku = 30_000
    prog = 120_000
    pod_progiem = 0.12
    nad_progiem = 0.32

    @staticmethod
    def podatek(dochod_mies):
        roczny_dochod = dochod_mies * 12
        if roczny_dochod <= Skala.kwota_wolna_od_podatku:
            return 0
        elif Skala.kwota_wolna_od_podatku < roczny_dochod <= Skala.prog:
            return (dochod_mies - Skala.kwota_wolna_od_podatku/12) * Skala.pod_progiem
        elif Skala.prog < roczny_dochod:
            return (Skala.prog - Skala.kwota_wolna_od_podatku)/12 * Skala.pod_progiem + (dochod_mies - Skala.prog/12) * Skala.nad_progiem
    
    @staticmethod
    def skladka_zdrowotna(dochod_mies):
        return 0.09 * dochod_mies
    


class Liniowy:

    @staticmethod
    def podatek(dochod_mies):
        return dochod_mies * 0.19
    
    @staticmethod
    def skladka_zdrowotna(dochod_mies):
        return 0.049 * dochod_mies



class Ryczalt:

    @staticmethod
    def podatek(przychod_mies, proc):
        return przychod_mies * proc
    
    @staticmethod
    def skladka_zdrowotna(przychod_mies, przecietne_wynagrodzenie_miesieczne_gus):
        proc = 0.09
        roczny_przychod = przychod_mies * 12
        if roczny_przychod <= 60_000:
            return proc * 0.6 * przecietne_wynagrodzenie_miesieczne_gus
        elif roczny_przychod <= 300_000:
            return proc * przecietne_wynagrodzenie_miesieczne_gus
        else:
            return proc * 1.8 * przecietne_wynagrodzenie_miesieczne_gus






def main():
    miesieczne_wydatki_hurtownia = np.arange(1,70000,1)
    marza_proc = [0.1, 0.2, 0.5, 1, 2, 3, 5]
    vat_proc = 0.23
    przecietne_wynagrodzenie_miesieczne_gus = 7005.76

    for m_proc in marza_proc:
        marza = miesieczne_wydatki_hurtownia * m_proc
        dochod = marza
        przychod = miesieczne_wydatki_hurtownia + marza
        vat = vat_proc * marza


        skala_podatek = np.array([Skala.podatek(dochod_mies=d) for d in marza])
        skala_skladka_zdrowotna = np.array([Skala.skladka_zdrowotna(dochod_mies=d) for d in marza])
        skala_razem = skala_podatek + skala_skladka_zdrowotna
        skala_razem_vat = skala_razem + vat


        liniowy_podatek = np.array([Liniowy.podatek(dochod_mies=d) for d in marza])
        liniowy_skladka_zdrowotna = np.array([Liniowy.skladka_zdrowotna(dochod_mies=d) for d in marza])
        liniowy_razem = liniowy_podatek + liniowy_skladka_zdrowotna
        liniowy_razem_vat = liniowy_razem + vat


        ryczalt_skladka_zdrowotna = np.array([Ryczalt.skladka_zdrowotna(przychod_mies=p, przecietne_wynagrodzenie_miesieczne_gus=przecietne_wynagrodzenie_miesieczne_gus) for p in przychod])


        ryczalt3_podatek = np.array([Ryczalt.podatek(przychod_mies=p, proc=0.03) for p in przychod])
        ryczalt3_razem = ryczalt3_podatek + ryczalt_skladka_zdrowotna
        ryczalt3_razem_vat = ryczalt3_razem + vat


        ryczalt85_podatek = np.array([Ryczalt.podatek(przychod_mies=p, proc=0.085) for p in przychod])
        ryczalt85_razem = ryczalt85_podatek + ryczalt_skladka_zdrowotna
        ryczalt85_razem_vat = ryczalt85_razem + vat


        # sam podatek
        if True:
            plt.plot(dochod, skala_podatek, label = "skala")
            plt.plot(dochod, liniowy_podatek, label = "liniowy")
            plt.plot(dochod, ryczalt3_podatek, label = "ryczałt 3%")
            plt.plot(dochod, ryczalt85_podatek, label = "ryczałt 8,5%")
            plt.legend()
            plt.title("sam podatek, marża {}".format(m_proc))
            plt.xlabel("dochód miesięczny")
            plt.ylabel("podatek")
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
            plt.show()  


        # sama skladka
        if True:
            plt.plot(dochod, skala_skladka_zdrowotna, label = "skala")
            plt.plot(dochod, liniowy_skladka_zdrowotna, label = "liniowy")
            plt.plot(dochod, ryczalt_skladka_zdrowotna, label = "ryczałt")
            plt.legend()
            plt.title("sama składka zdrowotna, marża {}".format(m_proc))
            plt.xlabel("dochód miesięczny")
            plt.ylabel("składka zdrowotna")
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
            plt.show()


        # podatek + skladka
        if True:
            plt.plot(dochod, skala_razem, label = "skala")
            plt.plot(dochod, liniowy_razem, label = "liniowy")
            plt.plot(dochod, ryczalt3_razem, label = "ryczałt 3%")
            plt.plot(dochod, ryczalt85_razem, label = "ryczałt 8,5%")
            plt.legend()
            plt.title("podatek + składka, marża {}".format(m_proc))
            plt.xlabel("dochód miesięczny")
            plt.ylabel("podatek")
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
            plt.show()


        # podatek + skladka + vat
        if True:
            plt.plot(dochod, skala_razem_vat, label = "skala")
            plt.plot(dochod, liniowy_razem_vat, label = "liniowy")
            plt.plot(dochod, ryczalt3_razem_vat, label = "ryczałt 3%")
            plt.plot(dochod, ryczalt85_razem_vat, label = "ryczałt 8,5%")
            plt.legend()
            plt.title("podatek + składka + vat, marża {}".format(m_proc))
            plt.xlabel("dochód miesięczny")
            plt.ylabel("podatek")
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
            plt.show()


main()



