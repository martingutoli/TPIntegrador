import csv
import os
import sys

CSV_HEADERS = ["nombre", "poblacion", "superficie", "continente"]


def is_non_negative_int_string(s):
   
    return isinstance(s, str) and s.strip().isdigit()

def normalize_str(s):
    return " ".join(s.strip().split())


def load_csv(path):
   
    countries = []
    if not os.path.exists(path):
        return countries

    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        if reader.fieldnames is None or [h.lower() for h in reader.fieldnames] != CSV_HEADERS:
            print("ERROR: cabecera del CSV invalida. se espera:", ",".join(CSV_HEADERS))
            return countries

        for i, row in enumerate(reader, start=1):
            nombre = normalize_str(row.get("nombre", ""))
            poblacion_s = normalize_str(row.get("poblacion", ""))
            superficie_s = normalize_str(row.get("superficie", ""))
            continente = normalize_str(row.get("continente", ""))

            
            if not nombre or not continente:
                print(f"warning: fila {i} con campos vacíos omitida.")
                continue
            if not is_non_negative_int_string(poblacion_s) or not is_non_negative_int_string(superficie_s):
                print(f"warning: fila {i} con valores numaricos invalidos omitida.")
                continue

            countries.append({
                "nombre": nombre,
                "poblacion": int(poblacion_s),
                "superficie": int(superficie_s),
                "continente": continente
            })
    return countries

def save_csv(path, countries):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for c in countries:
            writer.writerow({
                "nombre": c["nombre"],
                "poblacion": c["poblacion"],
                "superficie": c["superficie"],
                "continente": c["continente"]
            })


def input_non_empty(prompt):
    while True:
        val = input(prompt).strip()
        if val == "":
            print("no se permiten campos vacios. intente nuevamente.")
        else:
            return val

def input_int_non_negative(prompt):
   
    while True:
        val = input(prompt).strip()
        if is_non_negative_int_string(val):
            return int(val)
        print("valor invalido. ingrese un numero entero no negativo.")


def add_country(countries):
    nombre = input_non_empty("nombre del pais: ")

    
    if any(c["nombre"].lower() == nombre.lower() for c in countries):
        print("ya existe un pais con ese nombre. use la opcion de actualizar si desea cambiar datos.")
        return

    poblacion = input_int_non_negative("poblacion (entero): ")
    superficie = input_int_non_negative("superficie en km² (entero): ")
    continente = input_non_empty("continente: ")

    countries.append({
        "nombre": normalize_str(nombre),
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": normalize_str(continente)
    })
    print("pais agregado correctamente.")

def update_country(countries):
    nombre = input_non_empty("ingrese el nombre del pais a actualizar: ")
    matches = [c for c in countries if nombre.lower() in c["nombre"].lower()]
    if not matches:
        print("no se encontraron pais con esa cadena.")
        return
    print("paises encontrado:")
    for i, c in enumerate(matches, start=1):
        print(f"{i}. {c['nombre']} - poblacion: {c['poblacion']}, superficie: {c['superficie']} km²")
    idx = input_int_non_negative("seleccione el numero de pais a actualizar: ")
    if idx < 1 or idx > len(matches):
        print("selección invalida.")
        return
    selected = matches[idx - 1]
    print(f"actualizando {selected['nombre']}. dejar en blanco para mantener valor actual.")

    while True:
        pob = input("nueva poblacion (enter para mantener): ").strip()
        if pob == "":
            break
        if is_non_negative_int_string(pob):
            selected['poblacion'] = int(pob)
            break
        print("valor invalido. ingrese un numero entero no negativo o deje vacio.")

    while True:
        sup = input("nueva superficie (enter para mantener): ").strip()
        if sup == "":
            break
        if is_non_negative_int_string(sup):
            selected['superficie'] = int(sup)
            break
        print("valor invalido. ingrese un numero entero no negativo o deje vacio.")

    print("Actualización finalizada.")


def search_country(countries):
    termino = input_non_empty("ingrese nombre o parte del nombre a buscar: ")
    results = [c for c in countries if termino.lower() in c["nombre"].lower()]
    if not results:
        print("no se encontraron coincidencias.")
        return
    for c in results:
        print(f"- {c['nombre']}: poblacion={c['poblacion']}, superficie={c['superficie']} km², continente={c['continente']}")

def filter_by_continent(countries):
    cont = input_non_empty("continente a filtrar: ")
    results = [c for c in countries if c["continente"].lower() == cont.lower()]
    if not results:
        print("no hay paises en ese continente (segun dataset).")
        return
    for c in results:
        print(f"- {c['nombre']} ({c['continente']}): poblacion={c['poblacion']}, superficie={c['superficie']}")

def filter_by_range(countries, key):
    print(f"ingrese el rango para {key}. use numeros enteros. dejar vacio para no establecer limite.")
    low = input("limite inferior: ").strip()
    high = input("limite superior: ").strip()

    if low != "" and not is_non_negative_int_string(low):
        print("limite inferior invalido. debe ser entero no negativo o vacio.")
        return
    if high != "" and not is_non_negative_int_string(high):
        print("liimite superior invalido. debe ser entero no negativo o vacio.")
        return

    low_v = int(low) if low != "" else None
    high_v = int(high) if high != "" else None

    results = []
    for c in countries:
        val = c[key]
        if low_v is not None and val < low_v:
            continue
        if high_v is not None and val > high_v:
            continue
        results.append(c)

    if not results:
        print("no hay paises que cumplan ese rango.")
        return
    for c in results:
        print(f"- {c['nombre']}: {key}={c[key]}")


def selection_sort_countries(countries, key, reverse=False):
 
    arr = countries[:]
    n = len(arr)
    for i in range(n - 1):
    
        selected_idx = i
        for j in range(i + 1, n):
            a = arr[j][key].lower() if key == "nombre" else arr[j][key]
            b = arr[selected_idx][key].lower() if key == "nombre" else arr[selected_idx][key]
            if not reverse:
                if a < b:
                    selected_idx = j
            else:
                if a > b:
                    selected_idx = j
        if selected_idx != i:
            arr[i], arr[selected_idx] = arr[selected_idx], arr[i]
    return arr

def sort_countries(countries):
    print("ordenar por: 1) nombre 2) poblacion 3) superficie")
    choice = input_non_empty("elija (1/2/3): ")
    if choice == "1":
        key = "nombre"
    elif choice == "2":
        key = "poblacion"
    elif choice == "3":
        key = "superficie"
    else:
        print("opcion invalida.")
        return

    order = input_non_empty("orden ascendente? (s/n): ").lower()
    reverse = False
    if order in ('s', 'si', 'y', 'yes'):
        reverse = False
    else:
        reverse = True

    sorted_list = selection_sort_countries(countries, key, reverse=reverse)
    for c in sorted_list:
        print(f"- {c['nombre']}: poblacion={c['poblacion']}, superficie={c['superficie']} km², continente={c['continente']}")


def statistics(countries):
    if not countries:
        print("Dataset vacío.")
        return

    mayor = countries[0]
    menor = countries[0]
    suma_p = 0
    suma_s = 0
    per_cont = {}

    for c in countries:
        if c["poblacion"] > mayor["poblacion"]:
            mayor = c
        if c["poblacion"] < menor["poblacion"]:
            menor = c
        suma_p += c["poblacion"]
        suma_s += c["superficie"]
        per_cont[c["continente"]] = per_cont.get(c["continente"], 0) + 1

    avg_pop = suma_p / len(countries)
    avg_sup = suma_s / len(countries)

    print(f"pais con mayor poblacion: {mayor['nombre']} ({mayor['poblacion']})")
    print(f"país con menor poblacion: {menor['nombre']} ({menor['poblacion']})")
    print(f"promedio de poblacion: {avg_pop:.2f}")
    print(f"promedio de superficie: {avg_sup:.2f} km²")
    print("cantidad de paises por continente:")
    for cont, n in per_cont.items():
        print(f"- {cont}: {n}")


def menu():
    print("""\n==== gestion de paises - menu ====
1) cargar dataset (desde CSV)
2) guardar dataset (a CSV)
3) agregar pais
4) actualizar pais (poblacion/superficie)
5) buscar pais por nombre
6) filtrar por continente
7) filtrar por rango de poblacion
8) filtrar por rango de superficie
9) ordenar
10) mostrar estadisticas
0) salir
""")
    return input_non_empty("seleccione una opcion: ")

def main():
    csv_file = "paises_base.csv"

    countries = load_csv(csv_file)
    if countries:
        print(f"se cargaron {len(countries)} paises desde {csv_file}.")
    else:
        print("dataset vacio. puede agregar paises o cargar un CSV con la opción 1.")

    while True:
        choice = menu()
        if choice == "1":
            path = input_non_empty("ruta del CSV a cargar: ")
            countries = load_csv(path)
            print(f"se cargaron {len(countries)} paises.")
        elif choice == "2":
            path = input("ruta donde guardar CSV (enter para '{}'): ".format(csv_file)).strip()
            if path == "":
                path = csv_file
            save_csv(path, countries)
            print(f"dataset guardado en {path}.")
        elif choice == "3":
            add_country(countries)
        elif choice == "4":
            update_country(countries)
        elif choice == "5":
            search_country(countries)
        elif choice == "6":
            filter_by_continent(countries)
        elif choice == "7":
            filter_by_range(countries, "poblacion")
        elif choice == "8":
            filter_by_range(countries, "superficie")
        elif choice == "9":
            sort_countries(countries)
        elif choice == "10":
            statistics(countries)
        elif choice == "0":
            confirm = input("guardar cambio antes de salir? (s/n): ").lower().strip()
            if confirm in ('s', 'si', 'y', 'yes'):
                save_csv(csv_file, countries)
                print(f"guardado en {csv_file}.")
            print("saliendo. hasta luego!")
            break
        else:
            print("opcion invalida. intente nuevamente.")

if __name__ == '__main__':
    main()

