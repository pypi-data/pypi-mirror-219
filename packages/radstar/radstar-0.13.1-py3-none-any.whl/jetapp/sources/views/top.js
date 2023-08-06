// ------------------------------------------------------------------------------------------------------------------ //

// Copyright © 2021-2023 Peter Mathiasson
// SPDX-License-Identifier: ISC

// ------------------------------------------------------------------------------------------------------------------ //

import {JetView, plugins} from 'webix-jet';
import rs from 'radstar';

// ------------------------------------------------------------------------------------------------------------------ //

export default class BaseTopView extends JetView {

    // config_header()
    title_template() { return webix.template.escape(SETTINGS.title || APPNAME); }
    menu_items() { throw 'not implemented'; }
    // config_footer()

    // -------------------------------------------------------------------------------------------------------------- //

    config() {

        let header;
        if (this.config_header !== undefined)
            header = this.config_header()
        else {
            header = {
                type: 'header',
                template: this.title_template(),
                css: 'webix_header app_header',
            };
        }

        const menu = {
            view: 'menu',
            id: 'core:top:menu',
            css: 'app_menu',
            width: 180,
            layout: 'y',
            select: true,
            template: '<span class="webix_icon #icon#" style="padding-right: 8px;"></span> #value# ',
            data: this.menu_items(),
        };

        let rows = [header, menu];

        // TODO: move to namespaces app
        if (SETTINGS.namespace_enabled) {
            const ns_select = {
                id: 'core:top:ns-select',
                // XXX: use richselect only if available
                view: 'richselect',
                options: 'rs->rs.NamespaceOptions',
                on: {
                    onAfterRender: function() {
                        if (rs.session_data.ns_id)
                            this.setValue(rs.session_data.ns_id);
                    },
                    onChange: function(new_value,  old_value, config) {
                        if (config === 'user') {
                            rs.welcome_set('ns_id', parseInt(new_value));
                            rs.reload();
                        }
                    },
                },
            };
            rows.push(ns_select);
        }

        if (this.config_footer !== undefined)
            rows.push(this.config_footer());

        return {
            type: 'clean',
            paddingX: 5,
            css: 'app_layout',
            cols: [
                {
                    paddingX: 5,
                    paddingY: 10,
                    rows: [{css: 'webix_shadow_medium', rows: rows}]
                },
                {
                    type: 'wide',
                    paddingX: 5,
                    paddingY: 10,
                    rows: [{$subview: true}],
                },
            ],
        };
    }

    // -------------------------------------------------------------------------------------------------------------- //

    init() {
        this.use(plugins.Menu, 'core:top:menu');
    }

}

// ------------------------------------------------------------------------------------------------------------------ //
