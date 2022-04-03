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
            startTime:"2021-11-17 16:23:23",
            status:"",
            counselor:{
                gender:"男",
                name:"gyy"
            },
            duration:"16:23:23",
            evaluate:3,
        },
        {
            startTime:"2021-11-17 16:23:23",
            status:"WAITING",
            counselor:{
                gender:"女",
                name:"cy"
            },
            duration:"34:23:34",
            evaluate:4,
        },
        {
            startTime:"2021-11-17 16:23:23",
            status:"WAITING",
            counselor:{
                gender:"女",
                name:"wrc"
            },
            duration:"14:23:34",
            evaluate:2,
        },
        {
            startTime:"2021-11-17 16:23:23",
            status:"WAITING",
            counselor:{
                gender:"男",
                name:"xsh"
            },
            duration:"14:23:34",
            evaluate:4,
        }
    ]
  },
  // 事件处理函数
  // bindViewTap() {
  //   wx.navigateTo({
  //     url: '../logs/logs'
  //   })
  // },
  onLoad() {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
  },
  getUserProfile(e) {
    wx.getUserProfile({
      desc: '展示用户信息', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        console.log(res)
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    })
  },

  // getPhoneNumber (e) {
  //   this.setData({
  //     userNumber: e.detail
  //   })
  //   // console.log(e.detail.errMsg)
  //   // console.log(e.detail.iv)
  //   // console.log(e.detail.encryptedData)
  // }
  handleSwitch: function(){
    wx.switchTab({
      url: '/pages/informed_consent/main',
    });
}
});
