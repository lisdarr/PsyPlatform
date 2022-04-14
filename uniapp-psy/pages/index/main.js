// pages/saveInfo/main.js

const app = getApp()

Page({
  data: {
    userInfo: {},
    // userNumber:{},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    canIUseGetUserProfile: false,
    canIUseOpenData: wx.canIUse('open-data.type.userAvatarUrl') && wx.canIUse('open-data.type.userNickName') ,// 如需尝试获取用户信息可改为false

    "type": " ",
    historyConversation: [
      {
        startTime:"04-08 16:23",
        status:"",
        counselor:{
          avatar: "https://i03piccdn.sogoucdn.com/0354d6ffc3ecbe11",
          name:"王咨询师"
        },
        duration:"6:23",
        evaluate:3,
      },
      {
        startTime:"04-08 16:22",
        status:"",
        counselor:{
          avatar: "https://i03piccdn.sogoucdn.com/0354d6ffc3ecbe11",
          name:"王咨询师"
        },
        duration:"4:23",
        evaluate:4,
      },
      {
        startTime:"04-07 15:21",
        status:"",
        counselor:{
          avatar: "https://i03piccdn.sogoucdn.com/0354d6ffc3ecbe11",
          name:"王咨询师"
        },
        duration:"3:23",
        evaluate:1,
      }
    ],

    friend: {
      name: "王咨询师",
      uuid: "consult1",
      avatar: "https://i03piccdn.sogoucdn.com/0354d6ffc3ecbe11"
    },
    currentUser: {
      uuid: "user1",
      name: "cymm",
      avatar: "/static/images/Avatar-1.png"
    },
    messages:[]
  },

  onLoad: function(options) {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
  },

  onShow: function(){
    let model = getApp().globalData.model
    if(model){
      console.log("历史记录：", model)
      var items = JSON.parse(model);
      console.log("历史记录：",items)
      var self = this
      self.setData({
        historyConversation:items,
      });
    }
    else{
      console.log("没有历史记录")
    }
  },
  getUserProfile(e) {
    wx.getUserProfile({
      desc: '展示用户信息', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
        console.log(res.userInfo)
      }
    })
  },

  handleSwitch: function(){
    wx.switchTab({
      url: '/pages/informed_consent/main',
    });
},
  change: function(){
    wx.navigateTo({
      url: '/pages/changeInfo/main',
    })
  }
});
