// Generated by CoffeeScript 1.10.0
(function(window, $, templates) {
  var bindForms, container, errorMessage, languagesForm, languagesFormSelector, onSelect, onSubmit, regionForm, regionFormSelector, resizeSection, submitForm;
  errorMessage = templates.filterError;
  container = $('.content-filter');
  regionFormSelector = '#content-filter-region-form';
  languagesFormSelector = '#content-filter-languages-form';
  regionForm = null;
  languagesForm = null;
  resizeSection = function(form) {
    return form.parents('section').trigger('remax');
  };
  submitForm = function(form) {
    var data, method, res, url;
    method = form.attr('method');
    url = form.attr('action');
    data = form.serialize();
    res = $.ajax({
      url: url,
      data: data,
      type: method
    });
    res.done(function(result) {
      container.html(result);
      return bindForms();
    });
    return res.fail(function(xhr) {
      form.prepend(errorMessage);
      return resizeSection(form);
    });
  };
  onSubmit = function(e) {
    var form;
    e.preventDefault();
    form = $(this);
    return submitForm(form);
  };
  onSelect = function(e) {
    var form, select;
    e.preventDefault();
    select = $(this);
    form = select.parents('form');
    return submitForm(form);
  };
  bindForms = function() {
    var regionButton, regionSelect;
    languagesForm = $(languagesFormSelector);
    languagesForm.on('submit', onSubmit);
    regionForm = $(regionFormSelector);
    regionButton = regionForm.find('button');
    regionSelect = regionForm.find('select');
    regionButton.hide();
    regionSelect.on('change', onSelect);
    regionForm.parents('section').trigger('remax');
    return resizeSection(regionForm);
  };
  return bindForms();
})(this, this.jQuery, this.templates);
