<%namespace name="regions" file="_regions.tpl"/>
<%namespace name="languages" file="_languages.tpl"/>

${regions.body()}
% if region:
${languages.body()}
% endif
