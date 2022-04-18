// pages/saveInfo/main.js

const app = getApp()

Page({
  data: {
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    canIUseGetUserProfile: false,
    canIUseOpenData: wx.canIUse('open-data.type.userAvatarUrl') && wx.canIUse('open-data.type.userNickName') ,// 如需尝试获取用户信息可改为false

    "type": " ",
    historyConversation: [],
  },

  onLoad: function(options) {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
  },

  onReady: function(){
    var that = this;
    var cookienow = app.globalData.mycookie;
    wx.request({
      url: 'http://123.57.45.27:8022/visitor/weChat/conversation/',
      method: "GET",
      header : {'cookie': cookienow},
      success: function(res){
          that.setData(
            {
                historyConversation: res.data.historyConversation
            }
          )
          
          var model = JSON.stringify(that.data.historyConversation);
          getApp().globalData.historyConversation = model;
      },
    fail: function() {
      console.log('咨询记录获取失败');
      }
    })
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
