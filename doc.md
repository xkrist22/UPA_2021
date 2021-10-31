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
Jako NoSQL databázi jsme se rozhodli využít Cassandru od Apache. Cassandra je distribuovaná, sloupcově orientovaná open-source databáze.

Při výběru databáze jsme zohledňovali, že potřebujeme zpracovávat veliké množství dat, které cassandra ukládá v komprimované podobě. Nad těmito daty provádět analytické operace a slučování, na tyto operace jsou sloupcově orientované databáze vhodné. Také jsme zohledňovali, že do databáze nebudeme pravidelně přidávat data a nepotřebujeme využívat transakce, na které Cassandra ideální není. 

### tvorba tabulek

Knihovna Cassandra poskytuje třídu `Cluster`, která si metodou `connect()` vyžádá připojení k nějak běžící databázi. Funkce vrátí objekt třídy `Session`, který repsezentuje připojení k vybrané fatabázi. Pomocí `Session` můžeme spouštět příkazy v syntaxi CQL pomocí `execute()`. Každou tabulku vytvoříme pomocí příkazu `CREATE TABLE` se specifikovanými sloupci, jejich typy a zvolenými primárními klíčemi. 

### předzpracování dat

### ukládání dat

Použijeme stejnou metodu, jako při vytváření tabulek, `execute()`. Každý záznam vložíme do příslušně tabulky pomocí příkazu `INSERT INTO`, kterému poskytneme předzpracovaná data z předchozího části.

## členové týmu
- Křištof Jiří (vedoucí)
- Češka Petr
- Sulzer Dominik
