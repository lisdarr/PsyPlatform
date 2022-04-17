<template>
  <div>
    <div style="height: 442px">
      <div style="width: 40%; margin-top: 10px; margin-left: 10px">
        <el-card style="width: 100%; height: 200px">
          <div
            style="
              text-align: center;
              width: 35%;
              float: left;
              margin-top: 30px;
            "
          >
            <div style="font-size: 20px; color: #304156; font-weight: bold">
              今日咨询数
            </div>
            <div style="font-size: 60px; margin-top: 15px">
              {{ consultTodayNum }}
            </div>
          </div>
          <div style="width: 2%; float: left">
            <el-divider direction="vertical" />
          </div>
          <div
            style="
              text-align: center;
              width: 55%;
              float: right;
              margin-top: 30px;
            "
          >
            <div style="font-size: 20px; color: #304156; font-weight: bold">
              今日咨询时长
            </div>
            <div style="font-size: 60px; margin-top: 15px">
              {{ consultTodayTime }}
            </div>
          </div>
        </el-card>
      </div>
      <div style="float: left; width: 56%; height: 150px; margin: 10px">
        <el-card>
          <!--            在线咨询师-->
          <div style="float: left; width: 60%">
            <div style="height: 50px">
              <div
                style="
                  float: left;
                  margin-top: 5px;
                  font-size: 14px;
                  font-weight: bold;
                "
              >
                在线咨询师
              </div>
              <div style="float: right; margin-bottom: 15px">
                <el-pagination background layout="prev, pager, next" :total="1">
                </el-pagination>
              </div>
            </div>
            <div style="height: 150px">
              <el-row type="flex" :gutter="1">
                <el-col
                  :span="8"
                  v-for="(item, index) in oncallConsult"
                  :key="item.id"
                >
                  <el-card :key="index" style="margin-bottom: 1px">
                    <div style="float: left; font-size: 12px">
                      {{ item.name }}
                    </div>
                    <div v-if="item.state === 'true'" style="float: right">
                      <i
                        class="el-icon-user-solid"
                        style="color: lightgreen"
                      ></i>
                    </div>
                    <div v-if="item.state === 'false'" style="float: right">
                      <i class="el-icon-user-solid" style="color: gray"></i>
                    </div>
                  </el-card>
                </el-col>
              </el-row>
            </div>
          </div>
          <!--            正在进行的咨询数-->
          <div
            style="
              background-color: #304156;
              width: 35%;
              height: 170px;
              float: right;
            "
          >
            <div
              style="
                text-align: center;
                color: white;
                font-size: 20px;
                margin-top: 50px;
              "
            >
              正在进行的咨询
            </div>
            <div
              style="
                text-align: center;
                color: white;
                padding-top: 10%;
                font-size: 50px;
              "
            >
              {{ consultNum }}
            </div>
          </div>
        </el-card>
      </div>
      <div
        style="
          float: right;
          width: 41%;
          height: 150px;
          margin-top: 10px;
          margin-right: 10px;
        "
      >
        <el-card>
          <!--            在线督导-->
          <div style="float: left; width: 50%">
            <div style="height: 50px">
              <div
                style="
                  float: left;
                  margin-top: 5px;
                  font-size: 14px;
                  font-weight: bold;
                "
              >
                在线督导
              </div>
              <div style="float: right; margin-bottom: 15px">
                <el-pagination background layout="prev, pager, next" :total="1">
                </el-pagination>
              </div>
            </div>
            <div style="height: 150px">
              <el-row type="flex" :gutter="1">
                <el-col
                  :span="24"
                  v-for="(item, index) in oncallMonitor"
                  :key="item.id"
                >
                  <el-card :key="index" style="margin-bottom: 1px">
                    <div style="float: left; font-size: 12px">
                      {{ item.name }}
                    </div>
                    <div v-if="item.state === 'true'" style="float: right">
                      <i
                        class="el-icon-user-solid"
                        style="color: lightgreen"
                      ></i>
                    </div>
                    <div v-if="item.state === 'false'" style="float: right">
                      <i class="el-icon-user-solid" style="color: gray"></i>
                    </div>
                  </el-card>
                </el-col>
              </el-row>
            </div>
          </div>
          <!--            正在进行的督导会话-->
          <div
            style="
              background-color: #304156;
              width: 45%;
              height: 170px;
              float: right;
            "
          >
            <div
              style="
                text-align: center;
                color: white;
                font-size: 20px;
                margin-top: 50px;
              "
            >
              正在进行的督导会话
            </div>
            <div
              style="
                text-align: center;
                color: white;
                padding-top: 10%;
                font-size: 50px;
              "
            >
              {{ chatNum }}
            </div>
          </div>
        </el-card>
      </div>
    </div>
    <!-- 当日咨询量变化 -->
    <el-card
      style="
        float: right;
        width: 57%;
        height: 200px;
        position: absolute;
        right: 10px;
        top: 10px;
      "
      ><div id="mychart" :style="myChartStyle"></div>
    </el-card>
    <!-- 七日咨询量变化 -->
    <el-card style="float: left; width: 46%; height: 220px; margin-left: 10px"
      ><div id="weekchart" :style="weekChartStyle"></div>
    </el-card>
    <!-- 当月咨询量排行 -->
    <el-card
      style="
        float: left;
        width: 25%;
        height: 220px;
        margin-left: 10px;
        margin-bottom: 10px;
      "
    >
      <div
        style="
          height: 20px;
          margin-bottom: 10px;
          margin-top: 5px;
          font-size: 14px;
          font-weight: bold;
        "
      >
        当月咨询数量排行
      </div>
      <div style="float: left; width: 100%; height: 200px; margin-top: 10px">
        <el-row type="flex" :gutter="10">
          <el-col :span="2">
            <div v-for="o in 4" :key="o" style="height: 40px">
              {{ o }}
            </div></el-col
          >
          <el-col :span="22">
            <div v-for="(item, index) in sumList">
              <el-col :span="6">
                <div style="float: left; height: 40px">
                  <el-avatar shape="circle" :size="25" :src="item.photo" />
                </div>
              </el-col>
              <el-col :span="12">
                <div style="float: left; font-size: 12px; height: 40px">
                  {{ item.name }}
                </div>
              </el-col>
              <el-col :span="6">
                <div style="float: left; font-size: 12px; height: 40px">
                  {{ item.consultNum }}
                </div>
              </el-col>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
    <!-- 当月好评量排行 -->
    <el-card
      style="
        float: left;
        width: 25%;
        height: 220px;
        margin-left: 10px;
        margin-bottom: 10px;
      "
    >
      <div
        style="
          height: 20px;
          margin-bottom: 10px;
          margin-top: 5px;
          font-size: 14px;
          font-weight: bold;
        "
      >
        当月咨询评级排行
      </div>
      <div style="float: left; width: 100%; height: 200px; margin-top: 10px">
        <el-row type="flex" :gutter="10">
          <el-col :span="2">
            <div v-for="o in 4" :key="o" style="height: 40px">
              {{ o }}
            </div></el-col
          >
          <el-col :span="22">
            <div v-for="(item, index) in rateList">
              <el-col :span="6">
                <div style="float: left; height: 40px">
                  <el-avatar shape="circle" :size="25" :src="item.photo" />
                </div>
              </el-col>
              <el-col :span="12">
                <div style="float: left; font-size: 12px; height: 40px">
                  {{ item.name }}
                </div>
              </el-col>
              <el-col :span="6">
                <div style="float: left; font-size: 12px; height: 40px">
                  {{ item.averageScore }}
                </div>
              </el-col>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
    <!-- 四星及以上为好评 -->
  </div>
</template>


<script>
import ECharts from "vue-echarts";
import * as echarts from "echarts";
import { getToken } from "@/utils/auth";
import { dashboardAdmin } from "@/api/admin";

export default {
  name: "DashboardAdmin",
  components: {
    "v-chart": ECharts,
  },
  data() {
    return {
      oncallConsult:'',
      oncallMonitor:'',
      consultNum: "",
      chatNum: "",
      consultTodayNum: "",
      consultTodayTime: "",
      myChart: {},
      myChartStyle: {
        float: "left",
        width: "100%",
        height: "210px",
        position: "absolute",
      }, //图表样式
      weekChartStyle: {
        float: "left",
        width: "100%",
        height: "230px",
      },
      myChartData: "",
      weekChartData: "",
      sumList: [],
      rateList: [],
    };
  },
  mounted() {
    this.init_dashboardAdmin();
    this.init_myChart();
    this.init_weekChart();
  },
  methods: {
    init_dashboardAdmin() {
      var that = this;
      dashboardAdmin(getToken())
        .then((response) => {
          that.oncallConsult = response.oncallConsult;
          that.oncallMonitor = response.oncallMonitor;
          that.consultNum = response.consultNum;
          that.chatNum = response.chatNum;
          that.consultTodayNum = response.consultTodayNum;
          that.consultTodayTime = response.consultTodayTime;
          that.sumList = response.sumList;
          that.rateList = response.rateList;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    init_myChart() {
      this.myChart = echarts.init(document.getElementById("mychart"));
      this.myChart.setOption({
        title: {
          show: "true",
          text: "今日咨询数量变化",
          textStyle: {
            fontSize: "14",
          },
        },
        tooltip: {
          trigger: "axis",
        },
        grid: {
          show: "true",
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          splitLine: {
            show: "true",
          },
        },
        yAxis: {
          type: "value",
          name: "咨询量",
        },
        series: [
          {
            type: "line",
            smooth: "true",
            data: [],
            itemStyle: {
              color: "#D6AB15",
            },
            areaStyle: {
              color: {
                type: "linear",
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: "#D9981B", // 0% 处的颜色
                  },
                  {
                    offset: 1,
                    color: "#BDD99A", //   100% 处的颜色
                  },
                ],
                global: false, // 缺省为 false
              },
            },
          },
        ],
      });
      var that = this;
      dashboardAdmin(getToken())
        .then((response) => {
          that.myChartData = response.myChartData;
          // console.log(that.myChartData);
          this.myChart.setOption({
            series: [
              {
                type: "line",
                smooth: "true",
                data: this.myChartData,
                itemStyle: {
                  color: "#D6AB15",
                },
                areaStyle: {
                  color: {
                    type: "linear",
                    x: 0,
                    y: 0,
                    x2: 0,
                    y2: 1,
                    colorStops: [
                      {
                        offset: 0,
                        color: "#D9981B", // 0% 处的颜色
                      },
                      {
                        offset: 1,
                        color: "#BDD99A", //   100% 处的颜色
                      },
                    ],
                    global: false, // 缺省为 false
                  },
                },
              },
            ],
          });
        })
        .catch((error) => {
          console.log(error);
        });
    },
    init_weekChart() {
      this.weekChart = echarts.init(document.getElementById("weekchart"));
      this.weekChart.setOption({
        title: {
          show: "true",
          text: "7日咨询数量统计",
          textStyle: {
            fontSize: "14",
          },
        },
        tooltip: {
          trigger: "axis",
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          splitLine: {
            show: "true",
          },
          // data: ["3-28", "3-29", "3-30", "3-31", "4-1", "4-2", "4-3"],
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            type: "line",
            data: [],
            itemStyle: {
              color: "#68D7A8",
            },
          },
        ],
      });
      var that = this;
      dashboardAdmin(getToken())
        .then((response) => {
          that.weekChartData = response.weekChartData;
          this.weekChart.setOption({
            series: [
              {
                type: "line",
                data: that.weekChartData,
                itemStyle: {
                  color: "#68D7A8",
                },
              },
            ],
          });
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
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
