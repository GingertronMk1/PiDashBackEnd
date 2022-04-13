<script setup>
  
  import { ref } from "vue";

  const data = ref({
    cpu: {
      url: "/cpu",
      data: {}
    },
    memory: {
      url: "/memory",
      data: {}
    },
    transmission: {
      url: "/transmission",
      data: {}
    }
  });

  Object.entries(data.value).forEach(([key, { url }]) => {
    axios.get(url).then(({ data: returnedData }) => data.value[key].data = returnedData);
  });

</script>
<template>
<h1>Test</h1>
  
</template>