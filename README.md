{{# Ovládání EcoVolter přes HomeAssistant

Chytrá a bezpečná česká nabíječka od https://www.nabijelektromobil.cz/ má možnost ovládání a plánování z HomeAssistent. Tohle je první implementace API takže možná budou nějaké chyby.

5% sleva na nabíječky https://EcoVolter.cz s kódem TYGRI nebo TYGRISK

## Postup instalace:
1. instalujte PyScript přes HACS:
HACS -> Integrace, zvolit "+", hledeje pyscript a instalujte.

2. přidejte obsah `configuration.yaml` do své konfigurace

3. přidejta automatizaci `ecovolter_automations.yaml` do automatizací

4. kopírujte adresáře ecovolter a pyscript do svého konfiguračního adresáře

5. zadejte seriové číslo do obou skriptů v adresáři pyscript

6. restartujte HomeAssitant

7. přidejte si do dashboardů z adresáře dashboard


## V případě problémů:
- kontolujte log: https://my.home-assistant.io/redirect/logs/
- nabíječka musí být zapojené do elektřiny a v dosahu wi-fi.
- možná vyšla aktualizace: https://github.com/rattkin/ecovolter-control
- pište chybu do githubu, pokud to není hlášeno
}}