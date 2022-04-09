<template>
  <div class="send-box">
    <div class="send-box-top">
      <el-button icon="el-icon-microphone" class="send-button-icon"/>
      <el-popover
          v-model="emojiShow"
          placement="top"
          width="500"
          height="700"
          trigger="click"
      >
        <div class="browBox">
          <ul style="display: flex;flex-wrap: wrap;list-style: none;">
            <li
                v-for="(item, index) in faceList"
                :key="index"
                style="cursor: pointer;width: 10%;font-size: 26px;text-align: center;list-style: none;"
                @click="getBrow(index)"
            >
              {{ item }}
            </li>
          </ul>
        </div>
        <el-button slot="reference" icon="emoji-icon" class="send-button-icon"/>
      </el-popover>
      <el-button icon="el-icon-picture" class="send-button-icon"/>
      <el-button type="success" class="send-button-icon-send" :disabled="content == ''" @click="submitMessage">发送
      </el-button>
    </div>
    <el-input
        v-model="content"
        class="send-box-bottom"
        placeholder="请输入内容"
        type="textarea"
        :rows="5"
        @keyup.enter.native="submitMessage"
    />
  </div>
</template>

<script>
const appData = require('@/assets/emojis.json')
export default {
  name: 'SendBox',
  components: {},
  props: ['to', 'type'],
  data() {
    return {
      audio: {
        // 语音录音中
        recording: false,
        // 录音按钮展示
        visible: false
      },
      // 聊天框内输入对内容
      content: '',
      //  表情框是否展示
      emojiShow: false,
      // 表情列表
      faceList: [],
      // 表情文本
      getBrowString: '',
      //   历史聊天记录
      history: []
    }
  },
  created() {
    this.loadEmojis()
  },
  methods: {
    loadEmojis() {
      for (const i in appData) {
        this.faceList.push(appData[i].char)
      }
    },
    // 获取用户点击之后的标签，存储在输入框中
    getBrow(index) {
      console.log('用户选择表情')
      for (const i in this.faceList) {
        if (index === i) {
          this.getBrowString = this.faceList[index]
          this.content += this.getBrowString
        }
      }
      this.emojiShow = false
    },
    submitMessage() {
      if (this.content.trim().length !== 0) {
        const textMessage = this.goEasy.im.createTextMessage({
          text: this.content,
          to: {
            id: this.to.uuid,
            type: this.type,
            data: {
              name: this.to.name,
              avatar: this.to.avatar
            }
          }
        })
        this.sendMessage(textMessage)
        this.$emit('onSent')
        this.content = ''
      }
    },
    sendMessage(message) {
      const toId = message.to.id
      const type = message.to.type
      if (type === this.GoEasy.IM_SCENE.PRIVATE) {
        this.history = this.service.getPrivateMessages(toId)
      } else {
        this.history = this.service.getGroupMessages(toId)
      }
      this.history.push(message)
      // console.log(this.history)
      // if (toId === 'user1') {
      //   this.$store.dispatch('history/setMessages', this.history)
      //   const test = { 'messages in store:': this.$store.getters.synmessages }
      //   console.log(test)
      // }
      this.goEasy.im.sendMessage({
        message: message,
        onSuccess: function(message) {
          console.log('发送成功.', message)
        },
        onFailed: function(error) {
          console.log('发送失败:', error)
        }
      })
    }
  }
}
</script>

<style>
@import "./sendBox.css";
</style>
