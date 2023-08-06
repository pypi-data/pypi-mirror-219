// ------------------------------------------------------------------------------------------------------------------ //

// Copyright © 2021-2023 Peter Mathiasson
// SPDX-License-Identifier: ISC

// ------------------------------------------------------------------------------------------------------------------ //

import RSProxy from './proxy';
import RSSocket from './socket';

// ------------------------------------------------------------------------------------------------------------------ //

export default class rs {

    // -------------------------------------------------------------------------------------------------------------- //

    static init() {
        rs.socket = new RSSocket();
        rs.session_data = {}; // for storing "session" data
        webix.proxy.rs = RSProxy;
    }

    // -------------------------------------------------------------------------------------------------------------- //

    static bind(master, slave) {
        if (typeof master === 'string')
            master = $$(master);
        if (typeof slave === 'string')
            slave = $$(slave);

        slave.bind(master);
        if (slave.config.view === 'form')
            master.attachEvent('onAfterCursorChange', () => slave.clearValidation());
    }

    // -------------------------------------------------------------------------------------------------------------- //

    static reload() {
        rs.session_data.reload_in_progress = true;
        location.reload();
    }

    // -------------------------------------------------------------------------------------------------------------- //

    static save(master, form) {

        if (typeof master === 'string')
            master = $$(master);

        if (typeof form === 'string')
            form = $$(form);
        else if (form === undefined)
            form = master;

        if (!form.validate())
            return;

        return new webix.promise((resolve, reject) => {
            var values = form.getValues();
            if (values.id) {
                webix.dp(master).save(values.id, 'update', values).then(
                    () => resolve(),
                    () => reject()
                )
            } else {
                webix.dp(master).save(webix.uid(), 'insert', values).then(
                    (obj) => {
                        webix.dp(master).ignore(() => {
                            if (!master.exists(obj.id))
                                master.add(obj);
                            master.select(obj.id);
                        });
                        resolve();
                    },
                    () => reject()
                );
            }
        });

    }

    // -------------------------------------------------------------------------------------------------------------- //

    static spin_button(p, button) {
        if (typeof button === 'string')
            button = $$(button);

        const old_value = button.getValue();
        button.setValue('<span class="webix_icon fas fa-spinner fa-spin"></span>');
        button.disable()

        return new webix.promise((resolve, reject) => {
            p.then((...params) => {
                button.setValue(old_value);
                button.enable();
                resolve(...params);
            }).fail((...params) => {
                button.setValue(old_value);
                button.enable();
                reject(...params);
            });
        });
    }

    // -------------------------------------------------------------------------------------------------------------- //

    static welcome_get(key) {
        let wd = webix.storage.local.get('welcome_data');
        return wd && wd[key];
    }

    static welcome_set(key, value) {
        let wd = webix.storage.local.get('welcome_data') || {};
        wd[key] = value;
        webix.storage.local.put('welcome_data', wd);
    }

}

// ------------------------------------------------------------------------------------------------------------------ //
