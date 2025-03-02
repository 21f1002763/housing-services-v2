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
            <!-- Check if there's a custom slot for this column -->
            <slot :name="col.key" :row="row">
              {{ row[col.key] }} <!-- Default behavior if no slot is provided -->
            </slot>
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
  table-layout:inherit; /* Fixes column width */
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
