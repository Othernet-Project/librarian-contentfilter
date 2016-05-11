((window, $, templates) ->
  errorMessage = templates.filterError
  container = $ '.content-filter'
  regionFormSelector = '#content-filter-region-form'
  languagesFormSelector = '#content-filter-languages-form'
  fieldSelector = '.o-field'
  regionForm = null
  languagesForm = null

  resizeSection = (form) ->
    form.parents('section').trigger('remax')

  submitForm = (form) ->
    method = form.attr 'method'
    url = form.attr 'action'
    data = form.serialize()
    res = $.ajax({url: url, data: data, type: method})
    res.done (result) ->
      # removes all event handlers automatically
      container.html result
      bindForms()
    res.fail (xhr) ->
      form.prepend errorMessage
      resizeSection(form)

  onSubmit = (e) ->
    e.preventDefault()
    form = $ @
    submitForm form

  onSelect = (e) ->
    e.preventDefault()
    select = $ @
    form = select.parents('form')
    submitForm form

  bindForms = () ->
    # intercept form submission through save button
    languagesForm = $ languagesFormSelector
    languagesForm.on 'submit', onSubmit
    # hide change button and make field use full width
    regionForm = $ regionFormSelector
    regionForm.find(fieldSelector).removeClass('inline-field')
    regionButton = regionForm.find 'button'
    regionButton.hide()
    # bind select element's onchange event to submit automatically
    regionSelect = regionForm.find 'select'
    regionSelect.on 'change', onSelect
    # responses differ in height, so a resize of the section is triggered
    resizeSection(regionForm)

  bindForms()

) this, this.jQuery, this.templates
