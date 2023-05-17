import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        path: '/ ',
        name: "GPU-Monitor",
        children: [
            {
                path: '/',
                name: '首页',
                component: () => import('@/views/gpu_monitor/gpu_monitor'),
            },

        ],
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
