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
          <el-button
            type="danger"
            plain
            size="mini"
            @click="scope.$index, scope.row"
            >禁用</el-button
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
          name: "用户某某某",
          gender: "女",
          username: "oicw138aib47GasW",
          phonenumber: "18362482284",
          contact: "lucy",
          contactnumber: "19362829173",
          role: "访客",
          date: "2022-3-15",
          state: "正常"
        },
        {
          name: "用户某某某",
          gender: "女",
          username: "oicw138aib47GasW",
          phonenumber: "18362482284",
          contact: "lucy",
          contactnumber: "19362829173",
          role: "访客",
          date: "2022-3-15",
          state: "正常"
        },
        {
          name: "用户某某某",
          gender: "女",
          username: "oicw138aib47GasW",
          phonenumber: "18362482284",
          contact: "lucy",
          contactnumber: "19362829173",
          role: "访客",
          date: "2022-3-15",
          state: "正常"
        },
        {
          name: "用户某某某",
          gender: "女",
          username: "oicw138aib47GasW",
          phonenumber: "18362482284",
          contact: "lucy",
          contactnumber: "19362829173",
          role: "访客",
          date: "2022-3-15",
          state: "正常"
        },
        {
          name: "用户某某某",
          gender: "女",
          username: "oicw138aib47GasW",
          phonenumber: "18362482284",
          contact: "lucy",
          contactnumber: "19362829173",
          role: "访客",
          date: "2022-3-15",
          state: "正常"
        },
        {
          name: "用户某某某",
          gender: "女",
          username: "oicw138aib47GasW",
          phonenumber: "18362482284",
          contact: "lucy",
          contactnumber: "19362829173",
          role: "访客",
          date: "2022-3-15",
          state: "正常"
        },
        {
          name: "用户某某某",
          gender: "女",
          username: "oicw138aib47GasW",
          phonenumber: "18362482284",
          contact: "lucy",
          contactnumber: "19362829173",
          role: "访客",
          date: "2022-3-15",
          state: "正常"
        },
        {
          name: "用户某某某",
          gender: "女",
          username: "oicw138aib47GasW",
          phonenumber: "18362482284",
          contact: "lucy",
          contactnumber: "19362829173",
          role: "访客",
          date: "2022-3-15",
          state: "正常"
        },
        {
          name: "用户某某某",
          gender: "女",
          username: "oicw138aib47GasW",
          phonenumber: "18362482284",
          contact: "lucy",
          contactnumber: "19362829173",
          role: "访客",
          date: "2022-3-15",
          state: "正常"
        },
        {
          name: "用户某某某",
          gender: "女",
          username: "oicw138aib47GasW",
          phonenumber: "18362482284",
          contact: "lucy",
          contactnumber: "19362829173",
          role: "访客",
          date: "2022-3-15",
          state: "正常"
        },
        {
          name: "用户某某某",
          gender: "女",
          username: "oicw138aib47GasW",
          phonenumber: "18362482284",
          contact: "lucy",
          contactnumber: "19362829173",
          role: "访客",
          date: "2022-3-15",
          state: "正常"
        },
        {
          name: "用户某某某",
          gender: "女",
          username: "oicw138aib47GasW",
          phonenumber: "18362482284",
          contact: "lucy",
          contactnumber: "19362829173",
          role: "访客",
          date: "2022-3-15",
          state: "正常"
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