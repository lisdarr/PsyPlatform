<template>
  <div>
    <div>{{ $route.params }}</div>
    <!--    <div-->
    <!--      style="border: #304156; width: 10%;height: 700px; border-style: solid; margin-top: 20px; margin-left: 20px; float: left"-->
    <!--    >-->
    <!--      <div-->
    <!--        v-for="(item, index) in userList"-->
    <!--        :key="index"-->
    <!--        class="userList"-->
    <!--        :class=" {active:index===findIndex} "-->
    <!--        @click="getIndex(index)"-->
    <!--      >-->
    <!--        <div style="float: left;margin-left: 5px;">-->
    <!--          <el-avatar shape="circle" :size="50" :src="item.avatar"/>-->
    <!--        </div>-->
    <!--        <div style="float: left; color: white;margin-top:18px;margin-left: 5px">-->
    <!--          {{ item.name }}-->
    <!--        </div>-->
    <!--        <div-->
    <!--          style="float: left; color: white; background-color: red; border-radius: 50%; width: 17px; height: 17px; text-align: center; margin-top: 1px"-->
    <!--          v-if="item.unread"-->
    <!--        >-->
    <!--          {{ item.unread }}-->
    <!--        </div>-->
    <!--      </div>-->

    <!--    </div>-->
    <!--    <div-->
    <!--      style="border: #304156; width: 20%;height: 700px; border-style: solid; border-left-style: none; margin-top: 20px; float: left;background-color: #99a9bf"-->
    <!--    >-->
    <!--      <div class="el-icon-phone-outline" style="font-size: 50px; float: left;margin-top: 20px"></div>-->
    <!--      <div style="margin-top: 40px; margin-left: 70px; font-weight: bold; font-size: 20px">正在咨询中...</div>-->
    <!--      <div style="margin-top: 60px; margin-left: 5px; font-weight: bold; font-size: 20px">已咨询时间：</div>-->
    <!--      <div style="margin-top: 30px; margin-left: 15px; font-size: 50px">{{ consultTime }}</div>-->
    <!--      <div style="margin-top: 310px">-->
    <!--        <el-link>-->
    <!--          请求督导-->
    <!--        </el-link>-->
    <!--      </div>-->
    <!--      <el-divider></el-divider>-->
    <!--      <div>-->
    <!--        <el-link>-->
    <!--          结束咨询-->
    <!--        </el-link>-->
    <!--      </div>-->
    <!--    </div>-->
    <!--    <div-->
    <!--      style="border: #304156; width: 60%;height: 700px; border-style: solid; border-left-style: none; margin-top: 20px; float: left;"-->
    <!--    >-->

    <!--    </div>-->
  </div>
</template>

<script>

export default {
  name: 'Chat',
  data() {
    return {
      userList: [
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
      consultTime: '15:20',
      // 用于判断用户栏指向，对选择对用户栏进行高亮
      findIndex: 0
    }
  },
  methods: {
    getIndex(index) {
      this.findIndex = index
      this.consultTime = '13:00'
    },
    init_chat() {
      console.log(this.$route.param)
      var that = this
      this.$axios.get(
        // 后端接口
        '/chatList'
      ).then((response) => {
        that.userList = response.data.userList
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
  background-color: #304156;
  border: #2b2f3a;
}

.userList:hover {
  background-color: #99a9bf;
}

.active {
  background-color: #99a9bf;
  border: #99a9bf;
}

.el-link {
  color: #304156;
  font-size: 40px;
  margin-left: 40px;
}

.el-link:hover {
  color: white;
}

</style>
