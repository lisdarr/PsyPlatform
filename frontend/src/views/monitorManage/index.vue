<template>
  <div>
    <div style="display: inline">
      <div
        style="width: 200px; float: left; margin-top: 20px; margin-left: 20px"
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
        style="width: 30px; float: left; margin-top: 50px; margin-left: 10px"
      >
        <el-button size="small" icon="el-icon-search" @click="search"
          >搜索</el-button
        >
      </div>
      <div class="addbtn">
        <el-button type="primary" @click="dialogFormVisible = true" size="small"
          >新增督导
        </el-button>
      </div>
    </div>

    <el-table
      style="width: 100%; margin-left: 12px; padding-top: 15px; height = 400px"
      :data="list.slice((page - 1) * limit, page * limit)"
    >
      <el-table-column
        prop="name"
        label="姓名"
        width="80px"
        align="center"
      ></el-table-column>
      <!-- <el-table-column
        prop="role"
        label="身份"
        width="80px"
        align="center"
      ></el-table-column> -->
      <el-table-column
        prop="consultant"
        label="绑定咨询师"
        width="280px"
        align="center"
      ></el-table-column>
      <el-table-column
        align="center"
        prop="sum"
        label="总咨督导次数"
        width="120px"
      ></el-table-column>
      <el-table-column
        align="center"
        prop="time"
        label="督导总时长"
        width="180px"
      ></el-table-column>
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
            size="small"
            @click="editMonitor(scope.row)"
            >修改</el-button
          >
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

    <!-- 新增督导 -->
    <el-dialog title="新增督导" :visible.sync="dialogFormVisible">
      <el-form
        ref="form"
        :model="form"
        :rules="addRule"
        label-width="100px"
        size="small"
      >
        <el-row>
          <el-col :span="12"
            ><el-form-item label="姓名" prop="name"
              ><el-input
                v-model="form.name"
                placeholder="请输入姓名"
                autocomplete="off"
              ></el-input> </el-form-item
          ></el-col>
          <el-col :span="12"
            ><el-form-item label="性别" prop="gender">
              <el-radio-group v-model="form.gender">
                <el-radio label="男"></el-radio>
                <el-radio label="女"></el-radio>
              </el-radio-group> </el-form-item
          ></el-col>
        </el-row>
        <el-row>
          <el-col :span="12"
            ><el-form-item label="年龄" prop="age"
              ><el-input
                v-model="form.age"
                placeholder="请输入年龄"
                autocomplete="off"
              ></el-input></el-form-item
          ></el-col>
          <el-col :span="12"
            ><el-form-item label="身份证号码" prop="idNumber">
              <el-input
                v-model="form.idNumber"
                placeholder="请输入身份证号码"
                autocomplete="off"
              ></el-input> </el-form-item
          ></el-col>
        </el-row>
        <el-row>
          <el-col :span="12"
            ><el-form-item label="电话" prop="phone">
              <el-input
                v-model="form.phone"
                placeholder="请输入联系电话"
                autocomplete="false"
              ></el-input> </el-form-item
          ></el-col>
          <el-col :span="12"
            ><el-form-item label="邮箱" prop="email">
              <el-input
                v-model="form.email"
                placeholder="请输入邮箱地址"
                autocomplete="false"
              ></el-input> </el-form-item
          ></el-col>
        </el-row>
        <el-row>
          <el-col :span="12"
            ><el-form-item label="用户名" prop="userName">
              <el-input
                v-model="form.userName"
                placeholder="请输入用户名"
                autocomplete="false"
              ></el-input> </el-form-item
          ></el-col>
          <el-col :span="12"
            ><el-form-item label="密码" prop="pwd">
              <el-input
                v-model="form.pwd"
                :type="[flag ? 'text' : 'password']"
                style="border: 1px solid #fff; width: 170px"
                placeholder="请输入密码"
              >
                <i
                  slot="suffix"
                  :class="[flag ? 'el-icon-lock' : 'el-icon-view']"
                  style="margin-top: 8px; font-size: 14px"
                  autocomplete="false"
                  @click="flag = !flag"
                />
              </el-input> </el-form-item
          ></el-col>
        </el-row>
        <el-row>
          <el-col :span="12"
            ><el-form-item label="工作单位" prop="company">
              <el-input
                v-model="form.company"
                placeholder="请输入工作单位"
                autocomplete="false"
              ></el-input> </el-form-item
          ></el-col>
          <el-col :span="12"
            ><el-form-item label="职称" prop="rank">
              <el-input
                v-model="form.rank"
                placeholder="请输入个人职称"
                autocomplete="false"
              ></el-input> </el-form-item
          ></el-col>
        </el-row>
        <el-row>
          <el-col :span="12"
            ><el-form-item label="督导资质" prop="qualId">
              <el-select v-model="form.qualId" placeholder="请选择督导资质">
                <el-option
                  v-for="item in qualList"
                  :key="item.qualId"
                  :label="item.qualName"
                  :value="item.qualId"
                >
                </el-option>
              </el-select> </el-form-item
          ></el-col>
          <el-col :span="12"
            ><el-form-item label="资质编号" prop="certId">
              <el-input
                v-model="form.certId"
                placeholder="请输入资质编号"
                autocomplete="false"
              ></el-input> </el-form-item
          ></el-col>
        </el-row>
        <el-form-item style="text-align: center">
          <el-button size="small" @click="dialogFormVisible = false"
            >取 消
          </el-button>
          <el-button size="small" type="primary" @click="saveAdd(form)"
            >确 定
          </el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <!-- 修改督导信息 -->
    <el-dialog title="修改督导信息" :visible.sync="dialogVisible">
      <el-form :model="editform" label-width="90px" size="small">
        <el-form-item label="姓名">
          <el-input v-model="editform.name"></el-input>
        </el-form-item>
        <el-form-item label="周值班安排">
          <el-checkbox-group v-model="editform.schedule">
            <el-checkbox label="Mon"
              ><el-tag type="success">周一</el-tag></el-checkbox
            >
            <el-checkbox label="Tue"
              ><el-tag type="success">周二</el-tag></el-checkbox
            >
            <el-checkbox label="Wed"
              ><el-tag type="success">周三</el-tag></el-checkbox
            >
            <el-checkbox label="Thu"
              ><el-tag type="success">周四</el-tag></el-checkbox
            >
            <el-checkbox label="Fri"
              ><el-tag type="success">周五</el-tag></el-checkbox
            >
            <el-checkbox label="Sat"
              ><el-tag type="success">周六</el-tag></el-checkbox
            >
            <el-checkbox label="Sun"
              ><el-tag type="success">周日</el-tag></el-checkbox
            >
          </el-checkbox-group>
        </el-form-item>
      </el-form>

      <div slot="footer">
        <el-button @click="dialogVisible = false" size="small">取 消</el-button>
        <el-button type="primary" @click="saveEdit" size="small"
          >确 定</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { dir_edit, dir_info, dir_add } from "@/api/admin";
import qs from "qs";

export default {
  name: "monitorManage",
  data() {
    return {
      flag: "false",
      page: 1,
      limit: 7,
      total: 12,
      inputValue: "",
      list: [],
      dialogFormVisible: false,
      dialogVisible: false,
      form: {
        name: "",
        gender: "",
        age: "",
        idNumber: "",
        phone: "",
        email: "",
        userName: "",
        pwd: "",
        company: "",
        rank: "",
        qualId: "",
        certId: "",
      },
      editform: {
        id: "",
        name: "",
        schedule: [],
      },
      qualList: "",
      addRule: {
        name: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          {
            min: 3,
            max: 10,
            message: "用户名长度在3~10个字符",
            trigger: "blur",
          },
        ],
        gender: [{ required: true, message: "请选择性别", trigger: "change" }],
        age: [{ required: true, message: "请输入年龄", trigger: "blur" }],
        idNumber: [
          { required: true, message: "请输入身份证号码", trigger: "blur" },
          { min: 18, max: 18, message: "身份证号码为18位", trigger: "blur" },
        ],
        phone: [
          { required: true, message: "请输入电话号码", trigger: "blur" },
          { min: 11, max: 11, message: "电话号码为11位", trigger: "blur" },
        ],
        email: [{ required: true, message: "请输入邮箱", trigger: "blur" }],
        userName: [
          { required: true, message: "请输入昵称", trigger: "blur" },
          { min: 3, max: 10, message: "昵称长度在3~10个字符", trigger: "blur" },
        ],
        pwd: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { min: 6, max: 15, message: "密码长度在6~15个字符", trigger: "blur" },
        ],
        company: [
          { required: true, message: "请输入工作单位", trigger: "blur" },
        ],
        rank: [{ required: true, message: "请输入职称", trigger: "blur" }],
        qualId: [
          { required: true, message: "请选择督导资质", trigger: "change" },
        ],
        certId: [
          { required: true, message: "请输入资质编号", trigger: "blur" },
        ],
      },
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
      dir_info({
        name: this.inputValue,
      })
        .then((response) => {
          that.list = response.list;
          that.total = response.total;
          // console.log(that.total);
          that.qualList = response.qualList;
          // console.log(that.qualList);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    editMonitor(row) {
      this.editform.id = row.id;
      this.dialogVisible = true;
    },
    saveEdit() {
      this.dialogVisible = false;
      var that = this;
      // 所有的list类型的都要进行这个格式转换，否则后端取值异常
      this.editform.schedule = qs.stringify(this.editform.schedule, {
        arrayFormat: "indices",
      });
      dir_edit(this.editform)
        .then(() => {
          that.$message.success("修改成功！");
          that.search();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    saveAdd(form) {
      this.$refs.form.validate(async (success) => {
        if (success) {
          this.dialogFormVisible = false;
          var that = this;
          dir_add(form)
            .then((response) => {
              if (response.status == 500) {
                that.$message.error("保存失败！");
              } else {
                that.$message.success("添加成功！");
                that.search();
              }
            })
            .catch((error) => {
              console.log(error);
            });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
  },
};
</script>

<style>
.addbtn {
  margin-top: 50px;
  text-align: right;
  margin-right: 30px;
  margin-bottom: 15px;
  float: right;
}
</style>