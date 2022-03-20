<template>
  <div>
    <div style="width: 300px; float: left; margin-top: 20px; margin-left: 20px">
      <div style="color: #304156; font-size: 15px; margin-bottom: 10px">
        搜索姓名：
      </div>
      <el-input
        v-model="inputValue"
        style="width: 200px"
        type="text"
        label="搜索"
        placeholder="请输入姓名进行搜索"
      />
    </div>
    <el-table
      style="width: 100%; margin-left: 12px; padding-top: 15px; height = 400px"
    :data="list.slice((page-1)*limit, page*limit)">
      <el-table-column
        prop="name"
        label="姓名"
        width="80px"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="role"
        label="身份"
        width="80px"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="monitor"
        label="绑定督导"
        width="100px"
        align="center"
      ></el-table-column>
      <el-table-column
        align="center"
        prop="sum"
        label="总咨询数"
        width="100px"
      ></el-table-column>
      <el-table-column
        align="center"
        prop="time"
        label="咨询总时长"
        width="180px"
      ></el-table-column>
      <el-table-column
        prop="rate"
        label="平均咨询评级"
        width="180px"
        align="center"
      ><template slot-scope="scope">
          <el-rate
            v-model="scope.row.rate"
            :allow-half="true"
            disabled
            text-color="#ff9900"
          ></el-rate>
        </template>
      </el-table-column>
      <el-table-column
        prop="schedule"
        label="周值班安排"
        width="180px"
        align="center"
      ></el-table-column>
      <el-table-column prop="operate" label="操作" align="center">
        <template slot-scope="scope">
          <el-button
            type="primary"
            plain
            icon="el-icon-edit"
            size="mini"
            @click="scope.$index, scope.row"
            >修改</el-button
          >
        </template>
      </el-table-column>
    </el-table>
        <el-pagination
      style="margin-top: 20px; text-align: center"
      :current-page.sync="page"
      :page-sizes="[5,7,10]"
      :page-size="limit"
      :pager-count="7"
      :total="total"
      @current-change="handleCurrentChange"
      @size-change="handleSizeChange"
      layout="prev, pager, next, jumper,->,sizes,total "
    >
    </el-pagination>
  </div>
</template>

<script>
export default {
  name: "consultantManage",
  data() {
    return {
      value1: null,
      page: 1,
      limit: 7,
      total: 12,
      list: [
        {
          name: "咨询师A",
          role: "咨询师",
          monitor: "督导1",
          sum: "128",
          time: "34:12:50",
          rate: 3,
          schedule: "周一、周三、周五"
        },
        {
          name: "咨询师A",
          role: "咨询师",
          monitor: "督导1",
          sum: "128",
          time: "34:12:50",
          rate: 3,
          schedule: "周一、周三、周五"
        },
        {
          name: "咨询师A",
          role: "咨询师",
          monitor: "督导1",
          sum: "128",
          time: "34:12:50",
          rate: 3,
          schedule: "周一、周三、周五"
        },
        {
           name: "咨询师A",
          role: "咨询师",
          monitor: "督导1",
          sum: "128",
          time: "34:12:50",
          rate: 3,
          schedule: "周一、周三、周五"
        },
        {
          name: "咨询师A",
          role: "咨询师",
          monitor: "督导1",
          sum: "128",
          time: "34:12:50",
          rate: 3,
          schedule: "周一、周三、周五"
        },
        {
          name: "咨询师A",
          role: "咨询师",
          monitor: "督导1",
          sum: "128",
          time: "34:12:50",
          rate: 3,
          schedule: "周一、周三、周五"
        },
        {
           name: "咨询师A",
          role: "咨询师",
          monitor: "督导1",
          sum: "128",
          time: "34:12:50",
          rate: 3,
          schedule: "周一、周三、周五"
        },
        {
          name: "咨询师A",
          role: "咨询师",
          monitor: "督导1",
          sum: "128",
          time: "34:12:50",
          rate: 3,
          schedule: "周一、周三、周五"
        },
        {
           name: "咨询师A",
          role: "咨询师",
          monitor: "督导1",
          sum: "128",
          time: "34:12:50",
          rate: 3,
          schedule: "周一、周三、周五"
        },
        {
          name: "咨询师A",
          role: "咨询师",
          monitor: "督导1",
          sum: "128",
          time: "34:12:50",
          rate: 3,
          schedule: "周一、周三、周五"
        },
        {
          name: "咨询师A",
          role: "咨询师",
          monitor: "督导1",
          sum: "128",
          time: "34:12:50",
          rate: 3,
          schedule: "周一、周三、周五"
        },
        {
          name: "咨询师A",
          role: "咨询师",
          monitor: "督导1",
          sum: "128",
          time: "34:12:50",
          rate: 3,
          schedule: "周一、周三、周五"
        }
      ]
    };
  },
  methods: {
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
    }
  }
};
</script>

<style>
</style>