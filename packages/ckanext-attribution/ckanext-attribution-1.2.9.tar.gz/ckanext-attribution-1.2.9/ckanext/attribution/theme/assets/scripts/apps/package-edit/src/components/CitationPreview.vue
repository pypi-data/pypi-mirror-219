<template>
  <div class="citation-preview">
    <div class="citation-preview-header">
      <span class="citation-preview-title">Citation preview</span>
      <help-tooltip>
        This is a <em>rough guide</em> to help visualise how changes made to the
        contributors below will affect the citation output.
        <br />
        Only numbered contributors are counted as citeable authors. Click the
        plus icon on the left side of a contributor to make them citeable.
      </help-tooltip>
    </div>
    <div class="citation-preview-body">
      <div class="scroll-select" :style="{ width: selectWidth }">
        <i class="fas fa-angle-left fa-lg" @click="scrollFormat(-1)"></i>
        <span>{{ availableFormats[citationFormat] }}</span>
        <i class="fas fa-angle-right fa-lg" @click="scrollFormat(1)"></i>
      </div>
      <div class="citation-string">
        {{ citation }}
      </div>
    </div>
    <div class="attribution-warning">
      <small>
        <i class="fas fa-warning"></i>
        <em>This is a <b>guide</b>. Do not use this as an actual citation.</em>
        <em v-if="warning">{{ warning }}</em>
      </small>
    </div>
  </div>
</template>

<script>
import { Agent } from '../models/main';
require('@citation-js/plugin-csl'); // this MUST go before the import of @citation-js/core
import { Cite, plugins } from '@citation-js/core';
import { mapState } from 'vuex';
import ieee from '../../vendor/ieee.csl';
import chicago from '../../vendor/chicago-author-date.csl';
import mla from '../../vendor/modern-language-association.csl';

export default {
  name: 'CitationPreview',
  data: function () {
    return {
      etal: false,
      citationFormat: 'apa',
      availableFormats: {
        apa: 'APA',
        vancouver: 'Vancouver',
        harvard1: 'Harvard',
        mla: 'MLA',
        chicago: 'Chicago',
        ieee: 'IEEE',
      },
    };
  },
  computed: {
    ...mapState(['packageDetail', 'results']),
    citedContributors() {
      return Agent.query()
        .with('meta')
        .where('isActive', true)
        .where('citeable', true)
        .get()
        .sort((a, b) => {
          // .orderBy doesn't seem to update automatically but this does
          return a.citation.order - b.citation.order;
        });
    },
    warning() {
      if (this.results.total <= this.results.pageSize) {
        return null;
      }
      let warningString = `This preview only includes the ${this.results.pageSize} contributors on this page; the `;
      let otherContributors = [];
      if (this.results.offset > 0) {
        otherContributors.push(`${this.results.offset} previous`);
      }
      let remaining =
        this.results.total - (this.results.pageSize + this.results.offset);
      if (remaining > 0) {
        otherContributors.push(`${remaining} subsequent`);
      }
      warningString +=
        otherContributors.join(' and ') + ' contributors are not shown.';
      return warningString;
    },
    citation() {
      let contributors = this.citedContributors.map((c) => {
        if (c.agent_type === 'person') {
          return { family: c.family_name, given: c.given_names };
        } else {
          return { literal: c.name };
        }
      });
      let _citation = new Cite({
        type: 'dataset',
        title: this.packageDetail ? this.packageDetail.title : 'Dataset Title',
        author: contributors,
        issued: { 'date-parts': [[new Date().getFullYear()]] },
      });
      return _citation.format('bibliography', {
        template: this.citationFormat,
      });
    },
    selectWidth() {
      // this is a very rough estimate
      let widestText = Object.values(this.availableFormats).sort(
        (a, b) => b.length - a.length,
      )[0];
      return widestText.length * 10 + 20 + 'px';
    },
  },
  methods: {
    scrollFormat(direction) {
      let formatKeys = Object.keys(this.availableFormats);
      let currentIx = formatKeys.indexOf(this.citationFormat);
      if (currentIx === -1) {
        currentIx = 0;
      }
      let newIx = currentIx + direction;
      if (newIx < 0) {
        newIx = formatKeys.length - 1;
      } else if (newIx === formatKeys.length) {
        newIx = 0;
      }
      this.citationFormat = formatKeys[newIx];
    },
  },
  created() {
    let config = plugins.config.get('@csl');
    config.templates.add('ieee', ieee);
    config.templates.add('chicago', chicago);
    config.templates.add('mla', mla);
  },
};
</script>
