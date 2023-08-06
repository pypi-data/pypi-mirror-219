// ------------------------------------------------------------------------------------------------------------------ //

// Copyright © 2021-2023 Peter Mathiasson
// SPDX-License-Identifier: ISC

// ------------------------------------------------------------------------------------------------------------------ //

import BaseView from 'jet-views/base';
import rs from 'radstar';

// ------------------------------------------------------------------------------------------------------------------ //

export default class UserView extends BaseView {

    make_id(x) {
        return 'core:users:' + x;
    }

    rs_model() {
        return 'rs.User';
    }

    popup_title() {
        return 'User';
    }

    config_table() {
        return {
            multiselect: true,
            columns: [
                {
                    id: 'uid',
                    header: 'User',
                    width: 200,
                    fillspace: true,
                    format: webix.template.escape,
                },
                {
                    id: 'name',
                    header: 'Name',
                    width: 200,
                    fillspace: true,
                    format: webix.template.escape,
                },
                {
                    id: 'super_user',
                    header: 'Super User',
                    width: 100,
                    template: (obj) => obj.super_user ? '<span class="webix_icon fas fa-check-circle"></span>' : '',
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
                    id: 'core:users:connect-button',
                    hidden: SETTINGS.namespace_enabled !== true,
                    disabled: true,
                    value: 'Connect',
                    width: 150,
                    click: function() {
                        let ns_id = $$('core:users:table').getSelectedId().id;
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
                    x => `Delete ${webix.template.escape(x.name)} (${webix.template.escape(x.uid)})?`,
                    'users'
                ),
            ]
        };
    }

    config_form() {
        return {
            elements: [
                {
                    label: 'User',
                    labelWidth: 100,
                    view: 'text',
                    name: 'uid',
                },
                {
                    label: 'Name',
                    labelWidth: 100,
                    view: 'text',
                    name: 'name',
                },
                {
                    label: 'Password',
                    labelWidth: 100,
                    view: 'text',
                    type: 'password',
                    name: 'password',
                },
                {
                    label: 'Super User',
                    labelWidth: 100,
                    view: 'checkbox',
                    name: 'super_user',
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
                uid: webix.rules.isNotEmpty,
                name: webix.rules.isNotEmpty,
            }
        };
    }

    on_select_change(items) {
        if (SETTINGS.namespace_enabled === true) {
            let connect_button = $$('core:users:connect-button');
            items.length === 1 ? connect_button.enable() : connect_button.disable();
        }
    }

}

// ------------------------------------------------------------------------------------------------------------------ //
