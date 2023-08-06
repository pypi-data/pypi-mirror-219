// ------------------------------------------------------------------------------------------------------------------ //

// Copyright © 2021-2023 Peter Mathiasson
// SPDX-License-Identifier: ISC

// ------------------------------------------------------------------------------------------------------------------ //

import BaseView from 'jet-views/base';
import rs from 'radstar';

// ------------------------------------------------------------------------------------------------------------------ //

export default class NamespaceView extends BaseView {

    make_id(x) {
        return 'namespaces:' + x;
    }

    rs_model() {
        return 'rs.Namespace';
    }

    popup_title() {
        return 'Namespace';
    }

    config_table() {
        return {
            multiselect: true,
            columns: [
                {
                    id: 'name',
                    header: 'Name',
                    width: 200,
                    fillspace: true,
                    format: webix.template.escape,
                },
            ],
        };
    }

    config_footer() {
        return {
            cols: [
                this.tmpl_pager(),
                {},
                {
                    view: 'button',
                    id: 'namespaces:connect-button',
                    disabled: true,
                    value: 'Connect',
                    width: 150,
                    click: function() {
                        let ns_id = $$('namespaces:table').getSelectedId().id;
                        if (ns_id) {
                            rs.welcome_set('ns_id', parseInt(ns_id));
                            rs.reload();
                        }
                    },
                },
                {width: 50},
                this.tmpl_add_button(),
                this.tmpl_edit_button(),
                this.tmpl_delete_button(
                    x => `Delete ${webix.template.escape(x.name)}?`,
                    'namespaces'
                ),
            ]
        };
    }

    config_form() {
        return {
            elements: [
                {
                    label: 'Name',
                    labelWidth: 100,
                    view: 'text',
                    name: 'name',
                },
                {
                    cols: [
                        {},
                        this.tmpl_cancel_button(),
                        this.tmpl_save_button(),
                    ]
                }
            ],
            rules: {
                name: webix.rules.isNotEmpty,
            }
        };
    }

    on_select_change(items) {
        let connect_button = $$('namespaces:connect-button');
        items.length === 1 ? connect_button.enable() : connect_button.disable();
    }

}

// ------------------------------------------------------------------------------------------------------------------ //
