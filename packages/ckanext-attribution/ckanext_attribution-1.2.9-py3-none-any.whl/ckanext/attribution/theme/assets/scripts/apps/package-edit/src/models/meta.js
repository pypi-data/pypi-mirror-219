import { Model } from '@vuex-orm/core';

export default class Meta extends Model {
  static entity = 'metadata';

  static fields() {
    return {
      id: this.uid(),
      item_id: this.attr(null),
      item_type: this.attr(null),
      is_hidden: this.boolean(false), // do not show with other items
      is_editing: this.boolean(false), // is currently being edited
      to_delete: this.boolean(false), // delete when saved
      is_dirty: this.boolean(false), // has been edited
      syncing: this.boolean(false), // currently downloading from external source
      is_new: this.boolean(false), // is a new item
      is_temporary: this.boolean(false), // is a temporary item that won't be saved
      is_saved_edit: this.boolean(false), // is an edited item from another page
      item: this.morphTo('item_id', 'item_type'),
    };
  }

  get isShown() {
    return !this.is_hidden && !this.to_delete;
  }
}
