<%inherit file="/narrow_base.tpl"/>
<%namespace name="regions" file="_regions.tpl"/>

<%block name="title">
## Translators, used as page title
${_('Content filter')}
</%block>

<div class="regions">
    ${regions.body()}
</div>
