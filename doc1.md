# Ukládání a příprava dat - Projektová dokumentace 1. části
V rámci projektu jsou využívány tyto technologie:
- jazyk Python3,
- utilita pip3 umožňující stažení balíčků knihovních funkcí,
- databázový server Cassandra, skript předpokládá komunikaci na portu 9042,
- pro snadnou instalaci a spuštění je možné využít utility `make`,
- pro spuštění testů skriptů je nutné mít nainstalovanou utilitu `pytest`.

## Spuštění
Před spuštěním skriptu `proj1.py` vytvářející tabulky pro data a ukládající data ze stažených datasetů je nutné provést instalaci závislostí a spustit databázový server Cassandra. Pro instalaci závislostí je možné využít příkazu `make install`. 
Databázový server Cassandra je možné spustit dle pokynů popisovaných v rámci cvičení předmětu UPA, přičemž před spuštěním virtuálního stroje nastavíme port forwarding portu 9042 (pro hostitele i hosta). 
Test skriptů je možné spustit pomocí příkazu `make test`. Vlastní skript poté pomocí příkazu `make run1`. 

## Popis použitých tabulek

### Nakažení
Základní denní incidenční přehled osob s prokázanou nákazou COVID-19 dle hlášení krajských hygienických stanic.

- datum : datum
- vek : číslo
- pohlavi : textový řetězec
- kraj_nuts_kod : textový řetězec
- okres_lau_kod : textový řetězec
- nakaza_v_zahranici : boolean
- nakaza_zeme_csu_kod : textový řetězec

### Vyléčení
Záznamy o vyléčených po onemocnění COVID‑19 dle hlášení krajských hygienických stanic.

- datum : datum
- vek : číslo
- pohlavi : textový řetězec
- kraj_nuts_kod : textový řetězec
- okres_lau_kod : textový řetězec

### Úmrtí na covid
Záznamy o úmrtích v souvislosti s onemocněním COVID‑19 dle hlášení krajských hygienických stanic.

- datum : datum
- vek : číslo
- pohlavi : textový řetězec
- kraj_nuts_kod : textový řetězec
- okres_lau_kod : textový řetězec

### Hospitalizovaní
Datová sada obsahující data hospitalizovaných pacientů popisující průběh hospitalizace.

- datum : datum
- pacient_prvni_zaznam : číslo
- kum_pacient_prvni_zaznam : číslo
- pocet_hosp : číslo
- stav_bez_priznaku : číslo
- stav_lehky : číslo
- stav_stredni : číslo
- stav_tezky : číslo
- jip : číslo
- kyslik : číslo
- hfno : číslo
- upv : číslo
- ecmo : číslo
- tezky_upv_ecmo : číslo
- umrti : číslo
- kum_umrti : číslo

### Testy
Datová sada obsahující přírůstkové a kumulativní denní počty provedených PCR testů s korekcí na opakovaně pozitivní (kontrolní) testy.

- datum : datum
- kraj_nuts_kod : textový řetězec
- okres_lau_kod : textový řetězec
- prirustkovy_pocet_testu_okres : číslo
- kumulativni_pocet_testu_okres : číslo
- prirustkovy_pocet_testu_kraj : číslo
- kumulativni_pocet_testu_kraj : číslo
- prirustkovy_pocet_prvnich_testu_okres : číslo
- kumulativni_pocet_prvnich_testu_okres : číslo
- prirustkovy_pocet_prvnich_testu_kraj : číslo
- kumulativni_pocet_prvnich_testu_kraj : číslo

### Očkování
Datová sada poskytuje agregovaná data o vykázaných očkováních na úrovni krajů ČR.

- datum : datum
- vakcina : textový řetězec
- kraj_nuts_kod : textový řetězec
- kraj_nazev : textový řetězec
- vekova_skupina : textový řetězec
- prvnich_davek : číslo
- druhych_davek : číslo
- celkem_davek : číslo

### Úmrtí
Úmrtí obyvatelstva podle pětiletých věkových skupin a pohlaví v krajích a okresech.

- vek_text : text
- casref_od : datum
- casref_do : datum
- rok : int
- tyden : int
- hodnota : int

## Stahování datasetů
Pro stahování datasetů využívá projekt třídu Downloader implementovanou v souboru /src/downloader. Třídní metody umožňují z dané URL adresy stáhnout dataset a provést parsování uložených dat do datových typů "list" či "dict". Skript podporuje parsování datasetů uložených ve formátech json a csv. 

## Cassandra
Jako NoSQL databázi jsme se rozhodli využít Cassandru od Apache. Cassandra je distribuovaná, sloupcově orientovaná open-source databáze.

Při výběru databáze jsme zohledňovali, že potřebujeme zpracovávat veliké množství dat, které cassandra ukládá v komprimované podobě. Nad těmito daty provádět analytické operace a slučování, na tyto operace jsou sloupcově orientované databáze vhodné. Také jsme zohledňovali, že do databáze nebudeme pravidelně přidávat data a nepotřebujeme využívat transakce, na které Cassandra ideální není. 

### Tvorba tabulek
Knihovna Cassandra poskytuje třídu `Cluster`, která si metodou `connect()` vyžádá připojení k nějak běžící databázi. Funkce vrátí objekt třídy `Session`, který repsezentuje připojení k vybrané fatabázi. Pomocí `Session` můžeme spouštět příkazy v syntaxi CQL pomocí `execute()`. Každou tabulku vytvoříme pomocí příkazu `CREATE TABLE` se specifikovanými sloupci, jejich typy a zvolenými primárními klíčemi. 

### Předzpracování dat
V rámci předzpracování dat jsou odebrány ty položky, u nichž není vyplněna hodnota používaná v rámci primárního klíče. V případě, že položku nelze vložit do tabulky, pak je tato skutečnost poznamenána v logu uloženém v souboru`insert.log` a tato informace je uživateli vypsána do okna terminálu. 

### Ukládání dat
Použijeme stejnou metodu, jako při vytváření tabulek, `execute()`. Každý záznam vložíme do příslušně tabulky pomocí příkazu `INSERT INTO`, kterému poskytneme předzpracovaná data z předchozího části. 

Vkládání dat je možné ukončit dříve pomocí přerušení z klávesnice. V tomto případě skript přechází na vkládání dat do další tabulky. Tuto vlastnost je vhodné využít pouze pro účely ladění programu. 

## členové týmu
- Křištof Jiří (vedoucí)
- Češka Petr
- Sulzer Dominik
