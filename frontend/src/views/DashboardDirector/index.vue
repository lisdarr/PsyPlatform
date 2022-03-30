<template>
  <div>
    <div style="height: 500px">
      <div style="width: 60%; float: left; height:500px; margin: 2% 1%">
        <div style="width: 100%; height: 250px; margin-bottom: 10px">
          <div style="float: left; width: 40%; height: 250px">
            <el-card>
              <div style="float: left; margin-bottom: 17px">
                <el-avatar shape="square" :size="160" :src="squareUrl"/>
              </div>
              <div style="margin-left: 180px">
                <div style="margin-bottom: 30%; font-size: 20px; font-weight: bold">{{ directorName }}</div>
              </div>
            </el-card>
          </div>
          <div style="float: left; width: 56%; height: 250px; margin-left: 4%">
            <el-card style="width: 100%; height: 201px">
              <div style="text-align: center; width: 35%; float: left; margin-top: 30px">
                <div style="font-size: 20px; color: #304156; font-weight: bold">今日咨询数</div>
                <div style="font-size: 60px; margin-top: 15px">{{ consultTodayNum }}</div>
              </div>
              <div style="width: 2%; float: left">
                <el-divider direction="vertical"/>
              </div>
              <div style="text-align: center; width: 55%; float: right; margin-top: 30px">
                <div style="font-size: 20px; color: #304156; font-weight: bold">今日咨询时长</div>
                <div style="font-size: 60px; margin-top: 15px">{{ consultTodayTime }}</div>
              </div>
            </el-card>
          </div>
        </div>
        <div style="width: 100%; height: 250px;margin-top: 10px">
          <el-card>
            <!--            在线咨询师-->
            <div style="float: left;width: 60%; ">
              <div style="height: 50px">
                <div style="float: left;margin-top: 5px">
                  在线咨询师
                </div>
                <div style="float: right; margin-bottom: 15px">
                  <el-pagination
                    background
                    layout="prev, pager, next"
                    :total="1"
                  >
                  </el-pagination>
                </div>
              </div>
              <div style="height: 173px">
                <el-row type="flex" :gutter="4">
                  <el-col :span="8" v-for="(item,index) in consultList" :key="item.id">
                    <el-card :key="index" style="margin-bottom: 4px">
                      <div style="float: left; font-size: 15px">
                        {{ item.name }}
                      </div>
                      <div v-if="item.state === 1" style="float: right;">
                        <i class="el-icon-user-solid" style="color: lightgreen"></i>
                      </div>
                      <div v-if="item.state !== 1" style="float: right;">
                        <i class="el-icon-user-solid" style="color: gray"></i>
                      </div>
                    </el-card>
                  </el-col>
                </el-row>
              </div>
            </div>
            <!--            正在进行的咨询数-->
            <div style="background-color: #304156; width: 35%; height: 200px; float: right;">
              <div style="text-align: center; color: white; font-size: 20px; margin-top: 50px">正在进行的咨询</div>
              <div style="text-align: center; color: white; padding-top: 10%; font-size: 50px">{{ consultNum }}</div>
            </div>
          </el-card>
        </div>
      </div>
      <!--    右侧排班表-->
      <div style="width: 35%; float: left; height: 450px; margin: 2% 1%">
        <el-card>
          <Calendar :calendarData="calendarData"/>
        </el-card>
      </div>
    </div>
    <div style="margin-top: 50px">
      <el-card style="margin: 2% 1% 2% 1%; width: 97%; height: 400px">
        <div
          style="color: #304156; float: left; font-size: 18px; font-weight: bold;"
        >最近完成的求助会话
        </div>
        <div style="float: right">
          <el-button style="font-size: 10px;" @click="jump">
            查看全部
          </el-button>
        </div>
        <el-divider/>
        <div>
          <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="name" label="咨询师" width="300"/>
            <el-table-column prop="time" label="咨询时长" width="300"/>
            <el-table-column prop="date" label="咨询日期" width="300"/>
            <el-table-column label="操作" width="300">
              <el-button size="mini" type="primary">查看详情</el-button>
              <el-button size="mini" type="success">导出记录</el-button>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import Calendar from '@/components/Calendar'
import { dashboardDirector } from '@/api/director'
import { getToken } from '@/utils/auth'

export default {
  name: 'DashboardDirector',
  components: { Calendar },
  data() {
    return {
      consultList: [],
      consultNum: 5,
      directorName: '督导',
      consultTodayNum: 15,
      consultTodayTime: '6:12:30',
      squareUrl: 'https://images.pexels.com/photos/4491461/pexels-photo-4491461.jpeg?cs=srgb&dl=pexels-karolina-grabowska-4491461.jpg&fm=jpg',
      tableData: [{
        name: '王小虎',
        time: '00:12:54',
        date: '2016-05-02'
      }],
      calendarData: [
        {
          month: '04',
          day: '15'
        },
        {
          month: '06',
          day: '14'
        }
      ]
    }
  },
  methods: {
    jump() {
      this.$router.push({ path: '/RecordDirector' })
    },
    init_dashboardDirector() {
      var that = this
      dashboardDirector(getToken()).then((response) => {
        that.consultList = response.consultList
        that.squareUrl = response.squareUrl
        that.directorName = response.directorName
        that.consultNum = response.consultNum
        that.consultTodayNum = response.today_num
        that.consultTodayTime = response.today_time
        that.tableData = response.tableData
        that.calendarData = response.calendarData
      })
    }
  },
  mounted() {
    this.init_dashboardDirector()
  }
}
</script>

<style scoped>
.el-row {
  flex-wrap: wrap;
}

.el-divider--vertical {
  height: 160px;
}

.el-divider--horizontal {
  display: block;
  height: 1px;
  width: 14%;
  margin: 30px 0;
}
</style>
