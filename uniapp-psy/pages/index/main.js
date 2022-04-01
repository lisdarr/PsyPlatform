// pages/saveInfo/main.js

const app = getApp()

Page({
  data: {
    userInfo: {},
    // userNumber:{},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    canIUseGetUserProfile: false,
    canIUseOpenData: wx.canIUse('open-data.type.userAvatarUrl') && wx.canIUse('open-data.type.userNickName') // 如需尝试获取用户信息可改为false
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
    wx.navigateTo({
      url: '/pages/informed_consent/main',
      success: (result) => {},
      fail: () => {},
      complete: () => {}
    }) ;
}
});
