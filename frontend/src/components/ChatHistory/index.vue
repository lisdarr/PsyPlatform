<template>
  <div>
    <el-button size="mini" type="primary" @click="forDetails(id)" style="margin-right: 10px">
      查看详情
    </el-button>
    <el-dialog title="咨询记录" :visible.sync="dialogTableVisible">
      <el-table :data="gridData" max-height="500px">
        <el-table-column property="date" label="日期" width="170"></el-table-column>
        <el-table-column property="name" label="发送人" width="100"></el-table-column>
        <el-table-column property="message" label="消息"></el-table-column>
      </el-table>
    </el-dialog>
    <el-button size="mini" type="success" @click="exportHistory(id)">导出记录</el-button>
  </div>
</template>

<script>
import { getDetails } from '@/api/consultant'

export default {
  name: 'ChatHistory',
  data() {
    return {
      dialogTableVisible: false,
      gridData: []
    }
  },
  props: ['id'],
  methods: {
    forDetails(index) {
      getDetails(index).then(response => {
        this.dialogTableVisible = true
        const resdata = response.content
        for (const data in resdata) {
          const message = {}
          message['date'] = this.formatDate(resdata[data].timestamp)
          message['name'] = resdata[data].name
          // 需要针对不同的文件形式进行判断
          message['message'] = resdata[data].payload.text
          this.gridData.push(message)
        }
        console.log(this.gridData)
      }).catch(error => {
        console.log(error)
      })
    },
    formatDate(timestamp) {
      var date = new Date(timestamp * 1000)
      var YY = date.getFullYear() + '-'
      var MM = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-'
      var DD = (date.getDate() < 10 ? '0' + (date.getDate()) : date.getDate())
      var hh = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + ':'
      var mm = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()) + ':'
      var ss = (date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds())
      return YY + MM + DD + ' ' + hh + mm + ss
    },
    exportHistory(id) {
      getDetails(id).then(response => {
        const resdata = response.content
        for (const data in resdata) {
          const message = {}
          message['date'] = this.formatDate(resdata[data].timestamp)
          message['name'] = resdata[data].name
          // 需要针对不同的文件形式进行判断
          message['message'] = resdata[data].payload.text
          this.gridData.push(message)
        }
        let str = '日期, 发送人, 消息\n'
        for (let i = 0; i < this.gridData.length; i++) {
          for (const item in this.gridData[i]) {
            str += `${this.gridData[i][item] + '\t'},`
          }
          str += '\n'
        }
        const url = 'data:text/csv;charset=utf-8,\ufeff' + encodeURIComponent(str)
        var link = document.createElement('a')
        link.href = url
        link.download = '咨询记录' + id + '.csv'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      })
    }
  }

}
</script>

<style scoped>

</style>
