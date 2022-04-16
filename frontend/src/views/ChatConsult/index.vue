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
                  <el-form-item label="咨询类型" :label-width="formLabelWidth">
                    <el-select v-model="form.type" placeholder="请选择咨询类型">
                      <el-option label="类型1" value="类型1"/>
                      <el-option label="类型2" value="类型2"/>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="评价" :label-width="formLabelWidth">
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
                    :current-user="currentUser"
                    :type="type"
                    @showImageFullScreen="showImageFullScreen"
                  />
                </div>
              </div>
              <send-box :to="friend" :type="type" @onSent="scrollToBottom"/>
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
import { AllDir, AllUser } from '@/api/im'

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
      friend: {},
      users: [],
      // 存储进行通话的用户id
      friendsid: [],
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
          { required: true, message: '请选择咨询类型', trigger: 'change' }
        ]
      },
      RecordHistory: []
    }
  },
  beforeMount() {
    if (this.$store.getters.roles[0] === 'Consultant') {
      this.currentUser.uuid = 'consult' + this.$store.getters.id
    } else if (this.$store.getters.roles[0] === 'Director') {
      this.currentUser.uuid = 'director' + this.$store.getters.id
    }
    const user = this.currentUser
    // 把全部在线督导加入friends列表，用于判断是否要新生成一个record记录
    AllDir().then(response => {
      this.friends = response.content
    }).catch(error => {
      console.log(error)
    })
    // 获取全部用户信息，用于查找
    AllUser().then(response => {
      this.users = response.content
    }).catch(error => {
      console.log(error)
    })
    // 建立会话连接，user包含用户名+头像+用户id
    if (this.goEasy.getConnectionStatus() === 'disconnected') {
      this.service.connect(user)
    }
    const self = this
    // 加载会话列表
    this.goEasy.im.latestConversations({
      onSuccess: function(res) {
        const content = res.content
        // 开始新的通话，启动新计时器
        if (content.conversations !== self.conversations) {
          const oldcon = new Set(self.conversations)
          const minuscon = content.conversations.filter(x => !oldcon.has(x))
          console.log('开启计时器')
          var d = new Date()
          self.initTime[minuscon[0].userId] = d.getTime()
          console.log(self.initTime[minuscon[0].userId])
        }
        self.conversations = content.conversations
      },
      onFailed: function(error) {
        console.log('失败获取最新会话列表, code:' + error.code + ' content:' + error.content)
      }
    })
    this.scrollToBottom()
    this.initialPrivateListeners()
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
      // this.friend = this.service.findFriendById(friendId)
      if (id === 'user1') {
        this.friend = this.friends[0]
      } else {
        this.friend = this.friends[1]
      }
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
    initialPrivateListeners() {
      const self = this
      console.log('监听到新消息')
      // 传入监听器，收到一条私聊消息总是滚到到页面底部
      this.service.onNewPrivateMessageReceive = (friendId, message) => {
        // 存储该条消息进RecordHistory
        const tmpMessage = {}
        const tmpUser = self.findUserById(friendId)
        // 如果通话列表中没有该条消息的发送人，则说明该条咨询为新的咨询，需要创建新的record_id
        // 并把该条消息的发送人存入通信列表中，把该用户信息添加record字段（生命期仅限于该次咨询，咨询结束后删除该字段）
        if (!self.friendsid.includes(friendId)) {
          self.friendsid.push(friendId)
          tmpUser.record_id = self.genRecordId()
        }
        tmpMessage.recordid = tmpUser.record_id
        tmpMessage.sendername = tmpUser.name
        tmpMessage.timestamp = message.timestamp
        tmpMessage.type = message.type
        tmpMessage.content = self.getContent(message)
        self.RecordHistory.push(tmpMessage)
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
      const dir_conversation = {
        type: 'private',
        userId: 'director1',
        unread: 0, // 未读消息条数
        // 私聊好友Data信息，来源于发送私聊消息时的to.data和发送方im.connect时传入的data
        data: {
          'avatar': 'https://images.pexels.com/photos/4491461/pexels-photo-4491461.jpeg?cs=srgb&dl=pexels-karolina-grabowska-4491461.jpg&fm=jpg',
          'name': '周导'
        },
        lastMessage: {}
      }
      this.dialogVisible = false
      this.conversations.push(dir_conversation)
      this.$router.push({
        name: 'ChatConsult',
        query: {
          id: dir_conversation.userId
        }
      })
      var d = new Date()
      this.initTime[dir_conversation.userId] = d.getTime()
      if (!this.timer[dir_conversation.userId]) {
        this.timer[dir_conversation.userId] = setInterval(this.timeComputed, 1000)
      }
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
      this.dialogFormVisible = false
      console.log(this.form.type)
      const self = this
      self.showLoading = true
      clearInterval(this.timer[this.$route.query.id])
      // 把当前计时器相关数据上传数据库后，清空
      var d = new Date()
      this.timer[this.$route.query.id] = ''
      this.consultTime[this.$route.query.id] = ''
      this.initTime[this.$route.query.id] = d.getTime()
      this.goEasy.im.removePrivateConversation({
        userId: this.$route.query.id,
        onSuccess: function() {
          self.showLoading = false
        },
        onFailed: function(error) {
          console.log(error)
        }
      })
    },
    findUserById(userId) {
      var user = this.users.find(user => (user.uuid === userId))
      return user
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
