// ------------------------------------------------------------------------------------------------------------------ //

// Copyright © 2021-2023 Peter Mathiasson
// SPDX-License-Identifier: ISC

// ------------------------------------------------------------------------------------------------------------------ //

import rs from './index';
import login_window from './login-window';

// ------------------------------------------------------------------------------------------------------------------ //

export default class RSSocket {

    constructor() {
        this._socket = new WebSocket(
            (window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/_ws'
        );

        this._socket.onopen = () => {
            this._socket.send(webix.stringify({
                operation: 'hello',
                data: webix.storage.local.get('welcome_data') || {},
            }));
        };

        this._socket.onclose = () => {
            this.connection_lost();
        };

        this._socket.onerror = (/*err*/) => {
            this.connection_lost();
        };

        this._socket.onmessage = (e) => {

            // parse data
            var data = JSON.parse(e.data, (key, value) => {
                if (value && value['$t'] !== undefined && value['$v'] !== undefined) {
                    if (value['$t'] === 'dt')
                        return new Date(value['$v']);
                    return value['$v'];
                }
                return value;
            });

            var p = null;
            if (data.call_id) {
                p = this._calls[data.call_id];
                delete this._calls[data.call_id];
            }

            // handle login
            if (data.status === 'login-required') {
                login_window((username, password) => {
                    this._socket.send(webix.stringify({
                        operation: 'login',
                        data: {
                            username: username,
                            password: password,
                        },
                    }))
                });
                return;
            }

            // handle welcome message
            if (data.status === 'welcome') {

                // TODO: move to namespaces app? START
                rs.session_data.ns_id = data.data.ns_id;
                rs.session_data.is_ns_admin = data.data.admin;
                rs.session_data.is_super_user = data.data.super_user;

                let s = $$('core:top:ns-select');
                if (s)
                    s.setValue(data.data.ns_id);
                // TODO: move to namespaces app? END

                // send queued subscribe requests
                if (this._queue)
                    this._queue.forEach(x => this._socket.send(x));
                this._queue = null;

                return;
            }

            if (data.status === 'error') {
                if (p)
                    p.reject(data.error);
                webix.alert({
                    title: 'Error',
                    text: data.error,
                    type: 'alert-error',
                    width: 600,
                });
                return;
            }

            if (p)
                p.resolve(data.data);

            if (!data.event || !data.model)
                return;

            const views = this._models[data.model];
            if (!views)
                return;

            // we introduce a tiny delay before handling event updates to make sure that data returned by
            // an insert operation is handled before its insert event.
            webix.delay(() => {

                views.forEach((view) => {
                    view = $$(view);
                    webix.dp(view).ignore(() => {
                        if (data.event === 'insert')
                            view.exists(data.id) ? view.updateItem(data.id, data.data) : view.add(data.data);
                        else if (data.event === 'update' && view.exists(data.id))
                            view.updateItem(data.id, data.data);
                        else if (data.event === 'delete' && view.exists(data.id))
                            view.remove(data.id);
                    });
                });

            }, this);

        };

        this._models = {};
        this._calls = {};
        this._queue = [];
    }

    // -------------------------------------------------------------------------------------------------------------- //

    connection_lost() {
        if (!rs.session_data.reload_in_progress) {
            webix.alert({
                title: 'Websocket Connection Error',
                text: 'Press OK to reload.',
                type: 'alert-error',
                width: 600,
            }).then(() => location.reload());
        }
    }

    // -------------------------------------------------------------------------------------------------------------- //

    send(data) {

        data.call_id = webix.uid();
        let p = new webix.promise((resolve, reject) => {
            this._calls[data.call_id] = {resolve: resolve, reject: reject};
        });

        if (this._queue === null)
            this._socket.send(webix.stringify(data));
        else
            this._queue.push(webix.stringify(data));

        return p;

    }

    // -------------------------------------------------------------------------------------------------------------- //

    subscribe(model, view_id) {
        if (this._models[model] === undefined)
            this._models[model] = []
        if (this._models[model].length === 0)
            this.send({operation: 'subscribe', model: model});
        this._models[model].push(view_id);
    }

    // -------------------------------------------------------------------------------------------------------------- //

    unsubscribe(model, view_id) {
        if (this._models[model] === undefined || this._models[model].includes(view_id) === false)
            return;
        this._models[model] = this._models[model].filter(x => x !== view_id);
        if (this._models[model].length === 0)
            this.send({operation: 'unsubscribe', model: model});
    }

}

// ------------------------------------------------------------------------------------------------------------------ //
