// ------------------------------------------------------------------------------------------------------------------ //

// Copyright © 2021-2023 Peter Mathiasson
// SPDX-License-Identifier: ISC

// ------------------------------------------------------------------------------------------------------------------ //

import BaseView from 'jet-views/base';

// ------------------------------------------------------------------------------------------------------------------ //

export default class MembersView extends BaseView {

    make_id(x) {
        return 'members:' + x;
    }

    rs_model() {
        return 'rs.Member';
    }

    popup_title() {
        return 'Member';
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
                    template: (obj) => `${webix.template.escape(obj.name)} (${webix.template.escape(obj.uid)})`,
                },
                {
                    id: 'admin',
                    header: 'Admin',
                    width: 75,
                    template: (obj) => obj.admin ? '<span class="webix_icon fas fa-check-circle"></span>' : '',
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
                this.tmpl_delete_button(
                    x => `Delete ${webix.template.escape(x.name)} (${webix.template.escape(x.uid)}) from project?`,
                    'members'
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
                    label: 'Admin',
                    labelWidth: 100,
                    view: 'checkbox',
                    name: 'admin',
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
                uid: webix.rules.isNotEmpty
            }
        };
    }

}

// ------------------------------------------------------------------------------------------------------------------ //
