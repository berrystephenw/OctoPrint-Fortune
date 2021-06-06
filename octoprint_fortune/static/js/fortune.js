/*
 * View model for OctoPrint-Fortune
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
    function FortuneViewModel(parameters) {
        var self = this;
        self.settings = parameters[1];

        self.onUserLoggedIn = function(user) {
            self.yourFortune();
        };

        self.yourFortune = function () {
            $.ajax({
                url: API_BASEURL + "plugin/fortune",
                type: "GET",
                dataType: "json",
                data: "test", // {
                    //command: "test",
                    /* token: self.settings.settings.plugins.OctoText.access_token(), */
                    //channel: 1
                //},
                contentType: "application/json; charset=UTF-8",
                success: function (response) {
                    if (response.result) {
                        new PNotify({
                            title: gettext("Your Fortune!"),
                            text: gettext(response.data),
                            type: "success",
                            // adding both string lengths, parseInt in case something wonky is in response, 55ms per letter read time, additional 100ms as reaction speed to notice the popup and move your eyes there
                            delay: parseInt(gettext("Your Fortune!").length + gettext(response.data).length) * 55 + 100
                        });
                    } else {
                        var text;

                        text = gettext("Sorry, no fortune for you today!");

                        new PNotify({
                            title: gettext("Something went wrong"),
                            text: text,
                            type: "error"
                        });
                    }
                },
            });
        };
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: FortuneViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: ["navigationViewModel", "settingsViewModel"],
        // Elements to bind to, e.g. #settings_plugin_fortune, #tab_plugin_fortune, ...
        elements: ["#navbar_plugin_fortune", "#settings_plugin_fortune"]
    });
});
