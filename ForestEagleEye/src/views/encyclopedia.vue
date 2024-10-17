<template>
<div id="app">
  <table>
    <thead>
      <tr>
        <th>字段 1</th>
        <th>字段 2</th>
        <th>操作</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in dataList" :key="item.id">
        <td v-if="!isEditing(item.id)">{{ item.field1 }}</td>
        <td v-if="!isEditing(item.id)">{{ item.field2 }}</td>
        <td>
          <button @click="toggleEdit(item.id)">编辑</button>
        </td>
        <td v-if="isEditing(item.id)">
          <input v-model="editedItem.field1" />
        </td>
        <td v-if="isEditing(item.id)">
          <input v-model="editedItem.field2" />
        </td>
        <td v-if="isEditing(item.id)">
          <button @click="saveEdit(item.id)">保存</button>
          <button @click="cancelEdit(item.id)">取消</button>
        </td>
      </tr>
    </tbody>
  </table>
</div>  </template>
  
  <script>
  import NavigationBar from '../components/navbar.vue'
  
  export default {
    name: 'encyclopedia',
    components: {
      NavigationBar
    },
    data() {
      return {
        dataList: [
          { id: 1, field1: '数据 1', field2: '数据 2' },
          // 更多数据项...
        ],
        editingId: null,
        editedItem: {}
      };
    },
    methods: {
    isEditing(id) {
      return this.editingId === id;
    },
    toggleEdit(id) {
      this.editingId = id;
      this.editedItem = {...this.dataList.find(item => item.id === id) };
    },
    saveEdit(id) {
      const index = this.dataList.findIndex(item => item.id === id);
      this.dataList[index] = {...this.editedItem };
      this.editingId = null;
    },
    cancelEdit(id) {
      this.editingId = null;
    }
  }
};
  </script>
  
  <style scoped>
  </style>