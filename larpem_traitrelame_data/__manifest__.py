{
    "name": "LARPEM traitrelame data",
    "version": "12.0.1.0",
    "author": "TechnoLibre",
    "license": "AGPL-3",
    "website": "https://technolibre.ca",
    "depends": ["larpem", "migrator_larpem_admin"],
    "data": ["data/larpem_banque.xml", "data/larpem_banque_compte.xml"],
    "installable": True,
    "uninstall_hook": "uninstall_hook",
}
