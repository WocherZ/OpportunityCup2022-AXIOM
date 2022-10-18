<template>

<div class="q-pa-md">
    <q-table
      title="Patterns description"
      :rows="rows"
      :columns="columns"
      separator="cell"
    />
  </div>

</template>

<script>


const columns = [
  {
    name: 'Pattern №',
    required: true,
    label: 'pattern',
    align: 'center',
    field: 'pattern',
    sortable: true
  },

  { name: 'description', align: 'center', label: 'Description', field: 'description'},
]

const rows = [
    {
        pattern: 0,
        description: "notfraud",
    },
    {
        pattern: 1,
        description: "Some desciption here 1",
    },
    {
        pattern: 2,
        description: "Some desciption here 2",
    },
    {
        pattern: 3,
        description: "Some desciption here 3",
    },
    {
        pattern: 4,
        description: "Some desciption here 4",
    },
    {
        pattern: 5,
        description: "Some desciption here 5",
    },
    {
        pattern: 6,
        description: "Some desciption here 6",
    },

]

export default {
    name: "PatternsGuidePage",
    data() {
        return {
            columns,
            rows
        }
    }

}

</script>