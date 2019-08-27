/**
 * Created by wangjunfu on 2017/8/30.
 */
odoo.define('hq_product.pop_window_dataexport', function (require) {
    "use strict";

    var core = require('web.core');
    var crash_manager = require('web.crash_manager');
    var data = require('web.data');
    var Dialog = require('web.Dialog');
    var framework = require('web.framework');
    var pyeval = require('web.pyeval');
    var DataExport = require('web.DataExport');
    var QWeb = core.qweb;
    var _t = core._t;

    DataExport.include({
        show_exports_list: function() {
            if (this.$('.o_exported_lists_select').is(':hidden')) {
            this.$('.o_exported_lists').show();
            return $.when();
        }

        var self = this;
        return this.exports.read_slice(['name'], {
            domain: [['resource', '=', this.dataset.model]]
        }).then(function (export_list) {
            if (!export_list.length) {
                return;
            }
            self.$('.o_exported_lists').append(QWeb.render('Export.SavedList', {'existing_exports': export_list}));
            self.$('.o_exported_lists_select').on('change', function() {
                self.$fields_list.empty();
                var export_id = self.$('.o_exported_lists_select option:selected').val();
                if(export_id) {
                    self.rpc('/web/export/namelist', {
                        model: self.dataset.model,
                        export_id: parseInt(export_id, 10),
                    }).then(do_load_export_field);
                }
            });
            self.$('.o_delete_exported_list').click(function() {
                Dialog.confirm(this,'是否删除！',{
                confirm_callback: function () {
                        var select_exp = self.$('.o_exported_lists_select option:selected');
                        if(select_exp.val()) {
                            self.exports.unlink([parseInt(select_exp.val(), 10)]);
                            select_exp.remove();
                            self.$fields_list.empty();
                            if (self.$('.o_exported_lists_select option').length <= 1) {
                                self.$('.o_exported_lists').hide();
                            }
                        }
                    },
                    title: "删除！",
                });
            });
        });

        function do_load_export_field(field_list) {
            _.each(field_list, function (field) {
                self.$fields_list.append(new Option(field.label, field.name));
            });
        }
        }
    });
});
