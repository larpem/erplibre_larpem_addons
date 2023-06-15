{
    "name": "Synchronize larpem database old software angularjs",
    "category": "Tools",
    "version": "12.0.1.0",
    "author": "TechnoLibre",
    "license": "AGPL-3",
    "website": "https://technolibre.ca",
    "depends": ["mail", "web_tree_dynamic_colored_field"],
    "external_dependencies": {
        "python": ["requests"],
    },
    "data": [
        "security/ir.model.access.csv",
        "views/sync_db_result.xml",
        "views/sync_db.xml",
        "views/menu.xml",
    ],
    "installable": True,
}
