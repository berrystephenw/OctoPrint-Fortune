/*
 * View model for OctoPrint-Textapi
 *
 * Author: Stephen Berry
 * License: AGPLv3
 */

$(document).ready(function(){
    $('[tool-tip-toggle="tooltip"]').tooltip({
        placement : 'bottom'
    });
});

$(function() {
    function TextapiViewModel(parameters) {
        var self = this;

        self.settings = parameters[0];

        self.busy = ko.observable(false);

        self.sendTestMessage = function () {
            self.busy(true);
            $.ajax({
                url: API_BASEURL + "plugin/textapi",
                type: "GET",
                dataType: "json",
                data: JSON.stringify({
                    command: "test",
                    /* token: self.settings.settings.plugins.OctoText.access_token(), */
                    channel: self.settings.settings.plugins.textapi.push_message()
                }),
                contentType: "application/json; charset=UTF-8",
                success: function (response) {
                    self.busy(false);
                    if (response.result) {
                        new PNotify({
                            title: gettext("Congratulations!"),
                            text: gettext("A test message was sent to OctoText (through the API), everything appears good on our side. \n\r Give your service a minute to route the text or email to you!"),
                            type: "success"
                        });
                    } else {
                        var text;
                        if (response.error === "NOT_LOADED") {
                            text = gettext("OctoText is either not loaded or an older installation. Requires OctoText 0.3.0 or higher!");
                        } else if (response.error === "NOT_ENABLED") {
                            text = gettext("OctoText is not responding. Is the plugin disabled or older than 0.3.0?");
                        }
                        new PNotify({
                            title: gettext("Test message could not be sent"),
                            text: text,
                            type: "error"
                        });
                    }
                },
                error: function () {
                    self.busy(false);
                }
            });
        };
        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.
    }
    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: TextapiViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ "settingsViewModel", "navigationViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_textapi, #tab_plugin_textapi, ...
        elements: [ "#settings_plugin_textapi", "#navbar_plugin_textapi" ]
    });
});
