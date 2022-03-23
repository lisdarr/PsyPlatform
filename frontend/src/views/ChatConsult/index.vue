<template>
  <div>
    <div v-for="(message, index) in messages" :key="index">
      <div
        class="time-lag"
        v-if="index == 0 || (messages[index].timestamp - messages[index - 1].timestamp > 5 * 60 * 1000)"
      >
        {{ formatDate(message.timestamp) }}
      </div>
      <chat-message
        :message="message"
        :to="friend"
        :currentUser="currentUser"
        :type="type"
        @showImageFullScreen="showImageFullScreen"
      />
    </div>
  </div>
</template>

<script>
import GoEasy from 'goeasy'

export default {
  name: 'ChatConsult',
  props: ['messages'],
  beforeMount() {
    // 连接GoEasy
    this.goEasy.connect({
      // 当前用户的id
      id: '001',
      // 当前用户的用户名和头像
      data: { name: 'consult', avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif' },
      onSuccess: function() {
        // 连接成功
        console.log('GoEasy connect successfully.')
      },
      onFailed: function(error) {
        // 连接失败
        console.log('Failed to connect GoEasy, code:' + error.code + ',error:' + error.content)
      },
      onProgress: function(attempts) {
        // 连接或自动重连中
        console.log('GoEasy is connecting', attempts)
      }
    })
    // 发送消息
    const im = this.goeasy.im
    // 创建消息, 内容最长不超过3K，可以发送字符串，对象和json格式字符串
    const textMessage = im.createTextMessage({
      text: 'Hello, GoEasyIM', // 消息内容
      to: {
        type: GoEasy.IM_SCENE.PRIVATE, // 私聊还是群聊，群聊为GoEasy.IM_SCENE.GROUP
        id: '002',
        data: { 'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif', 'name': 'user' } // 好友扩展数据, 任意格式的字符串或者对象，用于更新会话列表conversation.data
      }
    })
    // 发送消息
    im.sendMessage({
      message: textMessage,
      onSuccess: function(message) { // 发送成功
        console.log('Private message sent successfully.', message)
      },
      onFailed: function(error) { // 发送失败
        console.log('Failed to send private message，code:' + error.code + ' ,error ' + error.content)
      }
    })
  }
}
</script>

<style scoped>

</style>
