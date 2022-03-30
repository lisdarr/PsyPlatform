<template>
  <div class="send-box">
    <div class="send-box-top">
      <el-button icon="el-icon-microphone" class="send-button-icon"></el-button>
      <el-button icon="emoji-icon" class="send-button-icon"></el-button>
      <el-button icon="el-icon-picture" class="send-button-icon"></el-button>
      <el-button type="success" class="send-button-icon">发送</el-button>
    </div>
    <el-input class="send-box-bottom" v-model="input" placeholder="请输入内容" type="textarea" :rows="5"/>
  </div>
</template>

<script>
import GoEasyRecorder from '@/layout/components/GoEasyRecorder/GoEasyRecorder'

export default {
  name: 'SendBox',
  components: {
    GoEasyRecorder
  },
  props: ['to', 'type'],
  data() {
    const emojiUrl = 'https://imgcache.qq.com/open/qcloud/tim/assets/emoji/'
    const emojiMap = {
      '[么么哒]': 'emoji_3@2x.png',
      '[乒乓]': 'emoji_4@2x.png',
      '[便便]': 'emoji_5@2x.png',
      '[信封]': 'emoji_6@2x.png',
      '[偷笑]': 'emoji_7@2x.png',
      '[傲慢]': 'emoji_8@2x.png'
    }
    return {
      audio: {
        // 语音录音中
        recording: false,
        // 录音按钮展示
        visible: false
      },
      emoji: {
        url: emojiUrl,
        map: emojiMap,
        show: false
      },
      more: {
        show: false
      },
      content: '',
      // 聊天框内输入对内容
      input: ''
    }
  },
  methods: {
    onRecordComplete(file) {
      const audioMessage = this.goEasy.im.createAudioMessage({
        to: {
          id: this.to.uuid,
          type: this.type,
          data: {
            name: this.to.name,
            avatar: this.to.avatar
          }
        },
        file: file,
        onProgress: function(progress) {
          console.log(progress)
        }
      })
      this.sendMessage(audioMessage)
      this.$emit('onSent')
    },
    chooseImage(e) {
      const file = e.target.files[0]
      const imageMessage = this.goEasy.im.createImageMessage({
        to: {
          id: this.to.uuid,
          type: this.type,
          data: {
            name: this.to.name,
            avatar: this.to.avatar
          }
        },
        file: file,
        onProgress: function(progress) {
          console.log(progress)
        }
      })
      this.sendMessage(imageMessage)
      this.$emit('onSent')
    },
    chooseVideo(e) {
      const file = e.target.files[0]
      const videoMessage = this.goEasy.im.createVideoMessage({
        to: {
          id: this.to.uuid,
          type: this.type,
          data: {
            name: this.to.name,
            avatar: this.to.avatar
          }
        },
        file: file,
        onProgress: function(progress) {
          console.log(progress)
        }
      })
      this.sendMessage(videoMessage)
      this.$emit('onSent')
    },
    chooseFile(e) {
      const file = e.target.files[0]
      const fileMessage = this.goEasy.im.createFileMessage({
        to: {
          id: this.to.uuid,
          type: this.type,
          data: {
            name: this.to.name,
            avatar: this.to.avatar
          }
        },
        file: file,
        onProgress: function(progress) {
          console.log(progress)
        }
      })
      this.sendMessage(fileMessage)
      this.$emit('onSent')
    },
    sendTextMessage() {
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
      let localHistory
      if (type === this.GoEasy.IM_SCENE.PRIVATE) {
        localHistory = this.service.getPrivateMessages(toId)
      } else {
        localHistory = this.service.getGroupMessages(toId)
      }
      localHistory.push(message)
      this.goEasy.im.sendMessage({
        message: message,
        onSuccess: function(message) {
          console.log('发送成功.', message)
        },
        onFailed: function(error) {
          console.log('发送失败:', error)
        }
      })
    },
    showCustomMessageForm() {
      this.$router.push({
        name: 'customMessage',
        query: {
          to: JSON.stringify(this.to),
          type: this.type
        }
      })
    },
    messageInputFocusin() {
      this.more.show = false
      this.emoji.show = false
    },
    showEmoji() {
      this.emoji.show = !this.emoji.show
      this.more.show = false
    },
    selectEmoji(emojiKey) {
      this.content += emojiKey
    },
    showMore() {
      this.more.show = !this.more.show
      this.emoji.show = false
    }
  }
}
</script>

<style>
@import "./sendBox.css";
</style>
