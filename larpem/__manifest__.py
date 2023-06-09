{
    "name": "Larpem",
    "category": "Uncategorized",
    "version": "12.0.2.0",
    "author": "TechnoLibre",
    "license": "AGPL-3",
    "application": True,
    "depends": [
        "mail",
        "portal",
        "website",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/larpem_banque.xml",
        "views/larpem_templates.xml",
        "views/larpem_banque_compte.xml",
        "views/larpem_banque_transaction.xml",
        "views/larpem_manuel.xml",
        "views/larpem_personnage.xml",
        "views/larpem_system_point.xml",
        "views/menu.xml",
        "views/snippets.xml",
        "templates/website.xml",
    ],
    "installable": True,
}
