<template>
  <div>
    <el-table style="width: 100%" border height="500" :data="list">
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
      ></el-table-column>
      <el-table-column
        prop="level"
        label="咨询评级"
        width="100px"
        align="center"
      ></el-table-column>
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
          <el-button type = "info" plain icon="el-icon-info" size="mini" @click="(scope.$index, scope.row)"
            >查看详情</el-button
          >
          <el-button
            size="mini"
            type="success" plain
            icon="el-icon-download"
            @click="handleDelete(scope.$index, scope.row)"
            >导出记录</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <!-- @size-change="handleSizeChange"
            @current-change="handleCurrentChange" -->
    <el-pagination
      style="margin-top: 20px; text-align: center"
      :current-page="page"
      :page-sizes="[3,5,8]"
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
  name: "consultRecord",
//   methods: {
//     handleClick(row) {
//       console.log(row);
//     },
//   },
  data() {
    return {
      page: 1,
      limit: 3,
      total: 12,
      list: [
        {
          name: "张先生",
          time: "100min",
          date: "2022-03-14 13:45:06",
          level: "4.5",
          eva: "体验很好",
          assit: "无",
        },
        {
          name: "张先生",
          time: "100min",
          date: "2022-03-14 13:45:06",
          level: "4.5",
          eva: "体验很好",
          assit: "无",
        },
        {
          name: "张先生",
          time: "100min",
          date: "2022-03-14 13:45:06",
          level: "4.5",
          eva: "体验很好",
          assit: "无",
        },
        {
          name: "张先生",
          time: "100min",
          date: "2022-03-14 13:45:06",
          level: "4.5",
          eva: "体验很好",
          assit: "无",
        },
        {
          name: "张先生",
          time: "100min",
          date: "2022-03-14 13:45:06",
          level: "4.5",
          eva: "体验很好",
          assit: "无",
        },
        {
          name: "张先生",
          time: "100min",
          date: "2022-03-14 13:45:06",
          level: "4.5",
          eva: "体验很好",
          assit: "无",
        },
        {
          name: "张先生",
          time: "100min",
          date: "2022-03-14 13:45:06",
          level: "4.5",
          eva: "体验很好",
          assit: "无",
        },
        {
          name: "张先生",
          time: "100min",
          date: "2022-03-14 13:45:06",
          level: "4.5",
          eva: "体验很好",
          assit: "无",
        },
        {
          name: "张先生",
          time: "100min",
          date: "2022-03-14 13:45:06",
          level: "4.5",
          eva: "体验很好",
          assit: "无",
        },
        {
          name: "张先生",
          time: "100min",
          date: "2022-03-14 13:45:06",
          level: "4.5",
          eva: "体验很好",
          assit: "无",
        },
        {
          name: "张先生",
          time: "100min",
          date: "2022-03-14 13:45:06",
          level: "4.5",
          eva: "体验很好",
          assit: "无",
        },
        {
          name: "张先生",
          time: "100min",
          date: "2022-03-14 13:45:06",
          level: "4.5",
          eva: "体验很好",
          assit: "无",
        }
      ]
    };
  },
  //组件挂载完毕发请求
  mounted() {
    //   获取列表数据方法
    this.getPageList();
  },
  methods: {
    //   获取品牌列表的数据
    async getPageList(pager = 1) {
        this.page = pager;
      // 获取品牌列表的接口
      const { page, limit } = this;
      // 当向服务器发请求的时候，这个函数需要参数，在上面的data中初始化两个字段，代表给服务器传递参数
      //在consultRecord.js中定义了读取数据的url
      let result = await this.$API.consultRecord.reqConsultRecordList(
        page,
        limit
      );
    //   if (result.code == 200) {
        // this.total = result.data.total;
        // this.list = result.data.records;
    //   }
    },
    handleCurrentChange(pager){
        // 修改参数
        this.page = pager;
        this.getPageList();
    },
    handleSizeChange(limit){
        this.limit = limit;
        this.getPageList();
    }
  },
};
</script>

<style>
</style>