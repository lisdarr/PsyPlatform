<template>
  <el-calendar v-model="value">
    <template slot="dateCell" slot-scope="{date, data}">
      <div>
        <div class="calendar-day">{{ data.day.split('-').slice(2).join('-') }}</div>
        <div v-for="(item, index) in calendarData" :key="index">
          <div v-if="(item.months).indexOf(data.day.split('-').slice(1)[0])!==-1">
            <div v-if="(item.days).indexOf(data.day.split('-').slice(2).join('-'))!==-1">
              <el-tooltip class="item" effect="dark" placement="right">
                <div class="is-selected" style="text-align: center; font-weight: bold;">值班</div>
              </el-tooltip>
            </div>
            <div v-else/>
          </div>
          <div v-else/>
        </div>
      </div>
    </template>
  </el-calendar>
</template>

<script>
export default {
  name: 'Calendar',
  data() {
    return {
      calendarData: [
        {
          months: ['03'],
          days: ['15']
        }
      ],
      value: new Date()
    }
  }
}
</script>

<style>
.calendar-day {
  text-align: center;
  color: #202535;
  line-height: 30px;
  font-size: 12px;
}

.is-selected {
  color: #F8A535;
  font-size: 10px;
  margin-top: 5px;
}

.el-calendar-table .el-calendar-day {
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  padding: 8px;
  height: 56px;
}

.el-calendar__body {
  padding: 12px 20px 12px;
}

/*.el-calendar {*/
/*  width: 60px;*/
/*  height: 60px;*/
/*}*/
</style>

