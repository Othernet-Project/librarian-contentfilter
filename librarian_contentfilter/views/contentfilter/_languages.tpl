<%namespace name="forms" file="/ui/forms.tpl"/>

${h.form('post', action=i18n_url('contentfilter:languages'), id='content-filter-form')}
    <p class="selected-region">
        ## Translators, message shows which region was selected previously,
        ## and the below listed languages belong to this specific region
        <span>${_("Available languages for:")}</span>&nbsp;<label>${region}</label>
    </p>
    ${forms.form_message(message)}
    ${forms.hidden('region', h.urlquote(region))}
    <ul>
    % for language in region_languages:
        <li>${forms.checkbox('language', h.urlquote(language), is_checked=language in selected_languages, label=language)}</li>
    % endfor
    </ul>
    <p class="controls">
        <button type="submit">${_("Save")}</button>
        <a id="change-region" class="button" href="${i18n_url('contentfilter:regions')}">${_("Change Region")}</a>
    </p>
<form>
