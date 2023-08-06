// ------------------------------------------------------------------------------------------------------------------ //

// Copyright © 2021-2023 Peter Mathiasson
// SPDX-License-Identifier: ISC

// ------------------------------------------------------------------------------------------------------------------ //

export default function login_window(do_login_func) {

    let form_id = webix.uid();

    let popup = webix.ui({
        view: 'window',
        head: 'Login Required',
        modal: true,
        position: 'center',
        // position: function(state) {
        //     state.top = 5;
        // },
        body: {
            view: 'form',
            id: form_id,
            width: 400,
            rows: [
                {
                    view: 'text',
                    name: 'login',
                    label: 'User Name',
                    labelPosition: 'top'
                },
                {
                    view: 'text',
                    type: 'password',
                    name: 'password',
                    label: 'Password',
                    labelPosition: 'top'
                },
                {
                    view: 'button',
                    value: 'Login',
                    click: function() {
                        const form = $$(form_id);
                        if (form.validate()) {
                            const data = form.getValues();
                            do_login_func(data.login, data.password);
                            popup.close();
                        }
                    },
                    hotkey: 'enter'
                },
            ],
            rules: {
                login: webix.rules.isNotEmpty,
                password: webix.rules.isNotEmpty,
            },
        },
    });

    popup.show();
    $$(form_id).focus();

}

// ------------------------------------------------------------------------------------------------------------------ //
