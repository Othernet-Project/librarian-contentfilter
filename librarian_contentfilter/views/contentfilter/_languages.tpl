<%namespace name="forms" file="/ui/forms.tpl"/>

${h.form('post', action=i18n_url('contentfilter:languages'), id='content-filter-languages-form')}
    ${forms.form_message(message)}
    ${forms.hidden('region', h.urlquote(region))}
    <ul>
    % for language in region_languages:
        <li>${forms.checkbox('language', h.urlquote(language), is_checked=language in selected_languages, label=language)}</li>
    % endfor
    </ul>
    <p class="controls">
        <button type="submit">${_("Save settings")}</button>
    </p>
</form>
