((window, $, templates) ->
  errorMessage = templates.filterError
  container = $ '.content-filter'
  regionFormSelector = '#content-filter-region-form'
  languagesFormSelector = '#content-filter-languages-form'
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
    languagesForm = $ languagesFormSelector
    languagesForm.on 'submit', onSubmit
    regionForm = $ regionFormSelector
    regionForm.find('o-field').removeClass('inline-field')
    regionButton = regionForm.find 'button'
    regionSelect = regionForm.find 'select'
    regionButton.hide()
    regionSelect.on 'change', onSelect
    regionForm.parents('section').trigger('remax')
    resizeSection(regionForm)

  bindForms()

) this, this.jQuery, this.templates
