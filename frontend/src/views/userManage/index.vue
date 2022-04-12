<template>
  <div>
    <div style="width: 200px; float: left; margin-top: 20px; margin-left: 20px">
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
    <div style="width: 30px; float: left; margin-top: 50px; margin-left: 10px">
      <el-button size="small" icon="el-icon-search" @click="search"
        >搜索
      </el-button>
    </div>
    <el-table
      style="width: 100%; margin-left: 12px; padding-top: 15px; height = 400px"
      :data="list.slice((page - 1) * limit, page * limit)"
    >
      <el-table-column
        prop="name"
        label="姓名"
        width="100px"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="gender"
        label="性别"
        width="50px"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="username"
        label="用户名"
        width="180px"
        align="center"
      ></el-table-column>
      <el-table-column
        align="center"
        prop="phonenumber"
        label="联系电话"
        width="120px"
      ></el-table-column>
      <el-table-column
        align="center"
        prop="contact"
        label="紧急联系人"
        width="100px"
      ></el-table-column>
      <el-table-column
        prop="contactnumber"
        label="紧急联系电话"
        width="120px"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="role"
        label="身份"
        width="60px"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="date"
        label="注册时间"
        width="120px"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="state"
        label="帐号状态"
        width="80px"
        align="center"
      ></el-table-column>
      <el-table-column prop="operate" label="操作" align="center">
        <template slot-scope="scope">
          <el-button type="danger" plain size="mini" @click="stopUse(scope.row.name)"
            >禁用
          </el-button>
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
import { visitor_ban, visitor_info } from "@/api/admin";

export default {
  name: "userManage",
  data() {
    return {
      inputValue: "",
      page: 1,
      limit: 7,
      total: 12,
      list: "",
    };
  },
  mounted() {
    this.search();
  },
  methods: {
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
    },
    search() {
      var that = this;
      visitor_info({
        name: this.inputValue,
      })
        .then((response) => {
          that.list = response.list;
          that.total = response.total;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    stopUse(name) {
      this.$confirm("确定永久禁用该账号吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          visitor_ban({
            name: name,
          })
            .then(() => {
              this.search();
              this.$message({
                type: "success",
                message: "已禁用!",
              });
            })
            .catch((error) => {
              console.log(error);
            });
        })
        .catch((error) => {
          this.$message({
            type: "info",
            message: "已取消操作",
          });
          console.log(error);
        });
    },
  },
};
</script>

<style>
</style>
