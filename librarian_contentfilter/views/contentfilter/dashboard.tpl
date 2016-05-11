<%namespace name="forms" file="/ui/forms.tpl"/>
<%namespace name="settings" file="_settings.tpl"/>

<div class="content-filter">
    ${settings.body()}
</div>

<script type="text/template" id="filterError">
    <% 
    errors = [_('Operation could not be completed due to application error.')]
    %>
    ${forms.form_errors(errors)}
</script>
