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
    </div>
    <el-table
      style="width: 100%;
      margin-left: 12px;
      padding-top: 15px;
      height: 400px"
      :data="list.slice((page-1)*limit, page*limit)"
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
        width="180px"
        align="center"
      >
        <template slot-scope="scope">
          <el-rate v-model="scope.row.rate" :allow-half="true" disabled text-color="#ff9900"></el-rate>
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
        width="80px"
        align="center"
      ></el-table-column>
      <el-table-column prop="operate" label="操作" align="center">
        <template slot-scope="scope">
          <el-button type="info" plain icon="el-icon-info" size="mini" @click="(scope.$index, scope.row)"
          >查看详情
          </el-button
          >
          <el-button
            size="mini"
            type="success" plain
            icon="el-icon-download"
            @click="handleDelete(scope.$index, scope.row)"
          >导出记录
          </el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <!-- @size-change="handleSizeChange"
            @current-change="handleCurrentChange" -->
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
  name: 'RecordAdmin',
  //   methods: {
  //     handleClick(row) {
  //       console.log(row);
  //     },
  //   },
  data() {
    return {
      value1: null,
      page: 1,
      limit: 7,
      total: 12,
      list: [
        {
          name: '张先生',
          time: '1:02:00',
          date: '2022-03-12 13:45:06',
          rate: 4.5,
          eva: '体验很好',
          assit: '无'
        },
        {
          name: '张先生',
          time: '1:02:00',
          date: '2022-03-13 13:45:06',
          rate: 4.5,
          eva: '体验很好',
          assit: '无'
        },
        {
          name: '张先生',
          time: '1:02:00',
          date: '2022-03-14 13:43:06',
          rate: 4.5,
          eva: '体验很好',
          assit: '无'
        },
        {
          name: '张先生',
          time: '1:02:00',
          date: '2022-03-14 13:45:06',
          rate: 4.5,
          eva: '体验很好',
          assit: '无'
        },
        {
          name: '张先生',
          time: '1:02:00',
          date: '2022-03-14 13:45:06',
          rate: 4.5,
          eva: '体验很好',
          assit: '无'
        },
        {
          name: '张先生',
          time: '1:02:00',
          date: '2022-03-14 13:45:06',
          rate: 4.5,
          eva: '体验很好',
          assit: '无'
        },
        {
          name: '张先生',
          time: '1:02:00',
          date: '2022-03-14 13:45:06',
          rate: 4.5,
          eva: '体验很好',
          assit: '无'
        },
        {
          name: '张先生',
          time: '1:02:00',
          date: '2022-03-14 13:45:06',
          rate: 4.5,
          eva: '体验很好',
          assit: '无'
        },
        {
          name: '张先生',
          time: '1:02:00',
          date: '2022-03-14 13:45:06',
          rate: 4.5,
          eva: '体验很好',
          assit: '无'
        },
        {
          name: '张先生',
          time: '1:02:00',
          date: '2022-03-14 13:45:06',
          rate: 4.5,
          eva: '体验很好',
          assit: '无'
        },
        {
          name: '张先生',
          time: '1:02:00',
          date: '2022-03-14 13:45:06',
          rate: 4.5,
          eva: '体验很好',
          assit: '无'
        },
        {
          name: '张先生',
          time: '1:02:00',
          date: '2022-03-14 13:45:06',
          rate: 4.5,
          eva: '体验很好',
          assit: '无'
        }
      ]
    }
  },
  methods: {
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
    }
  }
  //组件挂载完毕发请求
  // mounted() {
  //   //   获取列表数据方法
  //   this.getPageList();
  // },
  // methods: {
  //   //   获取品牌列表的数据
  //   async getPageList(pager = 1) {
  //       this.page = pager;
  //     // 获取品牌列表的接口
  //     const { page, limit } = this;
  //     // 当向服务器发请求的时候，这个函数需要参数，在上面的data中初始化两个字段，代表给服务器传递参数
  //     //在consultRecord.js中定义了读取数据的url
  //     // let result = await this.$API.consultRecord.reqConsultRecordList(
  //     //   page,
  //     //   limit
  //     // );
  //   //   if (result.code == 200) {
  //       // this.total = result.data.total;
  //       // this.list = result.data.records;
  //   //   }
  //   },
  //   handleCurrentChange(pager){
  //       // 修改参数
  //       this.page = pager;
  //       this.getPageList();
  //   },
  //   handleSizeChange(limit){
  //       this.limit = limit;
  //       this.getPageList();
  //   }
  // },
}
</script>

<style>
</style>
