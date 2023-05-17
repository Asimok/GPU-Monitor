// @vue/component
import {ElMessage, ElMessageBox} from "element-plus";
import * as echarts from "echarts";
// import zhCn from "element-plus/lib/locale/lang/zh-cn";
import {
    ArrowRight,
    CaretBottom,
    CaretTop, ChatLineRound, Male,
    Warning,
} from '@element-plus/icons'


export default {
    name: 'Gpu_monitor',

    components: {ChatLineRound, Male, CaretBottom, Warning, ArrowRight, CaretTop},

    mixins: [],

    props: {},

    data() {
        return {
            clickCount: 0,
            clickCount_for_stop_mc: 0,
            easterEggVisible: false,
            sysInfoTimer: null,
            sysInfoShowDialog: false,
            sysInfoTimeout: 20 * 1000, //20s
            sysInfoTimeoutLimit: 5 * 60 * 1000,// 5min
            sysInfoDialogMessage: '您已经 20 秒没进行任何操作了, 服务已自动挂起!',
            get_gpu_status_time_gap: 2000,
            get_server_data_timer: null,
            gup_data: [],
            open_pro_box: false,
            open_log_drawer: false,
            open_log_box: false,
            pro_detail: {},
            input_cmd: '',
            activeName: 'All',
            // activeName: 'watcher',
            tags: ['', 'success', 'warning', 'danger', '', 'success', 'warning', 'danger', ''],
            tags_effect: ['dark', 'dark', 'dark', 'dark', 'light', 'light', 'light', 'light', 'plain'],
            total_pro: [],//进程数
            log_cmd: '日志系统',
            log_form: {
                "server_name": '',
                "pid": '',
                "cmd": ''
            },
            select_log: {
                "server_name": '',
                "pid": '',
            },
            //系统监测模块
            user_data: {
                //今日访问用户数量
                today_online_user_nums: 100,
                //相比昨日
                compare_yesterday: 1,
                compare_yesterday_value: "10%",
                //本月用户访问量
                month_online_user_nums: 210,
                //相比上月
                compare_last_month: 0,
                compare_last_month_value: "10%",
                //历史访问用户
                history_online_user_nums: 10021,

            },
            //本月活跃ip散点图
            his_ip_data: {},
            //系统更新日志
            update_log_data: [
                {
                    "timestamp": "2023-05-17",
                    "title": "v4.1",
                    "info": ["新增 系统监测模块,可展示历史ip访问统计", "新增 更新日志模块,展示版本迭代记录", "新增前端挂起后,用户手动激活每次延时1min, 上限5min, 超时自动挂起", "实现ip监控页面显示大小和颜色随访问次数动态变化", "优化数据库锁设计", "修复其他已知bug"]
                },
                {
                    "timestamp": "2023-05-14",
                    "title": "v4.0 史诗级重构",
                    "info": ["重构后端,实现多线程调度", "接口长时间无人访问,线程休眠,释放大量cpu资源,等待用户唤醒", "前端新增 服务器性能监管, 长时间未操作自动挂起, 需手动唤醒", "修复其他已知bug"]
                },
                {
                    "timestamp": "2023-04-13",
                    "title": "v3.0",
                    "info": ["新增 彩蛋(需要各位探索触发彩蛋)", "修复 日志系统bug", "修复其他已知bug"]
                },
                {
                    "timestamp": "2023-03-10",
                    "title": "v2.1",
                    "info": ["系统资源占用优化 降低查询频率", "修复已知bug"]
                },
                {
                    "timestamp": "2023-01-11",
                    "title": "v2.0",
                    "info": ["新增 日志系统", "新增 一键复制 进程号 和 程序运行命令 到剪切板", "修复已知bug"]
                },
                {
                    "timestamp": "2023-01-10",
                    "title": "v1.2",
                    "info": ["新增 进程创建时间 和 运行时间"]
                },
                {
                    "timestamp": "2023-01-10",
                    "title": "v1.1",
                    "info": ["新增 显示程序运行时间"]
                },
                {
                    "timestamp": "2023-01-09",
                    "title": "v1.0 船新版本上线",
                    "info": ["重构老版本GPUMonitor前端", "重构老版本GPUMonitor后端", "新增197和204两台服务器"]
                }
            ],
        }
    },

    computed: {},

    watch: {},

    created() {
    },
    mounted() {
        //初始化Echarts
        this.initEcharts()

        this.get_gpu_status()
        this.get_ip_data()
        this.get_statistics()
        // 监听后端数据
        this.get_server_data_timer = setInterval(() => {
            this.get_server_data()
        }, this.get_gpu_status_time_gap);
        //监听彩蛋
        this.egg_timer = setInterval(() => {
            this.clickCount = 0
        }, 1000);
        // 开始计时
        this.sysInfoTimer = setTimeout(this.showDialogBox, this.sysInfoTimeout)

        // 添加事件监听
        document.addEventListener('click', this.resetTimer)
        document.addEventListener('mousemove', this.resetTimer)
        document.addEventListener('keydown', this.resetTimer)


    },
    beforeDestroy() {
        // 页面销毁时, 移除事件监听
        document.removeEventListener('click', this.resetTimer)
        document.removeEventListener('mousemove', this.resetTimer)
        document.removeEventListener('keydown', this.resetTimer)
        //清除彩蛋计时器
        clearInterval(this.egg_timer)
    },
    methods: {
        resetTimer() {
            clearTimeout(this.sysInfoTimer) // 清除计时器
            this.sysInfoTimeout += 60 * 1000 //每次延时1min
            this.sysInfoTimeout = Math.min(this.sysInfoTimeout, this.sysInfoTimeoutLimit)
            this.sysInfoTimer = setTimeout(this.showDialogBox, this.sysInfoTimeout) // 开始新的计时
        },
        showDialogBox() {
            this.sysInfoShowDialog = true // 显示对话框
            clearInterval(this.get_server_data_timer)

        },
        closeTimerDialog() {
            this.sysInfoShowDialog = false // 关闭对话框
            this.get_server_data_timer = setInterval(() => {
                this.get_server_data()
            }, this.get_gpu_status_time_gap);
        },

        runMC() {
            console.log("启动mc")
            this.$http
                .get("/runMC")
                .then((res) => {
                    // console.log(res)
                    if (res.status === 200) {
                        console.log("runMC", res.data)
                        ElMessage.success("MC启动成功！");
                    }
                })
                .catch(() => {
                    ElMessage.error("MC启动失败！请重试！");
                });
        },
        stopMC() {
            console.log("关闭mc")
            this.$http
                .get("/stopMC")
                .then((res) => {
                    // console.log(res)
                    if (res.status === 200) {
                        console.log("stopMC", res.data)
                        ElMessage.success("MC关闭成功！");
                    }
                })
                .catch(() => {
                    ElMessage.error("MC关闭失败！请重试！");
                });
        },
        handleClick() {
            this.clickCount++;
            console.log(this.clickCount)
            if (this.clickCount === 6) {
                this.easterEggVisible = true;
                this.clickCount = 0;  // 重置计数器
            }
        },
        handleClick_closeMC() {
            this.clickCount_for_stop_mc++;
            console.log(this.clickCount_for_stop_mc)
            if (this.clickCount_for_stop_mc === 6) {
                this.clickCount_for_stop_mc = 0;  // 重置计数器
                this.stopMC()
            }
        },
        closeDialog() {
            this.handleClose()
        },
        handleClose() {
            ElMessageBox.confirm('真的不玩儿一把黑磊强烈推荐的MC吗?', '黒磊からの強い慰留',
                {
                    confirmButtonText: '玩玩玩！',
                    cancelButtonText: '狗都不玩！',
                    closeOnClickModal: false
                })
                .then(() => {
                    this.easterEggVisible = false;
                    console.log('玩玩玩')
                    this.runMC()
                })
                .catch(() => {
                    this.easterEggVisible = false;
                    console.log('狗都不玩')
                })
        },
        get_gpu_status() {
            this.$http
                .get("/get_gpu_state")
                .then((res) => {
                    // console.log(res)
                    if (res.status === 200) {
                        this.gup_data = res.data
                        // console.log('gup_data : ', this.gup_data)
                        // this.gpu_info = this.gup_data[2]
                        // // console.log("this.gpu_info.gpu_list[0].temp:", parseInt(this.gpu_info.gpu_list[0].temp))
                        //计算每个GPU进程数
                        this.total_pro = []
                        //初始化 this.total_pro
                        for (let i = 0; i < this.gup_data.length; i++) {
                            this.total_pro.push(0)
                        }
                        // console.log(this.total_pro)
                        for (let i = 0; i < this.gup_data.length; i++) {
                            for (let j = 0; j < this.gup_data[i].gpu_list.length; j++) {
                                this.total_pro[i] += this.gup_data[i].gpu_list[j].program_list.length
                            }
                        }

                        // 解析选中tag数据
                        this.update_tag(this.gup_data)
                        // console.log(this.total_pro)
                    }
                })
                .catch(() => {
                    ElMessage.error("数据加载失败,请刷新！");
                });

        },
        gen_title(num) {
            return "GPU-" + num
        },
        //计算内存占用百分比 保留整数位
        cal_memory_usage(used, total) {
            return parseInt(used / total * 100)
        },
        //计算用户资源占用
        get_user_usage(pro, total) {
            return pro.username + ": " + parseInt(pro.use_memory / total * 100) + "%"
        },
        get_user_usage_detail(pro, server_name, total, gpu_num) {
            return "GPU " + gpu_num + " " + pro.username + " " + parseInt(pro.use_memory / total * 100) + "%" + " " + pro.duration
        },
        //查看进程详情
        get_pro_detail(pro_info, server_name, total_memory, gpu_num) {
            this.open_pro_box = true
            this.select_log = {
                "server_name": '',
                "pid": '',
            }
            this.select_log.server_name = server_name
            this.select_log.pid = pro_info.pid
            this.update_pro_detail(pro_info, server_name, total_memory, gpu_num)
        },
        //更新进程
        update_pro_detail(pro_info, server_name, total_memory, gpu_num) {
            this.log_form = {
                "server_name": '',
                "pid": '',
                "cmd": ''
            }
            this.log_form.server_name = server_name
            this.log_form.pid = pro_info.pid
            // console.log("this.log_form:", this.log_form)

            this.pro_detail = {}
            this.log_cmd = pro_info.log_cmd
            this.pro_detail = {
                "use_memory": pro_info.use_memory,
                "pid": pro_info.pid,
                "username": pro_info.username,
                "command": pro_info.command,
                "start_time": pro_info.start_time,
                "duration": pro_info.duration,
                "cur_log": pro_info.cur_log,
                "total_memory": total_memory,
                "percent": parseInt(pro_info.use_memory / total_memory * 100),
                "gpu_num": gpu_num
            }
            // console.log("pro_detail: ", this.pro_detail)
        },
        open_log_form() {
            this.open_log_box = true
            this.input_cmd = ''
        },
        go_to_tab(server_name) {
            this.activeName = server_name
            // // console.log(server_name)
        },
        add_log_cmd() {
            if (this.input_cmd !== '') {
                this.log_form.cmd = this.input_cmd
                // console.log("this.log_form:", this.log_form)
                this.$http
                    .post("/add_log", this.log_form)
                    .then((res) => {
                        // console.log(res)
                        if (res.status === 200) {
                            ElMessage.success(res.data.message);
                            // this.open_log_box = false
                        }
                    })
                    .catch(() => {
                        ElMessage.error("添加失败！");
                    });
            } else {
                ElMessage.error("请输入命令！");
            }
        },
        update_log_cmd() {
            if (this.input_cmd !== '') {
                this.log_form.cmd = this.input_cmd
                this.$http
                    .post("/update_log", this.log_form)
                    .then((res) => {
                        // console.log(res)
                        if (res.status === 200) {
                            ElMessage.success(res.data.message);
                            // this.open_log_box = false
                        }
                    })
                    .catch(() => {
                        ElMessage.error("更新失败！");
                    });
            } else {
                ElMessage.error("请输入命令！");
            }

        },
        delete_log_cmd() {
            this.$http
                .post("/delete_log", this.log_form)
                .then((res) => {
                    // console.log(res)
                    if (res.status === 200) {
                        ElMessage.success(res.data.message);
                        // this.open_log_box = false
                    }
                })
                .catch(() => {
                    ElMessage.error("删除失败！");
                });
        },

        // 点击事件
        share(val) {
            // console.log("copy:", val)
            // this.handleData(val)
            this.$copyText(val).then(function () {
                ElMessage.success("复制到剪切板: " + val);
            }, function () {
                ElMessage.error("复制失败: " + val);
            })
        },

        //数据处理
        handleData(val) {
            this.message = this.message + ' ' + val
        },
        update_tag(gpu_data) {
            this.log_form = {
                "server_name": '',
                "pid": '',
                "cmd": ''
            }
            this.pro_detail = {}

            this.log_form.server_name = this.select_log.server_name
            this.log_form.pid = this.select_log.pid
            //解析 this.gpu_data
            for (let i = 0; i < gpu_data.length; i++) {
                if (gpu_data[i].server_name === this.select_log.server_name) {
                    for (let j = 0; j < gpu_data[i].gpu_list.length; j++) {
                        for (let k = 0; k < gpu_data[i].gpu_list[j].program_list.length; k++) {
                            if (gpu_data[i].gpu_list[j].program_list[k].pid === this.select_log.pid) {
                                // console.log("gpu_data[i].gpu_list[j].program_list[k]:", gpu_data[i].gpu_list[j].program_list[k])
                                this.update_pro_detail(gpu_data[i].gpu_list[j].program_list[k], this.select_log.server_name, gpu_data[i].gpu_list[j].total_memory, gpu_data[i].gpu_list[j].num)
                                return
                            }
                        }
                    }
                }
            }
        },
        //处理tab点击事件
        handleTabClick(tab) {
            if (tab === "watcher") {
                this.$nextTick(() => {
                    echarts.getInstanceByDom(this.$refs.hisEchart).resize()
                    this.his_ip_scatter()
                }).then()
            }
        },
        initEcharts() {
            let hisEchart = echarts.init(this.$refs.hisEchart)
            // 配置
            let valveOption = {}
            hisEchart.setOption(valveOption)
        },
        //历史用户ip分布
        his_ip_scatter() {
            let myChart = echarts.init(document.getElementById("his_ip_scatter"));
            //[时间,次数,大小,ip]
            const days = this.his_ip_data.datetime
            const data = this.his_ip_data.details
                .map(function (item) {
                    return [item[0], item[1], item[2], item[3]];
                });
            let option = {
                title: {
                    text: "本月活跃ip",
                    left: "0%",
                    top: "left",
                    textStyle: {
                        fontSize: 20
                    }
                },
                legend: {
                    data: ['IP'],
                    left: 'right'
                },
                xAxis: {
                    type: 'category',
                    data: days,
                    boundaryGap: false,
                    splitLine: {
                        show: true
                    },
                    axisLine: {
                        show: false
                    },
                    axisLabel: {
                        interval: 0,
                        rotate: 0,
                    },
                },
                yAxis: {
                    type: 'value',
                    // data: days,
                    axisLine: {
                        show: false
                    }
                },
                tooltip: {
                    position: 'bottom',
                    //[时间,次数,大小,ip]
                    formatter: function (params) {
                        return (
                            "ip: " + params.value[3] + " 在 " +
                            days[params.value[0]] +
                            ' 访问 ' +
                            params.value[1] + " 次"
                        );
                    }
                },
                series: [
                    {
                        name: 'IP',
                        type: 'scatter',
                        symbolSize: function (val) {
                            if (val[2] < 10) {
                                return 1 + val[2] * 3;
                            } else if (val[2] < 30) {
                                return 30 + val[2];
                            } else if (val[2] < 50) {
                                return 50 + val[2];
                            } else return 50;
                        },
                        // 定义颜色
                        itemStyle: {
                            color: function (params) {
                                const val = params.data
                                // console.log("val:", val.data)
                                const colorlist = ['#006E7F', '#F8CB2E', '#EE5007', '#B22727'];
                                if (val[2] < 10) {
                                    return colorlist[0];
                                } else if (val[2] < 30) {
                                    return colorlist[1];
                                } else if (val[2] < 50) {
                                    return colorlist[2];
                                } else return colorlist[3];
                            }
                        },
                        data: data,
                        animationDelay: function (idx) {
                            return idx * 5;
                        }
                    }
                ],
                grid: {
                    left: 2,
                    bottom: 10,
                    right: 10,
                    containLabel: true
                },
            };
            myChart.setOption(option);
        },
        get_ip_data() {
            this.$http
                .get("/get_ip_data")
                .then((res) => {
                    if (res.status === 200) {
                        this.his_ip_data = res.data
                        this.his_ip_scatter()
                    }
                })
                .catch(() => {
                    ElMessage.error("数据加载失败,请刷新！");
                });

        },
        get_statistics() {
            this.$http
                .get("/get_statistics")
                .then((res) => {
                    // console.log(res)
                    if (res.status === 200) {
                        this.user_data = res.data
                        // console.log("user_data:", this.user_data)
                    }
                })
                .catch(() => {
                    ElMessage.error("数据加载失败,请刷新！");
                });

        },
        get_server_data() {
            this.get_gpu_status()
            this.get_ip_data()
            this.get_statistics()
        }
    },


}


