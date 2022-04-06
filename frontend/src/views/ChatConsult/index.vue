<template>
  <div>
    <div
      style="border: #304156; width: 10%;height: 700px; border-style: solid; margin-top: 20px; margin-left: 20px; float: left"
    >
      <!--      需要监听通信列表-->
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
    <div
      style="border: #304156; width: 20%;height: 700px; border-style: solid; border-left-style: none; margin-top: 20px; float: left;background-color: #304156; color: white"
    >
      <div class="el-icon-phone-outline" style="font-size: 50px; float: left;margin-top: 20px"/>
      <div style="margin-top: 40px; margin-left: 70px; font-weight: bold; font-size: 20px">正在咨询中...</div>
      <div style="margin-top: 60px; margin-left: 5px; font-weight: bold; font-size: 20px">已咨询时间：</div>
      <div style="margin-top: 30px; font-size: 50px; margin-left: 70px">{{ consultTime }}</div>
      <div style="margin-top: 310px; margin-left: 20px">
        <el-link style="font-size: 35px;padding-left: 30px">
          请求督导
        </el-link>
      </div>
      <el-divider/>
      <div style="margin-left: 20px">
        <el-link style="font-size: 35px;padding-left: 30px">
          结束咨询
        </el-link>
      </div>
    </div>
    <div
      style="border: #304156; width: 60%;height: 700px; border-style: solid; border-left-style: none; margin-top: 20px; float: left;"
    >
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
      conversations: [
        // {
        //   name: 'cymm',
        //   userId: '123',
        //   avatar: 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
        //   // unread: 3,
        //   type: 'private'
        // }
      ],
      consultTime: '00:00',
      // 用于判断用户栏指向，对选择对用户栏进行高亮
      findIndex: 0,
      // 通讯需要的数据
      // 聊天记录:当前用户在该聊天窗口发生的全部聊天记录
      messages: [],
      // 聊天对象信息
      friend: {
        // avatar: '/IM/user/Avatar-3.png',
        // name: 'cymm',
        // // uuid: 'fdee46b0-4b01-4590-bdba-6586d7617f95'/
        // uuid: '123'
        avatar: 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
        name: 'Mattie',
        uuid: '08c0a6ec-a42b-47b2-bb1e-15e0f5f9a19a'
      },
      // 当前用户信息
      currentUser: {
        avatar: 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
        name: 'Tracy',
        uuid: 'fdee46b0-4b01-4590-bdba-6586d7617f95'
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
    const user = this.currentUser
    // 建立会话连接，user包含用户名+头像+用户id
    if (this.goEasy.getConnectionStatus() === 'disconnected') {
      this.service.connect(user)
    }
    this.goEasy.im.on(this.GoEasy.IM_EVENT.CONVERSATIONS_UPDATED, (conversations) => {
      console.log(conversations)
      this.conversations = conversations.conversations || []
      this.unreadTotal = conversations.unreadTotal
    })
    // 得到对话人的id
    const friendId = this.$route.query.id
    this.type = this.GoEasy.IM_SCENE.PRIVATE
    // 对话人的基本信息，包括name, avatar, uuid;
    // 之后随不同id取不同用户信息
    // this.friend = this.service.findFriendById(friendId)
    // 和该对话人的全部聊天记录
    this.messages = this.service.getPrivateMessages(friendId)
    console.log(this.messages)
    // var test = {'messages': this.messages}
    // console.log(test)
    this.scrollToBottom()
    this.initialPrivateListeners()
    if (this.messages.length !== 0) {
      this.markMessageAsRead(friendId)
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
    },
    showImageFullScreen(message) {
      this.image.url = message.payload.url
      this.image.show = true
    },
    scrollToBottom() {
      this.$nextTick(() => {
        this.$refs.scrollView.scrollTo(0, this.$refs.scrollView.scrollHeight)
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
</style>
