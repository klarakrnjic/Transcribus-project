def usporedi_datoteke(putanja1, putanja2, praznine):
    try:
        with open(putanja1, 'r', encoding='utf-8') as f1:
            linije1 = f1.readlines()
        with open(putanja2, 'r', encoding='utf-8') as f2:
            linije2 = f2.readlines()

        # Pronađi koja datoteka ima više linija
        broj_linija1 = len(linije1)
        broj_linija2 = len(linije2)
        max_broj_linija = max(broj_linija1, broj_linija2)

        ukupno_podudaranja = 0
        ukupno_znakova = 0

        print(f"{'Linija':<10} | {'Podudaranje (%)':<15}")
        print("-" * 30)

        for i in range(max_broj_linija):
            # Dohvaćamo liniju ili prazan string ako linija ne postoji u jednoj od datoteka
            l1 = linije1[i].rstrip('\n') if i < broj_linija1 else ""
            l2 = linije2[i].rstrip('\n') if i < broj_linija2 else ""

            if praznine:
                l1 = l1.replace(' ', '')
                l2 = l2.replace(' ', '')


            # Određujemo koliko znakova uspoređujemo (dužina duže linije)
            max_len_linije = max(len(l1), len(l2))
            lokalna_podudaranja = 0


            # 3. Usporedba znak po znak do dužine kraće linije
            min_len_linije = min(len(l1), len(l2))
            for j in range(min_len_linije):
                if l1[j] == l2[j]:
                    lokalna_podudaranja += 1

            # Izračun postotka za liniju
            if max_len_linije > 0:
                postotak_linije = (lokalna_podudaranja / max_len_linije) * 100
            else:
                postotak_linije = 100.0 if l1 == l2 else 0.0

            print(f"{i+1:<10} | {postotak_linije:>14.2f}%")

            # Dodavanje u ukupnu statistiku
            ukupno_podudaranja += lokalna_podudaranja
            ukupno_znakova += max_len_linije

        # 4. Ukupni postotak za cijele datoteke
        if ukupno_znakova > 0:
            ukupni_postotak = (ukupno_podudaranja / ukupno_znakova) * 100
        else:
            ukupni_postotak = 100.0

        print("-" * 30)
        print(f"{'UKUPNO':<10} | {ukupni_postotak:>14.2f}%")

    except FileNotFoundError:
        print("Pogreška: Datoteka nije pronađena.")

# Poziv metode
usporedi_datoteke('datoteka1.txt', 'datoteka2.txt',True)