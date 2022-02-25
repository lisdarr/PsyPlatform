<template>
  <div class="dashboard-container">
   <!--    <div class="dashboard-text">name: {{ name }}</div>-->
    <el-row style="height: 550px" :gutter="20">
      <el-col :span="15">
        <el-row style="width: 750px; height: 250px">
          <el-card class="box-card" style="width: auto">

          </el-card>
        </el-row>
        <el-row  style="width: 750px; height: 250px">
          <el-card class="box-card" style="width: auto">

          </el-card>
        </el-row>
      </el-col>
      <el-col :span="9" style="height: 520px;">
        <el-card class="box-card" style="width: auto; height: 520px" >
          日历
          <a-calendar :fullscreen="false" @panelChange="onPanelChange" />
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20">
      <!--        data:数组类型-->
      <el-col>
        <el-card style="width: auto;">
          <el-table
            :data="tableData">
            <el-table-column
              label="咨询人"
              width="100">
              <template slot-scope="scope">
                <i class="el-icon-time"></i>
                <span style="margin-left: 10px">{{ scope.row.date }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="咨询时长"
              width="180">
              <template slot-scope="scope">
                <el-popover trigger="hover" placement="top">
                  <p>姓名: {{ scope.row.name }}</p>
                  <p>住址: {{ scope.row.address }}</p>
                  <div slot="reference" class="name-wrapper">
                    <el-tag size="medium">{{ scope.row.name }}</el-tag>
                  </div>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column
              label="咨询日期"
              width="180">
              <template slot-scope="scope">
                <i class="el-icon-time"></i>
                <span style="margin-left: 10px">{{ scope.row.date }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="咨询评级"
              width="180">
              <template slot-scope="scope">
                <el-popover trigger="hover" placement="top">
                  <p>姓名: {{ scope.row.name }}</p>
                  <p>住址: {{ scope.row.address }}</p>
                  <div slot="reference" class="name-wrapper">
                    <el-tag size="medium">{{ scope.row.name }}</el-tag>
                  </div>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column
              label="咨询评价"
              width="180">
              <template slot-scope="scope">
                <el-popover trigger="hover" placement="top">
                  <p>姓名: {{ scope.row.name }}</p>
                  <p>住址: {{ scope.row.address }}</p>
                  <div slot="reference" class="name-wrapper">
                    <el-tag size="medium">{{ scope.row.name }}</el-tag>
                  </div>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                <el-button
                  size="mini"
                  type="danger"
                  @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

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
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  data() {
    return {
      tableData: [{
        date: '2016-05-02',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-04',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1517 弄'
      }, {
        date: '2016-05-01',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1519 弄'
      }, {
        date: '2016-05-03',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1516 弄'
      }],
      // value: new Date()
    }
  },
  methods: {
    handleEdit(index, row) {
      console.log(index, row);
    },
    handleDelete(index, row) {
      console.log(index, row);
    },
    onPanelChange(value, mode) {
      console.log(value, mode);
    },
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
</style>
