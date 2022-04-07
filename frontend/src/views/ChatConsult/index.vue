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
            <el-avatar shape="circle" :size="50" :src="conversation.avatar"/>
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
            <div style="margin-top: 30px; font-size: 50px; margin-left: 40px">{{ consultTime }}</div>
            <div style="margin-top: 280px; margin-left: 20px">
              <el-button type="text" style="font-size: 35px;padding-left: 15px" @click="ToDir">
                请求督导
              </el-button>
            </div>
            <el-divider/>
            <div style="margin-left: 20px">
              <el-button
                type="text"
                style="font-size: 35px;padding-left: 15px"
                @click="removeConversation"
              >
                结束咨询
              </el-button>
            </div>
          </div>
          <div class="chat-space">
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
                    :current-user="currentUser"
                    :type="type"
                    @showImageFullScreen="showImageFullScreen"
                  />
                </div>
              </div>
              <send-box :to="friend" :type="type" @onSent="scrollToBottom"/>
              <!--      放大查看图片-->
              <!--        <div>-->
              <!--          <img src="image.url" alt="[图片]">-->
              <!--        </div>-->
            </div>
            <!--      接收消息区：12-18 ，根据{{ this.$route.query.id }}-->
            <!--      chatmessage区：输入框和发送部分-->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import ChatMessage from '@/views/ChatConsult/ChatMessage'
import SendBox from '@/views/ChatConsult/SendBox'

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
      consultTime: '00:00',
      // 用于判断用户栏指向，对选择对用户栏进行高亮
      findIndex: -1,
      // 通讯需要的数据
      // 聊天记录:当前用户在该聊天窗口发生的全部聊天记录
      messages: [],
      // 聊天对象信息
      friends: [
        {
          avatar: 'http://inews.gtimg.com/newsapp_bt/0/13540171754/1000',
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
      // 当前用户信息
      currentUser: {
        avatar: 'https://i03piccdn.sogoucdn.com/0354d6ffc3ecbe11',
        name: '王咨询师',
        uuid: 'consult1'
      },
      // 控制图片，show：为true时放大查看
      image: {
        show: false,
        url: 'blob:https://localhost:8080/cf9c0c42-5f04-427f-806d-c250b3ceb2f2'
      },
      // private表示私聊
      type: 'private'
    }
  },
  beforeMount() {
    console.log('聊天页根目录重新挂载')
    const self = this
    const user = this.currentUser
    // 建立会话连接，user包含用户名+头像+用户id
    if (this.goEasy.getConnectionStatus() === 'disconnected') {
      this.service.connect(user)
    }
    // 加载会话列表
    this.goEasy.im.latestConversations({
      onSuccess: function(res) {
        const content = res.content
        self.conversations = content.conversations
        var test = { 'conversations': self.conversations }
        console.log(test)
      },
      onFailed: function(error) {
        console.log('失败获取最新会话列表, code:' + error.code + ' content:' + error.content)
      }
    })
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
      const friendId = this.$route.query.id
      this.type = this.GoEasy.IM_SCENE.PRIVATE
      // 对话人的基本信息，包括name, avatar, uuid;
      // 之后随不同id取不同用户信息
      // this.friend = this.service.findFriendById(friendId)
      if (friendId === 'user1') {
        this.friend = this.friends[0]
      } else {
        this.friend = this.friends[1]
      }
      // 和该对话人的全部聊天记录
      this.messages = this.service.getPrivateMessages(friendId)
      console.log(this.messages)
      // this.scrollToBottom()
      // this.initialPrivateListeners()
      // if (this.messages.length !== 0) {
      //   this.markMessageAsRead(friendId)
      // }
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
      // 传入监听器，收到一条私聊消息总是滚到到页面底部
      this.service.onNewPrivateMessageReceive = (friendId, message) => {
        if (friendId === this.friend.uuid) {
          this.markMessageAsRead(friendId)
          this.scrollToBottom()
        }
      }
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
      this.$alert('正在为您分配在线督导，点击确认按钮开始连线...', {
        confirmButtonText: '确定',
        callback: action => {
          this.$message({
            type: 'info',
            message: `已为您连线督导`
          })
          this.$router.push({
            name: 'ChatConsult',
            query: {
              id: 'director1'
            }
          })
        }
      })
    },
    removeConversation() {
      this.$prompt('本次咨询已结束，请填写评价', {
        confirmButtonText: '确定',
        cancelButtonText: '点错了，继续咨询'
      }).then(({ value }) => {
        this.$message({
          type: 'success',
          message: '感谢您的反馈！'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '咨询继续'
        })
      })
      const self = this
      self.showLoading = true
      this.goEasy.im.removePrivateConversation({
        userId: this.$route.query.id,
        onSuccess: function() {
          self.showLoading = false
        },
        onFailed: function(error) {
          console.log(error)
        }
      })
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
