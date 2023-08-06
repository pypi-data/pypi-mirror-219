import BaseModel from './utils';
import Activity from './activity';
import Affiliation from './affiliation';
import Meta from './meta';
import Citation from './citation';

export default class Agent extends BaseModel {
  static entity = 'agents';

  static fields() {
    return {
      id: this.attr(null),
      agent_type: this.attr('person'),
      family_name: this.attr(null),
      given_names: this.attr(null),
      given_names_first: this.attr(true),
      name: this.attr(null),
      location: this.attr(null),
      external_id: this.attr(null),
      external_id_scheme: this.attr(null),
      user_id: this.attr(null),
      meta: this.morphOne(Meta, 'item_id', 'item_type'),
      affiliations: this.hasMany(Affiliation, 'agent_id'),
      _activities: this.hasMany(Activity, 'agent_id'),
      _citation: this.hasOne(Citation, 'agent_id'),
    };
  }

  get isActive() {
    let hasActivities = this.activities.length > 0;
    let isShown = Meta.query()
      .where('item_id', this.id)
      .where('item_type', 'agents')
      .where('isShown', true)
      .exists();
    // if this is not a cited author, ignore this (set true); if it is, check that the citation is not hidden
    let citationShown = this.citeable ? this.citation.meta.isShown : true;
    return hasActivities && isShown && citationShown;
  }

  get citation() {
    return Citation.query().with('meta').where('agent_id', this.id).first();
  }

  get citeable() {
    return Citation.query()
      .where('agent_id', this.id)
      .whereHas('meta', (q) => {
        q.where('to_delete', false);
      })
      .exists();
  }

  get standardisedName() {
    // should be the same as in model/agent.py
    if (this.agent_type === 'person') {
      return [this.family_name, this.given_names].join(', ');
    } else {
      return this.displayName;
    }
  }

  get displayName() {
    // should be the same as in model/agent.py
    if (this.agent_type === 'person') {
      let nameParts = [this.given_names, this.family_name];
      return (this.given_names_first ? nameParts : nameParts.reverse()).join(
        ' ',
      );
    } else if (this.agent_type === 'org') {
      let name = this.name;
      if (this.location) {
        name += ` (${this.location})`;
      }
      return name;
    } else {
      return this.name;
    }
  }

  get citationName() {
    if (this.agent_type === 'person') {
      let givenNames = this.given_names
        .split(' ')
        .map((n) => n.slice(0, 1)[0] + '.')
        .join(' ');
      return [this.family_name, givenNames].join(', ');
    } else {
      return this.name;
    }
  }

  get activities() {
    // get only unhidden activities
    // makes it easier to query agents based on activities
    return Activity.query()
      .with('meta')
      .where('agent_id', this.id)
      .whereHas('meta', (q) => {
        q.where('is_hidden', false);
      })
      .get();
  }
}
