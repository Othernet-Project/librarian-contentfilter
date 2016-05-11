<%inherit file="/narrow_base.tpl"/>
<%namespace name="settings" file="_settings.tpl"/>

<%block name="extra_head">
    <link rel="stylesheet" href="${assets['css/contentfilter']}">
</%block>

<%block name="title">
## Translators, used as page title
${_('Content filter')}
</%block>

<div class="content-filter">
    ${settings.body()}
</div>
