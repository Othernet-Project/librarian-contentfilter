<%inherit file="/narrow_base.tpl"/>
<%namespace name="languages" file="_languages.tpl"/>

<%block name="title">
## Translators, used as page title
${_('Content filter')}
</%block>

<div class="languages">
    ${languages.body()}
</div>

