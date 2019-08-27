odoo.define('hq_product.search_inputs', function (require) {
    "use strict";
    /*---------------------------------------------------------
     * Odoo Pivot Table view of sale report
     *---------------------------------------------------------*/

    var data = require('web.data');
    var SearchInputs = require('web.search_inputs');
    var Field = SearchInputs.Field;

    Field.include({
        get_domain: function (facet) {
            if (!facet.values.length) {
                return;
            }

            var value_to_domain;
            var self = this;
            var domain = this.attrs.filter_domain;
            if (domain) {
                value_to_domain = function (facetValue) {
                    return new data.CompoundDomain(domain)
                        .set_eval_context({self: self.value_from(facetValue)});
                };
            } else {
                value_to_domain = function (facetValue) {
                    return self.make_domain(
                        self.attrs.name,
                        self.attrs.operator || self.default_operator,
                        facetValue);
                };
            }
            var domains = facet.values.map(value_to_domain);

            if (domains.length === 1) {
                return domains[0];
            }
            if (self.attrs.name === 'name' && self.attrs.context && self.attrs.context.separator === 'and') {
                return _.extend(new data.CompoundDomain(), {
                    __domains: domains
                });
            }
            for (var i = domains.length; --i;) {
                domains.unshift(['|']);
            }

            return _.extend(new data.CompoundDomain(), {
                __domains: domains
            });
        }
    });

});
