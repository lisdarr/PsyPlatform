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
          style="float: left; color: white; background-color: red; border-radius: 50%; width: 17px; height: 17px; text-align: center; margin-top: 1px"
          v-if="conversation.unread"
        >
          {{ conversation.unread }}
        </div>
      </div>

    </div>
    <div
      style="border: #304156; width: 20%;height: 700px; border-style: solid; border-left-style: none; margin-top: 20px; float: left;background-color: #304156; color: white"
    >
      <div class="el-icon-phone-outline" style="font-size: 50px; float: left;margin-top: 20px"></div>
      <div style="margin-top: 40px; margin-left: 70px; font-weight: bold; font-size: 20px">正在咨询中...</div>
      <div style="margin-top: 60px; margin-left: 5px; font-weight: bold; font-size: 20px">已咨询时间：</div>
      <div style="margin-top: 30px; margin-left: 15px; font-size: 50px; margin-left: 70px">{{ consultTime }}</div>
      <div style="margin-top: 310px; margin-left: 20px">
        <el-link @click="toDir">
          请求督导
        </el-link>
      </div>
      <el-divider></el-divider>
      <div style="margin-left: 20px">
        <el-link>
          结束咨询
        </el-link>
      </div>
    </div>
    <div
      style="border: #304156; width: 60%;height: 700px; border-style: solid; border-left-style: none; margin-top: 20px; float: left;"
    >
      接收消息区：12-18 ，根据{{ this.$route.query.id }}
      chatmessage区：输入框和发送部分
    </div>
  </div>
</template>

<script>

export default {
  name: 'ChatConsult',
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
      findIndex: 0
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
    init_chat() {
      var that = this
      this.$axios.get(
        // 后端接口
        '/chatList'
      ).then((response) => {
        // userList是当前收到的信息列表，包括发送方姓名、头像和未读消息数
        that.conversations = response.data.conversations
      })
    }
  },
  mounted() {
    this.init_chat()
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

.el-link {
  color: white;
  font-size: 40px;
  margin-left: 40px;
}

</style>
