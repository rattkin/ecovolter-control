# Ovládání EcoVolter přes HomeAssistant

Chytrá a bezpečná česká nabíječka od https://www.nabijelektromobil.cz/ má možnost ovládání a plánování z HomeAssistant. Tohle je první implementace API takže možná budou nějaké chyby.

5% sleva na nabíječky https://EcoVolter.cz s kódem TYGRI nebo TYGRISK

## Postup instalace:
1. instalujte PyScript přes HACS:
HACS -> Integrace, zvolit "+", hledeje pyscript a instalujte.

2. v editoru (například VSCode doplněk) přidejte obsah `configuration.yaml` do své konfigurace

3. kopírujte také adresáře ecovolter a pyscript do svého konfiguračního adresáře

4. a zadejte seriové číslo do obou skriptů v adresáři pyscript

5. přidejta automatizaci ze souboru `ecovolter_automations.yaml` do svých automatizací

6. restartujte HomeAssistant

7. přidejte si do dashboardů z adresáře dashboard


## V případě problémů:
- kontolujte log: https://my.home-assistant.io/redirect/logs/
- nabíječka musí být zapojené do elektřiny a v dosahu wi-fi.
- možná vyšla aktualizace: https://github.com/rattkin/ecovolter-control
- pište chybu do githubu, pokud to není hlášeno
