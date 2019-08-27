/**
 * Created by wangjunfu on 2017/8/29.
 */
odoo.define('hq_product.pop_window', function (require) {
    "use strict";
    // 修改
    var Dialog = require('web.Dialog');
    var list_view = require('web.ListView');

    list_view.include({
        do_archive_selected: function () {
            var mythis= this;
            Dialog.confirm(this,"被存档的内容将被隐藏，是否继续？", {
                confirm_callback: function() {
                    var records = mythis.groups.get_selection().records;
                    mythis.do_archive(records, true);
                },
                title: "存档",
            });
        }
    });
});