# Ukládání a příprava dat - Projektová dokumentace
V rámci projektu jsou využívány tyto technologie:
- jazyk Python3,
- utilita pip3 umožňující stažení balíčků knihovních funkcí,
- databázový server Cassandra, skript předpokládá komunikaci na portu 9042,
- pro snadnou instalaci a spuštění je možné využít utility `make`,
- pro spuštění testů skriptů je nutné mít nainstalovanou utilitu `pytest`.

## Spuštění
Před spuštěním skriptu `proj1.py` vytvářející tabulky pro data a ukládající data ze stažených datasetů je nutné provést instalaci závislostí a spustit databázový server Cassandra. Pro instalaci závislostí je možné využít příkazu `make install`. 
Databázový server Cassandra je možné spustit dle pokynů popisovaných v rámci cvičení předmětu UPA, přičemž před spuštěním virtuálního stroje nastavíme port forwarding portu 9042 (pro hostitele i hosta). 
Test skriptů je možné spustit pomocí příkazu `make test`. Vlastní skript poté pomocí příkazu `make run`. 

## struktura tabulek
- schéma
- datové typy
- volba ID
- propojení s ostatními tabulkami (souvislosti)
- ...

## Stahování datasetů
Pro stahování datasetů využívá projekt třídu Downloader implementovanou v souboru /src/downloader. Třídní metody umožňují z dané URL adresy stáhnout dataset a provést parsování uložených dat do datových typů "list" či "dict". Skript podporuje parsování datasetů uložených ve formátech json a csv. 

## Cassandra
- asi obecně co to je
- proč jsme ji vybrali

### tvorba tabulek

### předzpracování dat

### ukládání dat

## členové týmu
- Křištof Jiří (vedoucí)
- Češka Petr
- Sulzer Dominik
