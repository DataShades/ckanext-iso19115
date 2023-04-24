ckan.module("iso19115-check-validity", function ($, _) {
  "use strict";

  return {
    options: {
      debug: false,
      id: null,
    },

    initialize: function () {
      $.proxyAll(this, /_on/);
      this.el.on("click", this._onClick);
    },

    _onClick: function () {
      this.sandbox.client.call(
        "GET",
        "iso19115_package_check",
        "?id=" + this.options.id,
        this._onSuccess,
        this._onError
      );
    },

    _onSuccess: function () {
      const target = this.options.target
        ? $(this.options.target)
        : this.sandbox.notify.el;
      const msg = this.create(
        "",
        "Dataset can be converted into valid ISO 19115 XML",
        "info"
      );
      this.report(msg, target);
    },

    _onError: function (err) {
      const target = this.options.target
        ? $(this.options.target)
        : this.sandbox.notify.el;
      const errors = err.responseJSON.error;
      for (let type of Object.keys(errors)) {
        if (type.slice(0, 2) === "__") {
          continue;
        }

        let messages = errors[type];
        if (type === "message") {
          messages = [messages];
        }

        const content = $.map(messages, function (text) {
          return $('<pre class="iso-validation-report">').append(
            $("<code>", { text })
          );
        });
        const msg = this.create(type, content, "error");
        this.report(msg, target);
      }
    },

    report: function (msg, target) {
      target.append(msg.alert());
    },

    create: function (title, message, type) {
      var alert = $(
        '<div class="alert fade show alert-dismissible"><strong></strong></div>'
      );
      alert.addClass("alert-" + (type || "error"));
      alert.find("strong").text(title);

      alert.append(message);
      alert.append(
        '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>'
      );
      return alert;
    },
  };
});
