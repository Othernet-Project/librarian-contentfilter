<%namespace name="forms" file="/ui/forms.tpl"/>
<%namespace name="regions" file="_regions.tpl"/>
<%namespace name="languages" file="_languages.tpl"/>

<div class="content-filter">
    % if region:
        ${languages.body()}
    % else:
        ${regions.body()}
    % endif
</div>

<script type="text/template" id="filterLoadError">
    <% 
    errors = [_('Region list could not be fetched due to application error.')]
    %>
    ${forms.form_errors(errors)}
</script>
<script type="text/template" id="filterSaveError">
    <% 
    errors = [_('Filter settings could not be saved due to application error.')]
    %>
    ${forms.form_errors(errors)}
</script>
