import Vue from 'vue';
import store from './store/main';

const events = {
  saveActivity: 'save-activity',
  saveAgent: 'save-agent',
  closeActivity: 'close-activity',
  removeContributor: 'remove-contributor',
  editsSaved: 'saved',
  editsDone: 'done',
};

const eventBus = new Vue();

eventBus.$on(events.removeContributor, (contributorId) => {
  store.dispatch('removeContributor', contributorId);
});

export { eventBus, events };
