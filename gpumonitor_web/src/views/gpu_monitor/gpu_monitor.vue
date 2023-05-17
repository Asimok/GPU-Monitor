<template>
    <el-container>
        <el-main>
            <el-tabs v-model="activeName" class="demo-tabs" @tab-change="handleTabClick">
                <el-tab-pane label="在线服务器" name="All">
                    <el-card class="box-card" shadow="hover" v-for="(cur_gpu_data,i) in gup_data" :key="i">
                        <div @click="go_to_tab(cur_gpu_data.server_name)" class="card-header">
                            <span>{{ cur_gpu_data.server_name }}</span>
                            <div style="float: right;">
                                <span style="font-weight: 500;font-size: 14px">GPU状态: </span>
                                <template v-for="(cur_gpu_info,m) in cur_gpu_data.gpu_list" :key="m">
                                    <el-tag v-if="cur_gpu_info.use_memory<100" style="margin-left: 10px" size="large"
                                            type="success"
                                            effect="dark">
                                        {{ cur_gpu_info.num }}
                                    </el-tag>
                                    <el-tag v-else style="margin-left: 10px" size="large" type="info" effect="dark">
                                        {{ cur_gpu_info.num }}
                                    </el-tag>
                                </template>
                            </div>
                        </div>
                        <!--            详情-->
                        <el-divider v-if="total_pro[i]>0" style="margin-top: 15px;margin-bottom: 0"/>

                        <el-descriptions v-if="total_pro[i]>0" :column="4"
                                         style="margin-top: 10px;margin-bottom: -15px">
                            <template #title>
                                <div style="font-size: 16px;font-weight: 450; display: flex;align-items: center;padding-top: 10px">
                                    <template v-for="(cur_gpu_info,j) in cur_gpu_data.gpu_list" :key="j">
                                        <template v-if="cur_gpu_info.program_list.length>0">
                                            <el-tag size="large" :type="tags[j]" :effect="tags_effect[j]"
                                                    @click="get_pro_detail(pro,cur_gpu_data.server_name,cur_gpu_info.total_memory,cur_gpu_info.num)"
                                                    v-for="(pro,k) in cur_gpu_info.program_list" :key="k"
                                                    style="margin-right: 10px">
                                                {{
                                                get_user_usage_detail(pro, cur_gpu_data.server_name, cur_gpu_info.total_memory, cur_gpu_info.num)
                                                }}
                                            </el-tag>
                                        </template>
                                    </template>
                                </div>
                            </template>
                        </el-descriptions>
                    </el-card>
                </el-tab-pane>
                <el-tab-pane v-for="(cur_gpu_data,i) in gup_data" :key="i" :label="cur_gpu_data.server_name"
                             :name="cur_gpu_data.server_name">
                    <el-card class="box-card" shadow="hover">
                        <template #header>
                            <div class="card-header">
                                <span>{{ cur_gpu_data.server_name }}</span>
                                <!--            <el-button class="button" text>Operation button</el-button>-->
                                <div style="float: right;">
                                    <span style="font-weight: 500;font-size: 14px">GPU状态: </span>
                                    <template v-for="(cur_gpu_info,m) in cur_gpu_data.gpu_list" :key="m">
                                        <el-tag v-if="cur_gpu_info.use_memory<100" style="margin-left: 10px"
                                                size="large" type="success"
                                                effect="dark">
                                            {{ cur_gpu_info.num }}
                                        </el-tag>
                                        <el-tag v-else style="margin-left: 10px" size="large" type="info" effect="dark">
                                            {{ cur_gpu_info.num }}
                                        </el-tag>
                                    </template>
                                </div>

                            </div>
                        </template>
                        <div v-for="(cur_gpu_info,j) in cur_gpu_data.gpu_list" :key="j">
                            <el-descriptions :title="gen_title(cur_gpu_info.num)" :column="4" class-name="descriptions"
                                             label-class-name="descriptions">
                                <el-descriptions-item width="200px" label="温度:">{{
                                    cur_gpu_info.temp
                                    }}°C
                                </el-descriptions-item>
                                <el-descriptions-item width="200px" label="风扇转速:">{{
                                    cur_gpu_info.fan
                                    }}
                                </el-descriptions-item>
                                <el-descriptions-item width="200px" s label="功率:">{{
                                    cur_gpu_info.pwr
                                    }}
                                </el-descriptions-item>
                                <el-descriptions-item>
                                    <template v-slot:label>
                                        <el-row style="padding-top:  24px">
                                            <el-col :span="2">显存占用:</el-col>
                                            <el-col :span="5">
                                                <span>{{ cur_gpu_info.use_memory }} MB / {{ cur_gpu_info.total_memory }} MB&nbsp;</span>
                                            </el-col>
                                            <el-col :span="17">
                                                <el-progress
                                                        :text-inside="true"
                                                        :stroke-width="22"
                                                        :percentage="cal_memory_usage(cur_gpu_info.use_memory,cur_gpu_info.total_memory)"
                                                        status="warning"
                                                >
                                                </el-progress>
                                            </el-col>
                                        </el-row>
                                    </template>
                                </el-descriptions-item>
                                <el-descriptions-item v-if="cur_gpu_info.program_list.length>0"
                                                      label="在线用户:">
                                    <el-tag size="large" effect="dark"
                                            @click="get_pro_detail(pro,cur_gpu_data.server_name,cur_gpu_info.total_memory,cur_gpu_info.num)"
                                            v-for="(pro,k) in cur_gpu_info.program_list" :key="k"
                                            style="margin-right: 20px;">
                                        {{ get_user_usage(pro, cur_gpu_info.total_memory) }}
                                    </el-tag>
                                </el-descriptions-item>
                            </el-descriptions>
                            <el-divider v-if="j!==cur_gpu_data.gpu_list.length-1"/>
                        </div>
                    </el-card>
                </el-tab-pane>

                <el-tab-pane label="系统监测" name="watcher">


                    <el-row justify="center">
                        <el-col :span="8">
                            <div class="statistic-card">
                                <el-statistic :value="user_data.today_online_user_nums">
                                    <template #title>
                                        <div style="display: inline-flex; align-items: center;">
                                            今日活跃用户
                                            <el-tooltip
                                                    effect="dark"
                                                    content="今日访问GPU-Monitor用户数量"
                                                    placement="top"
                                            >
                                                <el-icon style="margin-left: 4px" :size="12">
                                                    <Warning/>
                                                </el-icon>
                                            </el-tooltip>
                                        </div>
                                    </template>
                                </el-statistic>
                                <div class="statistic-footer">
                                    <div class="footer-item">
                                        <span>相比昨日</span>
                                        <span v-if="user_data.compare_yesterday >=0" class="green">
              {{ user_data.compare_yesterday_value }}
              <el-icon>
                <CaretTop/>
              </el-icon>
            </span>
                                        <span v-else class="red">
              {{ user_data.compare_yesterday_value }}
              <el-icon>
                <CaretBottom/>
              </el-icon>
            </span>
                                    </div>
                                </div>
                            </div>
                        </el-col>
                        <el-col :span="8">
                            <div class="statistic-card">
                                <el-statistic :value="user_data.month_online_user_nums">
                                    <template #title>
                                        <div style="display: inline-flex; align-items: center">
                                            本月活跃用户
                                            <el-tooltip
                                                    effect="dark"
                                                    content="本月访问GPU-Monitor用户数量"
                                                    placement="top"
                                            >
                                                <el-icon style="margin-left: 4px" :size="12">
                                                    <Warning/>
                                                </el-icon>
                                            </el-tooltip>
                                        </div>
                                    </template>
                                </el-statistic>
                                <div class="statistic-footer">
                                    <div class="footer-item">
                                        <span>相比上月</span>
                                        <span v-if="user_data.compare_last_month >=0" class="green">
              {{ user_data.compare_last_month_value }}
              <el-icon>
                <CaretTop/>
              </el-icon>
            </span>
                                        <span v-else class="red">
              {{ user_data.compare_last_month_value }}
              <el-icon>
                <CaretBottom/>
              </el-icon>
            </span>
                                    </div>
                                </div>
                            </div>
                        </el-col>
                        <el-col :span="8">
                            <div class="statistic-card">
                                <el-statistic :value="user_data.history_online_user_nums"
                                              title="New transactions today">
                                    <template #title>
                                        <div style="display: inline-flex; align-items: center">
                                            历史访问用户
                                        </div>
                                    </template>
                                </el-statistic>
                            </div>
                        </el-col>
                    </el-row>

                    <el-container>
                        <el-main>
                            <div ref="hisEchart" style="height:600px;" id="his_ip_scatter"></div>
                        </el-main>
                    </el-container>

                </el-tab-pane>

                <el-tab-pane label="更新日志" name="log">

                    <el-timeline>
                        <template v-for="(cur_log,i) in update_log_data" :key="i">
                            <el-timeline-item :timestamp=cur_log.timestamp placement="top">
                                <el-card class="box-card">
                                    <template #header>

                                        <span style="color: #34528c;font-weight: 450;font-size: 18px">{{
                                            cur_log.title
                                            }}</span>

                                    </template>
                                    <template v-for="(log_info,j) in cur_log.info" :key="j">
                                        <p>{{ j + 1 }}. {{ log_info }}</p>
                                    </template>
                                </el-card>
                            </el-timeline-item>
                        </template>
                        <!--                        <el-timeline-item-->
                        <!--                            v-for="(cur_log_info, index) in update_log_data"-->
                        <!--                            :key="index"-->
                        <!--                            :timestamp="cur_log_info.timestamp"-->
                        <!--                        >-->
                        <!--                            {{ cur_log_info.info }}-->
                        <!--                        </el-timeline-item>-->
                    </el-timeline>

                </el-tab-pane>
            </el-tabs>

            <el-drawer
                    style="font-weight: 500;font-size: 16px;color: #606266"
                    v-model="open_log_drawer"
                    :title="log_cmd"
                    direction="rtl"
                    size="40%"
            >
                <p v-html="pro_detail.cur_log" style="line-height: 2;color: #02475E;font-weight: 400"></p>
            </el-drawer>

            <el-dialog v-model="open_pro_box" title="进程详情" style="width: 60vw;">
                <el-descriptions column="3">
                    <el-descriptions-item min-width="100px" label="用户名:">{{
                        pro_detail.username
                        }}
                    </el-descriptions-item>
                    <el-descriptions-item min-width="200px" label="进程号:"><span
                            @click="share('kill -9 ' + pro_detail.pid)"> {{ pro_detail.pid }}</span>
                    </el-descriptions-item>
                    <el-descriptions-item min-width="200px" label="占用显存:">GPU-{{ pro_detail.gpu_num }}
                        {{ pro_detail.percent }}% {{ pro_detail.use_memory }}MB / {{ pro_detail.total_memory }}MB
                    </el-descriptions-item>
                    <el-descriptions-item min-width="250px" label="创建时间:">{{
                        pro_detail.start_time
                        }}
                    </el-descriptions-item>
                    <el-descriptions-item min-width="100px" label="当前耗时:">{{
                        pro_detail.duration
                        }}
                    </el-descriptions-item>
                    <el-descriptions-item min-width="260px" label="">
                        <el-button @click="open_log_form" style="margin-left: -16px" type="primary">日志管理</el-button>
                        <el-button @click="open_log_drawer = true" type="success">查看日志</el-button>
                    </el-descriptions-item>
                    <el-descriptions-item label="进程:">
                        <p v-html=" pro_detail.command" @click="share(pro_detail.command)"
                           style="color: #219F94;font-weight: 400"></p>
                    </el-descriptions-item>
                </el-descriptions>
                <template #footer>
                    <div>
        <span style="color: #357C3C">
        提示: 点击 进程号 和 进程 可以复制到剪切板
      </span>
                    </div>
                </template>
            </el-dialog>
            <!--日志-->
            <el-drawer
                    style="font-weight: 500;font-size: 16px;color: #34528c;margin-bottom: -20px"
                    v-model="open_log_box"
                    title="日志管理"
                    direction="ttb"
                    size="40%"
            >
<span @click="share(log_cmd)">当前日志:   <p
        style="margin-top: 10px;color: darkgreen;font-weight: 400;font-size: 15px;"
        v-html="log_cmd"/></span>
                <span>日志命令:   </span>
                <el-row style="margin-top: 10px">
                    <el-col :span="14">
                        <el-input v-model="input_cmd"
                                  placeholder="请输入日志命令     必须使用绝对路径      例如 tail -100 /data0/maqi/log.out"></el-input>
                    </el-col>

                    <el-col :span="2" :offset="1">
                        <el-button type="success" @click="add_log_cmd">新增日志</el-button>
                    </el-col>
                    <el-col :span="2">
                        <el-button type="primary" @click="update_log_cmd">更新日志</el-button>
                    </el-col>
                    <el-col :span="2">
                        <el-button type="danger" @click="delete_log_cmd">删除日志</el-button>
                    </el-col>
                    <el-col :span="2">
                        <el-button type="info" @click="open_log_drawer = true">查看日志</el-button>
                    </el-col>
                </el-row>

                <template #footer>
                    <div>
                        <span style="color: #f85f73">特别说明：理论上新增日志功能可以执行任何Linux命令(权限允许),但是为了安全起见,请不要执行危险命令,例如rm -rf /data0/maqi/ 如果需要执行打印日志以外的命令,请务必在执行成功后使用删除功能,否则会影响其他用户使用。</span>
                    </div>
                </template>

            </el-drawer>

        </el-main>
        <el-footer style="text-align: center">
            <span @click="handleClick">{{ update_log_data[0].title }} powered by maqi {{
                update_log_data[0].timestamp
                }}  </span>
            <span @click="handleClick_closeMC"> © 2022-2023</span>
        </el-footer>

        <el-dialog
                v-model="easterEggVisible"
                title="恭喜你，发现了彩蛋！"
                width="30%"
                :before-close="handleClose"
        >
            <span>邀请加入neukg-mc！</span>
            <template #footer>
      <span class="dialog-footer">
        <el-button @click="closeDialog">我选择学习</el-button>
        <el-button type="primary" @click="runMC">
          MC-neukg 启动！
        </el-button>
      </span>
            </template>
        </el-dialog>

        <el-dialog
                v-model="sysInfoShowDialog"
                title="服务器性能监管"
                width="30%"
        >
            <span>{{ sysInfoDialogMessage }}</span>
            <template #footer>
      <span class="dialog-footer">
        <el-button type="success">
          保持挂起
        </el-button>
        <el-button type="primary" @click="closeTimerDialog">
            继续使用
        </el-button>
      </span>
            </template>
        </el-dialog>
    </el-container>
</template>

<script src="./_gpu_monitor.js" lang="js"></script>
<style src="./_gpu_monitor.less" lang="less" scoped></style>
