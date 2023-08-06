// ------------------------------------------------------------------------------------------------------------------ //

// Copyright © 2021-2023 Peter Mathiasson
// SPDX-License-Identifier: ISC

import rs from './index';

// ------------------------------------------------------------------------------------------------------------------ //

const proxy = {
    $proxy: true,

    load: function(view, params) {
        var view_id = view.config.id;

        rs.socket.subscribe(this.source, view_id);
        // TODO: this is not enough. this doesn't catch options for combobox
        view.attachEvent('onDestruct', () => rs.socket.unsubscribe(this.source, view_id));

        return rs.socket.send({
            model: this.source,
            operation: 'list',
            data: params
        });
    },

    save: function(view, update, dp) {
        update.model = this.source;
        return rs.socket.send(update);
    }
};

export default proxy;

// ------------------------------------------------------------------------------------------------------------------ //
