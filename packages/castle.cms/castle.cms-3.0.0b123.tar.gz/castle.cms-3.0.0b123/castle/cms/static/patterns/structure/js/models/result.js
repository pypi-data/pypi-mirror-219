define(['backbone'], function(Backbone) {
  'use strict';

  var Result = Backbone.Model.extend({
    defaults: function() {
      return {
        'is_folderish': false,
        'review_state': '',
        'getURL': ''
      };
    },
    uid: function() {
      return this.attributes.UID;
    }
  });

  return Result;
});
