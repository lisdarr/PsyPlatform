<template>
  <div>
    <div inline="true">
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
        >搜索
        </el-button>
      </div>
      <div class="addbtn">
        <el-button type="primary" @click="addConsultant" size="small"
        >新增咨询师
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
            @click="editConsultant(scope.row)"
          >修改
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

    <!-- 新增咨询师 -->
    <el-dialog title="新增咨询师" :visible.sync="dialogFormVisible">
      <el-form :model="form" inline="true" label-width="90px" size="small">
        <el-form-item label="姓名">
          <el-input
            v-model="form.name"
            placeholder="请输入姓名"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.gender">
            <el-radio label="男"></el-radio>
            <el-radio label="女"></el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <el-form :model="form" inline="true" label-width="90px" size="small">
        <el-form-item label="年龄">
          <el-input
            v-model="form.age"
            placeholder="请输入年龄"
            autocomplete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="身份证号码">
          <el-input
            v-model="form.idNumber"
            placeholder="请输入身份证号码"
            autocomplete="off"
          ></el-input>
        </el-form-item>
      </el-form>
      <el-form :model="form" inline="true" label-width="90px" size="small">
        <el-form-item label="电话">
          <el-input
            v-model="form.phone"
            placeholder="请输入联系电话"
            autocomplete="false"
          ></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input
            v-model="form.email"
            placeholder="请输入邮箱地址"
            autocomplete="false"
          ></el-input>
        </el-form-item>
      </el-form>
      <el-form :model="form" label-width="90px" size="small">
        <el-form-item label="绑定督导">
          <el-select v-model="form.monitorId" placeholder="请选择一个督导">
            <el-option
              v-for="item in monitorList"
              :key="item.monitorId"
              :label="item.name"
              :value="item.monitorId"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <el-form :model="form" inline="true" label-width="90px" size="small">
        <el-form-item label="用户名">
          <el-input
            v-model="form.userName"
            placeholder="请输入用户名"
            autocomplete="false"
          ></el-input>
        </el-form-item>
        <el-form-item label="密码">
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
          </el-input>
        </el-form-item>
      </el-form>
      <el-form :model="form" inline="true" label-width="90px" size="small">
        <el-form-item label="工作单位">
          <el-input
            v-model="form.company"
            placeholder="请输入工作单位"
            autocomplete="false"
          ></el-input>
        </el-form-item>
        <el-form-item label="职称">
          <el-input
            v-model="form.rank"
            placeholder="请输入个人职称"
            autocomplete="false"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false" size="small"
        >取 消
        </el-button>
        <el-button type="primary" @click="saveAdd" size="small"
        >确 定
        </el-button>
      </div>
    </el-dialog>

    <!-- 修改 -->
    <el-dialog title="修改咨询师信息" :visible.sync="dialogVisible">
      <el-form :model="editform" inline="true" label-width="90px" size="small">
        <el-form-item label="姓名">
          <el-input v-model="editform.name"></el-input>
        </el-form-item>
        <el-form-item label="绑定督导">
          <el-select v-model="editform.monitor" placeholder="请选择一个督导">
            <el-option
              v-for="item in monitorList"
              :key="item.monitorId"
              :label="item.monitorName"
              :value="item.monitorId"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <el-form :model="editform" label-width="90px" size="small">
        <el-form-item label="周值班安排">
          <el-checkbox-group v-model="editform.schedule">
            <el-checkbox
              v-for="(item, index) in totalWeek"
              :label="item.name"
              :key="index"
            >{{ item.name }}
            </el-checkbox
            >
            <!-- <el-checkbox label="Mon"
            >
              <el-tag type="success">周一</el-tag>
            </el-checkbox
            >
            <el-checkbox label="Tue"
            >
              <el-tag type="success">周二</el-tag>
            </el-checkbox
            >
            <el-checkbox label="Wen" name="schedule"
            >
              <el-tag type="success">周三</el-tag>
            </el-checkbox
            >
            <el-checkbox label="Thu" name="schedule"
            >
              <el-tag type="success">周四</el-tag>
            </el-checkbox
            >
            <el-checkbox label="Fri" name="schedule"
            >
              <el-tag type="success">周五</el-tag>
            </el-checkbox
            >
            <el-checkbox label="Sat" name="schedule"
            >
              <el-tag type="success">周六</el-tag>
            </el-checkbox
            >
            <el-checkbox label="Sun" name="schedule"
            >
              <el-tag type="success">周日</el-tag>
            </el-checkbox
            > -->
          </el-checkbox-group>
        </el-form-item>
      </el-form>

      <div slot="footer">
        <el-button @click="dialogVisible = false" size="small">取 消</el-button>
        <el-button type="primary" @click="saveEdit" size="small"
        >确 定
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { con_add, con_edit, con_info } from '@/api/admin'
import qs from 'qs'

export default {
  name: 'consultantManage',
  data() {
    return {
      totalWeek: [
        { name: 'Mon' },
        { name: 'Tue' },
        { name: 'Wen' },
        { name: 'Thu' },
        { name: 'Fri' },
        { name: 'Sat' },
        { name: 'Sun' }
      ],
      flag: 'false',
      page: 1,
      limit: 7,
      total: 12,
      inputValue: '',
      dataValue: '',
      list: [],
      dialogFormVisible: false,
      dialogVisible: false,
      form: {
        name: '',
        gender: '',
        age: '',
        idNumber: '',
        phone: '',
        email: '',
        monitorId: '',
        userName: '',
        pwd: '',
        company: '',
        rank: ''
      },
      editform: {
        id: '',
        name: '',
        monitor: '',
        schedule: []
      },
      // 选择督导框
      monitorList: ''
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
    search() {
      console.log('搜索')
      var that = this
      con_info({ name: this.inputValue })
        .then((response) => {
          that.list = response.list
          that.total = response.total
          that.monitorList = response.monitorList
        })
        .catch((error) => {
          console.log(error)
        })
    },
    addConsultant() {
      this.dialogFormVisible = true
    },
    editConsultant(row) {
      this.editform.id = row.id
      this.dialogVisible = true
      console.log(typeof this.editform)
    },
    saveEdit() {
      this.dialogVisible = false
      var that = this
      // 所有的list类型的都要进行这个格式转换，否则后端取值异常
      this.editform.schedule = qs.stringify(this.editform.schedule, { arrayFormat: 'indices' })
      con_edit(this.editform)
        .then(() => {
          that.$message.success('修改成功！')
          that.search()
        })
        .catch((error) => {
          console.log(error)
        })
    },

    saveAdd() {
      console.log('保存添加')
      this.dialogFormVisible = false
      var that = this
      console.log(typeof this.form)
      con_add(this.form)
        .then(() => {
          that.$message.success('添加成功！')
          that.search()
        })
        .catch((error) => {
          console.log(error)
        })
    }
  }
}
</script>

<style>
.addbtn {
  margin-top: 50px;
  text-align: right;
  margin-right: 35px;
  margin-bottom: 15px;
  float: right;
}
</style>
