<template>
  <div class="calendar_box">
    <el-row style="padding-top: 15px" :gutter="20">
      <el-col :span="18">
        <!-- <full-calendar
            ref="fullCalendar"
            style="height: 100%"
            :options="calendarOptions"
          ></full-calendar> -->
        <FullCalendar :options="calendarOptions" class="eventDeal-wrap" />
      </el-col>
      <el-col :span="6" class="detail_box">
        <div class="addbtn">
          <el-button type="primary" @click="addPaiban" size="small"
            >添加排班</el-button
          >
        </div>
        <el-alert title="排班信息" type="success" :closable="false"></el-alert>
        <el-form :model="form" label-width="100px">
          <el-form-item label="咨询师：">
            {{ form.consultant }}
          </el-form-item>
          <el-form-item label="督导：">
            {{ form.monitor }}
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>

  <script>
import FullCalendar from "@fullcalendar/vue";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";

export default {
  name: "schedule",
  components: { FullCalendar },
  
  data() {
    return {
      isShowBtn: false,
      dialogFormVisible: false,
      form: {
        consultant: "",
        monitor: "",
      },
      formLabelWidth: 120,
      calendarOptions: {
        height: 700,
        plugins: [dayGridPlugin, interactionPlugin],
        headerToolbar: {
          left: "prev,next today",
          center: "title",
          right: "",
        },
        buttonText: { today: "今天" },
        selectable: true,

        calendarEvents: [{ title: "部门会议", start: new Date() }],
        eventColor: "#f08f00",
        locale: "zh-cn",
        weekNumberCalculation: "ISO",
        customButtons: {},
      },
    };
  },
  mounted() {
    this.calendarApi = this.$refs.fullCalendar.getApi();
    this.title = this.calendarApi.view?.title;
    // 模拟动态获取数据
    this.getDtata();
  },
  watch: {
    // 切换视图显示不同的事件
    "calendarApi.view.type"() {
      this.getDtata();
    },
  },
  methods: {
    handleEvents(events) {
      console.log(events, "事件3");
    },

    dateToString(now) {
      var year = now.getFullYear();
      var month = (now.getMonth() + 1).toString();
      var day = now.getDate().toString();
      if (month.length == 1) {
        month = "0" + month;
      }
      if (day.length == 1) {
        day = "0" + day;
      }
      var dateTime = year + "-" + month + "-" + day;
      return dateTime;
    },
  },
};
</script>

  <style scoped>
.addbtn {
  margin-top: 15px;
  text-align: left;
  margin-bottom: 15px;
}
.calendar_box >>> .el-dialog {
  width: 450px;
}
.calendar_box >>> .el-date-editor.el-input {
  width: 330px;
}
.el-select {
  width: 100%;
}
.detail_box >>> .el-form {
  border: 1px solid #ddd;
}
.detail_box >>> .el-form-item__content {
  text-align: left;
  color: #333;
}
</style>

