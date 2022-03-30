<template>
  <div class="message-item" :class="{'self': message.senderId === currentUser.uuid}">
    <img v-if="type === 'group'" :src="message.senderData.avatar" class="chat-avatar">
    <img
      v-else-if="message.senderId === currentUser.uuid"
      :src="currentUser.avatar"
      class="chat-avatar"
    >
    <img v-else :src="to.avatar" class="chat-avatar">
    <div class="chat-message">
      <div v-if="message.status === 'sending'" class="pending"/>
      <div v-if="message.status === 'fail'" class="send-fail"/>
      <div v-if="message.type ==='text'" class="text-content" v-html="decoder.decode(message.payload.text)"/>
      <div v-if="message.type === 'image'" class="image-content">
        <img :src="message.payload.url" @click="showImageFullScreen">
      </div>
      <GoEasyAudioPlayer
        v-if="message.type ==='audio'"
        :src="message.payload.url"
        :duration="message.payload.duration"
      />
    </div>
  </div>
</template>

<script>

import GoEasyAudioPlayer from '@/layout/components/GoEasyAudioPlayer/GoEasyAudioPlayer'
import EmojiDecoder from '@/views/ChatConsult/EmojiDecoder'

export default {
  name: 'ChatMessage',
  components: {
    GoEasyAudioPlayer
  },
  props: ['message', 'to', 'currentUser', 'type'],
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
      decoder: new EmojiDecoder(emojiUrl, emojiMap)
    }
  },
  methods: {
    showImageFullScreen() {
      this.$emit('showImageFullScreen', this.message)
    }
  }
}
</script>

<style>
@import "./ChatMessage.css";
</style>
