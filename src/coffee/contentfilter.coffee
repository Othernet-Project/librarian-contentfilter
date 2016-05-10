((window, $, templates) ->
  loadErrorMessage = templates.filterLoadError
  saveErrorMessage = templates.filterSaveError
  formSelector = '#content-filter-form'
  changeRegionSelector = '#change-region'
  form = null
  url = null

  changeRegion = (e) ->
    e.preventDefault()
    el = $ @
    regionsUrl = el.attr 'href'
    res = $.get regionsUrl
    res.done (data) ->
      # removes all event handlers automatically
      form.replaceWith data
      bindForm()
    res.fail () ->
      form.prepend loadErrorMessage

  submitData = (data) ->
    res = $.post url, data
    res.done (data) ->
      # removes all event handlers automatically
      form.replaceWith data
      bindForm()
    res.fail () ->
      form.prepend saveErrorMessage

  onSubmit = (e) ->
    e.preventDefault()
    data = form.serialize()
    submitData data

  bindForm = () ->
    form = $ formSelector
    url = form.attr 'action'
    form.on 'submit', onSubmit
    form.parents('section').trigger('remax')
    $(changeRegionSelector).on 'click', changeRegion

  bindForm()

) this, this.jQuery, this.templates
