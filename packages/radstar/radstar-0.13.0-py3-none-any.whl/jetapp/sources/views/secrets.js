// ------------------------------------------------------------------------------------------------------------------ //

// Copyright © 2021-2023 Peter Mathiasson
// SPDX-License-Identifier: ISC

// ------------------------------------------------------------------------------------------------------------------ //

import BaseView from 'jet-views/base';

// ------------------------------------------------------------------------------------------------------------------ //

export default class SecretView extends BaseView {

    make_id(x) {
        return 'core:secrets:' + x;
    }

    rs_model() {
        return 'rs.Secret';
    }

    popup_title() {
        return 'Secret';
    }

    config_table() {
        return {
            multiselect: true,
            columns: [
                {
                    id: 'key',
                    header: 'Key',
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
                this.tmpl_add_button(),
                this.tmpl_edit_button(),
                this.tmpl_delete_button(x => `Delete ${webix.template.escape(x.key)}?`, 'secrets'),
            ]
        };
    }

    config_form() {
        return {
            elements: [
                {
                    label: 'Key',
                    labelWidth: 100,
                    view: 'text',
                    name: 'key',
                },
                {
                    label: 'Secret',
                    labelWidth: 100,
                    view: 'text',
                    type: 'password',
                    name: 'value',
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
                key: webix.rules.isNotEmpty,
            }
        };
    }

}

// ------------------------------------------------------------------------------------------------------------------ //
