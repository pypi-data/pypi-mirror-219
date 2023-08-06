this.list = this.list || {};

this.ckan.module('list', function ($, _) {
  function initialize() {
    this.view = new list.ListView({
      resource: JSON.parse(this.options.resource),
      resourceView: JSON.parse(this.options.resourceView),
      recordUrl: this.options.recordUrl,
      i18n: this.options.i18n,
    });
    $(this.el).append(this.view.el);
  }

  return {
    initialize: initialize,
    options: {
      resource: null,
      resourceView: null,
      i18n: {
        errorLoadingPreview: 'Could not load view',
        errorDataProxy: 'DataProxy returned an error',
        errorDataStore: 'DataStore returned an error',
        previewNotAvailableForDataType: 'View not available for data type: ',
        noRecords: 'No matching records',
      },
    },
  };
});
