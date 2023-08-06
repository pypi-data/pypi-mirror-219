import BaseModel from './utils';
import Agent from './agent';
import Meta from './meta';

export default class Activity extends BaseModel {
  static entity = 'activities';

  static fields() {
    return {
      id: this.attr(null),
      activity: this.attr(null),
      scheme: this.attr(null),
      level: this.attr(null),
      time: this.attr(null),
      order: this.attr(null),
      agent_id: this.attr(null),
      packaged_id: this.attr(null),
      agent: this.belongsTo(Agent, 'agent_id'),
      meta: this.morphOne(Meta, 'item_id', 'item_type'),
    };
  }
}
