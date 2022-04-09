<template>
  <div>
    <div style="display: inline">
      <div style="width: 300px;float: left;margin-top: 20px;margin-left: 20px">
        <div style="color: #304156; font-size: 15px; margin-bottom: 10px">搜索姓名：</div>
        <el-input v-model="inputValue" style="width: 200px" type="text" label="搜索" placeholder="请输入姓名进行搜索"/>
      </div>
      <div style="width: 300px;float: left;margin-top: 20px;margin-left: 20px">
        <div style="color: #304156; font-size: 15px; margin-bottom: 10px">选择日期：</div>
        <el-date-picker
          v-model="dataValue"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="yyyy-MM-dd"
        />
      </div>
      <div style="width: 300px;float: left;margin-top: 50px;margin-left: 100px;">
        <el-button size="small" icon="el-icon-search" @click="search">搜索</el-button>
      </div>
    </div>
    <el-table :data="tableData.slice((currentPage-1)*pageSize, currentPage*pageSize)"
              style="width: 100%;
              margin-left: 12px;
               padding-top: 15px"
    >
      <el-table-column prop="name" label="咨询师" width="300"/>
      <el-table-column prop="time" label="咨询时长" width="300"/>
      <el-table-column prop="date" label="咨询日期" width="300" sortable/>
      <el-table-column label="操作" width="300">
        <el-button size="mini" type="primary">查看详情</el-button>
        <el-button size="mini" type="success">导出记录</el-button>
      </el-table-column>
    </el-table>
    <el-pagination
      style="float: right;margin-top: 20px"
      :current-page.sync="currentPage"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pageSize"
      :total="totalSize"
      layout="total, jumper, sizes, prev, pager, next"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script>

import { recordDirector } from '@/api/director'

export default {
  name: 'RecordDirector',
  data() {
    return {
      tableData: [],
      inputValue: '',
      dataValue: '',
      currentPage: 1,
      pageSize: 10,
      totalSize: 6
    }
  },
  mounted() {
    this.search()
  },
  methods: {
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
    },
    search(inputValue, dataValue) {
      console.log('我在搜索')
      var that = this
      recordDirector({
        name: this.inputValue,
        begin_date: this.dataValue[0],
        end_date: this.dataValue[1]
      }).then((response) => {
        that.tableData = response.tableData
        that.totalSize = response.totalSize
      }).catch((error) => {
        console.log(error)
      })
    }
  }
}
</script>

<style scoped>

</style>
