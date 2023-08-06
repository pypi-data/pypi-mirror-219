this.list = this.list || {};
/**
 * NHMMap
 *
 * Custom backbone view to display the Windshaft based maps.
 */
(function (my, $) {
  var self;

  my.ListView = Backbone.View.extend({
    className: 'list-view',

    /**
     * Initialize
     */
    initialize: function () {
      self = this;
      self.el = $(self.el);
      self.el.ready(this._onReady);
      // We regex to get field labels, which we'll speed up by caching
      self._fieldLabelCache = {};
    },

    _onReady: function () {
      var resourceData = self.options.resource,
        resourceView = self.options.resourceView;

      self.loadView(resourceData, resourceView);
    },

    loadView: function (resourceData, resourceView) {
      var self = this;

      resourceData.url = this.normalizeUrl(resourceData.url);
      if (resourceData.formatNormalized === '') {
        var tmp = resourceData.url.split('/');
        tmp = tmp[tmp.length - 1];
        tmp = tmp.split('?'); // query strings
        tmp = tmp[0];
        var ext = tmp.split('.');
        if (ext.length > 1) {
          resourceData.formatNormalized = ext[ext.length - 1];
        }
      }

      var dataset;

      resourceData.backend = 'ckan';
      resourceData.endpoint = jQuery('body').data('site-root') + 'api';

      resourceData.fields = ['barcode', 'basisOfRecord'];

      dataset = new recline.Model.Dataset(resourceData);

      var query = new recline.Model.Query();
      query.set({ size: resourceView.limit || 100 });
      query.set({ from: resourceView.offset || 0 });
      if (window.parent.ckan.views && window.parent.ckan.views.filters) {
        var defaultFilters = resourceView.filters || {},
          urlFilters = window.parent.ckan.views.filters.get(),
          filters = $.extend({}, defaultFilters, urlFilters);
        $.each(filters, function (field, values) {
          query.addFilter({ type: 'term', field: field, term: values });
        });
        if (window.parent.ckan.views.filters._searchParams.q) {
          query.set({ q: window.parent.ckan.views.filters._searchParams.q });
        }
      }
      dataset.queryState.set(query.toJSON(), { silent: true });
      self.render(dataset, resourceView);
      // On query state change (user has changed page)
      this.listenTo(dataset.queryState, 'change', function () {
        self.render(dataset, resourceView);
      });
    },

    render: function (dataset, resourceView) {
      var errorMsg =
        this.options.i18n.errorLoadingPreview +
        ': ' +
        this.options.i18n.errorDataStore;
      dataset
        .fetch()
        .done(function (dataset) {
          self.initializeView(dataset, resourceView);
        })
        .fail(function (error) {
          if (error.message) errorMsg += ' (' + error.message + ')';
          self.showError(errorMsg);
        });
    },

    showError: function (msg) {
      msg = msg || _('error loading view');
      window.parent.ckan.pubsub.publish('data-viewer-error', msg);
    },

    normalizeUrl: function (url) {
      if (url.indexOf('https') === 0) {
        return 'http' + url.slice(5);
      } else {
        return url;
      }
    },

    /**
     * Given the record data and the resourceView info, extracts a single representative image
     * to display. The return is an object in the correct format for the mustache template.
     *
     * @param data the record data
     * @param resourceView the resourceView settings
     * @returns {null|{identifier, title}|*} either null if no image exists or an object with
     *                                       identifier and title attributes as per the mustache
     *                                       template.
     * @private
     */
    _extractImage(data, resourceView) {
      const images = data.attributes[resourceView.image_field];
      if (!images) {
        return null;
      }

      function fromString(source) {
        return { identifier: source, title: source };
      }

      function fromObject(source) {
        // remove the _id from the image (if present) so that mustache template renders
        // correctly - specifically so that the href in the a tag surrounding the actual
        // image goes to the record not the image's _id if indeed there is one defined
        delete source._id;
        return source;
      }

      switch ($.type(images)) {
        case 'string':
          let url = images;
          // if there is a delimiter specified, use it to split the string and then use
          // the first element
          if (!!resourceView.image_delimiter) {
            url = images.split(resourceView.image_delimiter)[0];
          }
          return fromString(url);
        case 'array':
          if ($.type(images[0]) === 'string') {
            // just use the first string in the list
            return fromString(images[0]);
          } else {
            // by default, we'll use the first image for the record
            let imageIndex = 0;
            // if there are multiple images available, see if there's a "specimen" image
            // and use it if so
            if (images.length > 1) {
              const spIndex = images.findIndex(
                (image) => image.category === 'Specimen',
              );
              if (spIndex !== -1) {
                imageIndex = spIndex;
              }
            }
            return fromObject(images[imageIndex]);
          }
        default:
          return fromObject(images);
      }
    },

    initializeView: function (dataset, resourceView) {
      var controls = [
        new recline.View.Pager({ model: dataset }),
        new recline.View.RecordCount({ model: dataset }),
      ];
      if (
        typeof dataset.recordCount == 'undefined' ||
        dataset.recordCount == 0
      ) {
        self.el.html('<p class="recline-norecords">No matching records</p>');
      } else {
        var record;
        var recordUrl = this.options.recordUrl;
        var records = dataset.records.models.map(function (data) {
          record = {
            _id: data.attributes._id,
            attributes: [],
            url: recordUrl.replace(/REPLACEME/g, data.attributes._id),
          };
          // Add title
          if (resourceView.title_field) {
            record.title = data.attributes[resourceView.title_field];
            if (!record.title && resourceView.secondary_title_field) {
              record.title =
                data.attributes[resourceView.secondary_title_field];
            }
          }
          // Add image
          if (resourceView.image_field) {
            const image = self._extractImage(data, resourceView);
            if (!!image) {
              record.image = image;
            }
          }
          $.each(resourceView.fields, function (_, fieldName) {
            if (data.attributes[fieldName]) {
              record.attributes.push({
                label: self.fieldNameToLabel(fieldName),
                value: data.attributes[fieldName],
              });
            }
          });
          return record;
        });
        var data = {
          records: records,
          resourceView: resourceView,
          versionPart: self._getVersionPart(),
        };

        $.get('/mustache_templates/list.mustache', function (template) {
          var newElements = $('<div />');
          self._renderControls(newElements, controls);
          newElements.append(Mustache.render(template, data));
          self.el.html(newElements);
        });
      }
    },

    /**
     * Retrieve a version value, if there is one, from the filters in the query string for use
     * in the record URL. We look for the filters __version__ value instead of using the top
     * level version query string parameter as this plugin isn't compatible with the version
     * parameter yet due to the way CKAN handlers query strings. If no version is found in the
     * filters, an empty string is returned. If there is a version found the format of the
     * response is "/<version>".
     *
     * @returns {string}
     * @private
     */
    _getVersionPart: function () {
      // see if we can use ckan core code to get to the filters
      if (window.parent.ckan.views && window.parent.ckan.views.filters) {
        // get the version if it's there
        let version = window.parent.ckan.views.filters.get('__version__');
        // if the version isn't present we get back undefined
        if (typeof version !== 'undefined') {
          // version will be an array, get the first element as there should only ever be
          // one
          return '/' + version[0];
        }
      }
      return '';
    },

    _renderControls: function (el, controls) {
      var controlsEl = $('<div class="clearfix controls" />');
      for (var i = 0; i < controls.length; i++) {
        controlsEl.append(controls[i].el);
      }
      $(el).append(controlsEl);
    },

    fieldNameToLabel: function (fieldName) {
      // If the field label does exists in the cache, create it
      if (!(fieldName in self._fieldLabelCache)) {
        var fieldLabel;
        // If fieldName is all in caps, treat it as an acronym; do not format
        if (fieldName.replace(/[A-Z]/g, '').length == 0) {
          fieldLabel = fieldName;
        } else {
          // Otherwise, split field on capital letters...
          fieldLabel = fieldName.replace(/([A-Z])/g, ' $1');
          // ... and capitalise the first letter
          fieldLabel = fieldLabel.charAt(0).toUpperCase() + fieldLabel.slice(1);
        }
        // Cache the label
        self._fieldLabelCache[fieldName] = fieldLabel;
      }
      return self._fieldLabelCache[fieldName];
    },
  });
})(this.list, jQuery);
