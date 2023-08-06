import Vue from 'vue';
import store from './store/main';
import App from './App.vue';
import Help from './components/fields/Help.vue';
import Field from './components/fields/Field.vue';
import TextField from './components/fields/TextField.vue';
import SelectField from './components/fields/SelectField.vue';
import Autocomplete from './components/fields/Autocomplete.vue';
import AutocompleteList from './components/fields/AutocompleteList.vue';

Vue.component('app', App);

// fields
Vue.component('help-tooltip', Help);
Vue.component('input-field', Field);
Vue.component('text-field', TextField);
Vue.component('select-field', SelectField);
Vue.component('autocomplete-field', Autocomplete);
Vue.component('autocomplete-list', AutocompleteList);

// app
new Vue({
  el: '#contributors',
  store,
});
