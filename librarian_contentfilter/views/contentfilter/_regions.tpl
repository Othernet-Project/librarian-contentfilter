<%namespace name="forms" file="/ui/forms.tpl"/>

${h.form('get', action=i18n_url('contentfilter:languages'), id='content-filter-region-form')}
    ${forms.form_errors([form.error]) if form.error else ''}
    ${forms.field(form.region)}
    <p class="controls">
        <button type="submit">${_("Change")}</button>
    </p>
</form>
