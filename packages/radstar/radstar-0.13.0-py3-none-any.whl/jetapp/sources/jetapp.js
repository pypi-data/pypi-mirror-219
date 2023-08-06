// ------------------------------------------------------------------------------------------------------------------ //

// Copyright © 2021-2023 Peter Mathiasson
// SPDX-License-Identifier: ISC

// ------------------------------------------------------------------------------------------------------------------ //

import './styles/app.css';
import {JetApp} from 'webix-jet';

import rs from 'radstar';
import TopRouter from 'radstar/router';

// ------------------------------------------------------------------------------------------------------------------ //

class RadstarApp extends JetApp {

    constructor(config) {

        const defaults = {
            id: APPNAME,
            // version: VERSION,
            router: TopRouter,
            debug: !PRODUCTION,
            start: '/top/' + SETTINGS.start_view,
        };

        super({ ...defaults, ...config });

    }

    // -------------------------------------------------------------------------------------------------------------- //

    _loadViewDynamic(url) {
        url = url.replace(/\./g, '/');

        try {
            return require('app/views/' + url);
        } catch (e) {
            if (e.code !== 'MODULE_NOT_FOUND') {
                throw e;
            }
        }

        return require('jet-views/' + url);
    }

}

// ------------------------------------------------------------------------------------------------------------------ //

webix.ready(() => {
    document.title = SETTINGS.title || APPNAME;
    rs.init();
    new RadstarApp().render()
});

// ------------------------------------------------------------------------------------------------------------------ //
