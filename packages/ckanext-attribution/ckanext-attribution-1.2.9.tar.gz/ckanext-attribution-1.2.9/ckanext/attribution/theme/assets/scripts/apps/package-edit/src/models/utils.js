import { Model, Relation } from '@vuex-orm/core';
import Meta from './meta';
import cloneDeep from 'lodash.clonedeep';

export default class BaseModel extends Model {
  static updateMeta(itemId, data) {
    return new Promise((resolve, reject) => {
      let item = this.query().with('meta').find(itemId);
      if (!item) {
        reject('Item not found');
      }
      Meta.update({
        where: item.meta.id,
        data: data,
      })
        .then((x) => resolve(x))
        .catch((e) => reject(e));
    });
  }

  static afterCreate(model) {
    let metaRecords = Meta.query()
      .where('item_id', model.id)
      .where('item_type', this.entity)
      .exists();
    if (!metaRecords) {
      Meta.insert({ data: { item_id: model.id, item_type: this.entity } });
    }
  }

  getCopy() {
    // get a clone of all the non-relationship fields
    let clonedValues = cloneDeep(this.$getAttributes());
    let copied = {};
    Object.entries(this.$fields())
      .filter((f) => {
        return !(f[1] instanceof Relation);
      })
      .forEach((f) => {
        copied[f[0]] = clonedValues[f[0]];
      });
    delete copied.id; // don't include the ID - we don't want to update that
    return copied;
  }
}
