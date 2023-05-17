import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './assets/tsb.css'
import * as ElIcons from '@element-plus/icons-vue'
// import * as echarts from 'echarts'
import request from './request/request'
// eslint-disable-next-line no-unused-vars
import $ from 'jquery'
import VueClipboards from 'vue-clipboard2'


document.title = "GPU-Monitor"
const app = createApp(App)
for (const icname in ElIcons) {
    app.component(icname, ElIcons[icname])
}


app.config.globalProperties.$http = request
app.use(VueClipboards);
app.use(router)
app.use($)
app.use(ElementPlus, {size: 'default'})
app.mount('#app')


