import BaseModel from './utils';
import Agent from './agent';
import Meta from './meta';

export default class Affiliation extends BaseModel {
  static entity = 'affiliations';

  static fields() {
    return {
      id: this.attr(null),
      db_id: this.attr(null),
      agent_id: this.attr(null),
      other_agent_id: this.attr(null),
      affiliation_type: this.attr(null),
      description: this.attr(null),
      start_date: this.attr(null),
      end_date: this.attr(null),
      package_id: this.attr(null),
      agent: this.belongsTo(Agent, 'agent_id'),
      other_agent: this.belongsTo(Agent, 'other_agent_id'),
      meta: this.morphOne(Meta, 'item_id', 'item_type'),
    };
  }
}
