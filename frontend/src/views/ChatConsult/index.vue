<template>
  <div class="root-style">
    <!--      监听到没有conversations的时候，显示默认背景图-->
    <div v-show="!this.conversations.length">
      <div style="text-align: center; padding-top: 100px">
        <img src="~@/assets/chat.png" width="300">
        <p>努力做好每一次咨询!</p>
      </div>
    </div>
    <!--      监听到有conversations的时候，显示会话列表-->
    <div v-show="this.conversations.length">
      <!--      会话列表-->
      <div class="conversations">
        <div
          v-for="(conversation, index) in conversations"
          :key="index"
          class="userList"
          :class=" {active:index===findIndex} "
          @click="navigateToChat(index, conversation)"
        >
          <div style="float: left;margin-left: 5px;margin-top: 5px">
            <el-avatar shape="circle" :size="50" :src="conversation.data.avatar"/>
          </div>
          <div style="float: left; color: white;margin-top:18px;margin-left: 5px">
            {{ conversation.data.name }}
          </div>
          <div
            v-show="conversation.unread"
            style="float: left; color: white; background-color: red; border-radius: 50%; width: 17px; height: 17px; text-align: center; margin-top: 1px"
          >
            {{ conversation.unread }}
          </div>
        </div>
      </div>
      <div class="single-conversation">
        <div v-show="!this.$route.query.id">
          <div style="text-align: center; padding-top: 100px">
            <img src="~@/assets/chat.png" width="300">
            <p>努力做好每一次咨询!</p>
          </div>
        </div>
        <div v-show="this.$route.query.id">
          <div class="timer">
            <div class="el-icon-phone-outline" style="font-size: 50px; float: left;margin-top: 20px"/>
            <div style="margin-top: 40px; margin-left: 70px; font-weight: bold; font-size: 20px">正在咨询中...</div>
            <div style="margin-top: 60px; margin-left: 5px; font-weight: bold; font-size: 20px">已咨询时间：</div>
            <div style="margin-top: 30px; font-size: 40px; margin-left: 18px">{{
                this.consultTime[this.$route.query.id]
              }}
            </div>
            <div style="margin-top: 290px; margin-left: 20px">
              <el-button type="text" style="font-size: 35px;padding-left: 15px" @click="dialogVisible = true">
                请求督导
              </el-button>
              <el-dialog
                :visible.sync="dialogVisible"
                width="30%"
              >
                <span>正在为您连线督导，点击确认开始咨询...</span>
                <span slot="footer" class="dialog-footer">
                  <el-button @click="dialogVisible = false">取 消</el-button>
                  <el-button type="primary" @click="ToDir">确 定</el-button>
                </span>
              </el-dialog>

            </div>
            <el-divider/>
            <div style="margin-left: 20px">
              <el-button
                type="text"
                style="font-size: 35px;padding-left: 15px"
                @click="dialogFormVisible = true"
              >
                结束咨询
              </el-button>
              <el-dialog title="本次咨询已结束，请您填写评价" :visible.sync="dialogFormVisible" width="400px">
                <el-form ref="form" :model="form" :rules="rules">
                  <el-form-item label="咨询类型" :label-width="formLabelWidth" prop="type">
                    <el-select v-model="form.type" placeholder="请选择咨询类型">
                      <el-option label="类型1" value="类型1"/>
                      <el-option label="类型2" value="类型2"/>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="评价" :label-width="formLabelWidth" prop="contents">
                    <el-input
                      v-model="form.content"
                      autocomplete="off"
                      type="textarea"
                      :rows="3"
                      placeholder="请输入评价内容"
                    />
                  </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                  <el-button @click="dialogFormVisible = false">点错了，继续咨询</el-button>
                  <el-button type="primary" @click="removeConversation('form')">确 定</el-button>
                </div>
              </el-dialog>
            </div>
          </div>
          <div class="chat-space">
            <div class="message-container">
              <div ref="scrollView" class="scroll-view">
                <div v-for="(message, index) in messages" :key="index">
                  <div
                    v-show="index === 0 || messages[index].timestamp - messages[index-1].timestamp > 5 * 60 * 1000"
                    class="time-lag"
                  >
                    {{ formatDate(message.timestamp) }}
                  </div>
                  <ChatMessage
                    :message="message"
                    :to="friend"
                    :currentUser="currentUser"
                    :type="type"
                    @showImageFullScreen="showImageFullScreen"
                  />
                </div>
              </div>
              <send-box :to="friend" :type="type" @onSent="scrollToBottomNew()"/>
              <div>
                <img :src="image.url" alt="[图片]">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import ChatMessage from '@/views/ChatConsult/ChatMessage'
import SendBox from '@/views/ChatConsult/SendBox'
import { askForDir, getUserList, SaveCurrentRecord, SendCurrentRecord } from '@/api/im'
import { chatHistoryCon } from '@/api/chat'

export default {
  name: 'ChatConsult',
  components: {
    ChatMessage,
    SendBox
  },
  data() {
    return {
      // 记录了咨询师现有全部会话
      conversations: [],
      // 计时器相关
      consultTime: {},
      initTime: {},
      timer: {},
      // 用于判断用户栏指向，对选择对用户栏进行高亮
      findIndex: -1,
      // 通讯需要的数据
      // 聊天记录:当前用户在该聊天窗口发生的全部聊天记录
      messages: [],
      // 聊天对象信息
      friends: [
        {
          avatar: require('@/assets/test.png'),
          name: 'cymm',
          uuid: 'user1'
        },
        {
          avatar: 'https://images.pexels.com/photos/4491461/pexels-photo-4491461.jpeg?cs=srgb&dl=pexels-karolina-grabowska-4491461.jpg&fm=jpg',
          name: '周导',
          uuid: 'director1'
        }
      ],
      // 当前用户信息
      currentUser: {
        avatar: this.$store.getters.avatar,
        name: this.$store.getters.name
      },
      // 控制图片，show：为true时放大查看
      image: {
        show: false,
        url: ''
      },
      // private表示私聊
      type: 'private',
      // 请求督导会话框
      dialogVisible: false,
      //  评价框相关
      dialogFormVisible: false,
      form: {
        type: [],
        content: ''
      },
      formLabelWidth: '120px',
      rules: {
        type: [
          { required: true, message: '请至少选择一种类型', trigger: 'change' }
        ],
        content: [
          { required: true, message: '请填写评价信息', trigger: 'blur' }
        ]
      },
      // 用于记录每个用户发送的消息数量，根据该数量取聊天记录
      chatNums: {},
      SingleRecord: {},
      RecordHistory: [],
      recordId: '',
      RecordInfo: {},
      users: [],
      friend: {},
      // 记录分配给该用户的督导
      matchDir: {}
    }
  },
  beforeMount() {
    this.currentUser.uuid = 'consultant-' + this.$store.getters.id
    // if (this.$store.getters.roles[0] === 'Consultant') {
    //   this.currentUser.uuid = 'consult' + this.$store.getters.id
    // } else if (this.$store.getters.roles[0] === 'Director') {
    //   this.currentUser.uuid = 'director' + this.$store.getters.id
    // }
    // 建立会话连接，user包含用户名+头像+用户id
    if (this.goEasy.getConnectionStatus() === 'disconnected') {
      this.service.connect(this.currentUser)
    }
    getUserList().then(response => {
      this.users = response.content
      console.log(this.users)
    }).catch(error => {
      console.log(error)
    })
    const self = this
    // 加载会话列表
    this.initialPrivateListeners()
    this.goEasy.im.latestConversations({
      onSuccess: function(res) {
        const newconversations = res.content.conversations
        // 开始新的通话，启动新计时器
        if (newconversations.length !== self.conversations.length) {
          const oldcon = new Set(self.conversations)
          const minuscon = newconversations.filter(x => !oldcon.has(x))
          console.log('开启计时器')
          var d = new Date()
          self.initTime[minuscon[0].userId] = d.getTime()
          // console.log(self.initTime[minuscon[0].userId])
        }
        self.conversations = newconversations
        console.log(self.conversations)
      },
      onFailed: function(error) {
        console.log('失败获取最新会话列表, code:' + error.code + ' content:' + error.content)
      }
    })
    this.scrollToBottom()
    if (this.messages.length !== 0) {
      this.markMessageAsRead(this.friend.uuid)
    }
  },
  methods: {
    navigateToChat(index, conversation) {
      this.findIndex = index
      const id = conversation.userId
      this.$router.push({
        name: 'ChatConsult',
        query: {
          id: id
        }
      })
      // 得到对话人的id
      this.type = this.GoEasy.IM_SCENE.PRIVATE
      // 对话人的基本信息，包括name, avatar, uuid;
      // 之后随不同id取不同用户信息
      this.friend = this.findUserById(id)
      console.log(this.friend)
      // if (id === 'user1') {
      //   this.friend = this.friends[0]
      // } else {
      //   this.friend = this.friends[1]
      // }
      // 和该对话人的全部聊天记录
      this.messages = this.service.getPrivateMessages(id)
      if (!this.timer[id]) {
        this.timer[id] = setInterval(this.timeComputed, 1000)
      }
    },
    timeComputed() {
      var d = new Date()
      const id = this.friend.uuid
      const timeminus = (d.getTime() - this.initTime[id]) / 1000
      const hour = parseInt(timeminus / 3600)
      const minite = parseInt((timeminus % 3600) / 60)
      const second = Math.round(timeminus - hour * 3600 - minite * 60)
      const alltime = this.toZero(hour) + ':' + this.toZero(minite) + ':' + this.toZero(second)
      this.$set(this.consultTime, id, alltime)
      // this.consultTime[id] = this.toZero(hour) + ':' + this.toZero(minite) + ':' + this.toZero(second)
      console.log(this.consultTime)
      // alert(this.consultTime[this.$route.query.id])
    },
    toZero(timeNumber) {
      return timeNumber < 10 ? ('0' + timeNumber) : timeNumber
    },
    showImageFullScreen(message) {
      this.image.url = message.payload.url
      this.image.show = true
    },
    scrollToBottom() {
      this.$nextTick(() => {
        this.$refs.scrollView.scrollTo(0, this.$refs.scrollView.scrollHeight)
      })
    },
    scrollToBottomNew() {
      console.log('按完发送键前，当前消息记录数为：' + JSON.stringify(this.chatNums))
      if (this.chatNums[this.$route.query.id]) {
        this.chatNums[this.$route.query.id] = 1 + this.chatNums[this.$route.query.id]
      } else {
        this.chatNums[this.$route.query.id] = 2
      }
      // this.chatNums[this.$route.query.id] = this.chatNums[this.$route.query.id] + 1
      console.log('按完发送键后，当前消息记录数为：' + JSON.stringify(this.chatNums))
      this.$nextTick(() => {
        this.$refs.scrollView.scrollTo(0, this.$refs.scrollView.scrollHeight)
      })
    },
    initialPrivateListeners() {
      const self = this
      // 传入监听器，收到一条私聊消息总是滚到到页面底部
      this.service.onNewPrivateMessageReceive = (friendId, message) => {
        if (friendId in self.chatNums) {
          self.chatNums[friendId] = 1 + self.chatNums[friendId]
        } else {
          self.chatNums[friendId] = 1
        }
        console.log('监听器中统计chatNums：')
        console.log(self.chatNums)
        if (friendId === self.friend.uuid) {
          this.markMessageAsRead(friendId)
          this.scrollToBottom()
        }
      }
    },
    getContent(message) {
      // eslint-disable-next-line no-prototype-builtins
      if (message.payload.hasOwnProperty('text')) {
        return message.payload.text
      } else {
        return message.payload.url
      }
    },
    genRecordId() {
      return Math.random().toString().slice(-6)
    },
    markMessageAsRead(friendId) {
      this.goEasy.im.markPrivateMessageAsRead({
        userId: friendId,
        onSuccess: function() {
          console.log('标记为已读成功')
        },
        onFailed: function(error) {
          console.log('标记为已读失败', error)
        }
      })
    },
    ToDir() {
      const self = this
      askForDir(this.$store.getters.id).then(response => {
        var dir_conversation
        const data = response.content[0]
        self.matchDir[this.friend.uuid] = data.uuid
        dir_conversation = {
          type: 'private',
          userId: data.uuid,
          unread: 0, // 未读消息条数
          data: {
            'avatar': data.avator,
            'name': data.name
          },
          lastMessage: {}
        }
        this.conversations.push(dir_conversation)
        this.dialogVisible = false
        this.$router.push({
          name: 'ChatConsult',
          query: {
            id: dir_conversation.userId
          }
        })
        var d = new Date()
        this.initTime[dir_conversation.userId] = d.getTime()
        console.log('督导初始时间：' + JSON.stringify(this.initTime))
        if (!this.timer[dir_conversation.userId]) {
          this.timer[dir_conversation.userId] = setInterval(this.timeComputed, 1000)
        }
      }).catch(error => {
        console.log('askForDirError', error)
      })
    },
    removeConversation(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          console.log('success submit!!')
        } else {
          console.log('error submit!!')
          return false
        }
      })
      // 生成本次咨询的id
      this.recordId = this.genRecordId()
      var d = new Date()
      // 保存本次咨询相关信息RecordInfo
      this.RecordInfo.id = this.recordId
      var userinfo = this.findUserById(this.$route.query.id)
      this.RecordInfo.vis_name = userinfo.name
      this.RecordInfo.time = this.consultTime[this.$route.query.id]
      this.RecordInfo.date = this.formatDate(d.getTime())
      this.RecordInfo.con_name = this.$store.getters.name
      // 评级和评价由用户返回
      // 咨询师返回咨询类型和评价信息
      // this.RecordInfo.RecordType = this.form.type
      // this.RecordInfo.Recordcontent = this.form.content
      SaveCurrentRecord(this.RecordInfo).then(response => {
        console.log(response.msg)
      }).catch(error => {
        console.log(error)
      })
      this.dialogFormVisible = false
      const self = this
      self.showLoading = true
      // 把当前计时器相关数据上传数据库后，清空
      clearInterval(this.timer[this.$route.query.id])
      this.timer[this.$route.query.id] = ''
      this.consultTime[this.$route.query.id] = ''
      this.initTime[this.$route.query.id] = d.getTime()
      // 保存此次咨询的聊天记录到本地
      console.log('传给chatHistory的值：')
      console.log('userAId:' + JSON.stringify(self.$route.query.id))
      console.log('userBId:' + JSON.stringify(self.currentUser.uuid))
      console.log('limit:' + JSON.stringify(self.chatNums[self.$route.query.id]))
      chatHistoryCon({
        appkey: 'BC-a9e0b1b27564446d942734742f8cbf07',
        userAId: self.$route.query.id,
        userBId: self.currentUser.uuid,
        limit: self.chatNums[self.$route.query.id]
      }).then((response) => {
        self.RecordHistory = []
        console.log('response的值：', JSON.stringify(response))
        for (var item of response.content) {
          self.SingleRecord = {}
          self.SingleRecord.record_id = self.recordId
          if (item.senderId === self.$route.query.id) {
            var senderr = self.findUserById(item.senderId)
          } else {
            senderr = this.currentUser
          }
          self.SingleRecord.senderName = senderr.name
          self.SingleRecord.timestamp = item.timestamp
          self.SingleRecord.type = item.type
          self.SingleRecord.content = self.getContent(item)
          console.log(self.SingleRecord)
          self.RecordHistory.push(self.SingleRecord)
          console.log('RecordHistory：', JSON.stringify(self.RecordHistory))
        }
        // 所有的list类型的都要进行这个格式转换，否则后端取值异常
        // this.RecordHistory = qs.stringify(this.RecordHistory, {
        //   arrayFormat: 'indices'
        // })
        var data = {
          chathistory: JSON.stringify(self.RecordHistory)
        }
        SendCurrentRecord(data).then(response => {
          console.log(self.RecordHistory)
          console.log(response.msg)
        }).catch(error => {
          console.log('SendCurrentRecordError:' + error)
        })
      }).catch((error) => {
        console.log('出错！')
        console.log(error)
      })
      // 复原chatNums对应id的记录数为0
      self.chatNums[self.$route.query.id] = 0
      console.log('移除当前用户后的chatNums：' + JSON.stringify({ chatNums: self.chatNums }))
      this.goEasy.im.removePrivateConversation({
        userId: self.$route.query.id,
        onSuccess: function() {
          self.showLoading = false
        },
        onFailed: function(error) {
          console.log(error)
        }
      })
      // 判断删除该次咨询对应的督导的聊天框
      if (this.matchDir[this.friend.uuid]) {
        var tmpDirId = this.matchDir[this.friend.uuid]
        clearInterval(this.timer[tmpDirId])
        this.consultTime[tmpDirId] = ''
        this.goEasy.im.removePrivateConversation({
          userId: tmpDirId,
          onSuccess: function() {
            self.showLoading = false
          },
          onFailed: function(error) {
            console.log(error)
          }
        })
        this.matchDir[this.friend.uuid] = undefined
      }
      this.$router.replace({
        path: '/ChatConsult'
      })
    },
    findUserById(userId) {
      var user = this.users.find(user => (user.uuid === userId))
      return user
    },
    // 时间戳转换为标准格式 yyyy-MM-dd HH:mm:ss
    formatDate(timestamp) {
      var date = new Date(timestamp)
      var YY = date.getFullYear() + '-'
      var MM = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-'
      var DD = (date.getDate() < 10 ? '0' + (date.getDate()) : date.getDate())
      var hh = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + ':'
      var mm = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()) + ':'
      var ss = (date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds())
      return YY + MM + DD + ' ' + hh + mm + ss
    }
  }
}
</script>

<style scoped>
.userList {
  width: 100%;
  height: 60px;
  background-color: #1A374D;
  border: #1A374D;
}

.userList:hover {
  background-color: #304156;
  border: #304156;
}

.active {
  background-color: #304156;
  border: #304156;
}

.message-container {
  /*padding-bottom: 10rem;*/
  overflow: hidden;
  width: 100%;
  height: 100%;
}

.message-container .scroll-view {
  height: 80%;
  padding-left: 0.1rem;
  padding-right: 0.1rem;
  box-sizing: border-box;
  overflow-y: auto;
  /*使用具有回弹效果的滚动, 当手指从触摸屏上移开，内容会继续保持一段时间的滚动效果*/
  -webkit-overflow-scrolling: touch;
}

.message-container .scroll-view .time-lag {
  font-size: 18px;
  text-align: center;
  color: #304156;
  padding: 0.5rem;
}

.root-style {
  border: #304156;
  width: 95%;
  height: 700px;
  border-style: solid;
  border-left-style: solid;
  margin: 20px;
  float: left;
}

.conversations {
  width: 15%;
  border: #304156;
  height: 694px;
  border-style: none;
  float: left;
}

.single-conversation {
  width: 85%;
  border: #304156;
  height: 694px;
  border-style: solid;
  border-bottom-style: none;
  border-right-style: none;
  border-top-style: none;
  float: left;
}

.timer {
  border: #304156;
  width: 20%;
  height: 694px;
  border-style: solid;
  border-left-style: none;
  float: left;
  background-color: #304156;
  color: white
}

.chat-space {
  border: #304156;
  width: 80%;
  height: 694px;
  float: left;
}
</style>
