<template>
  <div class="calendar_box">
    <el-row style="padding-top: 15px" :gutter="20">
      <el-col :span="18">
        <FullCalendar :options="calendarOptions" />
      </el-col>
      <el-col :span="6" class="detail_box">
        <div class="addbtn">
          <el-button type="primary" @click="addPaiban" size="small"
            >添加排班
          </el-button>
        </div>
        <el-alert title="排班信息" type="success" :closable="false"></el-alert>
        <el-form :model="form" label-width="80px">
          <el-form-item label="咨询师：">
            {{ form.consultantName }}
          </el-form-item>
          <el-form-item label="督导：">
            {{ form.monitorName }}
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>

    <!-- 添加或修改 -->
    <el-dialog title="添加排班" :visible.sync="dialogFormVisible">
      <el-form label-width="100px">
        <el-form-item label="选择咨询师">
          <el-select v-model="addForm.consultantId" placeholder="请选择咨询师">
            <el-option
              v-for="(item, index) in consultantList"
              :key="item.consultantId"
              :label="item.consultantName"
              :value="item.consultantId"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="选择督导">
          <el-select v-model="addForm.monitorId" placeholder="请选择督导">
            <el-option
              v-for="item in monitorList"
              :key="item.monitorId"
              :label="item.monitorName"
              :value="item.monitorId"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="排班时间">
          <el-date-picker
            v-model="addForm.dateValue"
            format="yyyy-MM-dd"
            value-format="yyyy-MM-dd"
            type="date"
            placeholder="选择排班日期"
          >
          </el-date-picker>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false" size="small"
          >取 消</el-button
        >
        <el-button type="primary" @click="save" size="small">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import FullCalendar from "@fullcalendar/vue";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import { getToken } from "@/utils/auth";
import { addSchedule, scheduleInfo } from "@/api/admin";
import { scheduleQuery } from "@/api/admin";

export default {
  name: "ScheduleAdmin",
  components: { FullCalendar },

  data() {
    return {
      dialogFormVisible: false,
      form: {
        consultantName: "",
        monitorName: "",
      },
      // 添加排班的表单
      addForm: {
        consultantId: "",
        monitorId: "",
        dateValue: "",
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
        dateClick: this.handleDateClick,
        events: [],
        // events: [
        //   { title: "咨询师：5", start: "2022-03-21" },
        //   { title: "督导：2", start: "2022-03-21" },
        //   { title: "咨询师：4 ", start: "2022-03-22" },
        //   { title: "督导：3", start: "2022-03-22" },
        // ],
        eventColor: "#f08f00",
        locale: "zh-cn",
        weekNumberCalculation: "ISO",
        customButtons: {},
      },
      consultantList: [
        // {
        //   consultantName: "咨询师A",
        //   consultantId: "1",
        // },
      ],
      monitorList: [
        // {
        //   monitorName: "督导A",
        //   monitorId: 1,
        // },
      ],
    };
  },
  mounted() {
    this.init_Schedule();
  },

  methods: {
    init_Schedule() {
      var that = this;
      scheduleInfo(getToken())
        .then((response) => {
          this.calendarOptions.events = response.event;
          // console.log(that.events);
          that.consultantList = response.consultantList;
          // console.log(that.consultantList);
          that.monitorList = response.monitorList;
          console.log(that.monitorList);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    addPaiban() {
      this.dialogFormVisible = true;
      this.addform = {
        consultantName: "",
        monitorName: "",
        dateValue: "",
      };
    },
    save() {
      console.log("保存");
      this.dialogFormVisible = false;
      var that = this;
      addSchedule({
        addForm: this.addForm,
      })
        .then(() => {
          that.$message.success("保存成功！");
          that.init_Schedule();
        })
        .catch((error) => {
          console.log(error);
        });
      //send三个值，request new title
    },
    handleDateClick(info) {
      console.log("点击日期");
      console.log(info.dateStr);
      var that = this;
      scheduleQuery({
        dateStr: info.dateStr,
      })
        .then((response) => {
          that.form = response.form;
          // console.log(that.form);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    dateToString(now) {
      var year = now.getFullYear();
      var month = (now.getMonth() + 1).toString();
      var day = now.getDate().toString();
      if (month.length === 1) {
        month = "0" + month;
      }
      if (day.length === 1) {
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
.fc-unthemed >>> .fc-content {
  white-space: pre;
}
</style>

