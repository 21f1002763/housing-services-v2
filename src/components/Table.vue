<template>
  <div class="table-responsive">
    <table class="table text-center">
      <thead class="table-light">
        <tr>
          <th v-for="col in columns" :key="col.key" class="text-center text-capitalize">
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in data" :key="row.id">
          <td v-for="col in columns" :key="col.key">
            {{ row[col.key] }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    columns: { type: Array, required: true },
    data: { type: Array, required: true }
  }
};
</script>

<style scoped>
/* Ensure equal column width */
table {
  table-layout: fixed; /* Fixes column width */
  width: 100%;
}
th{
  background-color: #483434;
  color: #ffff;
  font-weight: bold;
}
th, td {
  text-align: center;
  vertical-align: middle;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
