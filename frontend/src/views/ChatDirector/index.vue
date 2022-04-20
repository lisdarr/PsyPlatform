<template>
  <div class="root-style">
    <!--      监听到没有conversations的时候，显示默认背景图-->
    <div v-if="!this.conversations.length">
      <div style="text-align: center; padding-top: 100px">
        <img src="~@/assets/chat.png" width="300">
        <p>努力做好每一次咨询!</p>
      </div>
    </div>
    <!--      监听到有conversations的时候，显示会话列表-->
    <div v-else>
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
            v-if="conversation.unread"
            style="float: left; color: white; background-color: red; border-radius: 50%; width: 17px; height: 17px; text-align: center; margin-top: 1px"
          >
            {{ conversation.unread }}
          </div>
        </div>
      </div>
      <div class="single-conversation">
        <div v-if="!this.$route.query.id">
          <div style="text-align: center; padding-top: 100px">
            <img src="~@/assets/chat.png" width="300">
            <p>努力做好每一次咨询!</p>
          </div>
        </div>
        <div v-else>
          <div class="timer">
            <div class="el-icon-phone-outline" style="font-size: 50px; float: left;margin-top: 20px"/>
            <div style="margin-top: 40px; margin-left: 70px; font-weight: bold; font-size: 20px">正在咨询中...</div>
            <div style="margin-top: 60px; margin-left: 5px; font-weight: bold; font-size: 20px">已咨询时间：</div>
            <div style="margin-top: 30px; font-size: 45px; margin-left: 20px">{{
                this.consultTime[this.$route.query.id]
              }}
            </div>
            <div style="margin-top: 290px; margin-left: 20px">
              <el-button
                type="text"
                style="font-size: 25px;padding-left: 10px"
              >
                请求督导中...
              </el-button>
            </div>
            <el-divider/>
            <div style="margin-left: 20px">
              <el-button
                type="text"
                style="font-size: 35px;padding-left: 15px"
                @click="removeConversation()"
              >
                结束咨询
              </el-button>
            </div>
          </div>
          <div class="dir-chat-space">
            <div class="message-container">
              <div ref="scrollView" class="scroll-view">
                <div v-for="(message, index) in messages" :key="index">
                  <div
                    v-if="index === 0 || messages[index].timestamp - messages[index-1].timestamp > 5 * 60 * 1000"
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
              <send-box :to="friend" :type="type" @onSent="scrollToBottomNew"/>
              <!--      放大查看图片-->
              <!--        <div>-->
              <!--          <img src="image.url" alt="[图片]">-->
              <!--        </div>-->
            </div>
          </div>
          <!--          右侧消息同步区-->
          <div class="syn-chat-space">
            <div class="message-container">
              <div ref="scrollViewside" class="scroll-view-side">
                <div v-for="(message, index) in synchat" :key="index">
                  <div
                    v-if="index === 0 || synchat[index].timestamp - synchat[index-1].timestamp > 5 * 60 * 1000"
                    class="time-lag"
                  >
                    {{ formatDate(message.timestamp) }}
                  </div>
                  <ChatMessage
                    :message="message"
                    :to="user"
                    :current-user="friend"
                    :type="type"
                    @showImageFullScreen="showImageFullScreen"
                  />
                </div>
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
import { getConsultList, SaveDirRecord, SendCurrentRecord } from '@/api/im'
import { chatHistoryDir } from '@/api/chat'

export default {
  name: 'ChatDirector',
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
      timerChat: {},
      // 用于判断用户栏指向，对选择对用户栏进行高亮
      findIndex: -1,
      // 通讯需要的数据
      // 聊天记录:当前用户在该聊天窗口发生的全部聊天记录
      messages: [],
      // 聊天对象信息
      friend: {},
      // 当前用户信息
      // currentUser: {
      //   avatar: 'https://images.pexels.com/photos/4491461/pexels-photo-4491461.jpeg?cs=srgb&dl=pexels-karolina-grabowska-4491461.jpg&fm=jpg',
      //   name: '周导',
      //   uuid: 'director1'
      // },
      currentUser: {
        avatar: this.$store.getters.avatar,
        name: this.$store.getters.name
      },
      // 控制图片，show：为true时放大查看
      image: {
        show: false,
        url: 'blob:https://localhost:8080/cf9c0c42-5f04-427f-806d-c250b3ceb2f2'
      },
      // private表示私聊
      type: 'private',
      // 请求督导会话框
      dialogVisible: false,
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
      synchat: [],
      user: {
        avatar: require('@/assets/test.png'),
        name: 'cymm',
        uuid: 'user1'
      },
      //  控制消息同步刷新
      timer: '',
      chatNums: {},
      HelpInfo: {},
      SingleRecord: {},
      consults: [],
      RecordHistory: []
    }
  },
  beforeMount() {
    // 获取咨询师列表
    getConsultList().then(response => {
      this.consults = response.content
      console.log('咨询师列表：' + JSON.stringify(this.consults))
    }).catch(error => {
      console.log('获取咨询师列表出错！', error)
    })
    const self = this
    this.currentUser.uuid = 'director-' + this.$store.getters.id
    // 建立会话连接，user包含用户名+头像+用户id
    if (this.goEasy.getConnectionStatus() === 'disconnected') {
      this.service.connect(this.currentUser)
    }
    // 加载会话列表
    this.goEasy.im.latestConversations({
      onSuccess: function(res) {
        const content = res.content
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
        name: 'ChatDirector',
        query: {
          id: id
        }
      })
      this.type = this.GoEasy.IM_SCENE.PRIVATE
      // 对话人的基本信息，包括name, avatar, uuid;
      // 之后随不同id取不同用户信息
      console.log('123')
      console.log(id)
      this.friend = this.findConsultById(id)
      console.log(this.friend)
      // 和该对话人的全部聊天记录
      this.messages = this.service.getPrivateMessages(id)
      console.log('开始获取同步消息')
      this.timer = setInterval(this.getHistory, 800)
      this.scrollToBottom()
      if (!this.timerChat[id]) {
        this.timerChat[id] = setInterval(this.timeComputed, 1000)
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
        console.log('触发下滑器')
        this.$refs.scrollView.scrollTo(0, this.$refs.scrollView.scrollHeight)
        this.$refs.scrollViewside.scrollTo(0, this.$refs.scrollViewside.scrollHeight)
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
        // this.getHistory()
        if (friendId === this.friend.uuid) {
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
    genHelpId() {
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
    removeConversation() {
      const self = this
      self.showLoading = true
      // 生成本次求助的id
      this.helpId = this.genHelpId()
      var d = new Date()
      // 保存本次求助相关信息HelpInfo
      this.HelpInfo.id = this.helpId
      var consultinfo = this.findConsultById(this.$route.query.id)
      this.HelpInfo.dir_name = this.currentUser.name
      this.HelpInfo.con_name = consultinfo.name
      this.HelpInfo.time = this.consultTime[this.$route.query.id]
      this.HelpInfo.date = this.formatDate(d.getTime())
      SaveDirRecord(this.HelpInfo).then(response => {
        console.log(response.msg)
      }).catch(error => {
        console.log('SaveDirRecord', error)
      })
      clearInterval(this.timerChat[this.$route.query.id])
      // 把当前计时器相关数据上传数据库后，清空
      this.timerChat[this.$route.query.id] = ''
      this.consultTime[this.$route.query.id] = ''
      // this.initTime[this.$route.query.id] = d.getTime()
      // 保存此次咨询的聊天记录到本地
      chatHistoryDir({
        appkey: 'BC-a9e0b1b27564446d942734742f8cbf07',
        userAId: self.$route.query.id,
        userBId: self.currentUser.uuid,
        limit: self.chatNums[self.$route.query.id]
      }).then((response) => {
        self.RecordHistory = []
        console.log(response)
        for (var item of response.content) {
          self.SingleRecord = {}
          self.SingleRecord.record_id = self.helpId
          if (item.senderId === self.$route.query.id) {
            var senderr = self.findConsultById(item.senderId)
          } else {
            senderr = this.currentUser
          }
          self.SingleRecord.senderName = senderr.name
          self.SingleRecord.timestamp = item.timestamp
          self.SingleRecord.type = item.type
          self.SingleRecord.content = self.getContent(item)
          self.RecordHistory.push(self.SingleRecord)
        }
        // 待改
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
      this.goEasy.im.removePrivateConversation({
        userId: self.$route.query.id,
        onSuccess: function() {
          self.showLoading = false
        },
        onFailed: function(error) {
          console.log(error)
        }
      })
      clearInterval(this.timer)
    },
    getHistory() {
      chatHistoryDir({
        appkey: 'BC-a9e0b1b27564446d942734742f8cbf07',
        userAId: 'user-1',
        userBId: this.friend.uuid,
        limit: 30
      }).then((response) => {
        console.log(response.content)
        this.synchat = response.content
        this.$refs.scrollViewside.scrollTo(0, this.$refs.scrollViewside.scrollHeight)
        // console.log(response.data.code)
      }).catch((error) => {
        console.log('出错！')
        console.log(error)
      })
    },
    findConsultById(userId) {
      var consult = this.consults.find(consult => (consult.uuid === userId))
      return consult
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
    }
  },
  beforeDestroy() {
    clearInterval(this.timer)
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

.message-container .scroll-view-side {
  height: 100%;
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
}

.message-container .scroll-view-side .time-lag {
  font-size: 18px;
  text-align: center;
  color: #304156;
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

.dir-chat-space {
  border: #304156;
  width: 45%;
  border-right-style: solid;
  height: 694px;
  float: left;
}

.syn-chat-space {
  border: #304156;
  width: 35%;
  height: 694px;
  float: left;
}
</style>
