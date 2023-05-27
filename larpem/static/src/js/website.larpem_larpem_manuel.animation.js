odoo.define("larpem_larpem_manuel.animation", function (require) {
    "use strict";

    let sAnimation = require("website.content.snippets.animation");

    sAnimation.registry.larpem_larpem_manuel = sAnimation.Class.extend({
        selector: ".o_larpem_larpem_manuel",

        start: function () {
            let self = this;
            this._eventList = this.$(".container");
            this._originalContent = this._eventList[0].outerHTML;
            let def = this._rpc({route: "/larpem/larpem_manuel_list"}).then(function (data) {
                if (data.error) {
                    return;
                }

                if (_.isEmpty(data)) {
                    return;
                }

                self._$loadedContent = $(data);
                self._eventList.replaceWith(self._$loadedContent);
            });

            return $.when(this._super.apply(this, arguments), def);
        },
        destroy: function () {
            this._super.apply(this, arguments);
            if (this._$loadedContent) {
                this._$loadedContent.replaceWith(this._originalContent);
            }
        },
    });
});
