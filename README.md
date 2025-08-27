# Ovládání EcoVolter přes HomeAssistant

# Tento doplněk je zastaralý a už nebude vyvíjený. Použijte novinku, která má lepší instalaci: https://github.com/rattkin/ha-ecovolter-integration
Video také budu dělat.

Chytrá a bezpečná česká nabíječka od https://www.nabijelektromobil.cz/ má možnost ovládání a plánování z HomeAssistant. Tohle je první implementace API takže možná budou nějaké chyby.

5% sleva na nabíječky https://www.nabijelektromobil.cz/ s kódem TYGRI nebo TYGRISK

Video návod: https://youtu.be/xeg4AKZQC_s

## Postup instalace:
1. instalujte PyScript přes HACS:
HACS -> Integrace, zvolit "+", hledeje pyscript a instalujte.

2. v editoru (například VSCode doplněk) přidejte obsah `configuration.yaml` do svého souboru  `configuration.yaml` v adresáři config

3. přidejte obsah souboru `automations.yaml` do vašeho souboru `automations.yaml`

4. kopírujte adresáře ecovolter a pyscript do svého adresáře config

5. a zadejte seriové číslo vačeho EcoVolter do obou skriptů v adresáři pyscript: `key = "revcr01000000"`

6. restartujte HomeAssistant

7. přidejte si do dashboardů z adresáře dashboard


## V případě problémů:
- kontolujte log: https://my.home-assistant.io/redirect/logs/
- nabíječka musí být zapojené do elektřiny a v dosahu wi-fi.
- možná vyšla aktualizace: https://github.com/rattkin/ecovolter-control
- pište chybu do githubu, pokud to není hlášeno
