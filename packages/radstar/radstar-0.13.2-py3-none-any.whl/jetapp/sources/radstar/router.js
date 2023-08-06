// ------------------------------------------------------------------------------------------------------------------ //

// Copyright © 2021-2023 Peter Mathiasson
// SPDX-License-Identifier: ISC

// ------------------------------------------------------------------------------------------------------------------ //

export default class TopRouter {

    constructor(cb, config) {
        this.config = config || {};
        this.prefix = document.location.href.split('#', 2)[0];
        this.suffix = '#';
        this.cb = cb;
        window.onpopstate = () => this.cb(this.get());
    }

    set(path, config) {
        if (path.startsWith('/top/'))
            path = path.substring(4);

        if (this.get() !== path)
            window.history.pushState(null, null, this.prefix + this.suffix + path);

        if (!config || !config.silent)
            setTimeout(() => this.cb(path), 1);
    }

    get() {
        let path = document.location.href.replace(this.prefix, '').replace(this.suffix, '');
        if (path === '' || path === '/' || path === '#')
            return '';
        return '/top' + path;
    }
}

// ------------------------------------------------------------------------------------------------------------------ //
