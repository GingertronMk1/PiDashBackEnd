window.axios = require("axios");

import { createApp } from "vue";
import App from "./App.vue";

createApp({}).component("BaseApp", App).mount("#app");

console.log("Mounted");
