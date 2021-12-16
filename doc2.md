# Ukládání a příprava dat - Projektová dokumentace 2. části
V rámci projektu jsou využívány tyto technologie:
- jazyk Python3,
- utilita pip3 umožňující stažení balíčků knihovních funkcí,
- databázový server Cassandra, skript předpokládá komunikaci na portu 9042,
- pro snadnou instalaci a spuštění je možné využít utility `make`,
- pro spuštění testů skriptů je nutné mít nainstalovanou utilitu `pytest`.

## Spuštění
Před spuštěním skriptu `proj2.py` vytvářející datové sady pro jednotlivé úlohy a produkující výstupní grafy je nutné provést instalaci závislostí a spustit databázový server Cassandra. Pro instalaci závislostí je možné využít příkazu `make install`. 
Poté je potřeba spustit skript `proj1.py`, který stáhne potřebné datasety a importuje data do databáze.
Databázový server Cassandra je možné spustit dle pokynů popisovaných v rámci cvičení předmětu UPA, přičemž před spuštěním virtuálního stroje nastavíme port forwarding portu 9042 (pro hostitele i hosta). 
Test skriptů je možné spustit pomocí příkazu `make test`. Vlastní skript poté pomocí příkazu `make run2`. 


## Vybrané úlohy ze zadání
Dotazy ze skupiny A: 1. a 2. bod.

## Výsledky
### Dotaz skupiny A#1: Spojnicový grafy zobrazující vývoj covidové situace po měsících:
![Spojnicový grafy zobrazující vývoj covidové situace po měsících](https://i.ibb.co/FHz6CmJ/A1.png)

### Dotaz skupiny A#2: Krabicový graf zobrazující rozložení věku nakažených osob v jednotlivých krajích.
![Krabicový graf zobrazující rozložení věku nakažených osob v jednotlivých krajích.](https://i.ibb.co/H7SL28w/A2.png)

## členové týmu
- Křištof Jiří (vedoucí)
- Češka Petr
- Sulzer Dominik