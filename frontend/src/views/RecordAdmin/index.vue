<template>
  <div>
    <div style="display: inline">
      <div
        style="width: 300px; float: left; margin-top: 20px; margin-left: 20px"
      >
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
      <div
        style="width: 300px; float: left; margin-top: 20px; margin-left: 20px"
      >
        <div style="color: #304156; font-size: 15px; margin-bottom: 10px">
          选择日期：
        </div>
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
    <el-table
      style="width: 100%; margin-left: 12px; padding-top: 15px; height: 400px"
      :data="list.slice((page - 1) * limit, page * limit)"
    >
      <el-table-column
        prop="name"
        label="咨询人"
        width="80px"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="time"
        label="咨询时长"
        width="100px"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="date"
        label="咨询日期"
        width="180px"
        align="center"
        sortable
      ></el-table-column>
      <el-table-column
        prop="rate"
        label="咨询评级"
        width="160px"
        align="center"
      >
        <template slot-scope="scope">
          <el-rate
            v-model="scope.row.rate"
            :allow-half="true"
            disabled
            text-color="#ff9900"
          ></el-rate>
        </template>
      </el-table-column>
      <el-table-column
        prop="eva"
        label="咨询评价"
        width="180px"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="assit"
        label="督导求助"
        width="90px"
        align="center"
      ></el-table-column>
      <el-table-column prop="operate" label="操作" align="center">
        <template slot-scope="scope">
          <!-- <el-button
            type="primary"
            plain
            icon="el-icon-info"
            size="mini"
            >查看详情
          </el-button>
          <el-button
            size="mini"
            type="success"
            plain
            icon="el-icon-download"
            >导出记录
          </el-button> -->
          <ChatHistory :id="scope.row.id"></ChatHistory>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      style="margin-top: 20px; text-align: center"
      :current-page.sync="page"
      :page-sizes="[5, 7, 10]"
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
import {record} from '@/api/admin';
import ChatHistory from '@/components/ChatHistory'

export default {
  name: 'RecordAdmin',
  components: { ChatHistory },
  data() {
    return {
      page: 1,
      limit: 7,
      total: 12,
      list: "",
      // list: [
      //   {
      //     name: '张先生',
      //     time: '1:02:00',
      //     date: '2022-03-12 13:45:06',
      //     rate: 4.5,
      //     eva: '体验很好',
      //     assit: '无'
      //   },
      //   {
      //     name: '张先生',
      //     time: '1:02:00',
      //     date: '2022-03-13 13:45:06',
      //     rate: 4.5,
      //     eva: '体验很好',
      //     assit: '无'
      //   },
      //   {
      //     name: '张先生',
      //     time: '1:02:00',
      //     date: '2022-03-14 13:43:06',
      //     rate: 4.5,
      //     eva: '体验很好',
      //     assit: '无'
      //   },
      //   {
      //     name: '张先生',
      //     time: '1:02:00',
      //     date: '2022-03-14 13:45:06',
      //     rate: 4.5,
      //     eva: '体验很好',
      //     assit: '无'
      //   },
      //   {
      //     name: '张先生',
      //     time: '1:02:00',
      //     date: '2022-03-14 13:45:06',
      //     rate: 4.5,
      //     eva: '体验很好',
      //     assit: '无'
      //   },
      //   {
      //     name: '张先生',
      //     time: '1:02:00',
      //     date: '2022-03-14 13:45:06',
      //     rate: 4.5,
      //     eva: '体验很好',
      //     assit: '无'
      //   },
      //   {
      //     name: '张先生',
      //     time: '1:02:00',
      //     date: '2022-03-14 13:45:06',
      //     rate: 4.5,
      //     eva: '体验很好',
      //     assit: '无'
      //   },
      //   {
      //     name: '张先生',
      //     time: '1:02:00',
      //     date: '2022-03-14 13:45:06',
      //     rate: 4.5,
      //     eva: '体验很好',
      //     assit: '无'
      //   },
      //   {
      //     name: '张先生',
      //     time: '1:02:00',
      //     date: '2022-03-14 13:45:06',
      //     rate: 4.5,
      //     eva: '体验很好',
      //     assit: '无'
      //   },
      //   {
      //     name: '张先生',
      //     time: '1:02:00',
      //     date: '2022-03-14 13:45:06',
      //     rate: 4.5,
      //     eva: '体验很好',
      //     assit: '无'
      //   },
      //   {
      //     name: '张先生',
      //     time: '1:02:00',
      //     date: '2022-03-14 13:45:06',
      //     rate: 4.5,
      //     eva: '体验很好',
      //     assit: '无'
      //   },
      //   {
      //     name: '刘女士',
      //     time: '1:02:00',
      //     date: '2022-04-01 13:45:06',
      //     rate: 4.7,
      //     eva: '体验很好',
      //     assit: '无'
      //   }
      // ],
      inputValue: '',
      dataValue: '',
    }
  },
  mounted(){
    this.search();
  },
  methods: {
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
    },
    search()
    {
      console.log('搜索')
      var that = this
      record({
        name: this.inputValue,
        begin_date: this.dataValue[0],
        end_date: this.dataValue[1]
      }).then((response) => {
        that.list = response.list
        that.total = response.total
      }).catch((error) => {
        console.log(error)
      })
    }
  }
}
</script>

<style>
</style>
