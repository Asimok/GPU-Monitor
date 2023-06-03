import axios from 'axios'

const request = axios.create({
    baseURL: 'http://219.216.64.197:7030', //197服务器
    // baseURL: 'http://127.0.0.1:7030',
    timeout: 10000,
})
// request 拦截器
request.interceptors.request.use(config => {
    config.headers['Content-Type'] = 'application/json;charset=utf-8';
    return config
}, error => {
    return Promise.reject(error)
});
export default request
