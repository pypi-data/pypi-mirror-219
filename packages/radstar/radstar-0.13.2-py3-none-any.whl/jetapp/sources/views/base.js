// ------------------------------------------------------------------------------------------------------------------ //

// Copyright © 2021-2023 Peter Mathiasson
// SPDX-License-Identifier: ISC

// ------------------------------------------------------------------------------------------------------------------ //

import {JetView} from 'webix-jet';
import rs from 'radstar';

// ------------------------------------------------------------------------------------------------------------------ //

export default class BaseView extends JetView {

    make_id(/*x*/) { throw 'not implemented'; }
    rs_model() { throw 'not implemented'; }
    config_table() { throw 'not implemented'; }
    // config_footer()
    // config_form()
    // on_before_add(id, obj)
    // on_select_change()
    // on_item_dbl_click(id)

    popup_title() {
        let title = this.rs_model();
        return title.charAt(0).toUpperCase() + title.slice(1);
    }

    tmpl_pager() {
        return {
            view: 'pager',
            id: this.make_id('pager'),
            template: '{common.first()} {common.prev()} {common.pages()} {common.next()} {common.last()}',
            size: 50,
            group: 5,
        };
    }

    tmpl_add_button() {
        let table_id = this.make_id('table');
        return {
            view: 'button',
            value: 'Add',
            width: 150,
            click: function() {
                $$(table_id).clearSelection();
                this.$scope.popup.show();
            },
            css: 'webix_primary',
        };
    }

    tmpl_edit_button() {
        return {
            view: 'button',
            id: this.make_id('edit-button'),
            disabled: true,
            value: 'Edit',
            width: 150,
            click: function() {
                this.$scope.popup.show();
            },
        };
    }

    tmpl_delete_button(text_func, multi_label) {
        let table_id = this.make_id('table');
        return {
            view: 'button',
            id: this.make_id('delete-button'),
            disabled: true,
            value: 'Delete',
            width: 150,
            click: function() {
                let button = this;
                let tbl = $$(table_id);
                let items = tbl.getSelectedItem(true);
                if (!items.length)
                    return;

                webix.confirm({
                    text: items.length === 1 ? text_func(items[0]) : `Delete ${items.length} ${multi_label}?`,
                    type: 'confirm-warning',
                    width: 600,
                }).then(() => {
                    let promises = [];
                    items.forEach(x => promises.push(webix.dp(tbl).save(x.id, 'delete')));
                    rs.spin_button(webix.promises.all(promises), button);
                });
            },
            css: 'webix_danger',
        };
    }

    tmpl_save_button() {
        let table_id = this.make_id('table');
        return {
            view: 'button',
            value: 'Save',
            width: 150,
            click: function() {
                let p = rs.save(table_id, this.getFormView());
                if (p) {
                    p = rs.spin_button(p, this);
                    let popup = this.getTopParentView();
                    p.then(() => popup.hide());
                }
            },
            css: 'webix_primary',
        };
    }

    tmpl_cancel_button() {
        let table_id = this.make_id('table');
        return {
            view: 'button',
            value: 'Cancel',
            width: 150,
            click: function() {
                this.getTopParentView().hide();

                // re-select current item to reset the form
                let tbl = $$(table_id);
                let item = tbl.getSelectedItem();
                if (item) {
                    tbl.clearSelection();
                    tbl.select(item.id);
                }
            },
        };
    }


    config() {
        let table = Object.assign({
            view: 'datatable',
            id: this.make_id('table'),
            select: 'row',
            url: 'rs->' + this.rs_model(),
            save: {
                url: 'rs->' + this.rs_model(),
                updateFromResponse: true,
                undoOnError: true
            },
            undo: true,
            pager: this.make_id('pager'),
            on: {
                onBeforeLoad: function() {
                    this.showOverlay("Loading...");
                },
                onAfterLoad: function() {
                    this.count() ? this.hideOverlay() : this.showOverlay('No data to display');
                },
                onBeforeAdd: function(id, obj) {
                    if (this.$scope.on_before_add !== undefined)
                        this.$scope.on_before_add(id, obj);
                },
                onAfterAdd: function() {
                    if (this.count())
                        this.hideOverlay();
                },
                onItemDblClick: function(id) {
                    if (this.$scope.on_item_dbl_click !== undefined)
                        this.$scope.on_item_dbl_click(id);
                    else if (this.$scope.popup !== undefined)
                        this.$scope.popup.show();
                },
                onSelectChange: function() {
                    let tbl = $$(this.$scope.make_id('table'));
                    let items = tbl.getSelectedItem(true);

                    let edit_button = $$(this.$scope.make_id('edit-button'));
                    if (edit_button)
                        items.length === 1 ? edit_button.enable() : edit_button.disable();

                    let delete_button = $$(this.$scope.make_id('delete-button'));
                    if (delete_button)
                        items.length ? delete_button.enable() : delete_button.disable();

                    if (this.$scope.on_select_change !== undefined)
                        this.$scope.on_select_change(items);
                },
            },
        }, this.config_table());

        let footer = {
            minHeight: 40,
            cols: [this.tmpl_pager()],
        };
        if (this.config_footer !== undefined)
            Object.assign(footer, this.config_footer());

        return {
            css: 'webix_shadow_medium',
            rows: [table, footer],
        };
    }

    init(/*view*/) {
        if (this.config_form === undefined)
            return;

        let form = Object.assign({
            view: 'form',
            id: this.make_id('form'),
        }, this.config_form());

        this.popup = this.ui({
            view: 'window',
            head: this.popup_title(),
            modal: true,
            // position: 'top',
            position: function(state) {
                state.top = 5;
            },
            width: 1000,
            body: form,
        });

        rs.bind(this.make_id('table'), this.make_id('form'));
    }

}

// ------------------------------------------------------------------------------------------------------------------ //
