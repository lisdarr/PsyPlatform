<template>
  <div class="dashboard-container">
    <!--    <div class="dashboard-text">name: {{ name }}</div>-->
    <el-row style="height: 550px" :gutter="20">
      <el-col :span="15">
        <el-row style="width: 750px; height: 250px">
          <el-card class="box-card" style="width: auto">
            <div style="width: 70%; float: left;">
              <div style="float: left;">
                <el-avatar shape="square" :size="200" :src="squareUrl"/>
              </div>
              <div style="margin-left: 220px">
                <div style="margin-bottom: 30%; font-size: 20px; font-weight: bold">{{ name }}</div>
                <div style="font-size: 20px; margin-bottom: 10%">我的综合评价</div>
                <div>
                  <el-rate v-model="value" disabled show-score text-color="#ff9900" score-template="{value}"/>
                </div>
              </div>
            </div>
            <div style="margin-left: 70%; background-color: #304156; height: 200px">
              <div style="text-align: center; color: white; padding-top: 30%; font-size: 20px">累积完成咨询</div>
              <div style="text-align: center; color: white; padding-top: 10%; font-size: 50px">{{ consultNum }}</div>
            </div>
          </el-card>
        </el-row>
        <el-row style="width: 750px; height: 250px">
          <el-card class="box-card" style="width: auto">
            <div style="display: flex; justify-content: space-around">
              <div style="text-align: center; padding-top: 5%">
                <div style="font-size: 20px; color: #304156; font-weight: bold">今日咨询数</div>
                <div style="padding-top: 20px; font-size: 60px">{{ consultTodayNum }}</div>
              </div>
              <div>
                <el-divider direction="vertical" style="height: 250px"/>
              </div>
              <div style="text-align: center;  padding-top: 5%">
                <div style="font-size: 20px; color: #304156; font-weight: bold">今日咨询时长</div>
                <div style="padding-top: 20px; font-size: 60px">{{ consultTodayTime }}</div>
              </div>
              <div>
                <el-divider direction="vertical" style="height: 250px"/>
              </div>
              <div style="text-align: center;  padding-top: 5%">
                <div style="font-size: 20px; color: #304156; font-weight: bold">当前会话数</div>
                <div style="padding-top: 20px; font-size: 60px">{{ callNum }}</div>
              </div>
            </div>
          </el-card>
        </el-row>
      </el-col>
      <!--        值班日历部分 -->
      <el-col :span="9" style="height: 520px;">
        <el-card class="box-card" style="width: auto; height: 520px">
          <Calendar :calendarData="calendarData"/>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <!--        data:数组类型-->
      <el-col>
        <el-card style="width: auto;">
          <div style="width: 100%; text-align: justify">
            <div
              style="display: inline-block; color: #304156; float: left; margin-left: 10px; font-size: 18px; font-weight: bold"
            >
              最近完成的咨询
              <el-divider/>
            </div>
            <el-button style="display: inline-block; float: right; font-size: 10px;" @click="jump">
              查看全部
            </el-button>
          </div>
          <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="name" label="咨询人" width="180"/>
            <el-table-column prop="time" label="咨询时长" width="180"/>
            <el-table-column prop="date" label="咨询日期" width="180"/>
            <el-table-column prop="rate" label="咨询评级" width="180">
              <template slot-scope="scope">
                <el-rate v-model="scope.row.rate" :allow-half="true" disabled text-color="#ff9900"/>
              </template>
            </el-table-column>
            <el-table-column prop="comment" label="咨询评价" width="180"/>
            <el-table-column label="操作" width="300">
              <el-button size="mini" type="primary">查看详情</el-button>
              <el-button size="mini" type="success">导出记录</el-button>
            </el-table-column>
          </el-table>
        </el-card>
        <div>{{ tableData.time }}</div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Calendar from '@/components/Calendar'
import { getToken } from '@/utils/auth'
import { dashboardConsultant } from '@/api/consultant'

// export default {
//   name: 'Dashboard',
//   computed: {
//     ...mapGetters([
//       'name'
//     ])
//   }
// }

// 表格-element ui自定义列模板
export default {
  name: 'DashboardConsult',
  components: { Calendar },
  data() {
    return {
      tableData: [],
      // value: new Date()
      squareUrl: 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
      value: 3.7,
      consultNum: 12345,
      consultTodayNum: 35,
      consultTodayTime: '6:32:24',
      callNum: 2,
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
  computed: {
    ...mapGetters([
      'name',
      'token'
    ])
  },
  methods: {
    handleEdit(index, row) {
      console.log(index, row)
    },
    handleDelete(index, row) {
      console.log(index, row)
    },
    onPanelChange(value, mode) {
      console.log(value, mode)
    },
    jump() {
      this.$router.push({ path: '/RecordConsult' })
    },
    init_dashboardConsult() {
      var that = this
      dashboardConsultant(getToken()).then(response => {
        console.log('12344455')
        const data = response
        that.tableData = Array(data.tableData)
        that.squareUrl = data.squareUrl
        that.value = data.value
        that.consultNum = data.consultNum
        that.consultTodayNum = data.consultTodayNum
        that.consultTodayTime = data.consultTodayTime
        that.callNum = data.callNum
      }).catch(error => {
        console.log(error)
      })
    }
  },
  mounted() {
    this.init_dashboardConsult()
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }

  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}

.box-card {
  width: 700px;
  height: 250px;
}

.el-row {
  margin-bottom: 20px;
  //&:last-child {
  //  margin-bottom: 0;
  //}
}

.el-col {
  border-radius: 4px;
}

.el-divider--vertical {
  display: inline-block;
  width: 1px;
  height: 210px;
  margin: 0 8px;
  vertical-align: middle;
  position: absolute;
}
</style>
