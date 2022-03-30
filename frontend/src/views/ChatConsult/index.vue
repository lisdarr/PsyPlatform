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
          {{ conversation.name }}
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
        <el-link @click="toDir">
          请求督导
        </el-link>
      </div>
      <el-divider/>
      <div style="margin-left: 20px">
        <el-link>
          结束咨询
        </el-link>
      </div>
    </div>
    <div
      style="border: #304156; width: 60%;height: 700px; border-style: solid; border-left-style: none; margin-top: 20px; float: left;"
    >
      <div class="message-container">
        <div class="scroll-view" ref="scrollView">
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
        {
          name: '张先生',
          userId: '001',
          avatar: 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
          unread: 1,
          type: 'private'
        },
        {
          name: '李女士',
          userId: '002',
          avatar: 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
          unread: 3,
          type: 'private'
        }
      ],
      consultTime: '12:30',
      // 用于判断用户栏指向，对选择对用户栏进行高亮
      findIndex: 0,
      // 通讯需要的数据
      // 聊天记录:当前用户在该聊天窗口发生的全部聊天记录
      messages: [
        {
          // 该条消息的id
          messageId: 'b0203bf0af5b11ec886bc306fa6c2977',
          // 发送该消息的用户id，之后用于判断消息置于左侧还是右侧
          senderId: '3bb179af-bcc5-4fe0-9dac-c05688484649',
          // 该条消息时间戳
          timestamp: 1648556887398,
          // 该条消息的类型
          type: 'text',
          payload: {
            text: '你好哇！！！'
          }
        },
        {
          messageId: 'febebdf0af5f11ecaaef5b30370e2287',
          senderId: 'fdee46b0-4b01-4590-bdba-6586d7617f95',
          // 如果是当前用户发送的消息，则没有这个字段
          receiverId: '3bb179af-bcc5-4fe0-9dac-c05688484649',
          timestamp: 1648558737286,
          type: 'text',
          payload: {
            text: '一切都会好的！！！'
          }
        }
      ],
      // 聊天对象信息
      friend: {
        avatar: '/IM/user/Avatar-3.png',
        name: 'Tracy',
        uuid: 'fdee46b0-4b01-4590-bdba-6586d7617f95'
      },
      // 当前用户信息
      currentUser: {
        avatar: '/IM/user/Avatar-2.png',
        name: 'Wallace',
        uuid: '3bb179af-bcc5-4fe0-9dac-c05688484649'
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
  mounted() {
    this.init_chat()
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
    init_chat() {
      var that = this
      this.$axios.get(
        // 后端接口
        '/chatList'
      ).then((response) => {
        // userList是当前收到的信息列表，包括发送方姓名、头像和未读消息数
        that.conversations = response.data.conversations
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
